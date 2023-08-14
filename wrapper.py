import openai
import json
import datetime

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

    @staticmethod
    def enhanced_chat_completion(*args, **kwargs):
        response = _original_chat_completion(*args, **kwargs)
        ChatWrapper.log_to_ndjson(kwargs, response)

        if ChatWrapper.reflection_enabled:
            from .reflection import generate_prompt_reflection
            generate_prompt_reflection(kwargs, response)

        return response

# Override the ChatCompletion with the enhanced version
openai.ChatCompletion.create = ChatWrapper.enhanced_chat_completion
