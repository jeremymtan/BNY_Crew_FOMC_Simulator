from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.knowledge.source.pdf_knowledge_source import PDFKnowledgeSource
from crewai.knowledge.source.csv_knowledge_source import CSVKnowledgeSource
from crewai import LLM
import os

### Add knowledge source, must add pdfs and csv in knoweldege folder
date = "24_3"
pdf_source = PDFKnowledgeSource(
    file_paths=[
        f"{date} beige book.pdf",
        f"{date} current macro.pdf",
        f"{date} dot plot description.pdf",
        "Fed Explanation.pdf",
    ]
)

csv_source = CSVKnowledgeSource(file_paths=[f"{date} historical macro.csv"])

### add llm
managerllm = LLM(model="openai/gpt-4o", temperature=0.03)
# Always keep manager as GPT 4o

gpt_llm = LLM(model="openai/gpt-4o-mini", temperature=0.03)

deepseek_llm = LLM(
    model="deepseek/deepseek-chat", api_key="DEEPSEEK_API_KEY", temperature=1.5
)

claude_llm = LLM(
    model="claude-3-5-sonnet-20240620",
    base_url="https://api.anthropic.com",
    api_key=os.environ["ANTHROPIC_API_KEY"],
)


@CrewBase
class BnyCapstoneCrew:
    """BnyCapstone crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # Define agents
    @agent
    def manager(self) -> Agent:
        return Agent(
            config=self.agents_config["manager"],
            verbose=True,
            llm=managerllm,
            max_iter=50,
        )

    @agent
    def Jerome_H_Powell(self) -> Agent:
        return Agent(
            config=self.agents_config["Jerome_H_Powell"],
            verbose=True,
            llm=claude_llm,
            knowledge_sources=[pdf_source, csv_source],
            max_iter=50,
            memory=True,
        )

    @agent
    def John_C_Williams(self) -> Agent:
        return Agent(
            config=self.agents_config["John_C_Williams"],
            verbose=True,
            llm=claude_llm,
            knowledge_sources=[pdf_source, csv_source],
            max_iter=50,
            memory=True,
        )

    @agent
    def Regional_Regulatory(self) -> Agent:
        return Agent(
            config=self.agents_config["Regional_Regulatory"],
            verbose=True,
            llm=claude_llm,
            knowledge_sources=[pdf_source, csv_source],
            max_iter=50,
            memory=True,
        )

    # Define tasks
    @task
    def discussion_1(self) -> Task:
        return Task(
            config=self.tasks_config["discussion_1"],
        )

    @task
    def discussion_2(self) -> Task:
        return Task(
            config=self.tasks_config["discussion_2"],
        )

    @task
    def summary_3(self) -> Task:
        return Task(
            config=self.tasks_config["summary_3"],
        )

    @task
    def summary_4(self) -> Task:
        return Task(
            config=self.tasks_config["summary_4"],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the BnyCapstone crew"""
        return Crew(
            manager_agent=self.manager(),
            agents=[
                self.Jerome_H_Powell(),
                self.John_C_Williams(),
                self.Regional_Regulatory(),
            ],
            tasks=[
                self.discussion_1(),
                self.discussion_2(),
                self.summary_3(),
                self.summary_4(),
            ],
            process=Process.hierarchical,  # Hierarchical process
            verbose=True,
            memory=True,
            output_log_file="discussion.md",
        )
