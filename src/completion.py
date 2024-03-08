import json
import os
from openai import OpenAI
from typing import List, Dict, Tuple, Generator
from src.base import CompletionData, CompletionResult
from src.constants import (
    BOT_INSTRUCTIONS,
    EXAMPLE_CONVOS,
    MAX_TOKEN
)
from src.utils import logger

client = OpenAI(
    base_url=os.environ["OPENAI_API_BASE"],
    api_key=os.environ["OPENAI_API_KEY"],
)

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

        responses = client.chat.completions.create(
            # model="gpt-4-1106-preview",
            model="gpt-4",
            max_tokens=600,
            messages=messages,
            stream=True
        )

        for response in responses:
            text = response.choices[0].delta.content or ""
            yield CompletionData(status=CompletionResult.OK, text=text, status_text=None)
    except Exception as e:
        logger.exception(e)
        # Retry from UI instead
