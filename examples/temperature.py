import requests

prompt = "Generate a BGP configuration for AS 65001 with neighbor 10.0.0.1"

# Temperature 0.0
response = requests.post("http://localhost:11434/api/generate", json={
    "model": "llama3.2:3b",
    "prompt": prompt,
    "stream": False,
    "options": {"temperature": 1.5, "num_predict": 200}
}).json()
print(response["response"])