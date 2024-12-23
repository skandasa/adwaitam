import os
from dotenv import load_dotenv
from embedchain import App
import time
from urllib.parse import urlparse, parse_qs
from fastapi import FastAPI, Request, Response, UploadFile  # type: ignore
from fastapi.responses import JSONResponse  # type: ignore
from youtube_transcript_api import YouTubeTranscriptApi  # type: ignore
import googleapiclient.discovery  # type: ignore
from googleapiclient.errors import HttpError  # type: ignore
from moviepy import *

load_dotenv()


app = App.from_config(config_path="config.yaml")

def createFolder():
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    folder_name = f"repo/{timestamp}"
    os.makedirs(folder_name, exist_ok=True)
    return folder_name

    
def get_video_id(youtube_url):
    parsed_url = urlparse(youtube_url)
    video_id = parse_qs(parsed_url.query).get("v")
    if video_id:
        return video_id[0]
    return None

def get_channel_id(channel_handle:str):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=os.getenv("YOUTUBE_API_KEY"))
    request = youtube.search().list(
        part="id",
        q=channel_handle,
        type="channel",
        maxResults=1,
    )    # type: ignore

    response = request.execute()
    if response["items"]:
        return response["items"][0]["id"]["channel_id"]
    else:
        return None
    
def list_channel_videos(channel_id:str):
    videos=[]
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=os.getenv("YOUTUBE_API_KEY"))
    request = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        type="video",
        maxResults=50,
    )

    while request:
        response = request.execute()
        for item in response["items"]:
            videos.append(
                {
                    "title": item["snippet"]["title"],
                    "video_id": item["id"]["videoId"],
                }
            )
        request = youtube.search().list_next(request, response)
    return videos

def transcribe_youtube_video(video_id:str,folder_name:str):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        with open(f"{folder_name}/{video_id}.txt", "w") as file:
            for line in transcript:
                file.write(line["text"] + "\n")
    except Exception as e:
        return {"error": str(e)}
    return transcript


def convert_video_to_audio(video_path:str):
    filename,extension = os.path.splitext(video_path)
    audio_path = f"{filename}.wav"
    video = VideoFileClip(video_path)
    audio = video.audio
    audio.write_audiofile(audio_path)
    return audio_path

def embed_youtube_video(youtube_url:str):
    folder_path = createFolder()
    video_id = get_video_id(youtube_url)
    if video_id:
        transcribe_youtube_video(video_id, folder_path)
        app.add(folder_path,data_type="directory")
        return "Video embedded successfully"
    else:
        return "Invalid YouTube URL"

def embed_youtube_channel(channel_handle:str):
    folder_path = createFolder()
    channel_id = get_channel_id(channel_handle)
    if channel_id:
        videos = list_channel_videos(channel_id)
        for video in videos:
            transcribe_youtube_video(video["video_id"], folder_path)
            print(f"Transcribed video: {video['title']}")
        app.add(folder_path,data_type="directory")
        return "Channel embedded successfully"
    else:
        return "Channel not found"


async def embed_pdf_file(files:list[UploadFile]):
    folder_path = createFolder()
    for file in files:
        if file.content_type != "application/pdf":
            return "Invalid file type. Only PDF files are allowed"
        file_name = f'{folder_path}/{file.filename}'
        with open(file_name, "wb") as f:
            f.write(await file.file.read())
            app.add(file_name,data_type="pdf_file")
    return "Files embedded successfully"

async def embed_audio_file(files:list[UploadFile]):
    folder_path = createFolder()
    for file in files:
        if file.content_type != "audio/wav" :
            return "Invalid file type. Only wav files are allowed"
        file_name = f'{folder_path}/{file.filename}'
        with open(file_name, "wb") as f:
            f.write(await file.file.read())
            app.add(file_name,data_type="audio")
    return "Files embedded successfully"


async def embed_video_file(files:list[UploadFile]):
    folder_path = createFolder()
    for file in files:
        if file.content_type != "video/mp4" :
            return "Invalid file type. Only mp4 files are allowed"
        file_name = f'{folder_path}/{file.filename}'
        with open(file_name, "wb") as f:
            f.write(await file.file.read())
            audio_file = convert_video_to_audio(file_name)
            app.add(audio_file,data_type="audio")
    return "Files embedded successfully"


def query_vault(query:str):
    results = app.query(query)
    return results