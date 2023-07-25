from dataclasses import dataclass
from enum import Enum
from typing import Optional, List


@dataclass
class Conversation:
    question: str
    answer: str

    def render(self):
        return [{"role": 'user', "content": self.question}, {"role": 'assistant', "content": self.answer}]


@dataclass(frozen=True)
class Config:
    instructions: str
    example_conversations: List[Conversation]


class CompletionResult(Enum):
    OK = 0
    TOO_LONG = 1
    INVALID_REQUEST = 2
    OTHER_ERROR = 3


@dataclass
class CompletionData:
    status: CompletionResult
    text: Optional[str]
    status_text: Optional[str]
