import gradio as gr
import logging
import src.constants  # Import ENV variables from .env
from src.completion import generate_completion_response as gpt_completion
from src.claude_completion import generate_completion_response as claude_completion

TEST_MODE = False  # This should be False all the time. Only set it to true for UI testing

logging.basicConfig(
    format="[%(asctime)s] [%(filename)s:%(lineno)d] %(message)s", level=logging.INFO
)


def callGPT(original_message, history, include_context):
    if TEST_MODE:
        # Do whatever test here
        test_message = 'hello <br> world <br> from <br> bot <br>' + original_message
        history.append((original_message, test_message))
        yield None, history, history
        return

    yield None, history + [(original_message, '')], history

    response_data = gpt_completion(
        history if include_context else [], original_message)

    response, result = "", ""
    for data in response_data:
        response = response + data.text
        result = response.strip()
        yield None, history + [(original_message, result)], history

    history.append((original_message, result))
    yield None, history, history


def callClaude(original_message, history, include_context):
    yield None, history + [(original_message, '')], history

    response_data = claude_completion(
        history if include_context else [], original_message)

    response, result = "", ""
    for data in response_data:
        response = response + data.text
        result = response.strip()
        yield None, history + [(original_message, result)], history

    history.append((original_message, result))
    yield None, history, history


def main():
    with gr.Blocks(css="code {display: block}", title="Chat GPT giả cầy") as demo:
        # gr.Markdown("""
        #     # GPT-chan dễ thương nhất quả đất ( ^ω^ )
        # """)

        with gr.Row():
            gpt_states = gr.State([])
            claude_states = gr.State([])

            with gr.Column(scale=4):
                claude_chatbot = gr.Chatbot(
                    label="Claude Bot").style(height=600)
                claude_input = gr.Textbox(
                    label="Claude Input (Enter to submit)")

            with gr.Column(scale=4):
                chatbot = gr.Chatbot(label="GPT Bot").style(height=600)
                gpt_input = gr.Textbox(label="GPT Input (Enter to submit)")

        with gr.Row():
            include_context = gr.Checkbox(
                label="Include past messages", value=False)

        claude_input.submit(fn=callClaude,
                            inputs=[claude_input,
                                    claude_states, include_context],
                            outputs=[claude_input, claude_chatbot, claude_states])
        gpt_input.submit(fn=callGPT,
                         inputs=[gpt_input,
                                 gpt_states, include_context],
                         outputs=[gpt_input, chatbot, gpt_states])

    demo.queue()
    demo.launch(share=False)


main()
