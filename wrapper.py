import openai
import json
import datetime
import time

_original_chat_completion = openai.ChatCompletion.create

class ChatWrapper:
    reflection_enabled = False

    @staticmethod
    def enable_reflection():
        ChatWrapper.reflection_enabled = True

    @staticmethod
    def disable_reflection():
        ChatWrapper.reflection_enabled = False

    @staticmethod
    def log_to_ndjson(params, task_label, response, response_time):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        model = params.get("model", "")
        total_tokens = response["usage"]["total_tokens"]

        log_entry = {
            "timestamp": timestamp,
            "response_time": round(response_time, 2),
            "params": params,
            "response": response,
            "total_tokens": total_tokens,
            "model": model,
            "taskLabel": task_label  # Add taskLabel here
        }

        with open("log.ndjson", mode='a', encoding='utf-8') as file:
            file.write(json.dumps(log_entry) + '\n')

    @staticmethod
    def enhanced_chat_completion(*args, **kwargs):
        timestamp_start = time.perf_counter()

        # Extract and remove taskLabel from kwargs if it exists
        task_label = kwargs.pop("taskLabel", None)

        # Call the original OpenAI method
        response = _original_chat_completion(*args, **kwargs)

        timestamp_end = time.perf_counter()    
        response_time = timestamp_end - timestamp_start
        
        # Log with taskLabel
        ChatWrapper.log_to_ndjson(kwargs, task_label, response, response_time)

        if ChatWrapper.reflection_enabled:
            from .reflection import generate_prompt_reflection
            generate_prompt_reflection(kwargs, response)

        return response

# Override the ChatCompletion with the enhanced version
openai.ChatCompletion.create = ChatWrapper.enhanced_chat_completion
