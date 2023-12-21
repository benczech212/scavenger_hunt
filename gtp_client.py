
from openai import OpenAI

def get_api_key():
    with open('E:\\dev\\api_keys\\OPENAI_API_KEY', 'r') as file:
        api_key = file.read().strip()
    return api_key

def create_gpt_client():
    return  OpenAI(api_key=get_api_key())