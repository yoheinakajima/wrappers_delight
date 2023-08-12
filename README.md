# Wrapper's Delight: An Enhanced OpenAI Wrapper
wrappers_delight is a Python wrapper built around OpenAI's ChatCompletion API. The wrapper provides automated logging to a CSV file for every interaction without needing to change any existing code.

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
from wrappers_delight.wrapper import _enhanced_chat_completion

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
import openai
from wrappers_delight.wrapper import _enhanced_chat_completion

# Set your OpenAI API key
openai.api_key = "YOUR_OPENAI_KEY"

completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-0613",
    messages=[
        {
            "role": "user", 
            "content": "I visited Tokyo, then moved to San Francisco, and finally settled in Toronto."
        }
    ],
    functions=[
        {
            "name": "extract_locations",
            "description": "Extract all locations mentioned in the text",
            "parameters": {
                "type": "object",
                "properties": {
                    "locations": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {
                                    "type": "string",
                                    "description": "The name of the location"
                                },
                                "country_iso_alpha2": {
                                    "type": "string",
                                    "description": "The ISO alpha-2 code of the country where the location is situated"
                                }
                            },
                            "required": ["name", "country_iso_alpha2"]
                        }
                    }
                },
                "required": ["locations"],
            },
        },
    ],
    function_call={"name": "extract_locations"}
)

response_data = completion.choices[0]['message']['function_call']['arguments']
print(response_data)
```
## Logging
All interactions with the model are automatically logged to log.csv. Each row in the CSV consists of the request parameters and the corresponding model response.

## Contributing
If you'd like to contribute, please fork the repository and make changes as you'd like. Pull requests are warmly welcomed.

## License
Distributed under the MIT License. See LICENSE for more information.
