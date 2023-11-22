"""agentml/manager.py"""

from pathlib import Path
from uuid import UUID, uuid4

from agentml.models import LlmMessage, LlmRole

from .agents import Agent, Coder, Planner, Vision
from .sandbox import Sandbox


class Manager:
    """Agent Manager Class"""

    STARTING_TASKS: dict[Agent, str] = []

    def __init__(self, goal: str, csv: Path, session_id: UUID = uuid4()) -> None:
        """
        Agent constructor

        Args:
            goal (str): goal of the agent
            csv (Path): CSV file path of the dataset
            session_id (UUID): Session ID
        """

        # Ensure the CSV file exists
        if not csv.exists():
            raise FileNotFoundError(f"Agent: CSV file not found: {csv}")

        self.goal = goal
        self.csv = csv
        self.session_id = session_id

        self.messages: list[LlmMessage] = [
            LlmMessage(
                role=LlmRole.SYSTEM,
                content="Overarching Goal: " + self.goal,
            ),
        ]

        self.sandbox = Sandbox.create(session_id=session_id, files=[csv])

        # Queue of tasks to run
        self.tasks: list[dict[callable, str]] = [
            *self.STARTING_TASKS,
            {
                Planner: "Outline the steps to learn about the dataset to achieve the goal"
            },
        ]

    def run(self) -> None:
        """Run the agent"""

        while self.tasks:
            # Get the next task in the queue
            task = self.tasks.pop(0)

            for agent, objective in task.items():
                print(f"Manager.run: Running agent {agent} with objective: {objective}")
                agent = agent(
                    session_id=self.session_id,
                    objective=objective,
                    messages=self.messages,
                )

                output = agent.run()
                self.messages.extend(output)

                # Handle output based on the agent type
                if isinstance(agent, Planner):
                    self.tasks.extend(
                        [
                            {self.get_agent(task["tool"]): task["objective"]}
                            for task in agent.plan
                        ]
                    )

    def run_single_task(self, task: dict) -> list[LlmMessage]:
        """Run a single task and return its output"""
        agent, objective = list(task.items())[0]
        print(
            f"Manager.run_single_task: Running agent {agent} with objective: {objective}"
        )
        agent = agent(
            session_id=self.session_id,
            objective=objective,
            messages=self.messages,
        )

        output = agent.run()
        return output

    @staticmethod
    def get_agent(agent: str):
        """Get the agent"""
        match agent:
            case "Coder":
                return Coder
            case "Planner":
                return Planner
            case "Vision":
                return Vision
            case _:
                raise ValueError(f"Manager.get_agent: Invalid agent: {agent}")
