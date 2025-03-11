from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.knowledge.source.pdf_knowledge_source import PDFKnowledgeSource
from .models import (
    EvaluationOutput,
    SkillAssessment
)

# resume_source = PDFKnowledgeSource(file_paths=["Resume.pdf"])
# job_desc_source = PDFKnowledgeSource(file_paths=["Job_description.pdf"])
from langchain_groq import ChatGroq  # Import Groq LLM

# Load Groq API Key from Environment Variables
import os
groq_api_key = os.getenv("GROQ_API_KEY")

# Ensure you set your API key in your environment before running
if not groq_api_key:
    raise ValueError("GROQ_API_KEY is missing. Set it in your environment.")

memory_config = {
    "provider": "mem0",
    "config": {"user_id": "User","output_format":"v1.1"},
}


@CrewBase
class CrewaiKnowledgeChatbot:
    """CrewaiKnowledgeChatbot crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    llm = ChatGroq(model="groq/llama-3.3-70b-versatile", groq_api_key=groq_api_key)

    # def __init__(self):
        # print(f"Available agents: {self.agents_config.items()}")  # Debugging step
        # print(f"Task Config: {self.tasks_config.items()}")
            
    @agent
    def interviewer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["interviewer_agent"],
            memory=True,
            memory_config=memory_config,
            verbose=False,
            llm=self.llm

        )

    @agent
    def evaluator_agent(self) -> Agent:
        """AI Evaluator responsible for analyzing candidate responses."""
        return Agent(
            config=self.agents_config["evaluator_agent"],
            memory=True,
            memory_config=memory_config,
            verbose=True,
            output_file='output/evalution_output.json',
            output_pydantic=EvaluationOutput,
            llm=self.llm
        )

    # @task
    # def problem_solving_task(self) -> Task:
    #     return Task(config=self.tasks_config["problem_solving_task"])

    # @task
    # def coding_task(self) -> Task:
    #     return Task(config=self.tasks_config["coding_task"])

    # @task
    # def sdlc_task(self) -> Task:
    #     return Task(config=self.tasks_config["sdlc_task"])

    # @task
    # def general_knowledge_task(self) -> Task:
    #     return Task(config=self.tasks_config["general_knowledge_task"])

    # @task
    # def essential_skills_task(self) -> Task:
    #     return Task(config=self.tasks_config["essential_skills_task"])

    @task
    def evaluation_task(self) -> Task:
        return Task(config=self.tasks_config["evaluation_task"])

    @task
    def chat_task(self) -> Task:
        return Task(
            config=self.tasks_config["chat_task"],
        )

    @crew
    def crew(self) -> Crew:

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            # knowledge_sources=[resume_source, job_desc_source],
            verbose=False,
        )
