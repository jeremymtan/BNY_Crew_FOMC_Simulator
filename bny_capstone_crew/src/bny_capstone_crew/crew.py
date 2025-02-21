from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.knowledge.source.pdf_knowledge_source import PDFKnowledgeSource
from crewai.knowledge.source.csv_knowledge_source import CSVKnowledgeSource
from crewai import LLM

### Add knowledge source, must add pdfs and csv in knoweldege folder
pdf_source = PDFKnowledgeSource(
    file_paths=[
        "BeigeBook_20230419.pdf",
        "current macro 5_23.pdf",
        "may 2023 dot plot description.pdf",
        "Fed Explanation.pdf",
        "fomcminutes_may2023.pdf",
        "prior_statement_may2023.pdf",
    ]
)

csv_source = CSVKnowledgeSource(file_paths=["Historical_macro_data_523.csv"])

### add llm
managerllm = LLM(model="openai/gpt-4o", temperature=0.03)
memberllm = LLM(model="openai/gpt-4o-mini", temperature=0.03)


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
            llm=memberllm,
            knowledge_sources=[pdf_source, csv_source],
            max_iter=50,
            memory=True,
        )

    @agent
    def John_C_Williams(self) -> Agent:
        return Agent(
            config=self.agents_config["John_C_Williams"],
            verbose=True,
            llm=memberllm,
            knowledge_sources=[pdf_source, csv_source],
            max_iter=50,
            memory=True,
        )

    @agent
    def Regional_Regulatory(self) -> Agent:
        return Agent(
            config=self.agents_config["Regional_Regulatory"],
            verbose=True,
            llm=memberllm,
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
