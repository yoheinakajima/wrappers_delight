import openai
import json
import csv

# Save the original chat completion method
_original_chat_completion = openai.ChatCompletion.create

# A dictionary to store user-registered functions
_registered_functions = {}

def register_function(name, function):
    """
    Allow users to register their own functions which can be called 
    by the assistant.
    """
    _registered_functions[name] = function

def log_to_csv(params, response):
    with open("log.csv", mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([json.dumps(params), json.dumps(response)])

def _enhanced_chat_completion(*args, **kwargs):
    
    response = _original_chat_completion(*args, **kwargs)

    # If there's a function_call in the response, log the structured data
    if 'function_call' in response.choices[0]['message']:
        log_to_csv(kwargs, response)
    
    return response

# Override the chat completion method
openai.ChatCompletion.create = _enhanced_chat_completion