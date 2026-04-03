#!/usr/bin/env python3
"""
Lab 3 Part A: Stateless Chatbot
Shows the problem - no memory between calls
"""

import anthropic
import os


def simple_chat(user_message: str) -> str:
    """Send single message with NO conversation history."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return "Error: Set ANTHROPIC_API_KEY environment variable"
    
    client = anthropic.Anthropic(api_key=api_key)
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[{"role": "user", "content": user_message}]
    )
    return response.content[0].text


if __name__ == "__main__":
    print("🤖 Stateless Chatbot Demo")
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
