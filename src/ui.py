import gradio as gr
import logging
from src.base import Message
import src.constants  # Import ENV variables from .env
from src.completion import generate_completion_response

logging.basicConfig(
    format="[%(asctime)s] [%(filename)s:%(lineno)d] %(message)s", level=logging.INFO
)


def callGPT(original_message):
    sentences = ""

    messages = []
    for message in original_message.split('\n'):
        messages.append(Message(
            user="Harry", text=message))
    response_data = generate_completion_response(
        messages=messages
    )

    for data in response_data:
        sentences = sentences + data.text
        yield '.\n'.join(sentences.split('. ')).strip()


def main():
    demo = gr.Interface(fn=callGPT,
                        inputs=gr.TextArea(label="Chat Input"),
                        outputs=gr.TextArea(label="Chat Output"),
                        title="Chat GPT giả cầy",
                        description="Chat GPT giả cầy - By Hoàng Code Dạo!")
    demo.queue()
    demo.launch()


main()
