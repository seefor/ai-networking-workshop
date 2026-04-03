#!/usr/bin/env python3
"""
Lab 3 Part B: Stateful Chatbot with Memory
Maintains conversation history for multi-turn conversations
"""

import anthropic
import os
import json
from datetime import datetime


class NetworkChatbot:
    """Chatbot with conversation memory for network engineering."""
    
    def __init__(self, api_key: str = None):
        if api_key is None:
            api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("Set ANTHROPIC_API_KEY environment variable")
        
        self.client = anthropic.Anthropic(api_key=api_key)
        self.conversation_history = []
        self.system_prompt = """You are a network engineer assistant.

Available devices:
- spine1, spine2 (core switches)
- leaf1, leaf2 (access switches)

Provide accurate, concise answers about networking."""
    
    def chat(self, user_message: str) -> str:
        """Send message with full conversation history."""
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2048,
            system=self.system_prompt,
            messages=self.conversation_history
        )
        
        assistant_message = response.content[0].text
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })
        
        return assistant_message
    
    def reset(self):
        """Clear conversation history."""
        self.conversation_history = []


if __name__ == "__main__":
    print("🤖 Stateful Chatbot Demo")
    print("="*70)
    
    bot = NetworkChatbot()
    
    print("\n👤 User: What is OSPF?")
    response1 = bot.chat("What is OSPF?")
    print(f"🤖 Bot: {response1}\n")
    
    print("👤 User: What did I just ask you?")
    response2 = bot.chat("What did I just ask you?")
    print(f"🤖 Bot: {response2}\n")
    
    print("✅ SUCCESS: The bot remembers!")
    print(f"   Conversation length: {len(bot.conversation_history)} messages")
