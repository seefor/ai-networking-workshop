from ollama import generate

text = """
router bgp 65001
 neighbor 10.0.0.1 remote-as 65002
 neighbor 10.0.0.1 description CORE-RTR-01
"""

response = generate(
    model="llama3.2",
    prompt=text
)

print(f"Tokens: {response['prompt_eval_count']}")