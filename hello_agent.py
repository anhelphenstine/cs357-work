import requests

response = requests.post(
    "http://host.docker.internal:11434/api/chat",
    json={
        "model": "llama3.2",
        "messages": [{"role": "user", "content": "Say hello to CS357 in five words."}],
        "stream": False,
    },
)
print(response.json()["message"]["content"])
