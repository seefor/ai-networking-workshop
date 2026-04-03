#!/usr/bin/env python3
"""
Lab 2: Prompt Engineering with P.E.N.E. Framework
AI Networking Workshop

Learn to write production-quality prompts that produce
consistent, accurate, parseable results.

P.E.N.E. Framework:
- Persona & Purpose
- Examples
- kNowledge & coNstraints
- Evaluation
"""

import requests
import json
from typing import Optional


def call_llm(prompt: str, model: str = "llama3.2:3b", temperature: float = 0.3) -> str:
    """Call Ollama API with a prompt."""
    url = "http://localhost:11434/api/generate"
    
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": temperature}
    }
    
    try:
        response = requests.post(url, json=payload, timeout=60)
        response.raise_for_status()
        return response.json().get("response", "")
    except Exception as e:
        return f"Error: {e}"


# ============================================================================
# CHALLENGE 1: Config Parser
# ============================================================================

def bad_config_parser_prompt():
    """
    BAD EXAMPLE: Vague, no structure, no examples.
    """
    return "Parse this config"


def good_config_parser_prompt(config_text: str) -> str:
    """
    GOOD EXAMPLE: Uses full P.E.N.E. framework.
    """
    prompt = f"""You are a network automation engineer building a device inventory system.

**TASK:** Parse interface configuration output and extract key fields as structured JSON.

**OUTPUT FORMAT:**
{{
  "interface": "string",
  "admin_status": "up|down",
  "oper_status": "up|down",
  "ip_address": "string|null",
  "subnet_mask": "string|null",
  "mac_address": "string|null",
  "mtu": "integer|null"
}}

**EXAMPLE INPUT:**
GigabitEthernet0/1 is up, line protocol is up
  Hardware is iGbE, address is 0000.0c07.ac01
  Internet address is 10.0.0.1/24
  MTU 1500 bytes

**EXAMPLE OUTPUT:**
{{
  "interface": "GigabitEthernet0/1",
  "admin_status": "up",
  "oper_status": "up",
  "ip_address": "10.0.0.1",
  "subnet_mask": "255.255.255.0",
  "mac_address": "0000.0c07.ac01",
  "mtu": 1500
}}

**CONSTRAINTS:**
- Output ONLY valid JSON, no markdown fences
- If a field is missing, use null
- admin_status must be "up" or "down"
- oper_status must be "up" or "down"

**NOW PARSE THIS:**
{config_text}

Output JSON:"""
    
    return prompt


def test_config_parser():
    """
    Test config parser with good and bad prompts.
    """
    test_config = """
GigabitEthernet0/2 is down, line protocol is down
  Hardware is iGbE, address is 0000.0c07.ac02
  MTU 1500 bytes, BW 1000000 Kbit/sec
"""
    
    print("\n🧪 Config Parser Test")
    print("="*70)
    
    # Test bad prompt
    print("\n❌ BAD PROMPT (vague):")
    print("-"*70)
    bad_prompt = bad_config_parser_prompt()
    print(f"Prompt: {bad_prompt}")
    bad_result = call_llm(bad_prompt + "\n\n" + test_config)
    print(f"\nResult: {bad_result[:200]}...")
    
    # Test good prompt
    print("\n✅ GOOD PROMPT (P.E.N.E.):")
    print("-"*70)
    good_prompt = good_config_parser_prompt(test_config)
    print(f"Prompt length: {len(good_prompt)} chars")
    good_result = call_llm(good_prompt)
    print(f"\nResult:\n{good_result}")
    
    # Try to parse as JSON
    try:
        clean_result = good_result.strip()
        if clean_result.startswith("```"):
            clean_result = clean_result.split("```")[1]
            if clean_result.startswith("json"):
                clean_result = clean_result[4:]
        
        parsed = json.loads(clean_result.strip())
        print("\n✅ Valid JSON! Parsed structure:")
        print(json.dumps(parsed, indent=2))
    except json.JSONDecodeError:
        print("\n⚠️  Could not parse as JSON (might need more prompt refinement)")


if __name__ == "__main__":
    print("🎯 P.E.N.E. Prompt Engineering Workshop")
    print("="*70)
    print("\nFramework:")
    print("  P - Persona & Purpose (Who is the AI? What's the goal?)")
    print("  E - Examples (Show the pattern with input/output pairs)")
    print("  N - kNowledge & coNstraints (Context and limitations)")
    print("  E - Evaluation (Test and iterate)")
    print("="*70)
    
    # Run test
    test_config_parser()
    
    print("\n\n💡 Key Takeaways:")
    print("="*70)
    print("1. BAD: 'Parse this config' → vague, no structure, inconsistent results")
    print("2. GOOD: P.E.N.E. prompts → specific role, clear format, concrete examples")
    print("3. Examples are more powerful than instructions")
    print("4. Always define your output format explicitly")
    print("5. Add constraints to prevent unwanted behavior")
    print("6. Lower temperature (0.1-0.3) for structured output")
    print("="*70)
