import gradio as gr
import logging
from src.base import Message
import asyncio
import src.constants  # Import ENV variables from .env
from src.completion import generate_completion_response

logging.basicConfig(
    format="[%(asctime)s] [%(filename)s:%(lineno)d] %(message)s", level=logging.INFO
)


async def callGPT(original_message):
    messages = []
    for message in original_message.split('\n'):
        messages.append(Message(
            user="Harry", text=message))
    response_data = await generate_completion_response(
        messages=messages
    )
    return '.\n'.join(response_data.reply_text.split('. '))


async def main():
    demo = gr.Interface(fn=callGPT, inputs=gr.TextArea(
        label="Chat Input"), outputs=gr.TextArea(label="Chat Output"))
    demo.launch()

asyncio.run(main())
