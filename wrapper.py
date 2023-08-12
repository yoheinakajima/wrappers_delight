import openai
import json
import csv

# Save the original chat completion method
_original_chat_completion = openai.ChatCompletion.create

def log_to_csv(params, response):
    with open("log.csv", mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([json.dumps(params), json.dumps(response)])

def _enhanced_chat_completion(*args, **kwargs):
    
    response = _original_chat_completion(*args, **kwargs)
    
    # Log every response regardless of whether there's a function_call or not
    log_to_csv(kwargs, response)
    
    return response

# Override the chat completion method
openai.ChatCompletion.create = _enhanced_chat_completion