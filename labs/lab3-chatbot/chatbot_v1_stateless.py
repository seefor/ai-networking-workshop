#!/usr/bin/env python3
"""
Lab 3 Part A: Stateless Chatbot
Shows the problem - no memory between calls
"""

import requests
import json


def simple_chat(user_message: str, model: str = "llama3.2:3b") -> str:
    """Send single message with NO conversation history."""
    url = "http://localhost:11434/api/generate"
    
    payload = {
        "model": model,
        "prompt": user_message,
        "stream": False,
        "options": {
            "temperature": 0.7
        }
    }
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data.get("response", "")
    except requests.exceptions.ConnectionError:
        return "Error: Cannot connect to Ollama. Is it running? Try: ollama serve"
    except Exception as e:
        return f"Error: {e}"


if __name__ == "__main__":
    print("🤖 Stateless Chatbot Demo (Ollama)")
    print("="*70)
    
    # First question
    print("\n👤 User: What is OSPF?")
    response1 = simple_chat("What is OSPF?")
    print(f"🤖 Bot: {response1}\n")
    
    # Second question (references first)
    print("👤 User: What did I just ask you?")
    response2 = simple_chat("What did I just ask you?")
    print(f"🤖 Bot: {response2}\n")
    
    print("❌ FAILURE: The bot doesn't remember!")
    print("   Each API call is independent.")
    print("\n💡 Next: See chatbot_v2_with_memory.py for the solution!")
