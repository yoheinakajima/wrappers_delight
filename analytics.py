import os
import openai
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
from .wrapper import _original_chat_completion

LOG_FILE = 'log.ndjson'

def calculate_cost(tokens):
    COST_PER_TOKEN = 0.01
    return tokens * COST_PER_TOKEN

def plot_token_usage():
    data = pd.read_json(LOG_FILE, lines=True)
    dates = data['timestamp']
    token_counts = data['total_tokens']
    
    plt.plot(dates, token_counts)
    plt.xticks(rotation=45)
    plt.ylabel("Tokens")
    plt.xlabel("Timestamp")
    plt.title("Token Usage Over Time")
    plt.tight_layout()
    plt.savefig("token_usage.png")

def plot_model_distribution():
    data = pd.read_json(LOG_FILE, lines=True)
    models = data['model'].value_counts().to_dict()

    plt.pie(models.values(), labels=models.keys(), autopct='%1.1f%%')
    plt.title("Model Usage Distribution")
    plt.savefig("model_distribution.png")


def query_log(columns=None, start_date=None, end_date=None, min_tokens=None, 
              max_tokens=None, filter_by=None, sort_by='timestamp', limit=None, keyword=None, 
              function_name=None, model_version=None):
    """
    This function queries the log based on various parameters.
    """
    data = pd.read_json(LOG_FILE, lines=True)

    # Helper function to extract the user's message
    def extract_user_message(params):
        for msg in params['messages']:
            if msg['role'] == 'user' and 'content' in msg:
                return msg['content']
        return None

    # Extract the user's message
    data['user_message'] = data['params'].apply(extract_user_message)

    # Helper function to extract the assistant's response
    def extract_response_content(row):
        if 'function_call' in row:
            return str(row['function_call'])
        elif 'choices' in row and len(row['choices']) > 0:
            content = row['choices'][0]['message'].get('content')
            return content if content else None
        return None

    # Extract the assistant's response
    data['response_content'] = data['response'].apply(extract_response_content)

    # Combine the user's message and the assistant's response
    data['combined_content'] = data['user_message'].astype(str) + " | " + data['response_content'].astype(str)
    
    # Filter by date range
    if start_date:
        data = data[data['timestamp'] >= start_date]
    if end_date:
        data = data[data['timestamp'] <= end_date]

    # Filter by token range
    if min_tokens:
        data = data[data['total_tokens'] >= min_tokens]
    if max_tokens:
        data = data[data['total_tokens'] <= max_tokens]

    # Search for a keyword in combined_content
    if keyword:
        data = data[data['combined_content'].str.contains(keyword, case=False)]

    # Filter by function name or model version 
    if function_name:
        data = data[data['function_name'] == function_name]

    if model_version:
        data = data[data['model'] == model_version]

    # Additional filter criteria
    if filter_by:
        for key, value in filter_by.items():
            data = data[data[key] == value]
    
    # Select specific columns
    if columns:
        data = data[columns]

    # Sort the data
    if sort_by:
        data = data.sort_values(by=sort_by, ascending=False)

    # Limit number of rows
    if limit:
        data = data.head(limit)

    # Use the create_file_name function to get the filename
    csv_filename = os.path.join("log_queries", create_file_name(start_date, end_date, keyword, model_version))
    
    if not os.path.exists('log_queries'):
        os.makedirs('log_queries')
    
    data.to_csv(csv_filename, index=False)

    return data


def create_file_name(start_date=None, end_date=None, keyword=None, model_version=None):
    """
    Create a file name based on the given parameters.
    
    Parameters:
        - start_date (str): The start date of the log.
        - end_date (str): The end date of the log.
        - keyword (str): The keyword used in the query.
        - model_version (str): The model version used in the query.

    Returns:
        str: The constructed file name.
    """
    details = []

    if start_date and end_date:
        details.append(f"date_{start_date}_to_{end_date}")
    elif start_date:
        details.append(f"from_{start_date}")
    elif end_date:
        details.append(f"until_{end_date}")

    if keyword:
        details.append(f"keyword_{keyword}")

    if model_version:
        details.append(f"model_{model_version}")

    # Combining the details with underscores and limiting the length to ensure the filename isn't too long
    details_str = '_'.join(details)[:150]  # Limiting to 150 characters
    timestamp_str = datetime.now().strftime('%Y%m%d_%H%M%S')

    return f"query_{timestamp_str}_{details_str}.csv"


def query_log_with_ai(natural_language_input):
    # Define the initial session prompt
    messages = [
        {
            "role": "system",
            "content": """
            The function 'query_log' allows users to query a log of API requests based on various parameters. 
            The available functionalities within 'query_log' are:
            1. Filtering by specific date ranges using 'start_date' and 'end_date'.
            2. Filtering by a range of token counts using 'min_tokens' and 'max_tokens'.
            3. Searching for keywords in the prompt and response using 'keyword'.
            4. Filtering by specific function names using 'function_name'.
            5. Filtering by specific model versions using 'model_version'.
            6. Adding custom filters through the 'filter_by' dictionary.
            7. Specifying columns to return using 'columns'.
            8. Sorting results by a specific column using 'sort_by' (default is 'timestamp').
            9. Limiting the number of rows returned using 'limit'.
            10. Always include .
            The goal is to turn natural language requests into specific queries for the 'query_log' function.
            """
        },
        {
            "role": "user",
            "content": "Show me the logs from August 12th to August 14th."
        },
        {
            "role": "assistant",
            "content": "{'start_date': '2023-08-12', 'end_date': '2023-08-14'}"
        },
        {
            "role": "user",
            "content": "I'd like to see the top 5 logs that mention 'weather'."
        },
        {
            "role": "assistant",
            "content": "{'keyword': 'weather', 'limit': 5}"
        },
        {
            "role": "user",
            "content": "Can you display the logs sorted by total tokens for the gpt-3.5-turbo model, but only show the timestamp, model, and total tokens columns?"
        },
        {
            "role": "assistant",
            "content": "{'model_version': 'gpt-3.5-turbo', 'sort_by': 'total_tokens', 'columns': ['timestamp', 'model', 'total_tokens']}"
        },
        {
            "role": "user",
            "content": "I want logs that used between 50 to 1000 tokens and only used the gpt-3.5-turbo model."
        },
        {
            "role": "assistant",
            "content": "{'min_tokens': 50, 'max_tokens': 1000, 'filter_by': {'model': 'gpt-3.5-turbo'}}"
        },
        {
            "role": "user",
            "content": "Give me up to 3 logs between August 10th and 15th, and only show their timestamp and response."
        },
        {
            "role": "assistant",
            "content": "{'start_date': '2023-08-10', 'end_date': '2023-08-15', 'columns': ['timestamp', 'response'], 'limit': 3}"
        },
        {
            "role": "user",
            "content": natural_language_input
        }
    ]

    # Send the messages to OpenAI's ChatCompletion API
    response = _original_chat_completion(
        model="gpt-3.5-turbo",
        messages=messages
    )

    # Extract the query from the assistant's most recent message
    query_str = response.choices[0].message['content'].strip()

    # Evaluate the query to get a Python dictionary
    query_dict = eval(query_str)

    # Use the query_log function to fetch the results
    results = query_log(**query_dict)

    return results
