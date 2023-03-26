import gradio as gr
import logging
import src.constants  # Import ENV variables from .env
from src.completion import generate_completion_response

TEST_MODE = False  # This should be False all the time. Only set it to true for UI testing

logging.basicConfig(
    format="[%(asctime)s] [%(filename)s:%(lineno)d] %(message)s", level=logging.INFO
)


def callGPT(original_message, history, include_context):
    # Keep linebreak
    original_message = original_message.replace('\n', '<br>')

    if TEST_MODE:
        # Do whatever test here
        test_message = 'hello <br> world <br> from <br> bot <br>' + original_message
        history.append((original_message, test_message))
        yield None, history, history
        return

    yield None, history + [(original_message, '')], history

    response_data = generate_completion_response(
        history if include_context else [], original_message)

    response, result = "", ""
    for data in response_data:
        response = response + data.text
        result = '.<br>'.join(response.split('. ')).strip()
        yield None, history + [(original_message, result)], history

    history.append((original_message, result))
    yield None, history, history


def main():
    with gr.Blocks(css="code {display: block}", title="Chat GPT giả cầy") as demo:
        gr.Markdown("""
            # GPT-chan dễ thương nhất quả đất ( ^ω^ )
        """)
        states = gr.State([])

        include_context = gr.Checkbox(
            label="Include past messages", value=False)
        input = gr.Textbox(label="Chat Input (Enter to submit)")
        chatbot = gr.Chatbot(label="Bot")

        input.submit(fn=callGPT,
                     inputs=[input, states, include_context],
                     outputs=[input, chatbot, states])

    demo.queue()
    demo.launch(share=False)


main()
