import requests, json

response = requests.post(
    "http://host.docker.internal:11434/api/chat",
    json={
        "model": "llama3.2",
        "messages": [{"role": "user", "content": "What is 2 + 2?"}],
        "stream": False
    }
)

print(json.dumps(response.json(), indent=2))
