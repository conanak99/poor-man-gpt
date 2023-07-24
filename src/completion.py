import json
from enum import Enum
from dataclasses import dataclass
import openai
from typing import Optional, List, Dict, Tuple
from src.constants import (
    BOT_INSTRUCTIONS,
    EXAMPLE_CONVOS,
    MAX_TOKEN
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
    return text.replace('<br>', '\n').replace('<em>', '*').replace('</em>', '*').replace('&quot;', '"')


# Chat GPT helped me write this, no shame
def generate_massage(history: List[Tuple[str, str]], message: str) -> List[Dict[str, str]]:
    messages = [{"role": "system", "content": BOT_INSTRUCTIONS}]
    for convo in EXAMPLE_CONVOS:
        messages = messages + convo.render()

    # remove old messages from history to reduce token count
    total_length = 0
    recent_history = []
    for mes in reversed(history):
        conversation = [
            {"role": "assistant", "content": clean_text(mes[1])},
            {"role": "user", "content": clean_text(mes[0])}
        ]
        conversation_length = len(json.dumps(
            conversation)) / 4  # 1 token = 4 character

        if total_length + conversation_length > MAX_TOKEN:
            break
        recent_history += conversation
        total_length = total_length + conversation_length

    messages += recent_history[::-1]
    messages = messages + [{"role": "user", "content": clean_text(message)}]
    return messages


def generate_completion_response(
    history: List[Tuple[str, str]],
    message: str
) -> CompletionData:
    try:
        messages = generate_massage(history, message)
        print("Full token:", messages)
        print("Token length: " + str(len(json.dumps(messages)) / 4))

        responses = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0301",
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
