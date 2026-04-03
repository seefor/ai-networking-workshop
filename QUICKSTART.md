# Quick Start Guide
## Get Running in 5 Minutes

This guide gets you from zero to running your first lab in 5 minutes.

## Prerequisites

- macOS (or Linux/Windows)
- 15 minutes of time
- Internet connection

## Installation

### 1. Install Ollama (2 min)

```bash
# macOS
brew install ollama

# Or download from https://ollama.com/download
```

### 2. Pull Model (2 min)

```bash
ollama pull llama3.2:3b
```

### 3. Clone Repository (1 min)

```bash
git clone https://github.com/sifbaksh/ai-networking-workshop.git
cd ai-networking-workshop
pip3 install -r requirements.txt
```

## Run Your First Lab

```bash
# Test Ollama
python3 labs/lab1-ollama/simple_ollama_test.py
```

Expected output:
```
🤖 Ollama API Test - AI Networking Workshop
==================================================

📝 Test 1: Simple Chat
Response: OSPF is a link-state routing protocol...
```

## What's Next?

### Without API Key (Free)
- ✅ Lab 1: Ollama basics
- ✅ Lab 2: Prompt engineering

### With API Key ($1-5)
- Lab 3: Network chatbot
- Lab 4: Agentic bot (the star!)

Get API key: https://console.anthropic.com/

```bash
export ANTHROPIC_API_KEY=sk-ant-your-key
python3 labs/lab3-chatbot/chatbot_v2_with_memory.py
```

## Troubleshooting

**Ollama not connecting?**
```bash
ollama serve
```

**Import errors?**
```bash
pip3 install -r requirements.txt --upgrade
```

**Need help?**
- Run: `python3 examples/test_setup.py`
- Check: `docs/SETUP_GUIDE.md`
- Open: GitHub Issue

## Skip to the Good Stuff

Want to see the agent in action?

```bash
# Set API key
export ANTHROPIC_API_KEY=your-key

# Jump to Lab 4 (star lab)
cd labs/lab4-agentic
python3 agentic_network_bot.py
```

This runs an autonomous AI agent that troubleshoots a mock network!

---

**Full setup guide:** `docs/SETUP_GUIDE.md`  
**Workshop outline:** `docs/COMPLETE_WORKSHOP_OUTLINE.md`
