from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.knowledge.source.pdf_knowledge_source import PDFKnowledgeSource

resume_source = PDFKnowledgeSource(file_paths=["Resume.pdf"])
job_desc_source = PDFKnowledgeSource(file_paths=["Job_description.pdf"])

memory_config = {
    "provider": "mem0",
    "config": {"user_id": "User"},
}

@CrewBase
class CrewaiKnowledgeChatbot:
    """CrewaiKnowledgeChatbot crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def assistant(self) -> Agent:
        return Agent(
            config=self.agents_config["assistant"],
            memory=True,
            memory_config=memory_config,
            verbose=False,
        )

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
            knowledge_sources=[resume_source, job_desc_source],
            verbose=False,
        )
