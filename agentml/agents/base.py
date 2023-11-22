"""
agentml/agents/base.py

Agent abstract base class file
"""

from abc import ABC, abstractmethod
from uuid import UUID

from agentml.models import LlmMessage


class Agent(ABC):
    """Agent abstract base class"""

    DEFAULT_MODEL: str = "gpt-3.5-turbo-1106"

    DEFAULT_SYSTEM_MESSAGE: str = """You are a helpful AI assistant.
Solve tasks using your coding and language skills.
In the following cases, suggest python code (in a python coding block) for the user to execute.
    1. When you need to collect info, use the code to output the info you need, for example, browse or search the web, download/read a file, print the content of a webpage or a file, get the current date/time, check the operating system. After sufficient info is printed and the task is ready to be solved based on your language skill, you can solve the task by yourself.
    2. When you need to perform some task with code, use the code to perform the task and output the result. Finish the task smartly.
Solve the task step by step if you need to. If a plan is not provided, explain your plan first. Be clear which step uses code, and which step uses your language skill.
When using code, you must indicate the script type in the code block. The user cannot provide any other feedback or perform any other action beyond executing the code you suggest. The user can't modify your code. So do not suggest incomplete code which requires users to modify. Don't use a code block if it's not intended to be executed by the user.
If you want the user to save the code in a file before executing it, put # filename: <filename> inside the code block as the first line. Don't include multiple code blocks in one response. Do not ask users to copy and paste the result. Instead, use 'print' function for the output when relevant. Check the execution result returned by the user.
If the result indicates there is an error, fix the error and output the code again. Suggest the full code instead of partial code or code changes. If the error can't be fixed or if the task is not solved even after the code is executed successfully, analyze the problem, revisit your assumption, collect additional info you need, and think of a different approach to try.
When you find an answer, verify the answer carefully. Include verifiable evidence in your response if possible.
Reply "TERMINATE" in the end when everything is done.
    """

    def __init__(
        self,
        session_id: UUID,
        objective: str,
        messages: list[LlmMessage] = None,
        prompt: str = DEFAULT_SYSTEM_MESSAGE,
    ) -> None:
        """
        Agent abstract base class constructor

        Args:
            session_id (UUID): Session ID
            objective (str): Objective of the agent
            messages (list[LlmMessage], optional): List of messages to be used for the agent. Defaults to [].
            prompt (str, optional): Prompt to be used for the agent. Defaults to DEFAULT_SYSTEM_MESSAGE.
        """

        self.session_id: UUID = session_id
        self.objective: str = objective
        self.messages: list[LlmMessage] = messages or []
        self.prompt: str = prompt

    @abstractmethod
    def run(self) -> list[LlmMessage]:
        """Run the agent"""
        raise NotImplementedError

    def get_messages(self) -> list[dict[str, str]]:
        """
        Get the list of messages

        Returns:
            list[dict[str, str]]: List of messages in JSON format
        """

        return [msg.model_dump(mode="json") for msg in self.messages]
