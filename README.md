# Harry's own chatbot

Original code: <https://github.com/openai/gpt-discord-bot>. No I don't want to fork...

This code removed all the moderation layer. Use at your own risk lol.

## Setup

1. Copy `.env.example` to `.env` and start filling in the values as detailed below.
2. Go to <https://beta.openai.com/account/api-keys>, create a new API key, and fill in `OPENAI_API_KEY`.
3. Open `src/config.yaml` to customize the bot and add some example conversation.
4. Install dependencies

    ```bash
    pip install -r requirements.txt
    ```

5. Run `python -m src.ui` to run the web UI.

## Warning
