from dataclasses import dataclass
from typing import List


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
