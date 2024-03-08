import json
import os
import openai
from typing import List, Dict, Tuple, Generator
from src.base import CompletionData, CompletionResult
from src.constants import (
    BOT_INSTRUCTIONS,
    EXAMPLE_CONVOS,
    MAX_TOKEN
)
from src.utils import logger

openai.api_base = os.environ["OPEN_API_BASE"]


def clean_text(text: str) -> str:
    return text
    # return text.replace('<br>', '\n').replace('<em>', '*').replace('</em>', '*').replace('&quot;', '"')


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
        total_length = total_length + int(conversation_length)

    messages += recent_history[::-1]
    messages = messages + [{"role": "user", "content": clean_text(message)}]
    return messages


def generate_completion_response(
    history: List[Tuple[str, str]],
    message: str
) -> Generator[CompletionData, None, None]:
    try:
        messages = generate_massage(history, message)
        print("Full token:", messages)
        print("Token length: " + str(len(json.dumps(messages)) / 4))

        responses = openai.ChatCompletion.create(
            # model="gpt-3.5-turbo",
            model="gpt-4-1106-preview",
            # model="gpt-4",
            max_tokens=600,
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
            yield CompletionData(
                status=CompletionResult.TOO_LONG, text=None, status_text=str(e)
            )
            return
        else:
            logger.exception(e)
            yield CompletionData(
                status=CompletionResult.INVALID_REQUEST,
                text=None,
                status_text=str(e),
            )
            return
    except Exception as e:
        logger.exception(e)
        # Retry from UI instead
