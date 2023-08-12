# Wrapper's Delight: An Enhanced OpenAI Wrapper
wrappers_delight is a Python wrapper built around OpenAI's GPT-3 Chat API. It not only allows users to easily converse with the model but also supports custom user-registered functions that the model can call during the conversation. The wrapper also provides automated logging to a CSV file for every interaction.

To get started, you'll need to clone this repository:

```
git clone https://github.com/yoheinakajima/wrappers_delight.git
cd wrappers_delight
```

Ensure you have OpenAI's Python client installed:

```
pip install openai
```
# Usage
## Basic Chat Completion
To use the wrapper for a basic chat with the model:

```
import openai
from wrapper import _enhanced_chat_completion

# Set your OpenAI API key
openai.api_key = "YOUR_API_KEY"

# Engage in a conversation with the model
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Tell me a fun fact."},
    ]
)

print(response.choices[0].message.content)
```
## With Custom Functions
To register and use a custom function:

```
from wrapper import register_function

# Define and register a custom function
def greet(name):
    return f"Hello, {name}!"

register_function("greet_function", greet)

# Use the function in a conversation
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": {
            "function_call": {
                "name": "greet_function",
                "arguments": json.dumps({"name": "Alice"})
            }
        }},
    ]
)

print(response.choices[0].message.content)
```
## Logging
All interactions with the model are automatically logged to log.csv. Each row in the CSV consists of the request parameters and the corresponding model response.

## Contributing
If you'd like to contribute, please fork the repository and make changes as you'd like. Pull requests are warmly welcomed.

## License
Distributed under the MIT License. See LICENSE for more information.
