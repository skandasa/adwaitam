from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from crewai_tools import ScrapeWebsiteTool

@CrewBase
class ComprehensiveBusinessDiagnosticAndMarketAnalysisToolCrew():
    """ComprehensiveBusinessDiagnosticAndMarketAnalysisTool crew"""

    @agent
    def company_analysis_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config['company_analysis_specialist'],
            tools=[SerperDevTool(), ScrapeWebsiteTool()],
        )

    @agent
    def digital_presence_analyzer(self) -> Agent:
        return Agent(
            config=self.agents_config['digital_presence_analyzer'],
            tools=[SerperDevTool(), ScrapeWebsiteTool()],
        )

    @agent
    def market_trend_analyzer(self) -> Agent:
        return Agent(
            config=self.agents_config['market_trend_analyzer'],
            tools=[SerperDevTool(), ScrapeWebsiteTool()],
        )


    @task
    def collect_company_info_task(self) -> Task:
        return Task(
            config=self.tasks_config['collect_company_info_task'],
            tools=[SerperDevTool(), ScrapeWebsiteTool()],
        )

    @task
    def analyze_digital_presence_task(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_digital_presence_task'],
            tools=[SerperDevTool(), ScrapeWebsiteTool()],
        )

    @task
    def industry_trend_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['industry_trend_analysis_task'],
            tools=[SerperDevTool(), ScrapeWebsiteTool()],
        )

    @task
    def competitor_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['competitor_analysis_task'],
            tools=[SerperDevTool(), ScrapeWebsiteTool()],
        )

    @task
    def consolidated_report_task(self) -> Task:
        return Task(
            config=self.tasks_config['consolidated_report_task'],
            tools=[],
        )

    @task
    def generate_markdown_report_task(self) -> Task:
        return Task(
            config=self.tasks_config['generate_markdown_report_task'],
            tools=[],
            output_file='diagonstic_report.md'
        )


    @crew
    def crew(self) -> Crew:
        """Creates the ComprehensiveBusinessDiagnosticAndMarketAnalysisTool crew"""
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
