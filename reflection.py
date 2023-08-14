import openai
import json
from .wrapper import _original_chat_completion

def log_reflection_to_ndjson(kwargs, reflection_response):
    reflection_entry = {
        "kwargs": kwargs,
        "reflection": reflection_response
    }
    
    with open("prompt_reflections.ndjson", mode='a', encoding='utf-8') as file:
        file.write(json.dumps(reflection_entry) + '\n')

def generate_prompt_reflection(kwargs, response):
    # Define the function to analyze and optimize prompts
    function_description = {
        "name": "analyze_and_optimize_prompt",
        "description": "Analyze the prompt and response to provide suggestions for optimization",
        "parameters": {
            "type": "object",
            "properties": {
                "analysis": {
                    "type": "string",
                    "description": "Analysis and possible optimizations for the prompt."
                },
                "is_satisfactory": {
                    "type": "boolean",
                    "description": "Indicates if the prompt was satisfactory."
                },
                "suggested_prompt": {
                    "type": "string",
                    "description": "A better version of the prompt, if applicable."
                }
            },
            "required": ["analysis", "is_satisfactory", "suggested_prompt"]
        },
    }

    function_call = {
        "name": "analyze_and_optimize_prompt",
        "arguments": {
            "prompt": kwargs.get("prompt", ""),  # extract the user's prompt
            "response": response.get("choices", [{}])[0].get("text", "").strip()
        }
    }

    reflection_response = _original_chat_completion(
        model="gpt-3.5-turbo-16k",
        messages=[
            {
                "role": "system",
                "content": "You are an AI assistant specializing in providing advice on the use of large language models, specifically optimizing prompts for the ChatCompletion or Function Call endpoint. Analyze the user message, which will be a JSON array with data about the API call (both input and output), and analyze the user prompt (or function call), and provide suggested improvements."
            },
            {
                "role": "user",
                "content": json.dumps({
                    "kwargs": kwargs,
                    "response": response
                })
            }
        ],
        functions=[function_description],
        function_call=function_call
    )

    reflection_content = reflection_response["choices"][0]["message"]["function_call"]["arguments"]

    # Log the reflection content
    log_reflection_to_ndjson(kwargs, reflection_content)

    return reflection_content
