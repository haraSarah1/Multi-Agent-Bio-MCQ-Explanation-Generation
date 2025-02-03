import requests
import json
import os
from message import azure1_message

def azure_generate_json(message,max_tokens=1000):
    headers = {
        'Content-Type': 'application/json',
        'api-key': os.getenv("OPENAI_API_KEY"),
    }
    data = {
        'messages': message,
        'max_tokens': max_tokens,
    }
    url = os.getenv("AZURE_OPENAI_ENDPOINT")
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        return response.json()['choices'][0]['message']
    else:
        print(f"Request failed with status code {response.status_code}: {response.text}")


if __name__ == '__main__':
    question = """
    hihi
    """
    solution = """
    hihi
    """
    message_a1 = azure1_message(question,solution)
    rep = azure_generate_json(message_a1)
    print(rep)