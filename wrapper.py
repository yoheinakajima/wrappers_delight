import openai
import json
import datetime

_original_chat_completion = openai.ChatCompletion.create

def log_to_ndjson(params, response):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    model = params.get("model", "")
    total_tokens = response["usage"]["total_tokens"]
    
    log_entry = {
        "timestamp": timestamp,
        "params": params,
        "response": response,
        "total_tokens": total_tokens,
        "model": model
    }
    
    with open("log.ndjson", mode='a', encoding='utf-8') as file:
        file.write(json.dumps(log_entry) + '\n')

def _enhanced_chat_completion(*args, **kwargs):
    response = _original_chat_completion(*args, **kwargs)
    log_to_ndjson(kwargs, response)
    return response

openai.ChatCompletion.create = _enhanced_chat_completion
