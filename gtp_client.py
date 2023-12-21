
from openai import OpenAI


def create_gpt_client():
    with open('/etc/OPENAI_API_KEY', 'r') as file:
        api_key = file.read().strip()
    return  OpenAI(api_key=api_key)