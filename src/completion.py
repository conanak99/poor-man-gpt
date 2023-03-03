from enum import Enum
from dataclasses import dataclass
import openai
from typing import Optional, List
from src.constants import (
    BOT_INSTRUCTIONS,
    EXAMPLE_CONVOS,
)
from src.utils import logger


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


def clean_text(text: str) -> str:
    return text.replace('<br>', '\n').replace('<em>', '*').replace('</em>', '*')


def generate_completion_response(
    history,
    message: str
) -> CompletionData:
    try:
        messages = [{"role": "system", "content": BOT_INSTRUCTIONS}]
        for convo in EXAMPLE_CONVOS:
            messages = messages + convo.render()

        for mes in history:
            messages = messages + [
                {"role": "user", "content": clean_text(mes[0])},
                {"role": "assistant", "content": clean_text(mes[1])}
            ]

        messages = messages + \
            [{"role": "user", "content": clean_text(message)}]
        print(messages)

        # TODO: Do something when this get more than 1 token lol

        responses = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            stream=True
        )

        for response in responses:
            choice = response.choices[0]
            if ('content' in choice.delta):
                text = choice.delta.content
                yield CompletionData(status=CompletionResult.OK, text=text, status_text=None)

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
