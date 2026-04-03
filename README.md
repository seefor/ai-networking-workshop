# AI Networking Workshop: From LLMs to Production Agents

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![macOS Compatible](https://img.shields.io/badge/macOS-compatible-green.svg)]()

> **Build autonomous AI agents for network operations** - A hands-on workshop teaching network engineers to create production-ready AI systems from scratch.

## 🎯 Workshop Overview

**Duration:** 3.25 hours  
**Format:** Hands-on labs with live instruction  
**Level:** Intermediate network engineers  
**Platform:** 100% macOS compatible (no VM needed!)

### What Makes This Workshop Unique

While most AI workshops teach you to *use* AI tools like ChatGPT and GitHub Copilot, this workshop teaches you to **build AI agents from scratch**.

**You'll learn to:**
- ✅ Understand how LLMs actually work (tokens, context windows, temperature)
- ✅ Write production-quality prompts using systematic frameworks
- ✅ Build stateful chatbots with conversation memory
- ✅ Create autonomous agents with tool calling
- ✅ Deploy agents to network infrastructure

**Key Differentiator:** Focus on building, not just using. You'll create a complete autonomous network agent that can troubleshoot, investigate, and operate your network devices.

## 🚀 Quick Start

### Prerequisites

```bash
# Check your versions
python3 --version  # Need 3.10+
docker --version   # Optional
git --version

# Install Ollama (if not installed)
brew install ollama

# Pull LLM models
ollama pull llama3.2:3b
```

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/ai-networking-workshop.git
cd ai-networking-workshop

# Install Python dependencies
pip3 install -r requirements.txt

# Test the environment
python3 examples/test_setup.py

# Optional: Set API key for Labs 3-4
export ANTHROPIC_API_KEY=your-key-here
```

### Run Your First Lab

```bash
# Lab 1: Local LLM interaction
python3 labs/lab1-ollama/simple_ollama_test.py

# Lab 2: Prompt engineering
python3 labs/lab2-prompts/prompt_engineering_pene.py

# Lab 3: Network chatbot (requires API key)
python3 labs/lab3-chatbot/chatbot_v2_with_memory.py

# Lab 4: Agentic network bot (requires API key)
python3 labs/lab4-agentic/agentic_network_bot.py
```

## 📚 Workshop Structure

| Time | Module | Type | What You'll Build |
|------|--------|------|-------------------|
| 0:00 | Setup & Welcome | Intro | Environment verification |
| 0:10 | How LLMs Work | Theory | Mental models |
| 0:30 | **Lab 1:** Ollama | Hands-on | Local LLM queries |
| 0:45 | Prompt Engineering | Theory | P.E.N.E. framework |
| 1:00 | **Lab 2:** AI-Assisted Dev | Hands-on | Ansible playbooks |
| 1:25 | LLM APIs & Tool Calling | Theory | Function calling |
| 1:40 | **Lab 3:** Network Chatbot | Hands-on | Stateful bot |
| 2:05 | **BREAK** | — | 10 minutes |
| 2:15 | Agentic Patterns | Theory | Autonomous systems |
| 2:35 | **Lab 4:** Production Agent | Hands-on | 🌟 **Star Lab** |
| 3:10 | Production Path | Demo | Real deployment |
| 3:20 | Wrap-Up | Q&A | Next steps |

**Total:** 195 minutes (3.25 hours)

## 🌟 The Star Lab: Autonomous Network Agent

Lab 4 is where everything comes together. You'll build a complete AI agent that:

- **Autonomously investigates** network issues
- **Operates mock devices** (production-ready code)
- **Makes multi-step decisions** without hardcoded logic
- **Troubleshoots intelligently** using 6 network tools

**Mock Network Topology:**
```
spine1 (192.168.0.11) ─┬─ leaf1 (192.168.0.21)
                       └─ leaf2 (192.168.0.22)
spine2 (192.168.0.12) ─┘
```

**Example Query:**
```python
bot = AgenticNetworkBot()
bot.chat("Are all BGP sessions up in the network?")

# Agent autonomously:
# 1. Calls get_bgp_summary('spine1')
# 2. Calls get_bgp_summary('spine2')
# 3. Calls get_bgp_summary('leaf1')
# 4. Calls get_bgp_summary('leaf2')
# 5. Synthesizes: "Yes, all BGP sessions established except leaf2 to spine2..."
```

## 📖 Lab Details

### Lab 1: Ollama + Network Prompts (15 min)

Learn to use local LLMs for network tasks.

**Skills:**
- Call Ollama API from Python
- Generate structured JSON output
- Parse network device output

**Files:**
- `simple_ollama_test.py`
- `json_output_challenge.py`

---

### Lab 2: Prompt Engineering (25 min)

Master the P.E.N.E. framework for production prompts.

**P.E.N.E. Framework:**
- **P**ersona & **P**urpose
- **E**xamples
- k**N**owledge & co**N**straints
- **E**valuation

**Skills:**
- Config parser prompts
- Alert triage prompts
- Documentation generation
- Risk scoring

**Files:**
- `prompt_engineering_pene.py`
- `PROMPT_TEMPLATES.md` (5 production templates)

---

### Lab 3: Network Chatbot (25 min)

Build a stateful chatbot with conversation memory.

**Skills:**
- Maintain conversation history
- System prompts for network engineering
- Token counting and management
- Save/load conversations

**Files:**
- `chatbot_v1_stateless.py` (shows the problem)
- `chatbot_v2_with_memory.py` (complete solution)

---

### Lab 4: Agentic Network Bot (35 min) 🌟

Build an autonomous agent that operates network devices.

**Skills:**
- Tool calling and schemas
- Agentic loop architecture
- Multi-step reasoning
- Network device integration

**Available Tools:**
- `get_device_status()` - Device info
- `get_bgp_summary()` - BGP neighbors
- `get_interface_status()` - Interface state
- `ping_device()` - Reachability test
- `execute_command()` - Show commands
- `get_topology_info()` - Network structure

**Files:**
- `agentic_network_bot.py` - Complete agent
- `mock_network_devices.py` - Device simulator

---

## 🌐 Mock Network Devices

All labs use realistic mock devices that work on any OS (macOS, Windows, Linux).

**Why Mock Devices?**

❌ **Traditional Approach (Containerlab):**
- Requires Linux
- 60+ minute setup
- VM overhead
- 8GB+ RAM

✅ **Our Approach (Mock Devices):**
- Works on macOS natively
- 5 minute setup
- Minimal resources
- Focus on AI agent development

### Production Migration

**Workshop Code:**
```python
def get_device_status(device: str) -> dict:
    return MOCK_DEVICES.get(device)
```

**Production Code:**
```python
import paramiko

def get_device_status(device: str) -> dict:
    ssh = paramiko.SSHClient()
    ssh.connect(device, username='admin', key_filename='~/.ssh/id_rsa')
    stdin, stdout, stderr = ssh.exec_command('show version')
    return parse_output(stdout.read().decode())
```

**Agent code stays identical** - just swap the tool functions!

## 📦 Repository Structure

```
ai-networking-workshop/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── LICENSE                      # MIT License
│
├── docs/                        # Documentation
│   ├── COMPLETE_OUTLINE.md      # Full workshop outline
│   ├── SETUP_GUIDE.md           # Environment setup
│   └── TROUBLESHOOTING.md       # Common issues
│
├── labs/                        # All lab code
│   ├── lab1-ollama/
│   │   ├── simple_ollama_test.py
│   │   └── json_output_challenge.py
│   ├── lab2-prompts/
│   │   ├── prompt_engineering_pene.py
│   │   └── PROMPT_TEMPLATES.md
│   ├── lab3-chatbot/
│   │   ├── chatbot_v1_stateless.py
│   │   └── chatbot_v2_with_memory.py
│   └── lab4-agentic/
│       └── agentic_network_bot.py
│
├── examples/                    # Utilities and examples
│   ├── mock_network_devices.py  # Device simulator
│   ├── test_setup.py            # Environment test
│   └── production_examples/     # Real device code
│
└── solutions/                   # Reference solutions
    └── [completed lab code]
```

## 🎓 Learning Outcomes

After completing this workshop, you will:

✅ Understand LLM architecture (tokenization, context windows, parameters)  
✅ Write production-quality prompts using systematic frameworks  
✅ Build stateful chatbots with conversation memory  
✅ Create autonomous AI agents with tool calling  
✅ Deploy agents to network infrastructure  
✅ Recognize when to use AI vs. traditional automation  

## 💡 Key Concepts

### The P.E.N.E. Framework

Our systematic approach to prompt engineering:

- **P**ersona & **P**urpose - Define role and goal
- **E**xamples - Show input/output patterns
- k**N**owledge & co**N**straints - Provide context and limits
- **E**valuation - Test and iterate

### The Agentic Loop

```
User Query
   ↓
LLM decides which tools to call
   ↓
Execute tools (your code)
   ↓
Results back to LLM
   ↓
LLM synthesizes answer OR calls more tools
   ↓
Repeat until done
```

**Key Insight:** The LLM decides the investigation strategy, not hardcoded logic.

## 🔧 Requirements

### Software (Required)

- **Python 3.10+**
- **Ollama** - https://ollama.com/
- **Git**

### Software (Optional)

- **Docker Desktop** - For future advanced labs
- **VS Code** - Recommended editor

### API Keys (Optional)

- **Anthropic API** - For Labs 3-4 (or use Ollama)
  - Get key: https://console.anthropic.com/
  - Estimated cost: $1-5 for workshop

### Models

```bash
# Free local models (Ollama)
ollama pull llama3.2:3b      # Fast, good quality
ollama pull llama3.1:8b      # Slower, better quality
```

## 🚀 Beyond the Workshop

### Next Steps (Week 1)

- Experiment with different prompts
- Add custom tools to the agent
- Test with your own network data

### Production Deployment (Month 1-2)

1. Replace mock devices with SSH/API calls
2. Add authentication and authorization
3. Implement audit logging
4. Add approval workflows for risky operations
5. Deploy as internal service

### Advanced Projects

- Multi-agent systems (specialized agents)
- SOAR platform integration
- Autonomous monitoring and alerting
- Configuration compliance checking

## 📚 Resources

### Documentation

- [Complete Workshop Outline](docs/COMPLETE_OUTLINE.md)
- [Setup Guide](docs/SETUP_GUIDE.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)

### External Resources

- [MCP Specification](https://modelcontextprotocol.io/)
- [Anthropic Documentation](https://docs.anthropic.com/)
- [Ollama Documentation](https://ollama.com/)

### Community

- Workshop Discord: [link]
- GitHub Discussions: [link]
- Office Hours: [schedule]

## 🤝 Contributing

We welcome contributions! Please see:

- Issues for bug reports and feature requests
- Pull requests for code improvements
- Discussions for questions and ideas

**Areas where we'd love help:**
- Additional network tools
- Real device integration examples
- Custom prompt templates
- Production deployment patterns

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Anthropic for Claude and MCP
- Ollama community
- Workshop participants and contributors

## 💬 Questions?

- **Issues:** [GitHub Issues](https://github.com/yourusername/ai-networking-workshop/issues)
- **Discussions:** [GitHub Discussions](https://github.com/yourusername/ai-networking-workshop/discussions)
- **Email:** your-email@example.com
- **LinkedIn:** [Your Profile](https://linkedin.com/in/sifbaksh)

---

**Workshop Date:** March 31, 2026  
**Version:** 2.0 (macOS Compatible)  
**Status:** ✅ Ready for delivery

**Built for network engineers who want to BUILD AI agents, not just USE AI tools.**
