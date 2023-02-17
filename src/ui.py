import gradio as gr
import logging
from src.base import Message
import src.constants  # Import ENV variables from .env
from src.completion import generate_completion_response

logging.basicConfig(
    format="[%(asctime)s] [%(filename)s:%(lineno)d] %(message)s", level=logging.INFO
)


def callGPT(original_message, history):
    yield None, history + [(original_message, '')], history

    messages = []
    for message in original_message.split('\n'):
        messages.append(Message(user="Harry", text=message))
    response_data = generate_completion_response(messages=messages)

    response = ""
    result = ""
    for data in response_data:
        response = response + data.text
        result = '.\n'.join(response.split('. ')).strip()
        yield None, history + [(original_message, result)], history

    history.append((original_message, result))
    yield None, history, history


def main():
    with gr.Blocks(title="Chat GPT giả cầy") as demo:
        gr.Markdown("""
            # Chat GPT giả cầy

            Chat GPT giả cầy - By Hoàng Code Dạo!
        """)
        states = gr.State([])

        input = gr.Textbox(label="Chat Input (Enter to submit)")
        chatbot = gr.Chatbot(label="Chat Output")

        input.submit(fn=callGPT,
                     inputs=[input, states],
                     outputs=[input, chatbot, states])

    demo.queue()
    demo.launch()


main()
