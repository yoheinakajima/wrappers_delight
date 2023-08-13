# Wrapper's Delight: An Enhanced OpenAI Wrapper
wrappers_delight is a Python wrapper built around OpenAI's ChatCompletion API. The main features of this wrapper are:

Automated logging to a CSV file for every interaction.
Analytics functions for visualizing model usage.
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

# Analytics
To run the analytics and visualize the model's usage:
```
from wrappers_delight.analytics import plot_token_usage, plot_model_distribution

# Generate and display the analytics plots
plot_token_usage()
plot_model_distribution()
```
# Query Logs
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
Example Usage:
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
## Automatic Storage of Log Queries
* The results are stored in the *log_queries* directory with a unique filename.
* Always ensure that sensitive data is properly handled and not exposed.

## Contributing
If you'd like to contribute, please fork the repository and make changes as you'd like. Pull requests are warmly welcomed.

## License
Distributed under the MIT License. See LICENSE for more information.
