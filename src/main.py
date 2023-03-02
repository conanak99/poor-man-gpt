import src.constants  # Import ENV variables from .env
import openai

responses = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who won the world series in 2020?"},
        {"role": "assistant",
            "content": "The Los Angeles Dodgers won the World Series in 2020."},
        {"role": "user", "content": "Where was it played?"}
    ],
    stream=True
)
for response in responses:
    choice = response.choices[0]
    if ('content' in choice.delta):
        print(choice.delta.content)
