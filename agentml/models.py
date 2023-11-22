"""
agentml/models.py

Models
"""

from enum import Enum

from pydantic import BaseModel


class LlmRole(Enum):
    """LLM Message Role"""

    ASSISTANT = "assistant"
    SYSTEM = "system"
    USER = "user"


class LlmMessage(BaseModel):
    """LLM Message"""

    role: LlmRole
    content: str
