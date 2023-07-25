import os
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
from typing import Optional, List, Dict, Tuple
from src.constants import (
    BOT_INSTRUCTIONS,
)

from src.base import CompletionData, CompletionResult
from src.utils import logger

anthropic = Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)

# Lol too lazy, not implement cutoff anyway


def generate_completion_response(
    history: List[Tuple[str, str]],
    message: str
) -> CompletionData:
    try:
        prompt = f"{BOT_INSTRUCTIONS}\n\n{HUMAN_PROMPT} {message}{AI_PROMPT}"
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
