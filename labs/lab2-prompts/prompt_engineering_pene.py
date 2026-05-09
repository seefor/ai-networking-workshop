#!/usr/bin/env python3
"""
Lab 2: Prompt Engineering with P.E.N.E. Framework
AI Networking Workshop

This lab demonstrates how better prompts produce more consistent,
accurate, and automation-ready JSON output.

P.E.N.E. Framework:
- Persona & Purpose
- Examples
- kNowledge & coNstraints
- Evaluation
"""

import json
import re
import requests
from typing import Any, Dict, Optional


# ============================================================================
# Ollama Helper
# ============================================================================

def call_llm(
    prompt: str,
    model: str = "llama3.2:3b",
    temperature: float = 0.3,
    timeout: int = 60
) -> str:
    """
    Call the local Ollama API with a prompt.
    """

    url = "http://localhost:11434/api/generate"

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": temperature
        }
    }

    try:
        response = requests.post(url, json=payload, timeout=timeout)
        response.raise_for_status()
        return response.json().get("response", "").strip()

    except requests.exceptions.ConnectionError:
        return (
            "Error: Could not connect to Ollama. "
            "Make sure Ollama is running with: ollama serve"
        )

    except requests.exceptions.Timeout:
        return "Error: Ollama request timed out."

    except Exception as e:
        return f"Error: {e}"


# ============================================================================
# JSON Helpers
# ============================================================================

def extract_json(text: str) -> Optional[Dict[str, Any]]:
    """
    Extract and parse JSON from an LLM response.

    Handles:
    - Raw JSON
    - JSON wrapped in markdown fences
    - Extra text before or after JSON
    """

    if not text:
        return None

    cleaned = text.strip()

    # Remove markdown code fences if present
    cleaned = re.sub(r"^```json\s*", "", cleaned)
    cleaned = re.sub(r"^```\s*", "", cleaned)
    cleaned = re.sub(r"\s*```$", "", cleaned)

    # Try direct JSON parsing first
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass

    # Try to extract the first JSON object from the response
    match = re.search(r"\{.*\}", cleaned, re.DOTALL)

    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            return None

    return None


def validate_interface_json(data: Dict[str, Any]) -> list[str]:
    """
    Validate that the parsed JSON contains the expected structure.
    """

    errors = []

    required_fields = {
        "interface": str,
        "admin_status": str,
        "oper_status": str,
        "ip_address": (str, type(None)),
        "prefix_length": (int, type(None)),
        "mac_address": (str, type(None)),
        "mtu": (int, type(None)),
    }

    for field, expected_type in required_fields.items():
        if field not in data:
            errors.append(f"Missing field: {field}")
            continue

        if not isinstance(data[field], expected_type):
            errors.append(
                f"Field '{field}' has wrong type. "
                f"Expected {expected_type}, got {type(data[field]).__name__}"
            )

    if data.get("admin_status") not in ["up", "down"]:
        errors.append("admin_status must be 'up' or 'down'")

    if data.get("oper_status") not in ["up", "down"]:
        errors.append("oper_status must be 'up' or 'down'")

    return errors


# ============================================================================
# CHALLENGE 1: Config Parser
# ============================================================================

def bad_config_parser_prompt() -> str:
    """
    BAD EXAMPLE:
    Vague prompt. No role. No structure. No examples. No constraints.
    """

    return "Parse this config"


def good_config_parser_prompt(config_text: str) -> str:
    """
    GOOD EXAMPLE:
    Uses the P.E.N.E. framework to create a structured prompt.
    """

    return f"""
You are a network automation engineer building a device inventory system.

TASK:
Parse network interface output and extract key fields as structured JSON.

OUTPUT FORMAT:
Return ONLY valid JSON using this schema:

{{
  "interface": "string",
  "admin_status": "up|down",
  "oper_status": "up|down",
  "ip_address": "string|null",
  "prefix_length": "integer|null",
  "mac_address": "string|null",
  "mtu": "integer|null"
}}

EXAMPLE INPUT:
GigabitEthernet0/1 is up, line protocol is up
  Hardware is iGbE, address is 0000.0c07.ac01
  Internet address is 10.0.0.1/24
  MTU 1500 bytes

EXAMPLE OUTPUT:
{{
  "interface": "GigabitEthernet0/1",
  "admin_status": "up",
  "oper_status": "up",
  "ip_address": "10.0.0.1",
  "prefix_length": 24,
  "mac_address": "0000.0c07.ac01",
  "mtu": 1500
}}

CONSTRAINTS:
- Return ONLY valid JSON
- Do not include markdown fences
- Do not include explanations
- If a field is missing, use null
- admin_status must be either "up" or "down"
- oper_status must be either "up" or "down"
- Do not invent values that are not present in the input
- If an IP address includes CIDR notation, split it into ip_address and prefix_length

NOW PARSE THIS CONFIG:

{config_text}

JSON OUTPUT:
""".strip()


def test_config_parser() -> None:
    """
    Test the config parser with both bad and good prompts.
    """

    test_config = """
GigabitEthernet0/2 is down, line protocol is down
  Hardware is iGbE, address is 0000.0c07.ac02
  MTU 1500 bytes, BW 1000000 Kbit/sec
""".strip()

    print("\n🧪 Config Parser Test")
    print("=" * 70)

    # ------------------------------------------------------------------------
    # Bad prompt test
    # ------------------------------------------------------------------------

    print("\n❌ BAD PROMPT")
    print("-" * 70)

    bad_prompt = bad_config_parser_prompt()
    print(f"Prompt:\n{bad_prompt}")

    bad_result = call_llm(f"{bad_prompt}\n\n{test_config}")

    print("\nLLM Result:")
    print(bad_result[:500])

    # ------------------------------------------------------------------------
    # Good prompt test
    # ------------------------------------------------------------------------

    print("\n✅ GOOD PROMPT USING P.E.N.E.")
    print("-" * 70)

    good_prompt = good_config_parser_prompt(test_config)
    print(f"Prompt length: {len(good_prompt)} characters")

    good_result = call_llm(good_prompt)

    print("\nLLM Result:")
    print(good_result)

    # ------------------------------------------------------------------------
    # Evaluation
    # ------------------------------------------------------------------------

    print("\n🔎 Evaluation")
    print("-" * 70)

    parsed = extract_json(good_result)

    if parsed is None:
        print("❌ Could not parse the LLM response as JSON.")
        print("This prompt may need more refinement.")
        return

    print("✅ Valid JSON detected.")

    errors = validate_interface_json(parsed)

    if errors:
        print("\n⚠️ JSON parsed, but validation found issues:")

        for error in errors:
            print(f"  - {error}")

    else:
        print("✅ JSON passed schema validation.")

    print("\nParsed Structure:")
    print(json.dumps(parsed, indent=2))


# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    print("🎯 P.E.N.E. Prompt Engineering Workshop")
    print("=" * 70)

    print("\nFramework:")
    print("  P - Persona & Purpose")
    print("  E - Examples")
    print("  N - kNowledge & coNstraints")
    print("  E - Evaluation")

    print("\nGoal:")
    print("  Show why vague prompts fail and structured prompts work better")
    print("  for network automation use cases.")
    print("=" * 70)

    test_config_parser()

    print("\n\n💡 Key Takeaways")
    print("=" * 70)
    print("1. BAD: 'Parse this config' creates inconsistent results.")
    print("2. GOOD: P.E.N.E. prompts give the model role, task, examples, and constraints.")
    print("3. Examples are often more powerful than instructions alone.")
    print("4. Automation needs structured output, not pretty paragraphs.")
    print("5. Always validate LLM output before using it in a workflow.")
    print("6. Lower temperature helps with predictable structured output.")
    print("=" * 70)