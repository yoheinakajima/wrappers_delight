# Wrapper's Delight: An Enhanced OpenAI Wrapper
**`wrappers_delight`** is a Python wrapper built around OpenAI's ChatCompletion API. The main features of this wrapper are:

* Automated logging to a CSV file for every interaction.
* Analytics functions for visualizing model usage.
* Parameter-based or AI-assisted querying of logs.
To get started, you'll need to clone this repository:

```
git clone https://github.com/yoheinakajima/wrappers_delight.git
cd wrappers_delight
```
## Prerequisites
Ensure you have OpenAI's Python client installed:

```
pip install openai
```
# Usage
## Basic Chat Completion
To use the wrapper for a basic chat with the model, load the wrapper and every prompt input and output will be stored:<br>
**Aside from line 2, this is a standard OpenAI ChatCompletion call.*
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
To register and use a custom function:<br>
**Aside from line 2, this is a standard OpenAI ChatCompletion call using functions.*
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
## Example Output
The following are 2 example outputs in log.csv. The first is a standard ChatCompletion call, the second is a function call:
```
{"timestamp": "2023-08-13 03:00:49", "params": {"model": "gpt-3.5-turbo", "messages": [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": "Tell me a fun fact."}]}, "response": {"id": "chatcmpl-7mvdPu0H1QULvDZOUVJS6npdMslul", "object": "chat.completion", "created": 1691895647, "model": "gpt-3.5-turbo-0613", "choices": [{"index": 0, "message": {"role": "assistant", "content": "Sure! Here's a fun fact: Did you know that honey never spoils? Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly edible! Honey's low moisture content and acidic pH create an inhospitable environment for bacteria and other microorganisms, allowing it to last indefinitely."}, "finish_reason": "stop"}], "usage": {"prompt_tokens": 23, "completion_tokens": 70, "total_tokens": 93}}, "total_tokens": 93, "model": "gpt-3.5-turbo"}
{"timestamp": "2023-08-13 03:01:16", "params": {"model": "gpt-3.5-turbo-0613", "messages": [{"role": "user", "content": "I visited Tokyo, then moved to San Francisco, and finally settled in Toronto."}], "functions": [{"name": "extract_locations", "description": "Extract all locations mentioned in the text", "parameters": {"type": "object", "properties": {"locations": {"type": "array", "items": {"type": "object", "properties": {"name": {"type": "string", "description": "The name of the location"}, "country_iso_alpha2": {"type": "string", "description": "The ISO alpha-2 code of the country where the location is situated"}}, "required": ["name", "country_iso_alpha2"]}}}, "required": ["locations"]}}], "function_call": {"name": "extract_locations"}}, "response": {"id": "chatcmpl-7mvdqfScl0uQ2tfye1HdfcPEV5XYI", "object": "chat.completion", "created": 1691895674, "model": "gpt-3.5-turbo-0613", "choices": [{"index": 0, "message": {"role": "assistant", "content": null, "function_call": {"name": "extract_locations", "arguments": "{\n  \"locations\": [\n    {\n      \"name\": \"Tokyo\",\n      \"country_iso_alpha2\": \"JP\"\n    },\n    {\n      \"name\": \"San Francisco\",\n      \"country_iso_alpha2\": \"US\"\n    },\n    {\n      \"name\": \"Toronto\",\n      \"country_iso_alpha2\": \"CA\"\n    }\n  ]\n}"}}, "finish_reason": "stop"}], "usage": {"prompt_tokens": 83, "completion_tokens": 74, "total_tokens": 157}}, "total_tokens": 157, "model": "gpt-3.5-turbo-0613"}
```

# Analytics
To run the analytics and visualize the model's usage, load the analytics:
```
from wrappers_delight.analytics import plot_token_usage, plot_model_distribution

# Generate and display the analytics plots
plot_token_usage()
plot_model_distribution()
```
# Query Logs
To enable querying your logs, load the two query functions:
```
from wrappers_delight.analytics import query_log, query_log_with_ai
```
*query_log()* and *query_log_with_ai()* are functions that serve to retrieve specific entries from logs. While query_log directly queries the log based on various parameters, query_log_with_ai uses an AI model to further refine those results based on context or more complex requirements.
## Prerequisits
Ensure you have the required libraries installed. This includes pandas, openai, and others depending on your needs.
## using query_log()
Parameters:
* columns: List of columns to be displayed in the result.
* start_date: The starting date for the logs you want to retrieve.
* end_date: The end date for the logs.
* min_tokens: Minimum number of tokens in the response.
* max_tokens: Maximum number of tokens in the response.
* filter_by: Additional filter criteria.
* sort_by: The column by which the results should be sorted (default is timestamp).
* limit: Limit the number of rows in the result.
* keyword: Search for a keyword in user message or response.
* function_name: Filter by the function name.
* model_version: Filter by model version.

Sample Code:

```
result = query_log(start_date="2023-08-01", end_date="2023-08-10", keyword="weather")
print(result)
```
## using query_log_with_ai
This function interprets natural language user queries and translates them into parameters to fetch appropriate log entries using the query_log function.
### Example Usage:
User Query:
```
result = query_log_with_ai("Show me the last 3 logs.")
```
Expected Parameters for query_log:
```
{
    "limit": 3,
    "sort_by": "timestamp"
}
```
User Query:
```
result = query_log_with_ai("I'd like to see the top 5 logs that mention 'weather'.")
```
Expected Parameters for query_log:
```
{
    "keyword": "weather",
    "limit": 5
}
```
User Query:
```
result = query_log_with_ai("Can you display the logs sorted by total tokens for the gpt-3.5-turbo model, but only show the timestamp, model, and total tokens columns?
")
```
Expected Parameters for query_log:
```
{
    "model_version": "gpt-3.5-turbo",
    "sort_by": "total_tokens",
    "columns": ["timestamp", "model", "total_tokens"]
}
```
User Query:
```
result = query_log_with_ai("I want logs that used between 50 to 1000 tokens and only used the gpt-3.5-turbo model.")
```
Expected Parameters for query_log:
```
{
    "min_tokens": 50,
    "max_tokens": 1000,
    "filter_by": {
        "model": "gpt-3.5-turbo"
    }
}
```
User Query:
```
result = query_log_with_ai("Show me the logs from August 12th to August 14th.")
```
Expected Parameters for query_log:
```
{
    "start_date": "2023-08-12",
    "end_date": "2023-08-14"
}
```
The *`query_log_with_ai()`* function will automatically use the generated parameters to call the *`query_log()`* function. The examples above were provides to help you understand the capabilities of *`query_log_with_ai()`* while also providing you with additional examples for the *`query_log()`* function.

## Automatic Storage of Log Queries
* The results are stored in the *log_queries* directory with a unique filename.
* Always ensure that sensitive data is properly handled and not exposed.

## Contributing
If you'd like to contribute, please fork the repository and make changes as you'd like. Pull requests are warmly welcomed.

## License
Distributed under the MIT License. See LICENSE for more information.
