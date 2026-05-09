---
theme: default
background: https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=1920
class: text-center
highlighter: shiki
lineNumbers: true
info: |
  ## AI Networking Workshop
  From LLMs to Production Agents
  
  Building AI-powered network automation with MCP
drawings:
  persist: false
transition: slide-left
title: AI Networking Workshop
mdc: true
---

# AI Networking Workshop

From LLMs to Production Agents

<div class="pt-12">
  <span @click="$slidev.nav.next" class="px-2 py-1 rounded cursor-pointer" hover="bg-white bg-opacity-10">
    Building AI-powered network automation with MCP <carbon:arrow-right class="inline"/>
  </span>
</div>

<div class="abs-br m-6 flex gap-2">
  <a href="https://github.com/seefor" target="_blank" alt="GitHub" title="GitHub"
    class="text-xl slidev-icon-btn opacity-50 !border-none !hover:text-white">
    <carbon-logo-github />
  </a>
</div>

---
layout: intro
---

# Workshop Overview

<v-clicks>

- **Duration:** 3.25 hours
- **Format:** Theory + hands-on labs
- **Goal:** Build production-ready AI agents for network automation
- **Stack:** Python, Anthropic Claude, Ollama, MCP

</v-clicks>

<br>

<v-clicks>

### What You'll Build

1. Local LLM interactions with Ollama
2. Production-grade prompts with P.E.N.E. framework
3. Stateful chatbot with memory
4. Agentic tool-calling system
5. MCP server with reusable network tools
6. Fully integrated AI network assistant

</v-clicks>

---
layout: center
class: text-center
---

# Module 0

## Welcome & Environment Check

10 minutes

---

# Environment Checklist

Make sure you have these installed and working:

<v-clicks>

### Required Software
- ✅ **Python 3.10+** - `python --version`
- ✅ **Ollama** - `ollama --version`
- ✅ **Code editor** - VS Code recommended
- ✅ **Git** - For cloning workshop materials

### Python Packages
```bash
pip install requests openai mcp flask streamlit
```

### Optional (for demos)
- OpenAI API key
- Anthropic API key (Claude)

</v-clicks>

---

# Quick Introductions

<v-clicks>

### Share with the group:
- 👤 Your name and role
- 🏢 Your organization (if comfortable)
- 🎯 What you want to build with AI + networking
- 💡 One network automation pain point you're facing

</v-clicks>

<br>

<v-click>

### Workshop Ground Rules
- ❓ Questions anytime - no stupid questions
- 🤝 Help your neighbors
- 💻 Follow along in the labs
- 📸 Screenshots/notes are encouraged
- ⏸️ Breaks every 60-90 minutes

</v-click>

---
layout: center
class: text-center
---

# Module 1

## How LLMs Actually Work

25 minutes

---

# LLMs: The 10,000 Foot View

<v-clicks>

## What is an LLM?

A **Large Language Model** is a neural network trained to predict the next token (word/subword) in a sequence.

### Key Insight
LLMs don't "understand" - they recognize statistical patterns in text at massive scale.

```
Input:  "The BGP neighbor is in the"
Output: "Established" (87% probability)
        "Idle" (8% probability)
        "Active" (3% probability)
```

### Why This Matters for Network Automation
- They're pattern matchers, not logic engines
- Great for: parsing unstructured data, generating configs, summarizing logs
- Bad for: precise calculations, deterministic logic, security-critical decisions

</v-clicks>

---

# Tokenization: Text → Numbers

<v-clicks>

LLMs don't see words - they see **tokens** (sub-word chunks)

### Example: "strawberry"
```
"strawberry" → ["straw", "berry"] → [2 tokens]
```

### Why This Matters

1. **API Costs** = input tokens + output tokens
   ```python
   "show ip interface brief" = 6 tokens
   1M tokens = $3 (Claude) / $5 (GPT-4)
   ```

2. **Context Window Limits**
   - GPT-4: 128k tokens (~100k words)
   - Claude 3.5: 200k tokens (~150k words)
   - Your entire conversation history counts against this limit

</v-clicks>

---

# Live Demo: Tokenization

<v-clicks>

Let's tokenize some network commands:

```python
import requests

# Count tokens via Ollama's generate endpoint
text = """
router bgp 65001
 neighbor 10.0.0.1 remote-as 65002
 neighbor 10.0.0.1 description CORE-RTR-01
"""

response = requests.post("http://localhost:11434/api/generate", json={
    "model": "llama3.2:3b",
    "prompt": text,
    "stream": False
}).json()

print(f"Prompt tokens: {response['prompt_eval_count']}")
# Output: Prompt tokens: ~47
```

**Rule of thumb:** 1 token ≈ 0.75 words

</v-clicks>

---

# Generation Parameters

<v-clicks>

## Temperature (0.0 - 2.0)

Controls randomness in output selection

```python
# Temperature = 0.0 (Deterministic)
"The capital of France is Paris"
"The capital of France is Paris"  # Same every time

# Temperature = 1.0 (Balanced)
"The capital of France is Paris"
"France's capital city is Paris"  # Varied but accurate

# Temperature = 2.0 (Creative/Random)
"The capital of France is Paris"
"Lyon is a major French city"     # Can drift off-topic
```

### When to Use What
- **0.0-0.3**: Config generation, log parsing, structured output
- **0.7-1.0**: Documentation, explanations, troubleshooting
- **1.5-2.0**: Creative tasks, brainstorming (rarely for network ops)

</v-clicks>

---

# Other Important Parameters

<v-clicks>

## Top-p (Nucleus Sampling)

Alternative to temperature - samples from top X% of likely tokens

```python
top_p=0.1  # Only consider top 10% most likely tokens
top_p=0.9  # Consider top 90% of likely tokens
```

## Max Tokens

Hard limit on response length

```python
max_tokens=100   # Short response (~75 words)
max_tokens=4096  # Long response (~3000 words)
```

**Cost tip:** Only request what you need. Max tokens affects billing even if not used.

</v-clicks>

---

# Context Window & Memory

<v-clicks>

## The Stateless Reality

LLMs have **zero memory** between API calls.

```python
# Call 1
chat("What is OSPF?")  
# LLM: "OSPF is a link-state routing protocol..."

# Call 2 (separate request)
chat("What did I just ask you?")
# LLM: "I don't have access to previous messages"
```

## How "Memory" Actually Works

You (the developer) maintain conversation history and re-send it:

```python
history = [
  {"role": "user", "content": "What is OSPF?"},
  {"role": "assistant", "content": "OSPF is a link-state..."},
  {"role": "user", "content": "What did I just ask you?"}
]
# LLM now sees the full context
```

</v-clicks>

---

# Context Window Management

<v-clicks>

## The Problem

```
Context window: 128k tokens
Your conversation: 
  - 50 messages = 80k tokens
  - Next message won't fit!
```

## Solutions

1. **Truncate old messages**
   ```python
   history = history[-20:]  # Keep last 20 messages
   ```

2. **Summarize periodically**
   ```python
   summary = summarize(history[:-5])
   history = [summary] + history[-5:]
   ```
3. **Use RAG (Retrieval Augmented Generation)**
   - Store full history in vector DB
   - Retrieve only relevant context for each message

</v-clicks>

---

# Live Demo: Temperature Effects

Let's see temperature in action:

<v-clicks>

```python
import requests

prompt = "Generate a BGP configuration for AS 65001 with neighbor 10.0.0.1"

# Temperature 0.0
response = requests.post("http://localhost:11434/api/generate", json={
    "model": "llama3.2:3b",
    "prompt": prompt,
    "stream": False,
    "options": {"temperature": 0.0, "num_predict": 200}
}).json()
print(response["response"])
```

Run this 3 times - output should be **identical**

Now try `temperature=1.5` - see the variation

</v-clicks>

---
layout: two-cols
---

# Key Takeaways

<v-clicks>

### LLMs Are...
- ✅ Stateless prediction machines
- ✅ Token-based (not word-based)
- ✅ Expensive at scale
- ✅ Controlled by parameters

### For Network Automation
- Use low temperature for configs
- Use high max_tokens sparingly
- Manage context windows carefully
- Always validate LLM outputs

</v-clicks>

::right::

<v-clicks>

### Common Misconceptions

❌ "LLMs remember our conversation"
✅ Your app stores and re-sends history

❌ "LLMs understand networking"
✅ They pattern-match training data

❌ "Higher temperature = smarter"
✅ Higher temp = more random

❌ "Context window is free"
✅ Every token costs money

</v-clicks>

---
layout: center
class: text-center
---

# Module 2

## Lab 1: Hands-On with Ollama

20 minutes

---

# What is Ollama?

<v-clicks>

## Run LLMs Locally

**Ollama** = Docker for LLMs

- Download and run models on your laptop
- No API keys, no internet required
- Free and open-source
- Support for Llama, Mistral, Phi, and more

### Why Use Ollama?

✅ **Privacy** - Your data never leaves your machine  
✅ **Cost** - No per-token charges  
✅ **Speed** - No network latency  
✅ **Development** - Iterate without API limits  
✅ **Production** - On-prem deployments  

❌ **Tradeoffs** - Smaller models, slower inference, requires GPU for best performance

</v-clicks>

---

# Lab 1 - Part A: Install Models

<v-clicks>

Open your terminal and run:

```bash
# Pull a small, fast model (3B parameters, ~2GB)
ollama pull llama3.2:3b

# Pull a larger, smarter model (8B parameters, ~4.7GB)
ollama pull llama3.1:8b

# Verify installation
ollama list

# Output:
# NAME              ID         SIZE    MODIFIED
# llama3.2:3b       abc123     1.9GB   2 minutes ago
# llama3.1:8b       def456     4.7GB   1 minute ago
```

**Tips:**
- First pull takes time (downloading GBs)
- Models stored in `~/.ollama/models/`
- Use `ollama rm <model>` to delete

</v-clicks>

---

# Lab 1 - Part B: CLI Interaction

<v-clicks>

Let's chat with the model:

```bash
ollama run llama3.2:3b
```

Try these networking prompts:

```
>>> Explain BGP route selection in 3 bullet points

>>> Write a Python script to parse 'show ip interface brief'

>>> What are the OSPF neighbor states?

>>> Generate a sample Cisco router config
```

**Exercise:** Compare the same prompt on both models:
```bash
ollama run llama3.1:8b  # Smarter but slower
```

Exit with `/bye`

</v-clicks>

---

# Lab 1 - Part C: API Interaction

<v-clicks>

Create `simple_ollama_test.py`:

```python
import requests
import json

def chat_with_ollama(prompt, model="llama3.2:3b"):
    url = "http://localhost:11434/api/generate"
    
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False  # Get complete response
    }
    
    response = requests.post(url, json=payload)
    return response.json()['response']

# Test it
result = chat_with_ollama(
    "Explain OSPF DR/BDR election in 2 sentences"
)
print(result)
```

Run it: `python simple_ollama_test.py`

</v-clicks>

---

# Challenge: JSON Output

<v-clicks>

Modify the script to get structured JSON:

```python
prompt = """
Parse this interface output and return JSON:

GigabitEthernet0/1 is up, line protocol is up
  Hardware is iGbE, address is 0000.0c07.ac01
  Internet address is 10.0.0.1/24

Return format:
{
  "interface": "...",
  "status": "...",
  "ip": "...",
  "mac": "..."
}
"""

result = chat_with_ollama(prompt)
print(result)

# Try to parse it
data = json.loads(result)
print(f"Interface {data['interface']} is {data['status']}")
```

**Challenge:** Make it robust (handle parsing errors, validate output)

</v-clicks>

---

# Lab 1 - Comparison Challenge

<v-clicks>

Compare models on the same task:

```python
import time

models = ["llama3.2:3b", "llama3.1:8b"]
prompt = "Generate a secure Cisco ASA firewall configuration with DMZ"

for model in models:
    start = time.time()
    result = chat_with_ollama(prompt, model=model)
    elapsed = time.time() - start
    
    print(f"\n{'='*60}")
    print(f"Model: {model}")
    print(f"Time: {elapsed:.2f}s")
    print(f"Response length: {len(result)} chars")
    print(f"{'='*60}")
    print(result[:500])  # First 500 chars
```

**What to notice:**
- Speed vs. quality tradeoff
- Smaller model = faster but less detailed
- Larger model = slower but more accurate

</v-clicks>

---

# Lab 1 Takeaways

<v-clicks>

### You Learned
✅ How to run local LLMs with Ollama  
✅ CLI and API interaction  
✅ Model size/quality tradeoffs  
✅ Structured output generation  

### When to Use Ollama
- **Development/testing** - No API costs
- **Privacy-sensitive** - Healthcare, finance, government
- **Air-gapped networks** - No internet connectivity
- **Batch processing** - No rate limits

### When to Use Cloud APIs
- **Production** - Better models, managed infrastructure
- **Low latency** - API inference faster than local CPU
- **Multimodal** - Vision, audio (Ollama is text-only)

</v-clicks>

---
layout: center
class: text-center
---

# Module 3

## Prompt Engineering (P.E.N.E.)

20 minutes

---

# Why Prompt Engineering Matters

<v-clicks>

## The Problem

```python
# Bad prompt
"Analyze this router config"

# What the LLM thinks:
# - Analyze how? Security? Performance? Compliance?
# - What format should the output be?
# - Should I be a junior engineer or CCIE-level?
# - What vendor? Cisco? Juniper? Arista?
```

**Result:** Vague, inconsistent, unhelpful output

## The Solution

Systematic prompting framework that produces **reliable, production-quality results**

</v-clicks>

---
layout: two-cols
---

# The P.E.N.E. Framework

<v-clicks>

### P - Persona & Purpose
**Who** is the AI?  
**What** is the goal?

### E - Examples
Show, don't just tell  
Input/output pairs

### N - kNowledge & coNstraints
Context the AI needs  
What it should NOT do

### E - Evaluation & iteration
Test with edge cases  
Refine based on failures

</v-clicks>

::right::

<v-click>

## Why This Works

```
Vague prompt:
"Check this config"

P.E.N.E. prompt:
✅ Clear role (security engineer)
✅ Specific goal (find risks)
✅ Output format (JSON)
✅ Example input/output
✅ Constraints (severity levels)
```

Result: **Consistent, actionable, parseable**

</v-click>

---

# Bad vs. Good Prompts

<v-clicks>

## ❌ Bad Examples

```
"Analyze this router config"
- No persona, no purpose, no format

"Tell me about BGP"
- Too vague, infinite possible answers

"Fix this network issue"
- No context, no constraints, no examples
```

## ✅ Good Examples (P.E.N.E.)

```
You are a senior network architect reviewing a data center design.
Goal: Identify single points of failure in the attached topology diagram.
Output: JSON list with {component, risk_level, mitigation}
Example: {"component": "Core Switch", "risk_level": "high", ...}
```

</v-clicks>

---

# P.E.N.E. Template

<v-clicks>

```markdown
## Persona & Purpose
You are a [ROLE] performing [TASK].

## Examples
Input:
[example input 1]

Output:
[desired output 1]

Input:
[example input 2]

Output:
[desired output 2]

## kNowledge & coNstraints
Context you need:
- [relevant fact 1]
- [relevant fact 2]

Do NOT:
- [forbidden action 1]
- [forbidden action 2]

## Format
Return your response as:
[structured format specification]

## Now process this:
[actual input]
```

</v-clicks>

---

# Real Example: Config Security Audit

<v-clicks>

```python
prompt = """
You are a network security engineer reviewing firewall configurations.

Your task: Identify security risks and suggest fixes.

Example Input:
access-list 101 permit ip any any

Example Output:
{
  "risks": [
    {
      "severity": "critical",
      "issue": "ACL permits all traffic",
      "recommendation": "Implement least-privilege with specific sources/destinations"
    }
  ]
}

Context:
- This is a production internet-facing firewall
- Company policy requires explicit deny-all at the end
- Logging should be enabled for all permits

Do NOT:
- Suggest changes without security justification
- Recommend features not supported in Cisco ASA 9.x

Now analyze this configuration:
{config_text}
"""
```

</v-clicks>

---

# Live Demo: Prompt Iteration

<v-clicks>

Start vague, iterate to perfection:

### Version 1 (Vague)
```
"Check this BGP config"
```
Result: Generic explanation, no actionable output

### Version 2 (Add Persona)
```
"You are a network engineer. Check this BGP config for errors."
```
Result: Better, but still unstructured

### Version 3 (Add Examples)
```
"You are a network engineer. Find BGP configuration errors.

Example:
neighbor 10.0.0.1 remote-as 65001
neighbor 10.0.0.1 remote-as 65002  # ERROR: AS mismatch
```
Result: Finds similar issues, but inconsistent format

</v-clicks>

---

# Live Demo: Prompt Iteration (cont.)

<v-clicks>

### Version 4 (Add Format + Constraints)
```
You are a CCIE-certified network engineer auditing BGP configs.

Task: Find configuration errors and inconsistencies.

Output format:
{
  "errors": [{"line": X, "issue": "...", "fix": "..."}],
  "warnings": [{"line": Y, "issue": "..."}],
  "summary": "X errors, Y warnings found"
}

Example:
Input: neighbor 10.0.0.1 remote-as 65001
       neighbor 10.0.0.1 remote-as 65002

Output: {"errors": [{"line": 2, "issue": "AS mismatch", "fix": "..."}]}

Now analyze: {config}
```

Result: ✅ Structured, parseable, consistent, actionable

</v-clicks>

---

# Common Prompt Patterns

<v-clicks>

## 1. Classification

```python
"You are a NOC analyst triaging alerts.
Classify this alert as: critical/high/medium/low/false-positive
Output only the classification level."
```

## 2. Extraction

```python
"Extract all IPv4 addresses from this log file.
Return as a JSON array: ['10.0.0.1', '192.168.1.1']
Do not include RFC1918 addresses."
```

## 3. Transformation

```python
"Convert this Cisco IOS config to Arista EOS format.
Preserve all functionality.
Add comments explaining any syntax differences."
```

</v-clicks>

---

# Common Prompt Patterns (cont.)

<v-clicks>

## 4. Validation

```python
"You are a network compliance auditor.
Check if this firewall config meets PCI-DSS requirements.
Return: {compliant: true/false, violations: [...], score: X/100}"
```

## 5. Generation

```python
"Generate a VLAN configuration for a 3-tier data center.
Requirements:
- Web tier: VLAN 10
- App tier: VLAN 20
- DB tier: VLAN 30
- No inter-VLAN routing

Output in Cisco IOS format."
```

</v-clicks>

---

# Anti-Patterns to Avoid

<v-clicks>

## ❌ Don't Do These

1. **Over-complicated instructions**
   ```
   "Please kindly review this configuration and if you find anything 
   that might potentially be a security risk, could you perhaps..."
   ```
   → Be direct and concise

2. **Asking multiple questions**
   ```
   "What is OSPF? How does it work? When should I use it? What are 
   the alternatives? Which is best?"
   ```
   → One question per prompt (or clearly separate them)

3. **Assuming context**
   ```
   "Fix the problem in this config"  # What problem?
   ```
   → Explicitly state the goal

</v-clicks>

---

# Module 3 Takeaways

<v-clicks>

### P.E.N.E. Framework
✅ **P**ersona & **P**urpose - Who and what  
✅ **E**xamples - Show the pattern  
✅ k**N**owledge & co**N**straints - Context and limits  
✅ **E**valuation - Test and iterate  

### Key Principles
- Specificity beats cleverness
- Examples > instructions
- Always define output format
- Iterate based on real failures

### Next Lab
We'll apply P.E.N.E. to real network automation tasks

</v-clicks>

---
layout: center
class: text-center
---

# Module 4

## Lab 2: Prompt Crafting Workshop

20 minutes

---

# Lab 2 Overview

<v-clicks>

You'll build production-ready prompts for 3 common network tasks:

1. **Config Parser** - Unstructured text → Structured JSON
2. **Alert Triage** - Security alerts → Severity + actions
3. **Documentation Generator** - Topology data → Human-readable docs

### Goals
- Practice the P.E.N.E. framework
- Build reusable prompt templates
- Learn to spot and fix hallucinations
- Create a prompt library you can use at work

### Time
- 8 min per challenge
- 4 min group share-out

</v-clicks>

---

# Challenge 1: Config Parser

**Goal:** Parse `show` command output into structured JSON

<v-clicks>

### Test Cases

```python
# Cisco IOS
"""
GigabitEthernet0/1 is up, line protocol is up
  Hardware is iGbE, address is 0000.0c07.ac01
  Internet address is 10.0.0.1/24
  MTU 1500 bytes, BW 1000000 Kbit/sec
"""

# Arista EOS
"""
Ethernet1 is up, line protocol is up (connected)
  Hardware is Ethernet, address is 001c.73a0.fc28
  Internet address is 192.168.1.1/24
"""

# Juniper JunOS
"""
ge-0/0/1.0 up up inet 172.16.0.1/30
"""
```

</v-clicks>

---

# Challenge 1: Starter Template

<v-clicks>

```python
prompt = """
You are a network automation engineer building a device inventory system.

Task: Parse interface status output and extract key fields as JSON.

Output format:
{
  "interface": "string",
  "admin_status": "up|down",
  "oper_status": "up|down",
  "ip_address": "string|null",
  "subnet_mask": "string|null",
  "mac_address": "string|null"
}

Example Input:
GigabitEthernet0/1 is up, line protocol is up
  Internet address is 10.0.0.1/24

Example Output:
{
  "interface": "GigabitEthernet0/1",
  "admin_status": "up",
  "oper_status": "up",
  "ip_address": "10.0.0.1",
  "subnet_mask": "255.255.255.0"
}

Now parse this:
{input_text}
"""
```

</v-clicks>

---

# Challenge 1: Your Task

<v-clicks>

### Build Your Prompt

1. Test it on all 3 vendor formats (Cisco, Arista, Juniper)
2. Handle edge cases:
   - Interface down
   - No IP address configured
   - IPv6 addresses
3. Make it robust - validate JSON output
4. Add error handling

### Bonus Points
- Support multiple interfaces in one output
- Return array of interface objects
- Detect vendor from output format

**Time: 8 minutes**

</v-clicks>

---

# Challenge 2: Alert Triage

**Goal:** Classify security alerts and suggest actions

<v-clicks>

### Test Alerts

```python
# Alert 1: DDoS
"""
2024-01-15 14:32:11 CRITICAL: High packet rate detected
Source: 203.0.113.42
Destination: 10.0.1.100:80
Rate: 50,000 pps (baseline: 1,000 pps)
"""

# Alert 2: Failed login
"""
2024-01-15 14:35:22 WARNING: SSH authentication failure
User: admin
Source IP: 192.168.1.105 (internal)
Attempts: 1
"""

# Alert 3: Config change
"""
2024-01-15 14:40:01 INFO: Configuration modified
User: jdoe
Device: FW-01
Change: ACL 101 modified
"""
```

</v-clicks>

---

# Challenge 2: Starter Template

<v-clicks>

```python
prompt = """
You are a SOC analyst performing initial alert triage.

Task: Classify alert severity and suggest next actions.

Severity levels:
- critical: Immediate response required, active threat
- high: Potential threat, investigate within 1 hour
- medium: Suspicious activity, investigate within 24 hours
- low: Informational, no immediate action
- false_positive: Benign event, can ignore

Output format:
{
  "severity": "critical|high|medium|low|false_positive",
  "reason": "Brief explanation",
  "next_actions": ["action 1", "action 2"],
  "escalate": true|false
}

Example Input:
HIGH packet rate from external IP: 50,000 pps

Example Output:
{
  "severity": "critical",
  "reason": "Potential DDoS attack from external source",
  "next_actions": ["Block source IP", "Enable rate limiting", "Notify NOC"],
  "escalate": true
}

Now triage this alert:
{alert_text}
"""
```

</v-clicks>

---

# Challenge 2: Your Task

<v-clicks>

### Build Your Prompt

1. Test on all 3 alert types
2. Handle context:
   - Internal vs. external IPs
   - Business hours vs. off-hours
   - Repeated vs. one-off events
3. Avoid false positives (don't over-alert)
4. Generate specific, actionable next steps

### Bonus Points
- Factor in alert history (repeat offenders)
- Consider compliance requirements (PCI-DSS, HIPAA)
- Suggest automation opportunities

**Time: 8 minutes**

</v-clicks>

---

# Challenge 3: Documentation Generator

**Goal:** Turn topology data into human-readable docs

<v-clicks>

### Input Data

```python
topology = {
    "devices": [
        {"name": "RTR-CORE-01", "type": "router", "role": "core"},
        {"name": "RTR-CORE-02", "type": "router", "role": "core"},
        {"name": "SW-ACCESS-01", "type": "switch", "role": "access"}
    ],
    "links": [
        {"from": "RTR-CORE-01", "to": "RTR-CORE-02", "type": "10G fiber"},
        {"from": "RTR-CORE-01", "to": "SW-ACCESS-01", "type": "1G copper"},
        {"from": "RTR-CORE-02", "to": "SW-ACCESS-01", "type": "1G copper"}
    ],
    "subnets": [
        {"network": "10.0.0.0/30", "vlan": 100, "purpose": "core-interconnect"},
        {"network": "10.0.1.0/24", "vlan": 10, "purpose": "user-access"}
    ]
}
```

</v-clicks>

---

# Challenge 3: Starter Template

<v-clicks>

```python
prompt = """
You are a network architect writing documentation.

Task: Generate clear, concise network documentation from topology data.

Format:
# Network Topology: {name}

## Overview
[2-3 sentence summary]

## Core Devices
[List with roles]

## Network Segments
[VLANs and purposes]

## Redundancy
[High-availability design notes]

## Troubleshooting Quick Reference
[Common issues and fixes]

Example Input:
{"devices": [{"name": "RTR-01", "role": "core"}], "links": [...]}

Example Output:
# Network Topology: Data Center Core

## Overview
This is a dual-core router design with redundant links to access layer.
Primary routing protocols: OSPF (area 0), BGP (AS 65001).

[Continue with other sections...]

Now document this topology:
{topology_json}
"""
```

</v-clicks>

---

# Challenge 3: Your Task

<v-clicks>

### Build Your Prompt

1. Generate documentation with clear sections
2. Include:
   - Network diagram (ASCII art or description)
   - IP addressing scheme
   - Redundancy/failover notes
   - Troubleshooting runbook
3. Make it readable for junior engineers
4. Include configuration snippets where relevant

### Bonus Points
- Auto-detect design patterns (spine-leaf, 3-tier, etc.)
- Generate Mermaid diagram syntax
- Add security best practices section

**Time: 8 minutes**

</v-clicks>

---

# Group Share-Out

<v-clicks>

### What Worked?
- Which prompts produced the best results?
- What examples were most helpful?
- Any surprising successes?

### What Failed?
- Common hallucination patterns?
- Edge cases that broke your prompts?
- What constraints were missing?

### Lessons Learned
- Prompt patterns to steal
- Debugging techniques
- Production readiness checks

**Time: 4 minutes**

</v-clicks>

---

# Lab 2 Takeaways

<v-clicks>

### Key Insights

✅ **Prompts are code** - Version control them, test them, refine them  
✅ **Examples drive consistency** - Show the pattern you want  
✅ **Edge cases reveal weaknesses** - Test with bad data, not just happy paths  
✅ **Domain knowledge still matters** - LLMs amplify expertise, don't replace it  

### Prompt Library

Save your prompts! You just built:
- `config_parser.txt`
- `alert_triage.txt`
- `documentation_generator.txt`

These are reusable templates for production work.

</v-clicks>

---
layout: center
class: text-center
---

# Module 5

## LLM APIs & Function Calling

20 minutes

---

# LLM APIs: The Basics

<v-clicks>

## How API Calls Work

```python
import requests

def call_ollama(prompt, model="llama3.2:3b", temperature=0.7):
    response = requests.post("http://localhost:11434/api/generate", json={
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": temperature}
    })
    return response.json()["response"]

print(call_ollama("What is BGP?"))
```

### Key Components
- **No API key needed** — Ollama runs locally
- **Model selection**: Which LLM to use (llama3.2:3b, etc.)
- **Prompt**: The input text
- **Parameters**: Temperature, num_predict, etc.
- **Response**: Text + metadata (tokens used, duration)

</v-clicks>

---

# API Cost Calculation

<v-clicks>

## Pricing with Ollama

- **Cost:** $0 — runs 100% locally on your machine
- **No rate limits, no billing surprises**
- **Data stays on-prem** — nothing leaves your network

### Example

```python
import requests

response = requests.post("http://localhost:11434/api/generate", json={
    "model": "llama3.2:3b",
    "prompt": "Parse this 2000-word config file...",
    "stream": False,
    "options": {"num_predict": 500}
}).json()

# Cost breakdown:
# Input: 2500 tokens = $0.00
# Output: 300 tokens = $0.00
# Total: $0.00 per API call
```

**At scale:** 10k calls/day = **$0/month** (just your GPU/CPU time)

</v-clicks>

---

# The Function Calling Problem

<v-clicks>

## LLMs Can't Take Actions

```python
User: "What's the status of router RTR-01?"

LLM: "I don't have access to your network. 
      I can't check the router status."
```

**LLMs are stateless text generators** - they can't:
- Access databases
- Make API calls
- Execute commands
- Read real-time data

## The Solution: Function/Tool Calling

LLM **decides** what function to call.  
Your code **executes** the function.  
LLM **synthesizes** the result into an answer.

</v-clicks>

---

# Tool Calling Architecture

<v-clicks>

```
┌─────────────────────────────────────────────────┐
│ 1. User: "Check status of router RTR-01"       │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│ 2. LLM: "I need to call get_device_status()     │
│         with device='RTR-01'"                   │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│ 3. Your Code: Execute SSH command,             │
│               return: "Status: UP, 4/4 BGP"     │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│ 4. LLM: "Router RTR-01 is operational.          │
│         All 4 BGP peers are established."       │
└─────────────────────────────────────────────────┘
```

**Key insight:** LLM is the orchestrator, not the executor

</v-clicks>

---

# Defining Tools

<v-clicks>

Tools are defined as JSON schemas:

```python
tools = [
    {
        "name": "get_device_status",
        "description": "Get current operational status of a network device",
        "input_schema": {
            "type": "object",
            "properties": {
                "device_name": {
                    "type": "string",
                    "description": "Device hostname or IP address"
                },
                "check_interfaces": {
                    "type": "boolean",
                    "description": "Include interface status in response",
                    "default": False
                }
            },
            "required": ["device_name"]
        }
    }
]
```

**Critical:** Good descriptions = better tool usage

</v-clicks>

---

# Tool Calling Example

<v-clicks>

```python
import requests

# Define tools (Ollama uses OpenAI-compatible format)
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_device_status",
            "description": "Get operational status of a network device",
            "parameters": {
                "type": "object",
                "properties": {
                    "device_name": {"type": "string"}
                },
                "required": ["device_name"]
            }
        }
    }
]

# Make API call with tools
response = requests.post("http://localhost:11434/api/chat", json={
    "model": "llama3.2:3b",
    "messages": [{"role": "user", "content": "Check status of RTR-CORE-01"}],
    "tools": tools,
    "stream": False
}).json()
```

</v-clicks>

---

# Handling Tool Use Response

<v-clicks>

```python
# LLM returns tool_calls in the message
msg = response["message"]
tool_calls = msg.get("tool_calls") or []

if tool_calls:
    tc = tool_calls[0]["function"]
    print(f"LLM wants to call: {tc['name']}")
    print(f"With arguments: {tc['arguments']}")
    # Output:
    # LLM wants to call: get_device_status
    # With arguments: {'device_name': 'RTR-CORE-01'}

    # Execute the function (YOUR CODE)
    def get_device_status(device_name):
        # SSH to device, run 'show' commands
        return {"status": "up", "bgp_peers": "4/4 established"}

    result = get_device_status(**tc["arguments"])
```

</v-clicks>

---

# Sending Results Back

<v-clicks>

```python
import json

# Send tool result back to LLM
messages = [
    {"role": "user", "content": "Check status of RTR-CORE-01"},
    msg,  # assistant message with tool_calls
    {"role": "tool", "content": json.dumps(result)},
]

# LLM processes result and generates final answer
final_response = requests.post("http://localhost:11434/api/chat", json={
    "model": "llama3.2:3b",
    "messages": messages,
    "tools": tools,
    "stream": False
}).json()

print(final_response["message"]["content"])
# Output:
# "Router RTR-CORE-01 is operational and all 4 BGP peers
#  are in established state."
```

</v-clicks>

---

# Multi-Step Tool Calling

<v-clicks>

LLMs can chain multiple tools:

```
User: "Why is router RTR-01 slow?"

LLM: → Call get_device_status("RTR-01")
You: → "Status: up, high CPU"

LLM: → Call get_cpu_processes("RTR-01")
You: → "Top process: OSPF using 80% CPU"

LLM: → Call search_logs("RTR-01", keyword="OSPF")
You: → "5000 OSPF LSA updates in last 5 minutes"

LLM: "Router RTR-01 is experiencing high CPU due to OSPF 
     LSA flooding. This suggests a network instability or 
     routing loop. Check OSPF neighbors and network topology."
```

**The agentic pattern** - LLM decides the investigation path

</v-clicks>

---

# Live Demo: Tool Calling

<v-clicks>

Let's build a simple network tool:

```python
def get_interface_status(device, interface):
    """Simulate getting interface status"""
    # In reality: SSH + parse output
    return {
        "interface": interface,
        "status": "up",
        "speed": "1000Mbps",
        "errors": 0
    }

# Define tool schema
tools = [{
    "name": "get_interface_status",
    "description": "Get status of a network interface",
    "input_schema": {
        "type": "object",
        "properties": {
            "device": {"type": "string", "description": "Device name"},
            "interface": {"type": "string", "description": "Interface name"}
        },
        "required": ["device", "interface"]
    }
}]

# Test it
response = requests.post("http://localhost:11434/api/chat", json={
    "model": "llama3.2:3b",
    "messages": [{"role": "user", "content": "Check Gi0/1 on RTR-01"}],
    "tools": tools,
    "stream": False
}).json()
```

</v-clicks>

---

# Tool Calling Best Practices

<v-clicks>

## 1. Clear Descriptions

```python
# Bad
"description": "Gets data"

# Good
"description": "Retrieves current operational status and statistics 
                for a specific network interface, including admin/oper 
                state, speed, duplex, and error counters"
```

## 2. Validate Tool Inputs

```python
def get_device_status(device_name):
    # Validate before execution
    if not re.match(r'^[a-zA-Z0-9\-]+$', device_name):
        raise ValueError(f"Invalid device name: {device_name}")
    
    # Execute
    return ssh_command(device_name, "show version")
```

</v-clicks>

---

# Tool Calling Best Practices (cont.)

<v-clicks>

## 3. Handle Errors Gracefully

```python
try:
    result = ssh_command(device, cmd)
except TimeoutError:
    return {
        "error": "Device unreachable (timeout)",
        "suggestion": "Check network connectivity"
    }
except PermissionError:
    return {
        "error": "Authentication failed",
        "suggestion": "Verify SSH credentials"
    }
```

## 4. Log Everything

```python
logger.info(f"Tool called: {tool_name} with args: {args}")
logger.info(f"Tool result: {result}")
logger.info(f"Execution time: {elapsed}s")
```

</v-clicks>

---

# When NOT to Use Tools

<v-clicks>

## LLMs Can Answer These Directly

❌ "What is BGP?" - General knowledge  
❌ "Explain OSPF areas" - Concept explanation  
❌ "How do VLANs work?" - Technical description  

## These Need Tools

✅ "What's the BGP status on router X?" - Real-time data  
✅ "Show me current OSPF neighbors" - Device query  
✅ "Which VLANs are configured?" - Configuration retrieval  

**Rule of thumb:** If it requires accessing systems, use tools

</v-clicks>

---

# Module 5 Takeaways

<v-clicks>

### Key Concepts

✅ **LLMs orchestrate, you execute** - Clear separation of concerns  
✅ **Tool schemas are critical** - Good descriptions = better usage  
✅ **Always validate inputs** - LLMs can hallucinate parameters  
✅ **Log everything** - Debugging and auditing are essential  

### The Agentic Pattern

```
User question → LLM decides tools → Execute → Results back → Final answer
```

This pattern enables **autonomous problem-solving**

### Next Lab

We'll build a chatbot that uses this pattern

</v-clicks>

---
layout: center
class: text-center
---

# 10 Minute Break

Stretch, grab coffee, check your environment

Next up: **Building a chatbot with memory**

---
layout: center
class: text-center
---

# Module 6

## Lab 3: Build a Basic Chatbot

20 minutes

---

# The Chatbot Challenge

<v-clicks>

## Problem: Stateless LLMs

```python
# Call 1
chat("What is OSPF?")
# LLM: "OSPF is a link-state routing protocol..."

# Call 2 (separate request)
chat("What did I just ask you?")
# LLM: "I don't have access to previous messages"
```

## Solution: Conversation History

**You** manage state, not the LLM

```python
history = [
    {"role": "user", "content": "What is OSPF?"},
    {"role": "assistant", "content": "OSPF is..."},
    {"role": "user", "content": "What did I just ask?"}
]
```

</v-clicks>

---

# Lab 3 - Part A: Stateless Chat

<v-clicks>

Let's start simple:

```python
# chatbot_v1.py
import requests

def simple_chat(user_message, model="llama3.2:3b"):
    response = requests.post("http://localhost:11434/api/generate", json={
        "model": model,
        "prompt": user_message,
        "stream": False
    })
    return response.json()["response"]

# Test it
print(simple_chat("What is OSPF?"))
print(simple_chat("What did I just ask you?"))
```

**Result:** Second question fails - no memory

</v-clicks>

---

# Lab 3 - Part B: Add Memory

<v-clicks>

Build a class to manage conversation state:

```python
# chatbot_v2.py
import requests

class NetworkChatbot:
    def __init__(self, model="llama3.2:3b"):
        self.model = model
        self.conversation_history = []

    def chat(self, user_message):
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })

        # Build a single prompt from history
        full_prompt = "\n".join(
            f"{m['role'].capitalize()}: {m['content']}"
            for m in self.conversation_history
        ) + "\nAssistant:"

        # Call Ollama with full history
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": self.model,
            "prompt": full_prompt,
            "stream": False
        })
        assistant_message = response.json()["response"].strip()

        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })
        return assistant_message
```

</v-clicks>

---

# Testing the Chatbot

<v-clicks>

```python
# Test with memory
bot = NetworkChatbot()

print(bot.chat("What is OSPF?"))
# Output: "OSPF is a link-state routing protocol..."

print(bot.chat("What did I just ask you?"))
# Output: "You asked me to explain what OSPF is."

print(bot.chat("What are the OSPF neighbor states?"))
# Output: "OSPF neighbor states are: Down, Init, 2-Way..."

print(bot.chat("Which state did you mention first?"))
# Output: "The first state I mentioned was 'Down'."
```

**✅ Memory works!** The chatbot remembers the conversation.

</v-clicks>

---

# Add Helper Methods

<v-clicks>

```python
class NetworkChatbot:
    # ... (previous code)
    
    def reset(self):
        """Clear conversation history"""
        self.conversation_history = []
        return "Conversation reset."
    
    def get_history(self):
        """Return conversation history"""
        return self.conversation_history
    
    def set_system_prompt(self, prompt):
        """Add a system message at the start"""
        system_msg = {
            "role": "system",
            "content": prompt
        }
        # Insert at beginning if not already there
        if not self.conversation_history or \
           self.conversation_history[0].get("role") != "system":
            self.conversation_history.insert(0, system_msg)
    
    def token_count(self):
        """Estimate tokens in conversation"""
        # Rough estimate: 0.75 tokens per character
        total_chars = sum(
            len(msg["content"]) 
            for msg in self.conversation_history
        )
        return int(total_chars * 0.75)
```

</v-clicks>

---

# Lab 3 - Part C: Context Window Management

<v-clicks>

## The Problem

```python
# After 50 messages:
bot.token_count()  # Output: 125,000 tokens

# Next message fails:
# Error: context_length_exceeded (max: 128,000)
```

## Solution: Truncate Old Messages

```python
class NetworkChatbot:
    def __init__(self, model="llama3.2:3b", max_messages=20):
        self.model = model
        self.conversation_history = []
        self.max_messages = max_messages
    
    def truncate_history(self):
        """Keep only recent messages"""
        if len(self.conversation_history) > self.max_messages:
            # Keep system message if present
            system_msg = None
            if self.conversation_history[0].get("role") == "system":
                system_msg = self.conversation_history[0]
            
            # Keep most recent messages
            recent = self.conversation_history[-self.max_messages:]
            
            # Reconstruct with system message
            if system_msg:
                self.conversation_history = [system_msg] + recent
            else:
                self.conversation_history = recent
```

</v-clicks>

---

# Smart Truncation Strategy

<v-clicks>

```python
def smart_truncate(self):
    """Keep important messages, summarize old ones"""
    
    if len(self.conversation_history) <= self.max_messages:
        return  # No truncation needed
    
    # Keep first message (system prompt)
    # Keep last N messages (recent context)
    # Summarize the middle
    
    system = self.conversation_history[0] if \
             self.conversation_history[0].get("role") == "system" else None
    
    recent = self.conversation_history[-10:]  # Last 10 messages
    old = self.conversation_history[1:-10] if system else \
          self.conversation_history[:-10]
    
    # Summarize old messages
    summary = self.summarize_messages(old)
    
    # Reconstruct
    new_history = []
    if system:
        new_history.append(system)
    if summary:
        new_history.append({
            "role": "assistant",
            "content": f"[Summary of earlier conversation: {summary}]"
        })
    new_history.extend(recent)
    
    self.conversation_history = new_history
```

</v-clicks>

---

# Add Persistence

<v-clicks>

```python
import json
from datetime import datetime

class NetworkChatbot:
    # ... (previous code)
    
    def save_conversation(self, filename=None):
        """Save conversation to JSON file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"conversation_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(self.conversation_history, f, indent=2)
        
        return filename
    
    def load_conversation(self, filename):
        """Load conversation from JSON file"""
        with open(filename, 'r') as f:
            self.conversation_history = json.load(f)
        
        return f"Loaded {len(self.conversation_history)} messages"
```

</v-clicks>

---

# Build a CLI Interface

<v-clicks>

```python
# cli.py
from chatbot_v2 import NetworkChatbot

def main():
    bot = NetworkChatbot()
    
    # Set system prompt
    bot.set_system_prompt(
        "You are a helpful network engineer assistant. "
        "Provide clear, accurate information about networking concepts "
        "and troubleshooting. When uncertain, say so."
    )
    
    print("🤖 Network Assistant Ready!")
    print("Commands: /reset, /save, /load <file>, /quit\n")
    
    while True:
        user_input = input("You: ").strip()
        
        # Handle commands
        if user_input == "/quit":
            print("👋 Goodbye!")
            break
        elif user_input == "/reset":
            bot.reset()
            print("🔄 Conversation reset\n")
            continue
        elif user_input == "/save":
            filename = bot.save_conversation()
            print(f"💾 Saved to {filename}\n")
            continue
        elif user_input.startswith("/load"):
            _, filename = user_input.split(maxsplit=1)
            result = bot.load_conversation(filename)
            print(f"📂 {result}\n")
            continue
        
        # Normal chat
        if not user_input:
            continue
        
        try:
            response = bot.chat(user_input)
            print(f"\n🤖: {response}\n")
        except Exception as e:
            print(f"❌ Error: {e}\n")

if __name__ == "__main__":
    main()
```

</v-clicks>

---

# Challenge: Enhanced Features

<v-clicks>

Build these improvements:

### 1. Token Counter Display
```python
# Show token usage after each message
tokens = bot.token_count()
print(f"[Tokens: {tokens:,}]")
```

### 2. Conversation Branching
```python
# Allow user to go back and try different path
def rewind(self, n=1):
    """Remove last n message pairs"""
    self.conversation_history = self.conversation_history[:-2*n]
```

### 3. Export to Markdown
```python
def export_markdown(self, filename):
    """Export as readable markdown"""
    with open(filename, 'w') as f:
        f.write("# Conversation Log\n\n")
        for msg in self.conversation_history:
            role = msg["role"].title()
            content = msg["content"]
            f.write(f"## {role}\n\n{content}\n\n")
```

</v-clicks>

---

# Lab 3 Takeaways

<v-clicks>

### What You Built

✅ Stateful chatbot with conversation memory  
✅ Context window management  
✅ Persistence (save/load conversations)  
✅ CLI interface for testing  

### Key Lessons

- **State lives in your app** - LLMs are stateless
- **Memory management is critical** - Costs and limits
- **System prompts set behavior** - Define the persona
- **Truncation strategies matter** - Simple vs. smart

### Next Module

Add **tool calling** to make the chatbot agentic

</v-clicks>

---
layout: center
class: text-center
---

# Module 7

## Lab 4: Agentic Loop in Python

20 minutes

---

# What Makes an Agent?

<v-clicks>

## Chatbot vs. Agent

**Chatbot:**
- Answers questions
- Uses only its training data
- Cannot take actions

**Agent:**
- Can use tools to gather information
- Can execute actions on your behalf
- Can chain multiple steps to solve problems

## The Agentic Loop

```
User question → LLM thinks → Needs tool? 
    ↓ Yes                      ↓ No
Call tool(s)              Answer directly
    ↓
Process results
    ↓
LLM synthesizes final answer
```

</v-clicks>

---

# Lab 4 - Part A: Define Network Tools

<v-clicks>

```python
# tools.py
def get_interface_status(device_name, interface):
    """Get current status of a network interface"""
    # In reality: SSH to device, run show command
    # For lab: Return mock data
    return {
        "interface": interface,
        "status": "up",
        "description": "Link to Core Switch",
        "speed": "10Gbps",
        "input_rate": "234 Mbps",
        "output_rate": "567 Mbps",
        "input_errors": 0,
        "output_errors": 0,
        "last_cleared": "never"
    }

def get_bgp_neighbors(device_name):
    """Get BGP neighbor status"""
    return {
        "total_peers": 4,
        "established": 3,
        "neighbors": [
            {"ip": "10.0.0.1", "state": "Established", "uptime": "3d2h"},
            {"ip": "10.0.0.2", "state": "Established", "uptime": "1d5h"},
            {"ip": "10.0.0.3", "state": "Established", "uptime": "2d1h"},
            {"ip": "10.0.0.4", "state": "Idle", "uptime": "0h"}
        ]
    }
```

</v-clicks>

---

# More Tools

<v-clicks>

```python
def search_logs(device_name, keyword, lines=50):
    """Search device logs for keywords"""
    # Simulate log search
    if keyword.lower() == "bgp":
        return """
2024-01-15 14:32:11: %BGP-5-ADJCHANGE: neighbor 10.0.0.4 Down
2024-01-15 14:32:08: %LINK-3-UPDOWN: Interface Gi0/1, changed state to down
2024-01-15 14:31:55: %LINEPROTO-5-UPDOWN: Line protocol on Interface Gi0/1, changed state to down
        """.strip()
    return f"No matches found for '{keyword}'"

def execute_ping(target, count=4):
    """Ping a network device"""
    import subprocess
    try:
        result = subprocess.run(
            ["ping", "-c", str(count), target],
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.stdout
    except subprocess.TimeoutExpired:
        return f"Ping to {target} timed out"
    except Exception as e:
        return f"Error: {str(e)}"
```

</v-clicks>

---

# Lab 4 - Part B: Tool Schemas

<v-clicks>

```python
# tool_schemas.py
TOOLS = [
    {
        "name": "get_interface_status",
        "description": "Get current status and statistics for a network interface",
        "input_schema": {
            "type": "object",
            "properties": {
                "device_name": {
                    "type": "string",
                    "description": "Hostname or IP of the device"
                },
                "interface": {
                    "type": "string",
                    "description": "Interface name (e.g., 'GigabitEthernet0/1', 'eth0')"
                }
            },
            "required": ["device_name", "interface"]
        }
    },
    {
        "name": "get_bgp_neighbors",
        "description": "Get BGP neighbor status and session information",
        "input_schema": {
            "type": "object",
            "properties": {
                "device_name": {
                    "type": "string",
                    "description": "Hostname or IP of the router"
                }
            },
            "required": ["device_name"]
        }
    },
    # ... (other tools)
]
```

</v-clicks>

---

# Lab 4 - Part C: The Agentic Loop

<v-clicks>

```python
# agentic_chatbot.py  (see agentic_network_bot.py for full code)
import requests, json
from tools import get_interface_status, get_bgp_neighbors, search_logs, execute_ping
from tool_schemas import TOOLS  # Ollama/OpenAI-compatible format

class AgenticNetworkBot:
    def __init__(self, model="llama3.2:3b"):
        self.model = model
        self.conversation_history = []
        self.tool_functions = {
            "get_interface_status": get_interface_status,
            "get_bgp_neighbors": get_bgp_neighbors,
            "search_logs": search_logs,
            "execute_ping": execute_ping
        }

    def chat(self, user_message):
        self.conversation_history.append({
            "role": "user", "content": user_message
        })

        # Agentic loop: keep calling tools until LLM is done
        while True:
            response = requests.post("http://localhost:11434/api/chat", json={
                "model": self.model,
                "messages": self.conversation_history,
                "tools": TOOLS,
                "stream": False
            }).json()

            msg = response["message"]
            tool_calls = msg.get("tool_calls") or []

            if not tool_calls:
                # LLM has final answer
                self.conversation_history.append(msg)
                return msg.get("content", "")
```

</v-clicks>

---

# Agentic Loop (continued)

<v-clicks>

```python
            if tool_calls:
                # LLM wants to call tools
                self.conversation_history.append(msg)
                
                # Execute all requested tools
                tool_results = []
                for block in response.content:
                    if block.type == "tool_use":
                        print(f"🔧 Calling: {block.name}({block.input})")
                        
                        # Get the function
                        tool_func = self.tool_functions[block.name]
                        
                        # Execute it
                        try:
                            result = tool_func(**block.input)
                        except Exception as e:
                            result = f"Error: {str(e)}"
                        
                        # Store result
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": str(result)
                        })
                
                # Send results back to LLM
                self.conversation_history.append({
                    "role": "user",
                    "content": tool_results
                })
                # Loop continues - LLM will process results
    
    def _extract_text(self, content):
        """Extract text from response content"""
        for block in content:
            if hasattr(block, 'text'):
                return block.text
        return ""
```

</v-clicks>

---

# Testing the Agent

<v-clicks>

```python
# test_agent.py
from agentic_chatbot import AgenticNetworkBot

bot = AgenticNetworkBot()

# Test 1: Simple question (no tools needed)
response = bot.chat("What is OSPF?")
print(response)
# Output: "OSPF is a link-state routing protocol..."
# No tools called ✅

# Test 2: Requires one tool
response = bot.chat("Check BGP neighbors on RTR-CORE-01")
# 🔧 Calling: get_bgp_neighbors({'device_name': 'RTR-CORE-01'})
print(response)
# Output: "Router RTR-CORE-01 has 3 of 4 BGP neighbors established. 
#          Neighbor 10.0.0.4 is in Idle state."

# Test 3: Requires multiple tools
response = bot.chat("Why is BGP neighbor 10.0.0.4 down on RTR-CORE-01?")
# 🔧 Calling: get_bgp_neighbors({'device_name': 'RTR-CORE-01'})
# 🔧 Calling: search_logs({'device_name': 'RTR-CORE-01', 'keyword': 'BGP'})
print(response)
# Output: "BGP neighbor 10.0.0.4 went down at 14:32:11 due to interface 
#          Gi0/1 going down. This appears to be a physical layer issue."
```

</v-clicks>

---

# Multi-Step Reasoning Demo

<v-clicks>

```python
# Complex troubleshooting scenario
response = bot.chat(
    "I can't reach 10.0.0.4 from RTR-CORE-01. What's wrong?"
)

# Watch the agentic loop:
# 🔧 Calling: execute_ping({'target': '10.0.0.4', 'count': 4})
# Result: 0% packet loss

# 🔧 Calling: get_interface_status({'device_name': 'RTR-CORE-01', 
#                                   'interface': 'GigabitEthernet0/1'})
# Result: interface up, no errors

# 🔧 Calling: get_bgp_neighbors({'device_name': 'RTR-CORE-01'})
# Result: 10.0.0.4 in Idle state

# 🔧 Calling: search_logs({'device_name': 'RTR-CORE-01', 'keyword': 'BGP'})
# Result: neighbor went down, interface flapped

# Final synthesis:
print(response)
# "The issue is that while the ping succeeds (layer 3 connectivity is OK),
#  the BGP session with 10.0.0.4 is down due to a recent interface flap.
#  The logs show Gi0/1 went down at 14:31:55. Check physical layer and
#  investigate why the interface flapped."
```

**This is autonomous troubleshooting** 🎯

</v-clicks>

---

# Challenge: Safety & Validation

<v-clicks>

Add safety checks:

### 1. Read-Only Mode
```python
class AgenticNetworkBot:
    def __init__(self, read_only=True):
        self.read_only = read_only
        # Filter out dangerous tools
        if read_only:
            self.tool_functions = {
                k: v for k, v in self.tool_functions.items()
                if k not in ['execute_command', 'modify_config']
            }
```

### 2. Tool Call Logging
```python
import logging

logger = logging.getLogger(__name__)

# In tool execution:
logger.info(f"Tool called: {block.name} with args: {block.input}")
logger.info(f"Result: {result}")
```

### 3. Input Validation
```python
def validate_device_name(device):
    if not re.match(r'^[a-zA-Z0-9\-\.]+$', device):
        raise ValueError(f"Invalid device name: {device}")
```

</v-clicks>

---

# Challenge: Error Handling

<v-clicks>

Make the agent resilient:

```python
# In tool execution loop:
for block in response.content:
    if block.type == "tool_use":
        print(f"🔧 Calling: {block.name}({block.input})")
        
        try:
            # Validate inputs
            self._validate_tool_input(block.name, block.input)
            
            # Execute
            tool_func = self.tool_functions[block.name]
            result = tool_func(**block.input)
            
            # Validate output
            if result is None:
                result = "No data returned"
            
        except KeyError:
            result = f"Error: Unknown tool '{block.name}'"
        except TypeError as e:
            result = f"Error: Invalid arguments - {str(e)}"
        except TimeoutError:
            result = "Error: Operation timed out"
        except Exception as e:
            result = f"Error: {type(e).__name__}: {str(e)}"
            logger.exception("Tool execution failed")
        
        tool_results.append({
            "type": "tool_result",
            "tool_use_id": block.id,
            "content": str(result),
            "is_error": "Error:" in str(result)
        })
```

</v-clicks>

---

# Lab 4 Takeaways

<v-clicks>

### What You Built

✅ Agentic chatbot that can use tools  
✅ Multi-step reasoning and problem-solving  
✅ Network troubleshooting automation  
✅ Safety mechanisms (read-only mode, validation)  

### Key Insights

- **Agents = LLM + Tools + Loop** - The pattern is simple
- **LLM decides strategy** - You provide capabilities
- **Tool quality matters** - Good tools = good agents
- **Safety is critical** - Always validate and log

### Next Module

Make this portable with **Model Context Protocol (MCP)**

</v-clicks>

---
layout: center
class: text-center
---

# Module 8

## Model Context Protocol (MCP)

20 minutes

---

# The Tool Portability Problem

<v-clicks>

## Current State

```
Your Chatbot:  Hardcoded tools, SSH functions
Claude Desktop: Filesystem tools
ChatGPT:        Calculator, web search
VS Code Copilot: Code tools

Everyone builds the same tools differently!
```

## What If...

```
You build a tool server ONCE
↓
Any MCP client can use it
↓
Claude Desktop ✅
Your chatbot ✅
Future apps ✅
```

**MCP = npm/pip for AI tools**

</v-clicks>

---

# What is MCP?

<v-clicks>

## Model Context Protocol

A **standard protocol** for connecting AI models to external tools and data

### Created by Anthropic (Dec 2024)
- Open specification
- Reference implementations (Python, TypeScript)
- Growing ecosystem of servers

### Key Idea
Decouple tool implementation from LLM applications

```
LLM Application (MCP Client) ←→ MCP Protocol ←→ Tool Server (MCP Server)
```

Like HTTP for web, MCP for AI tools

</v-clicks>

---

# MCP Architecture

```
┌─────────────────────────────────────────┐
│         MCP Client                      │
│  (Claude Desktop, your chatbot, etc.)   │
│                                         │
│  - Discovers available tools            │
│  - Calls tools via MCP protocol         │
│  - Processes results                    │
└────────────────┬────────────────────────┘
                 │
                 │ MCP Protocol
                 │ (JSON-RPC over stdio/SSE/HTTP)
                 │
┌────────────────▼────────────────────────┐
│         MCP Server                      │
│  (Your tool implementation)             │
│                                         │
│  ├─ Resources (read-only data)          │
│  ├─ Tools (actions/queries)             │
│  └─ Prompts (reusable templates)        │
└─────────────────────────────────────────┘
```

---

# MCP Core Concepts

<v-clicks>

## 1. Resources

**Read-only data sources**

Examples:
- File contents
- Database records
- API responses
- Configuration files

```json
{
  "uri": "network://devices/inventory",
  "name": "Device Inventory",
  "mimeType": "application/json"
}
```

## 2. Tools

**Actions the LLM can execute**

Examples:
- SSH commands
- API calls
- File modifications
- Database queries

```json
{
  "name": "get_device_status",
  "description": "Query device operational status",
  "inputSchema": {...}
}
```

</v-clicks>

---

# MCP Core Concepts (cont.)

<v-clicks>

## 3. Prompts

**Reusable prompt templates**

Example:
```json
{
  "name": "analyze_config",
  "description": "Analyze network config for security issues",
  "arguments": [
    {"name": "config_text", "required": true},
    {"name": "severity_threshold", "required": false}
  ]
}
```

When user selects this prompt:
- Client fills in arguments
- Sends complete prompt to LLM
- Gets analysis back

**Think: GitHub Gists for prompts**

</v-clicks>

---

# MCP vs. Direct Function Calling

<v-clicks>

| Aspect | Direct Function Calling | MCP |
|--------|------------------------|-----|
| **Portability** | Tied to your app | Works with any MCP client |
| **Discovery** | Hardcoded | Dynamic, runtime discovery |
| **Protocol** | App-specific | Standard JSON-RPC |
| **Sharing** | Copy/paste code | Deploy once, use everywhere |
| **Examples** | Anthropic tool use, OpenAI functions | Claude Desktop, Cline, Zed |

### When to Use What?

**Direct function calling:**
- Single app, internal use
- Maximum control
- Prototype/MVP

**MCP:**
- Multi-app deployment
- Community sharing
- Production systems

</v-clicks>

---

# MCP Transport Layers

<v-clicks>

## 1. stdio (Standard Input/Output)

```python
# Server runs as subprocess
# Client writes to stdin, reads from stdout
python server.py
```

**Use case:** Local tools, Claude Desktop integration

## 2. Server-Sent Events (SSE)

```python
# HTTP server with streaming responses
# Client subscribes to event stream
```

**Use case:** Remote tools, web applications

## 3. HTTP (Coming Soon)

Request/response model

**Use case:** RESTful tool servers

</v-clicks>

---

# MCP in Claude Desktop

<v-clicks>

## Configuration

```json
// ~/Library/Application Support/Claude/claude_desktop_config.json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/me/Documents"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "ghp_..."
      }
    },
    "network-tools": {
      "command": "python",
      "args": ["/path/to/network-mcp-server/server.py"]
    }
  }
}
```

Restart Claude Desktop → Tools appear automatically

</v-clicks>

---

# Live Demo: Existing MCP Servers

<v-clicks>

### Official Servers

1. **@modelcontextprotocol/server-filesystem**
   - Read/write files
   - Search directories
   - Create/edit/delete

2. **@modelcontextprotocol/server-github**
   - Create issues
   - Search repos
   - Manage PRs

3. **@modelcontextprotocol/server-postgres**
   - Query databases
   - Execute SQL
   - Schema inspection

### Community Servers

- AWS (S3, EC2, RDS)
- Slack (messages, channels)
- Google Drive (files, folders)
- Linear (issues, projects)

Find more: https://github.com/modelcontextprotocol/servers

</v-clicks>

---

# MCP Protocol Basics

<v-clicks>

## JSON-RPC 2.0

All MCP communication uses JSON-RPC:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/list",
  "params": {}
}
```

Response:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "tools": [
      {
        "name": "get_device_status",
        "description": "...",
        "inputSchema": {...}
      }
    ]
  }
}
```

</v-clicks>

---

# MCP Methods

<v-clicks>

## Core Methods

### Server → Client
- `initialize` - Handshake and capabilities
- `tools/list` - Get available tools
- `resources/list` - Get available resources
- `prompts/list` - Get available prompts

### Client → Server
- `tools/call` - Execute a tool
- `resources/read` - Read a resource
- `prompts/get` - Get a prompt template

### Lifecycle
- `notifications/initialized` - Server ready
- `ping` - Keep-alive

</v-clicks>

---

# When to Use MCP

<v-clicks>

## ✅ Use MCP When:

- Building tools for **multiple LLM apps**
- Want to **share tools** with the community
- Need **discoverability** (tools found at runtime)
- Building for **Claude Desktop, Cline, Zed**
- Want to **future-proof** your tool investments

## ❌ Skip MCP When:

- **Single app**, tightly integrated
- **Maximum performance** required (extra protocol overhead)
- **Prototype/MVP** phase (ship fast, refactor later)
- **Proprietary tools** that can't be shared

**Rule of thumb:** If your tools have value beyond one app, use MCP

</v-clicks>

---

# Module 8 Takeaways

<v-clicks>

### Key Concepts

✅ **MCP = Standard protocol** for AI tools  
✅ **Three primitives:** Resources, Tools, Prompts  
✅ **Transport:** stdio, SSE, HTTP  
✅ **Growing ecosystem:** Official + community servers  

### Why MCP Matters

- **Portability** - Write once, use everywhere
- **Discoverability** - Clients find tools dynamically
- **Standardization** - Common protocol vs. app-specific APIs
- **Ecosystem** - Community-built tools

### Next Lab

We'll **build our own MCP server** with network tools

</v-clicks>

---
layout: center
class: text-center
---

# 10 Minute Break

Stretch, review MCP docs, prepare for building

Next up: **Building an MCP server from scratch**

---
layout: center
class: text-center
---

# Module 9

## Lab 5: Build an MCP Tool Server

25 minutes

---

# Lab 5 Overview

<v-clicks>

### What We'll Build

A production-ready MCP server with:

1. ✅ Network device tools (status, ping, SSH)
2. ✅ Resources (device inventory, config templates)
3. ✅ Proper error handling
4. ✅ Logging and validation

### Structure

```
network-mcp-server/
├── server.py          # MCP server implementation
├── tools.py           # Tool functions
├── resources.py       # Resource handlers
└── README.md          # Documentation
```

**Time: 25 minutes**

</v-clicks>

---

# Setup

<v-clicks>

```bash
# Install MCP SDK
pip install mcp

# Create project
mkdir network-mcp-server
cd network-mcp-server

# Create files
touch server.py tools.py resources.py
```

### Install Dependencies

```bash
pip install mcp paramiko netmiko
```

**Note:** For the lab, we'll use mock data. In production, add:
- `paramiko` or `netmiko` for SSH
- `requests` for REST APIs
- Your network vendor libraries

</v-clicks>

---

# Lab 5 - Part A: Basic MCP Server

<v-clicks>

```python
# server.py
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Initialize MCP server
app = Server("network-tools-mcp")

@app.list_tools()
async def list_tools() -> list[Tool]:
    """Return available tools"""
    return [
        Tool(
            name="get_interface_status",
            description="Get status of a network interface including admin/oper state, speed, and error counters",
            inputSchema={
                "type": "object",
                "properties": {
                    "device": {
                        "type": "string",
                        "description": "Device hostname or IP address"
                    },
                    "interface": {
                        "type": "string",
                        "description": "Interface name (e.g., 'GigabitEthernet0/1', 'eth0')"
                    }
                },
                "required": ["device", "interface"]
            }
        ),
```

</v-clicks>

---

# More Tools

<v-clicks>

```python
        Tool(
            name="ping_device",
            description="Ping a network device to check reachability and measure latency",
            inputSchema={
                "type": "object",
                "properties": {
                    "target": {
                        "type": "string",
                        "description": "IP address or hostname to ping"
                    },
                    "count": {
                        "type": "integer",
                        "description": "Number of ping packets to send",
                        "default": 4,
                        "minimum": 1,
                        "maximum": 10
                    }
                },
                "required": ["target"]
            }
        ),
        Tool(
            name="get_bgp_summary",
            description="Get BGP neighbor summary including state, uptime, and prefix counts",
            inputSchema={
                "type": "object",
                "properties": {
                    "device": {
                        "type": "string",
                        "description": "Router hostname or IP address"
                    }
                },
                "required": ["device"]
            }
        )
    ]
```

</v-clicks>

---

# Implement Tool Execution

<v-clicks>

```python
@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Execute the requested tool"""
    
    if name == "get_interface_status":
        device = arguments["device"]
        interface = arguments["interface"]
        
        # In production: SSH to device, parse 'show interface' output
        # For lab: Return mock data
        result = {
            "device": device,
            "interface": interface,
            "admin_status": "up",
            "oper_status": "up",
            "speed": "1000Mbps",
            "duplex": "full",
            "mtu": 1500,
            "input_rate": "234 Mbps",
            "output_rate": "567 Mbps",
            "input_errors": 0,
            "output_errors": 0,
            "input_packets": 1234567890,
            "output_packets": 987654321,
            "last_cleared": "never"
        }
        
        # Format as human-readable text
        text = f"""Interface {interface} on {device}:
Status: {result['admin_status']}/{result['oper_status']}
Speed: {result['speed']}, Duplex: {result['duplex']}, MTU: {result['mtu']}
Traffic: {result['input_rate']} in, {result['output_rate']} out
Errors: {result['input_errors']} in, {result['output_errors']} out
Packets: {result['input_packets']:,} in, {result['output_packets']:,} out
"""
        
        return [TextContent(type="text", text=text)]
```

</v-clicks>

---

# More Tool Implementations

<v-clicks>

```python
    elif name == "ping_device":
        import subprocess
        
        target = arguments["target"]
        count = arguments.get("count", 4)
        
        # Actually ping the device
        try:
            result = subprocess.run(
                ["ping", "-c", str(count), target],
                capture_output=True,
                text=True,
                timeout=15
            )
            
            return [TextContent(type="text", text=result.stdout)]
            
        except subprocess.TimeoutExpired:
            return [TextContent(
                type="text",
                text=f"Error: Ping to {target} timed out after 15 seconds"
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Error pinging {target}: {str(e)}"
            )]
    
    elif name == "get_bgp_summary":
        device = arguments["device"]
        
        # Mock BGP data
        summary = {
            "router_id": "10.0.0.1",
            "local_as": 65001,
            "neighbors": [
                {"ip": "10.0.0.2", "remote_as": 65002, "state": "Established", "uptime": "3d2h", "prefixes": 150},
                {"ip": "10.0.0.3", "remote_as": 65003, "state": "Established", "uptime": "1d5h", "prefixes": 200},
                {"ip": "10.0.0.4", "remote_as": 65004, "state": "Idle", "uptime": "0h", "prefixes": 0}
            ]
        }
        
        text = f"""BGP Summary for {device}:
Router ID: {summary['router_id']}
Local AS: {summary['local_as']}

Neighbors:
"""
        for n in summary['neighbors']:
            text += f"  {n['ip']} (AS {n['remote_as']}): {n['state']}, Up: {n['uptime']}, Prefixes: {n['prefixes']}\n"
        
        return [TextContent(type="text", text=text)]
    
    else:
        raise ValueError(f"Unknown tool: {name}")
```

</v-clicks>

---

# Lab 5 - Part B: Add Resources

<v-clicks>

```python
from mcp.types import Resource
import json

@app.list_resources()
async def list_resources() -> list[Resource]:
    """Return available resources"""
    return [
        Resource(
            uri="network://devices/inventory",
            name="Device Inventory",
            description="Complete list of all managed network devices with metadata",
            mimeType="application/json"
        ),
        Resource(
            uri="network://configs/template/bgp",
            name="BGP Configuration Template",
            description="Standard BGP configuration template for new deployments",
            mimeType="text/plain"
        ),
        Resource(
            uri="network://topology/datacenter",
            name="Data Center Topology",
            description="Physical and logical topology of the data center network",
            mimeType="application/json"
        )
    ]
```

</v-clicks>

---

# Implement Resource Reading

<v-clicks>

```python
@app.read_resource()
async def read_resource(uri: str) -> str:
    """Read a resource by URI"""
    
    if uri == "network://devices/inventory":
        # In production: Query database, IPAM, or NetBox
        inventory = {
            "last_updated": "2024-01-15T14:30:00Z",
            "total_devices": 3,
            "devices": [
                {
                    "hostname": "RTR-CORE-01",
                    "ip": "10.0.0.1",
                    "type": "router",
                    "vendor": "Cisco",
                    "model": "ASR1000",
                    "location": "DC1",
                    "role": "core"
                },
                {
                    "hostname": "RTR-CORE-02",
                    "ip": "10.0.0.2",
                    "type": "router",
                    "vendor": "Cisco",
                    "model": "ASR1000",
                    "location": "DC1",
                    "role": "core"
                },
                {
                    "hostname": "SW-ACCESS-01",
                    "ip": "10.0.1.1",
                    "type": "switch",
                    "vendor": "Arista",
                    "model": "7050SX",
                    "location": "DC1",
                    "role": "access"
                }
            ]
        }
        return json.dumps(inventory, indent=2)
```

</v-clicks>

---

# More Resources

<v-clicks>

```python
    elif uri == "network://configs/template/bgp":
        # Configuration template
        template = """
! BGP Configuration Template
router bgp {AS_NUMBER}
 bgp log-neighbor-changes
 bgp router-id {ROUTER_ID}
 
 ! Neighbor configuration
 neighbor {PEER_IP} remote-as {PEER_AS}
 neighbor {PEER_IP} description {PEER_DESCRIPTION}
 neighbor {PEER_IP} password {PEER_PASSWORD}
 
 ! Address family IPv4
 address-family ipv4
  neighbor {PEER_IP} activate
  neighbor {PEER_IP} soft-reconfiguration inbound
  neighbor {PEER_IP} route-map {ROUTE_MAP_IN} in
  neighbor {PEER_IP} route-map {ROUTE_MAP_OUT} out
  neighbor {PEER_IP} maximum-prefix {MAX_PREFIX} 90
 exit-address-family
"""
        return template.strip()
    
    elif uri == "network://topology/datacenter":
        topology = {
            "name": "DC1",
            "tiers": ["core", "distribution", "access"],
            "devices": {
                "core": ["RTR-CORE-01", "RTR-CORE-02"],
                "access": ["SW-ACCESS-01"]
            },
            "links": [
                {"from": "RTR-CORE-01", "to": "RTR-CORE-02", "type": "10G"},
                {"from": "RTR-CORE-01", "to": "SW-ACCESS-01", "type": "1G"},
                {"from": "RTR-CORE-02", "to": "SW-ACCESS-01", "type": "1G"}
            ]
        }
        return json.dumps(topology, indent=2)
    
    else:
        raise ValueError(f"Unknown resource: {uri}")
```

</v-clicks>

---

# Start the MCP Server

<v-clicks>

```python
async def main():
    """Run the MCP server"""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
```

**Run it:**

```bash
python server.py
```

Server runs and waits for stdio communication from MCP client.

</v-clicks>

---

# Lab 5 - Part C: Test with MCP Inspector

<v-clicks>

```bash
# Install MCP inspector
npm install -g @modelcontextprotocol/inspector

# Run your server through inspector
mcp-inspector python server.py
```

The inspector provides a web UI to:
- ✅ List available tools and resources
- ✅ Test tool calls with custom inputs
- ✅ View server logs and errors
- ✅ Validate MCP protocol compliance

### Testing Checklist

1. List tools → Should show 3 tools
2. Call `get_interface_status` → Verify output format
3. Call `ping_device` with `8.8.8.8` → Check actual ping
4. List resources → Should show 3 resources
5. Read `network://devices/inventory` → Verify JSON structure

</v-clicks>

---

# Add Error Handling

<v-clicks>

```python
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Execute tool with error handling"""
    
    logger.info(f"Tool call: {name} with args: {arguments}")
    
    try:
        if name == "ping_device":
            target = arguments["target"]
            
            # Validate target
            if not target or len(target) > 253:
                raise ValueError("Invalid target hostname/IP")
            
            # Execute ping
            result = subprocess.run(
                ["ping", "-c", str(arguments.get("count", 4)), target],
                capture_output=True,
                text=True,
                timeout=15
            )
            
            logger.info(f"Ping result: {result.returncode}")
            return [TextContent(type="text", text=result.stdout)]
            
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return [TextContent(type="text", text=f"Validation error: {str(e)}")]
    except Exception as e:
        logger.exception(f"Unexpected error in {name}")
        return [TextContent(type="text", text=f"Error: {str(e)}")]
```

</v-clicks>

---

# Challenge: Add Real SSH Tool

<v-clicks>

```python
# Install netmiko
# pip install netmiko

from netmiko import ConnectHandler

Tool(
    name="execute_command",
    description="Execute a show command on a network device via SSH",
    inputSchema={
        "type": "object",
        "properties": {
            "device": {"type": "string"},
            "command": {"type": "string", "description": "Command to execute (show commands only)"},
            "username": {"type": "string"},
            "password": {"type": "string"}
        },
        "required": ["device", "command", "username", "password"]
    }
)

# In call_tool():
elif name == "execute_command":
    # Validate: only allow show commands
    if not arguments["command"].startswith("show"):
        raise ValueError("Only 'show' commands are allowed")
    
    device_config = {
        "device_type": "cisco_ios",
        "host": arguments["device"],
        "username": arguments["username"],
        "password": arguments["password"],
    }
    
    with ConnectHandler(**device_config) as conn:
        output = conn.send_command(arguments["command"])
    
    return [TextContent(type="text", text=output)]
```

</v-clicks>

---

# Production Considerations

<v-clicks>

### 1. Security

```python
# Never log sensitive data
logger.info(f"Tool: {name}, Device: {arguments.get('device')}")  # OK
logger.info(f"Args: {arguments}")  # BAD - may contain passwords

# Use environment variables for credentials
import os
SSH_USERNAME = os.getenv("NETWORK_SSH_USER")
SSH_PASSWORD = os.getenv("NETWORK_SSH_PASS")
```

### 2. Rate Limiting

```python
from datetime import datetime, timedelta

# Simple rate limiter
last_calls = {}

def rate_limit(key, max_calls=10, window=60):
    now = datetime.now()
    if key not in last_calls:
        last_calls[key] = []
    
    # Remove old calls outside window
    last_calls[key] = [t for t in last_calls[key] if now - t < timedelta(seconds=window)]
    
    if len(last_calls[key]) >= max_calls:
        raise Exception(f"Rate limit exceeded: {max_calls} calls per {window}s")
    
    last_calls[key].append(now)
```

</v-clicks>

---

# Production Considerations (cont.)

<v-clicks>

### 3. Caching

```python
from functools import lru_cache
from datetime import datetime, timedelta

# Cache device inventory for 5 minutes
inventory_cache = {"data": None, "timestamp": None}

@app.read_resource()
async def read_resource(uri: str) -> str:
    if uri == "network://devices/inventory":
        now = datetime.now()
        
        # Check cache
        if inventory_cache["data"] and \
           now - inventory_cache["timestamp"] < timedelta(minutes=5):
            logger.info("Returning cached inventory")
            return inventory_cache["data"]
        
        # Fetch fresh data
        inventory = fetch_inventory_from_netbox()
        
        # Update cache
        inventory_cache["data"] = json.dumps(inventory, indent=2)
        inventory_cache["timestamp"] = now
        
        return inventory_cache["data"]
```

</v-clicks>

---

# Lab 5 Takeaways

<v-clicks>

### What You Built

✅ Working MCP server with tools and resources  
✅ Error handling and logging  
✅ Tested with MCP inspector  
✅ Ready for Claude Desktop integration  

### Key Lessons

- **MCP servers are async** - Use `async`/`await`
- **stdio transport** - Read from stdin, write to stdout
- **Tools vs. resources** - Actions vs. read-only data
- **Testing is critical** - Use inspector before production

### Next Lab

**Wire this MCP server to the chatbot** from Lab 4

</v-clicks>

---
layout: center
class: text-center
---

# Module 10

## Lab 6: Wire MCP → Chatbot

15 minutes

---

# Lab 6 Overview

<v-clicks>

### Goal

Connect the MCP server (Lab 5) to the chatbot (Labs 3/4)

### Architecture

```
User Input
    ↓
Chatbot (Python)
    ↓
LLM API (decides to call tools)
    ↓
MCP Client → MCP Server (Lab 5)
    ↓
Tool execution (SSH, ping, etc.)
    ↓
Results → LLM → Final answer → User
```

**Time: 15 minutes**

</v-clicks>

---

# Setup MCP Client

<v-clicks>

```python
# chatbot_with_mcp.py
import asyncio, requests
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3.2:3b"

class MCPChatbot:
    def __init__(self):
        self.conversation_history = []
        self.mcp_session = None
        self.available_tools = []
    
    async def connect_to_mcp_server(self, server_script_path):
        """Connect to an MCP server"""
        
        # Define how to start the MCP server
        server_params = StdioServerParameters(
            command="python",
            args=[server_script_path],
            env=None
        )
        
        # Start server and create client session
        stdio_transport = await stdio_client(server_params)
        self.mcp_session = ClientSession(*stdio_transport)
        
        # Initialize session
        await self.mcp_session.initialize()
        
        print(f"✅ Connected to MCP server: {server_script_path}")
```

</v-clicks>

---

# Load Tools from MCP

<v-clicks>

```python
    async def connect_to_mcp_server(self, server_script_path):
        # ... (previous code)
        
        # Get available tools from MCP server
        tools_response = await self.mcp_session.list_tools()
        
        # Convert MCP tools to Anthropic format
        self.available_tools = [
            {
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.inputSchema
            }
            for tool in tools_response.tools
        ]
        
        print(f"📦 Loaded {len(self.available_tools)} tools:")
        for tool in self.available_tools:
            print(f"  - {tool['name']}: {tool['description'][:60]}...")
    
    async def get_resources(self):
        """List available resources"""
        resources_response = await self.mcp_session.list_resources()
        return [
            {
                "uri": r.uri,
                "name": r.name,
                "description": r.description
            }
            for r in resources_response.resources
        ]
```

</v-clicks>

---

# Implement Chat with MCP Tools

<v-clicks>

```python
    async def chat(self, user_message):
        """Chat with MCP tool support"""

        # Add user message
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })

        # Agentic loop
        while True:
            # Call Ollama with MCP tools
            response = requests.post(OLLAMA_URL, json={
                "model": MODEL,
                "messages": self.conversation_history,
                "tools": self.available_tools,
                "stream": False
            }).json()

            msg = response["message"]
            tool_calls = msg.get("tool_calls") or []

            if not tool_calls:
                # Final answer
                self.conversation_history.append(msg)
                return msg.get("content", "")
```

</v-clicks>

---

# Handle MCP Tool Calls

<v-clicks>

```python
            if tool_calls:
                # LLM wants to call MCP tools
                self.conversation_history.append(msg)
                
                # Execute each tool via MCP
                tool_results = []
                for block in response.content:
                    if block.type == "tool_use":
                        print(f"🔧 Calling MCP tool: {block.name}({block.input})")
                        
                        # Call the MCP server
                        result = await self.mcp_session.call_tool(
                            block.name,
                            block.input
                        )
                        
                        # Extract text from result
                        result_text = ""
                        for content in result.content:
                            if hasattr(content, 'text'):
                                result_text += content.text
                        
                        print(f"✅ Result: {result_text[:100]}...")
                        
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": result_text
                        })
                
                # Send results back to LLM
                self.conversation_history.append({
                    "role": "user",
                    "content": tool_results
                })
                # Loop continues
```

</v-clicks>

---

# Usage Example

<v-clicks>

```python
async def main():
    # Create chatbot
    bot = MCPChatbot()
    
    # Connect to MCP server from Lab 5
    await bot.connect_to_mcp_server("../network-mcp-server/server.py")
    
    # Show available resources
    resources = await bot.get_resources()
    print("\n📚 Available resources:")
    for r in resources:
        print(f"  - {r['name']}: {r['description']}")
    
    print("\n" + "="*60)
    print("💬 Network Assistant Ready!")
    print("="*60 + "\n")
    
    # Test queries
    queries = [
        "Can you ping 8.8.8.8 and tell me if it's reachable?",
        "Check the status of GigabitEthernet0/1 on RTR-CORE-01",
        "What devices are in our inventory?",
        "Show me the BGP summary for RTR-CORE-01"
    ]
    
    for query in queries:
        print(f"\n👤 User: {query}")
        response = await bot.chat(query)
        print(f"\n🤖 Assistant: {response}\n")
        print("-" * 60)

if __name__ == "__main__":
    asyncio.run(main())
```

</v-clicks>

---

# Build Interactive CLI

<v-clicks>

```python
# interactive_mcp_chat.py
import asyncio
from chatbot_with_mcp import MCPChatbot

async def run_chat_loop():
    bot = MCPChatbot()
    
    print("🔌 Connecting to MCP server...")
    await bot.connect_to_mcp_server("../network-mcp-server/server.py")
    
    print("\n💬 Network Assistant Ready!")
    print("Commands: /resources, /quit\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input == "/quit":
                print("👋 Goodbye!")
                break
            
            elif user_input == "/resources":
                resources = await bot.get_resources()
                print("\n📚 Available resources:")
                for r in resources:
                    print(f"  - {r['name']}")
                    print(f"    URI: {r['uri']}")
                    print(f"    {r['description']}\n")
                continue
            
            # Normal chat
            response = await bot.chat(user_input)
            print(f"\nAssistant: {response}\n")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")

if __name__ == "__main__":
    asyncio.run(run_chat_loop())
```

</v-clicks>

---
---
layout: section
---

# Module 6: Production Deployment

Moving from Workshop to Real Networks

---

# Production Migration Path

<v-clicks>

## Workshop → Production

**Mock Devices (Workshop):**
```python
from examples.mock_network_devices import get_device_status

status = get_device_status("spine1")
```

**Real Devices (Production):**
```python
import paramiko

def get_device_status(device_ip):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(device_ip, username="admin", password=...)
    
    stdin, stdout, stderr = ssh.exec_command("show version | json")
    result = json.loads(stdout.read())
    ssh.close()
    return result
```

**Your agent code stays the same!** Just swap the backend function.

</v-clicks>

---

# Production Best Practices

<v-clicks>

## Error Handling

```python
def get_device_status(device, retries=3):
    for attempt in range(retries):
        try:
            # SSH connection
            result = execute_ssh_command(device, "show version")
            return result
        except paramiko.SSHException as e:
            if attempt < retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
                continue
            else:
                return {"error": f"SSH failed after {retries} attempts: {e}"}
        except Exception as e:
            return {"error": f"Unexpected error: {e}"}
```

**Always:**
- Implement retries with backoff
- Handle SSH exceptions gracefully
- Log all errors
- Return structured error responses

</v-clicks>

---

# Security Considerations

<v-clicks>

## Credential Management

**❌ Never do this:**
```python
password = "admin123"  # Hardcoded!
```

**✅ Do this:**
```python
import os
from getpass import getpass

# Environment variables
username = os.getenv("NETWORK_USERNAME")
password = os.getenv("NETWORK_PASSWORD")

# Or use a secrets manager
from vault_client import get_secret
credentials = get_secret("network/credentials")
```

**Best practices:**
- Use SSH keys instead of passwords
- Leverage secrets management (HashiCorp Vault, AWS Secrets Manager)
- Implement role-based access control (RBAC)
- Audit all network operations

</v-clicks>

---

# Scaling Your Agent

<v-clicks>

## From Single Device to Fleet

**Sequential (Slow):**
```python
results = []
for device in devices:
    status = get_device_status(device)
    results.append(status)
```

**Parallel (Fast):**
```python
import asyncio

async def check_all_devices(devices):
    tasks = [check_device(device) for device in devices]
    return await asyncio.gather(*tasks)

# Check 100 devices in parallel
results = asyncio.run(check_all_devices(device_list))
```

**Key benefit:** Check entire data center in seconds instead of minutes

</v-clicks>

---

# Testing Scenarios

<v-clicks>

## Test Your Agent Like Production

**Scenario 1: Network Partition**
```python
# Simulate: Half of devices unreachable
mock_unreachable = ["spine1", "leaf1"]
```

**Scenario 2: Partial Failures**
```python
# Simulate: Some commands timeout
mock_slow_devices = {"leaf2": 5.0}  # 5 second delay
```

**Scenario 3: Bad Data**
```python
# Simulate: Malformed responses
mock_corrupted_output = {"device": "leaf3", "corrupt": True}
```

**Always test:**
- Network failures
- Timeouts and retries
- Malformed data
- Edge cases

</v-clicks>

---

# Observability

<v-clicks>

## Monitor Your Agent

```python
import logging
import prometheus_client as prom

# Metrics
tool_calls = prom.Counter('agent_tool_calls_total', 
                          'Total tool calls', 
                          ['tool_name', 'status'])
tool_duration = prom.Histogram('agent_tool_duration_seconds',
                               'Tool execution time')

class MonitoredAgent:
    @tool_duration.time()
    def execute_tool(self, tool_name, args):
        try:
            result = self.tools[tool_name](**args)
            tool_calls.labels(tool_name=tool_name, status='success').inc()
            return result
        except Exception as e:
            tool_calls.labels(tool_name=tool_name, status='error').inc()
            logging.error(f"Tool {tool_name} failed: {e}")
            raise
```

**Track:**
- Tool call frequency
- Success/failure rates
- Response times
- Error patterns

</v-clicks>

---
layout: section
---

# Wrap-Up & Next Steps

What You've Learned & Where to Go

---

# What We Covered Today

<v-clicks>

## Module 1: LLM Fundamentals
- Tokenization and context windows
- Temperature and sampling
- Why local models work great

## Module 2: Prompt Engineering
- P.E.N.E. framework
- Production prompt patterns
- Systematic iteration

## Module 3: LLM APIs
- Ollama API basics
- Building conversation memory
- Managing context

## Module 4: Agentic Patterns
- Tool calling with structured prompts
- Multi-step reasoning
- Autonomous troubleshooting

## Module 5: MCP Integration (Optional)
- Tool standardization
- Cross-application reuse

## Module 6: Production Path
- Migration strategy
- Best practices
- Scaling and observability

</v-clicks>

---

# Key Takeaways

<v-clicks>

## 1. 100% Free with Ollama
- No API keys required
- Runs entirely on your laptop
- Privacy-first architecture

## 2. Agents Are Code + LLM + Tools
```
Agent = Code Logic + LLM Reasoning + Tool Execution
```

## 3. Start Simple, Then Scale
- Begin with mock devices
- Test thoroughly
- Migrate to production incrementally

## 4. Tool Calling is Just Structured Prompts
- LLM outputs commands
- You parse and execute
- Feed results back
- **You understand the full loop!**

## 5. The Pattern Works Everywhere
- Same code works with any LLM
- Swap Ollama → Claude → GPT with 1 line
- Patterns are universal

</v-clicks>

---

# Your Next Steps

<v-clicks>

## Immediate (This Week)

1. **Run all 4 labs** on your network topology
2. **Customize tools** for your environment
3. **Test edge cases** (failures, timeouts)
4. **Deploy to dev network** (non-production)

## Short Term (This Month)

1. **Add more tools** (config generation, compliance checks)
2. **Implement logging** and observability
3. **Build test suite** with real scenarios
4. **Document your agent** for teammates

## Long Term (This Quarter)

1. **Production deployment** with proper auth
2. **Multi-agent orchestration** (different specialists)
3. **Integration with SOAR** platforms
4. **Share your learnings** with the community

</v-clicks>

---

# Resources

<v-clicks>

## Workshop Materials

- **GitHub:** github.com/sifbaksh/ai-networking-workshop
- **Full slides:** Available in repo
- **All lab code:** 100% free with Ollama
- **Mock devices:** Included

## Ollama

- **Docs:** ollama.com/docs
- **Models:** ollama.com/library
- **Discord:** ollama.com/discord

## Further Learning

- **LangChain:** langchain.com (multi-agent frameworks)
- **MCP:** modelcontextprotocol.io
- **Network Automation:** networktocode.com
- **Nornir:** nornir.tech

## Follow Along

- **Blog:** sifbaksh.com
- **LinkedIn:** linkedin.com/in/sifbaksh

</v-clicks>

---

# Common Questions

<v-clicks>

**Q: Can I use Claude/GPT instead of Ollama?**  
A: Yes! Same patterns work. Just swap the API client (1 line change).

**Q: How do I handle authentication?**  
A: SSH keys + secrets manager (Vault, AWS Secrets). Never hardcode credentials.

**Q: What about network devices without APIs?**  
A: Screen scraping with Netmiko/Paramiko + regex parsing. Works fine!

**Q: Can agents modify configurations?**  
A: Yes, but implement approval workflows. Never let agents auto-commit changes.

**Q: How do I prevent agents from breaking things?**  
A: Read-only tools first. Test extensively. Require human approval for writes.

**Q: What about rate limiting?**  
A: Ollama has no limits. For paid APIs, implement request queuing.

**Q: Can multiple agents work together?**  
A: Yes! Use message passing or shared state (Redis, database).

</v-clicks>

---
layout: center
class: text-center
---

# Thank You! 🎉

<div class="text-2xl mt-8">
  Questions?
</div>

<div class="mt-12 text-lg opacity-75">
  <p>Workshop: AI Networking - From LLMs to Production Agents</p>
  <p class="text-sm mt-4">100% Free with Ollama | No API Keys Required</p>
  <p class="text-sm">All materials: github.com/sifbaksh/ai-networking-workshop</p>
</div>

<div class="mt-12">
  <p class="text-sm">Created by Sif Baksh | March 31, 2026</p>
  <p class="text-sm">sifbaksh.com | @sifbaksh</p>
</div>

---
layout: center
class: text-center
---

# 🎊 Congratulations! 🎊

<div class="text-3xl font-bold mt-12">
You're Now an AI Agent Builder!
</div>

<div class="text-xl mt-8 opacity-75">
Go build something amazing! 🚀
</div>

<div class="mt-12 text-sm">
📧 Questions? Reach out anytime!<br>
💬 Share what you build - we'd love to see it!<br>
⭐ Star the repo if this was helpful!
</div>