from enum import Enum
from dataclasses import dataclass
import openai
from typing import Optional, List
from src.constants import (
    BOT_INSTRUCTIONS,
    BOT_NAME,
    EXAMPLE_CONVOS,
)
from src.base import Message, Prompt, Conversation
from src.utils import logger

MY_BOT_NAME = BOT_NAME
MY_BOT_EXAMPLE_CONVOS = EXAMPLE_CONVOS


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


def generate_completion_response(
    messages: List[Message]
) -> CompletionData:
    try:
        prompt = Prompt(
            header=Message(
                "System", f"Instructions for {MY_BOT_NAME}: {BOT_INSTRUCTIONS}"
            ),
            examples=MY_BOT_EXAMPLE_CONVOS,
            convo=Conversation(messages + [Message(MY_BOT_NAME)]),
        )
        rendered = prompt.render()
        responses = openai.Completion.create(
            engine="text-davinci-003",
            prompt=rendered,
            temperature=1.0,
            top_p=0.9,
            max_tokens=512,
            stop=["<|endoftext|>"],
            stream=True,
        )
        for response in responses:
            text = response.choices[0].text
            yield CompletionData(
                status=CompletionResult.OK, text=text, status_text=None
            )

    except openai.error.InvalidRequestError as e:
        if "This model's maximum context length" in e.user_message:
            return CompletionData(
                status=CompletionResult.TOO_LONG, reply_text=None, status_text=str(e)
            )
        else:
            logger.exception(e)
            return CompletionData(
                status=CompletionResult.INVALID_REQUEST,
                reply_text=None,
                status_text=str(e),
            )
    except Exception as e:
        logger.exception(e)
        # Retry from UI instead
