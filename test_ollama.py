import requests
import json
import config

print(f"Testing URL: {config.OLLAMA_BASE_URL}")
print(f"Testing Model: {config.OLLAMA_MODEL}")

payload = {
    "model": config.OLLAMA_MODEL,
    "prompt": "Hello",
    "stream": False
}

try:
    response = requests.post(config.OLLAMA_BASE_URL, json=payload)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("Success!")
        print(response.json().get("response"))
    else:
        print("Error Response:")
        print(response.text)
except Exception as e:
    print(f"Exception: {e}")
