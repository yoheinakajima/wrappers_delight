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
    
    # If there's a function_call in the latest message, execute it before calling the original completion
    latest_message = kwargs["messages"][-1]
    if "function_call" in latest_message["content"]:
        function_name = latest_message["content"]["function_call"]["name"]
        function_args = json.loads(latest_message["content"]["function_call"]["arguments"])
        
        if function_name in _registered_functions:
            function_response = _registered_functions[function_name](**function_args)
            
            kwargs["messages"].append({
                "role": "function",
                "name": function_name,
                "content": function_response
            })
    
    # Now call the original completion and log the response
    response = _original_chat_completion(*args, **kwargs)
    log_to_csv(kwargs, response)
    
    return response

# Override the chat completion method
openai.ChatCompletion.create = _enhanced_chat_completion
