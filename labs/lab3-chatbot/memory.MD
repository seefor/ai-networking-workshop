Absolutely. This script is **Lab 3 Part B**, and it shows the next step after the stateless chatbot.

The big idea:

> Instead of sending each question to Ollama by itself, this chatbot keeps a running conversation history and sends that history back with every new prompt.

That is what gives the bot “memory.”

---

# Lab 3 Part B: Stateful Chatbot with Memory

## What This Script Does

This script creates a simple **stateful chatbot** using Ollama.

Unlike the stateless version, this chatbot remembers previous messages in the conversation. That means you can ask a follow-up question like:

```text
What did I just ask you?
```

And the bot can answer correctly because the previous user question is stored in memory and included in the next prompt.

---

## Why This Matters

A stateless chatbot treats every message like a brand-new conversation.

A stateful chatbot keeps context.

That context is important when building real AI assistants for things like:

* Network troubleshooting
* Configuration review
* Multi-step reasoning
* Change planning
* Incident response
* Chatbots that need to remember what the user already asked

For example:

```text
User: What is OSPF?
Bot: OSPF is a link-state routing protocol...

User: What did I just ask you?
Bot: You asked me what OSPF is.
```

That only works because the chatbot stores the conversation history.

---

# Main Components

## 1. Imports

```python
import requests
import json
from typing import List, Dict
```

The script imports:

* `requests` to call the Ollama API
* `json`, although it is not really used directly in this script
* `List` and `Dict` to make the type hints clearer

This line:

```python
from typing import List, Dict
```

helps describe that the conversation history will be a list of dictionaries.

Example:

```python
[
    {"role": "user", "content": "What is OSPF?"},
    {"role": "assistant", "content": "OSPF is a routing protocol..."}
]
```

---

# The `NetworkChatbot` Class

```python
class NetworkChatbot:
    """Chatbot with conversation memory for network engineering."""
```

This class wraps the chatbot logic into one reusable object.

Instead of having loose functions everywhere, the chatbot now has:

* a model name
* a conversation history
* a system prompt
* a chat method
* a reset method
* a history counter

This is a cleaner structure and closer to how real chatbot applications are built.

---

## 2. The `__init__` Method

```python
def __init__(self, model: str = "llama3.2:3b"):
    self.model = model
    self.conversation_history: List[Dict[str, str]] = []
    self.system_prompt = """You are a network engineer assistant.

Available devices:
- spine1, spine2 (core switches)
- leaf1, leaf2 (access switches)

Provide accurate, concise answers about networking."""
```

This runs when you create a new chatbot:

```python
bot = NetworkChatbot()
```

It sets up three important things.

---

## The Model

```python
self.model = model
```

By default, the script uses:

```text
llama3.2:3b
```

That means Ollama must have that model downloaded already.

You can pull it with:

```bash
ollama pull llama3.2:3b
```

---

## The Conversation History

```python
self.conversation_history: List[Dict[str, str]] = []
```

This is where memory is stored.

At the beginning, it is empty:

```python
[]
```

After the user asks something, the script adds:

```python
{"role": "user", "content": "What is OSPF?"}
```

After the assistant replies, it adds:

```python
{"role": "assistant", "content": "OSPF is a routing protocol..."}
```

So over time, the history grows.

---

## The System Prompt

```python
self.system_prompt = """You are a network engineer assistant.

Available devices:
- spine1, spine2 (core switches)
- leaf1, leaf2 (access switches)

Provide accurate, concise answers about networking."""
```

The system prompt tells the model how to behave.

In this case, it says:

* Act like a network engineer assistant
* Assume these devices exist:

  * `spine1`
  * `spine2`
  * `leaf1`
  * `leaf2`
* Keep answers accurate and concise

This gives the chatbot a role and some basic context.

---

# The `chat()` Method

```python
def chat(self, user_message: str) -> str:
    """Send message with full conversation history."""
```

This is the main method.

Every time the user sends a message, this function:

1. Adds the user message to conversation history
2. Builds a full prompt with all previous messages
3. Sends that prompt to Ollama
4. Gets the assistant response
5. Adds the assistant response to history
6. Returns the response

---

## Step 1: Add User Message to History

```python
self.conversation_history.append({
    "role": "user",
    "content": user_message
})
```

When the user types:

```text
What is OSPF?
```

The script stores it like this:

```python
{
    "role": "user",
    "content": "What is OSPF?"
}
```

This is the first part of the memory.

---

## Step 2: Build the Full Prompt

```python
full_prompt = self._build_prompt()
```

This calls another method named `_build_prompt()`.

That method takes the system prompt and all previous messages, then turns them into one big prompt string.

Example:

```text
You are a network engineer assistant.

Available devices:
- spine1, spine2 (core switches)
- leaf1, leaf2 (access switches)

Provide accurate, concise answers about networking.

User: What is OSPF?
Assistant:
```

On the second question, the prompt becomes something like:

```text
You are a network engineer assistant.

Available devices:
- spine1, spine2 (core switches)
- leaf1, leaf2 (access switches)

Provide accurate, concise answers about networking.

User: What is OSPF?
Assistant: OSPF is a link-state routing protocol...
User: What did I just ask you?
Assistant:
```

That is the key difference.

The model is not magically remembering.

The script is resending the previous conversation every time.

---

## Step 3: Call Ollama

```python
url = "http://localhost:11434/api/generate"
```

This is the local Ollama API endpoint.

The script assumes Ollama is running locally on your machine.

You can start Ollama with:

```bash
ollama serve
```

---

## The Payload

```python
payload = {
    "model": self.model,
    "prompt": full_prompt,
    "stream": False,
    "options": {
        "temperature": 0.7,
        "num_predict": 1024
    }
}
```

This is the data being sent to Ollama.

### `model`

```python
"model": self.model
```

Uses the model from the class.

Default:

```text
llama3.2:3b
```

### `prompt`

```python
"prompt": full_prompt
```

This sends the full conversation to the model.

This is what creates memory.

### `stream`

```python
"stream": False
```

This means Ollama returns the complete response all at once.

If this were `True`, the response would stream token-by-token.

### `temperature`

```python
"temperature": 0.7
```

Temperature controls creativity.

* Lower values like `0.1` or `0.2` are more predictable
* Higher values like `0.7` are more creative
* For networking and technical answers, I would usually use something lower, like `0.2` or `0.3`

### `num_predict`

```python
"num_predict": 1024
```

This limits how many tokens the model can generate.

In plain English, it controls the maximum response length.

---

## Step 4: Send the Request

```python
response = requests.post(url, json=payload, timeout=60)
response.raise_for_status()
data = response.json()
assistant_message = data.get("response", "")
```

This sends the prompt to Ollama and gets the response back.

### This line sends the API call:

```python
response = requests.post(url, json=payload, timeout=60)
```

### This line checks for HTTP errors:

```python
response.raise_for_status()
```

If Ollama returns a bad response, Python raises an error.

### This line parses the JSON:

```python
data = response.json()
```

Ollama returns JSON data.

### This line extracts the model response:

```python
assistant_message = data.get("response", "")
```

The actual answer from Ollama is inside the `response` field.

---

## Step 5: Add Assistant Response to History

```python
self.conversation_history.append({
    "role": "assistant",
    "content": assistant_message
})
```

This stores the bot’s answer.

Now the conversation history contains both sides:

```python
[
    {
        "role": "user",
        "content": "What is OSPF?"
    },
    {
        "role": "assistant",
        "content": "OSPF is a link-state routing protocol..."
    }
]
```

That way, the next time the user asks something, the bot has the earlier context.

---

## Step 6: Return the Response

```python
return assistant_message
```

This sends the assistant’s answer back to the main program so it can be printed.

---

# Error Handling

```python
except requests.exceptions.ConnectionError:
    return "Error: Cannot connect to Ollama. Is it running? Try: ollama serve"
except Exception as e:
    return f"Error: {e}"
```

This handles problems gracefully.

If Ollama is not running, the user gets:

```text
Error: Cannot connect to Ollama. Is it running? Try: ollama serve
```

That is much better than a scary Python traceback.

---

# The `_build_prompt()` Method

```python
def _build_prompt(self) -> str:
    """Build prompt with system message and conversation history."""
    prompt_parts = [self.system_prompt, "\n\n"]
    
    for msg in self.conversation_history:
        if msg["role"] == "user":
            prompt_parts.append(f"User: {msg['content']}\n")
        elif msg["role"] == "assistant":
            prompt_parts.append(f"Assistant: {msg['content']}\n")
    
    prompt_parts.append("Assistant: ")
    return "".join(prompt_parts)
```

This method builds the full prompt that gets sent to Ollama.

This is the heart of the stateful chatbot.

---

## What It Does

It starts with the system prompt:

```python
prompt_parts = [self.system_prompt, "\n\n"]
```

Then it loops through the conversation history:

```python
for msg in self.conversation_history:
```

If the message came from the user, it adds:

```python
User: message text
```

If the message came from the assistant, it adds:

```python
Assistant: message text
```

Then it ends with:

```python
Assistant:
```

That tells the model:

> Now it is your turn to respond.

---

## Example Prompt

After one exchange, the prompt may look like this:

```text
You are a network engineer assistant.

Available devices:
- spine1, spine2 (core switches)
- leaf1, leaf2 (access switches)

Provide accurate, concise answers about networking.

User: What is OSPF?
Assistant: OSPF is a link-state routing protocol used for dynamic routing...
User: What did I just ask you?
Assistant:
```

That is why the bot can answer:

```text
You just asked me what OSPF is.
```

---

# The `reset()` Method

```python
def reset(self):
    """Clear conversation history."""
    self.conversation_history = []
```

This clears the bot’s memory.

After calling:

```python
bot.reset()
```

The history goes back to:

```python
[]
```

The bot forgets the conversation.

This is useful in interactive mode when you want to start fresh.

---

# The `get_history_length()` Method

```python
def get_history_length(self) -> int:
    """Get number of messages in history."""
    return len(self.conversation_history)
```

This returns how many messages are stored in memory.

Important detail:

Each user message counts as one message.

Each assistant response also counts as one message.

So after this exchange:

```text
User: What is OSPF?
Assistant: OSPF is...
```

The history length is:

```text
2 messages
```

After a second user question and assistant answer, it becomes:

```text
4 messages
```

---

# The Main Program

```python
if __name__ == "__main__":
```

This means:

> Only run this section when the file is executed directly.

For example:

```bash
python3 stateful_chatbot.py
```

---

## Demo Mode

```python
print("🤖 Stateful Chatbot Demo (Ollama)")
print("="*70)

bot = NetworkChatbot()
```

This prints a title and creates a new chatbot.

---

## First Question

```python
print("\n👤 User: What is OSPF?")
response1 = bot.chat("What is OSPF?")
print(f"🤖 Bot: {response1}\n")
```

The script asks the bot:

```text
What is OSPF?
```

The bot answers and stores both the question and answer in history.

---

## Second Question

```python
print("👤 User: What did I just ask you?")
response2 = bot.chat("What did I just ask you?")
print(f"🤖 Bot: {response2}\n")
```

Now the script asks:

```text
What did I just ask you?
```

Because the bot has memory, it should know the previous question was about OSPF.

---

## Success Message

```python
print("✅ SUCCESS: The bot remembers!")
print(f"   Conversation length: {bot.get_history_length()} messages")
```

This confirms that memory is working.

At this point, the conversation length should usually be:

```text
4 messages
```

Because the history contains:

1. User asked about OSPF
2. Assistant answered
3. User asked what they just asked
4. Assistant answered

---

# Interactive Mode

```python
print("\n" + "="*70)
print("💬 Interactive Mode - Type 'quit' to exit, 'reset' to clear history")
print("="*70)
```

After the demo, the script enters an interactive chatbot mode.

You can keep typing questions, and the bot keeps remembering.

---

## The Loop

```python
while True:
```

This starts an infinite loop.

The chatbot keeps running until the user types `quit`, `exit`, `q`, or presses `Ctrl+C`.

---

## Read User Input

```python
user_input = input("\n👤 You: ").strip()
```

This asks the user to type something.

The `.strip()` removes extra spaces before and after the input.

---

## Quit Commands

```python
if user_input.lower() in ['quit', 'exit', 'q']:
    print("👋 Goodbye!")
    break
```

If the user types:

```text
quit
```

or:

```text
exit
```

or:

```text
q
```

The program exits.

---

## Reset Command

```python
if user_input.lower() == 'reset':
    bot.reset()
    print("🔄 Conversation history cleared!")
    continue
```

If the user types:

```text
reset
```

The chatbot clears its memory.

This is useful when you want to start a brand-new conversation.

---

## Ignore Empty Input

```python
if not user_input:
    continue
```

If the user just presses Enter without typing anything, the script skips that turn.

---

## Chat With Memory

```python
response = bot.chat(user_input)
print(f"\n🤖 Bot: {response}")
print(f"   [{bot.get_history_length()} messages in history]")
```

This sends the user’s input to the chatbot.

Then it prints the bot response and shows how many messages are currently stored in memory.

Example:

```text
[6 messages in history]
```

---

## Handle Ctrl+C

```python
except KeyboardInterrupt:
    print("\n👋 Goodbye!")
    break
```

If the user presses:

```text
Ctrl+C
```

The program exits cleanly instead of showing a Python error.

---

# Why This Is Stateful

The chatbot is stateful because it saves previous messages here:

```python
self.conversation_history
```

And then it sends those messages back to the model every time here:

```python
full_prompt = self._build_prompt()
```

The model itself is not permanently remembering anything.

The script is doing the memory management.

That is a key concept.

---

# Stateless vs Stateful

## Stateless Chatbot

The stateless version sends only the current message:

```text
User: What did I just ask you?
```

The model has no idea what came before.

So it may say:

```text
I don't know what you asked me before.
```

## Stateful Chatbot

The stateful version sends the full conversation:

```text
User: What is OSPF?
Assistant: OSPF is a link-state routing protocol...
User: What did I just ask you?
Assistant:
```

Now the model has context.

So it can say:

```text
You asked me what OSPF is.
```

---

# Important Teaching Point

This script shows that “memory” is usually not magic.

In many chatbot systems, memory is created by:

1. Saving previous messages
2. Rebuilding the prompt
3. Sending the conversation history with each new request

That is exactly what this code does.

---

# One Thing to Watch Out For

The history keeps growing forever:

```python
self.conversation_history.append(...)
```

That is okay for a lab, but in real applications, this can become a problem.

Eventually, the prompt can get too large for the model.

In production, you would usually add:

* message limits
* summarization
* token counting
* short-term memory
* long-term memory
* vector search/RAG
* conversation trimming

For example, you might only keep the last 10 messages:

```python
self.conversation_history = self.conversation_history[-10:]
```

That keeps the chatbot from sending too much context.

---

# Cleaned-Up Summary

This script builds a chatbot that remembers the conversation.

It does this by storing every user message and assistant response in a list called:

```python
conversation_history
```

Each time the user sends a new message, the script rebuilds the full prompt using:

* the system prompt
* all previous user messages
* all previous assistant responses
* the latest user message

Then it sends that full prompt to Ollama.

That is why the chatbot can answer follow-up questions and remember what was previously discussed.

---

# Suggested README Description

````markdown
# Lab 3 Part B: Stateful Chatbot with Memory

This lab demonstrates how to build a simple stateful chatbot using Ollama.

Unlike a stateless chatbot, this version keeps track of the conversation history. Every user message and assistant response is stored in memory and included in the next prompt sent to the model.

This allows the chatbot to answer follow-up questions such as:

> What did I just ask you?

The goal of this lab is to show that chatbot memory is usually created by the application, not the model itself. The script stores previous turns in a conversation history list, rebuilds the prompt on every request, and sends the full conversation context to Ollama.

## Key Concepts

- Stateful chatbot design
- Conversation history
- System prompts
- Multi-turn conversations
- Local LLM calls with Ollama
- Basic memory management

## How It Works

1. The chatbot starts with a system prompt that defines its role as a network engineering assistant.
2. When the user sends a message, the message is added to conversation history.
3. The script builds a full prompt using the system prompt and all previous messages.
4. The full prompt is sent to Ollama.
5. The assistant response is stored in conversation history.
6. The chatbot can now use previous context in future responses.

## Commands

Start Ollama:

```bash
ollama serve
````

Pull the model:

```bash
ollama pull llama3.2:3b
```

Run the script:

```bash
python3 stateful_chatbot.py
```

## Interactive Commands

Type `quit`, `exit`, or `q` to leave the chatbot.

Type `reset` to clear the chatbot memory.

```
```
