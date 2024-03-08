import os
from anthropic import Anthropic, HUMAN_PROMPT
from typing import List, Tuple, Generator
from src.constants import (
    BOT_INSTRUCTIONS,
)

from src.base import CompletionData, CompletionResult
from src.utils import logger

anthropic = Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    # base_url=os.environ.get("ANTHROPIC_API_BASE"),
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)

# Lol too lazy, not implement cutoff anyway


def generate_completion_response(
    history: List[Tuple[str, str]],
    message: str
) -> Generator[CompletionData, None, None]:
    try:
        prompt = f"{BOT_INSTRUCTIONS}\n\n{HUMAN_PROMPT} {message}\n\nAssistant: Here is the translation of the text above:\n"
        stream = anthropic.completions.create(
            prompt=prompt,
            max_tokens_to_sample=800,
            model="claude-2",
            stream=True,
        )

        for completion in stream:
            # print(completion.completion)
            yield CompletionData(status=CompletionResult.OK, text=completion.completion, status_text=None)
            # print(completion.completion)
    except Exception as e:
        logger.exception(e)
        # Retry from UI instead


def generate_completion_response_v2(
    history: List[Tuple[str, str]],
    message: str
) -> Generator[CompletionData, None, None]:
    try:
        with anthropic.messages.stream(
            max_tokens=800,
            model="claude-3-opus-20240229",
            system=BOT_INSTRUCTIONS,
            messages=[
                {
                    "role": "user",
                    "content": message
                }
            ]
        ) as stream:
            for text in stream.text_stream:
                yield CompletionData(status=CompletionResult.OK, text=text, status_text=None)

    except Exception as e:
        logger.exception(e)
        # Retry from UI instead
