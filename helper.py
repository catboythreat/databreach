import requests
import os
from dotenv import load_dotenv

load_dotenv()

snusbase_auth = os.getenv("SNUSBASE_AUTH")
snusbase_api = "https://api.snusbase.com/"

def send_request(url, body=None):
    headers = {
        "Auth": snusbase_auth,
        "Content-Type": "application/json",
    }
    method = 'POST' if body else 'GET'
    response = requests.request(method, snusbase_api + url, headers=headers, json=body)
    return response.json()
