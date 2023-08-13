import openai
import json
import csv
import datetime

_original_chat_completion = openai.ChatCompletion.create

def log_to_csv(params, response):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    model = params.get("model", "")
    total_tokens = response["usage"]["total_tokens"]
    
    with open("log.csv", mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, json.dumps(params), json.dumps(response), total_tokens, model])

def _enhanced_chat_completion(*args, **kwargs):
    response = _original_chat_completion(*args, **kwargs)
    log_to_csv(kwargs, response)
    return response

openai.ChatCompletion.create = _enhanced_chat_completion
