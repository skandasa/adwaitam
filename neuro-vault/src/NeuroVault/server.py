from http.client import HTTPResponse
from fastapi import FastAPI, UploadFile
from typing import List
import uvicorn
from fastapi.responses import JSONResponse
from NeuroVault.vault import embed_youtube_video, embed_youtube_channel, embed_pdf_file, embed_audio_file, embed_video_file, query_vault

# ... other imports from the original file

app = FastAPI()  # Define FastAPI app instance

@app.post("/embed_youtube_video/")
async def embed_youtube_video_endpoint(youtube_url: str):
    result = embed_youtube_video(youtube_url)
    if "Invalid" in result:  # Check for error message
        return HTTPResponse(status_code=400, content=result) # Return 400 Bad Request
    return {"message": result}


@app.post("/embed_youtube_channel/")
async def embed_youtube_channel_endpoint(channel_handle: str):
    result = embed_youtube_channel(channel_handle)
    if "not found" in result.lower():
      return HTTPResponse(status_code=404, content=result)
    return {"message": result}

@app.post("/embed_pdf_file/")
async def embed_pdf_file_endpoint(files: List[UploadFile]):
    result = await embed_pdf_file(files)
    if "Invalid" in result:
        return HTTPResponse(status_code=400, content=result)
    return {"message": result}


@app.post("/embed_audio_file/")
async def embed_audio_file_endpoint(files: List[UploadFile]):
    result = await embed_audio_file(files)
    if "Invalid" in result:
        return HTTPResponse(status_code=400, content=result)
    return {"message": result}


@app.post("/embed_video_file/")
async def embed_video_file_endpoint(files: List[UploadFile]):
    result = await embed_video_file(files)
    if "Invalid" in result:
        return HTTPResponse(status_code=400, content=result)
    return {"message": result}


@app.get("/query_vault/")
async def query_vault_endpoint(query: str):
    results = query_vault(query)
    return JSONResponse(content=results)

def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)

