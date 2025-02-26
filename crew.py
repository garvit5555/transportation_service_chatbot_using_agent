from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class Myproject():
    """Myproject crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # Define agents
    @agent
    def route_researcher(self) -> Agent:
        return Agent(config=self.agents_config['route_researcher'], verbose=True)

    @agent
    def traffic_analyst(self) -> Agent:
        return Agent(config=self.agents_config['traffic_analyst'], verbose=True)

    @agent
    def personalization_expert(self) -> Agent:
        return Agent(config=self.agents_config['personalization_expert'], verbose=True)

    @agent
    def reporting_analyst(self) -> Agent:
        return Agent(config=self.agents_config['reporting_analyst'], verbose=True)

    # Define tasks
    @task
    def route_research_task(self) -> Task:
        return Task(config=self.tasks_config['route_research_task'])

    @task
    def traffic_analysis_task(self) -> Task:
        return Task(config=self.tasks_config['traffic_analysis_task'])

    @task
    def personalization_task(self) -> Task:
        return Task(config=self.tasks_config['personalization_task'])

    @task
    def reporting_task(self) -> Task:
        return Task(config=self.tasks_config['reporting_task'], output_file='travel_report.md')

    @crew
    def crew(self) -> Crew:
        """Creates the Myproject crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
