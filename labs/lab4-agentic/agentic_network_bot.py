#!/usr/bin/env python3
"""
Lab 4: Agentic Network Bot with Real Device Integration
AI Networking Workshop - macOS Compatible

This lab demonstrates how to build an AI agent that can autonomously
query and operate network devices using tool calling.

The agent can:
- Check device status
- Query BGP neighbors
- Check interface status
- Execute show commands
- Make multi-step decisions autonomously
"""

import os
import json
from typing import Dict, List
import anthropic

# Import our mock network devices
from mock_network_devices import (
    get_device_status,
    get_interface_status,
    get_bgp_summary,
    ping_device,
    execute_command,
    get_topology_info,
    MockNetworkDevice
)


class AgenticNetworkBot:
    """
    An AI agent that can autonomously operate network devices.
    
    Features:
    - Autonomous decision making
    - Multi-step problem solving
    - Tool calling for device interaction
    - Conversation memory
    """
    
    def __init__(self, api_key: str = None):
        """
        Initialize the agentic network bot.
        
        Args:
            api_key: Anthropic API key (or use ANTHROPIC_API_KEY env var)
        """
        if api_key is None:
            api_key = os.getenv("ANTHROPIC_API_KEY")
        
        if not api_key:
            raise ValueError(
                "No API key provided. Set ANTHROPIC_API_KEY environment variable"
            )
        
        self.client = anthropic.Anthropic(api_key=api_key)
        self.conversation_history: List[Dict] = []
        
        # Map tool names to Python functions
        self.tools_map = {
            "get_device_status": get_device_status,
            "get_interface_status": get_interface_status,
            "get_bgp_summary": get_bgp_summary,
            "ping_device": ping_device,
            "execute_command": execute_command,
            "get_topology_info": get_topology_info
        }
        
        # Define tool schemas for the LLM
        self.tools = [
            {
                "name": "get_device_status",
                "description": "Get operational status of a network device (version, uptime, role)",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "device": {
                            "type": "string",
                            "description": "Device hostname (spine1, spine2, leaf1, or leaf2)"
                        }
                    },
                    "required": ["device"]
                }
            },
            {
                "name": "get_interface_status",
                "description": "Get status of network interfaces on a device",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "device": {
                            "type": "string",
                            "description": "Device hostname"
                        },
                        "interface": {
                            "type": "string",
                            "description": "Specific interface name (optional, returns all if not specified)"
                        }
                    },
                    "required": ["device"]
                }
            },
            {
                "name": "get_bgp_summary",
                "description": "Get BGP neighbor summary from a device",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "device": {
                            "type": "string",
                            "description": "Device hostname"
                        }
                    },
                    "required": ["device"]
                }
            },
            {
                "name": "ping_device",
                "description": "Ping a network device to check reachability",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "target": {
                            "type": "string",
                            "description": "Device hostname or IP address"
                        },
                        "count": {
                            "type": "integer",
                            "description": "Number of ping packets (default 4)",
                            "default": 4
                        }
                    },
                    "required": ["target"]
                }
            },
            {
                "name": "execute_command",
                "description": "Execute a show command on a device (read-only, show commands only)",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "device": {
                            "type": "string",
                            "description": "Device hostname"
                        },
                        "command": {
                            "type": "string",
                            "description": "Show command to execute (e.g., 'show version')"
                        }
                    },
                    "required": ["device", "command"]
                }
            },
            {
                "name": "get_topology_info",
                "description": "Get information about the network topology structure",
                "input_schema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        ]
        
        # System prompt defines the agent's role and context
        self.system_prompt = f"""You are an expert network engineer assistant working with a spine-leaf Arista cEOS network topology.

Available devices in the lab:
- spine1 (192.168.0.11) - Core spine switch
- spine2 (192.168.0.12) - Core spine switch  
- leaf1 (192.168.0.21) - Leaf/access switch
- leaf2 (192.168.0.22) - Leaf/access switch

Network design:
- 2-spine, 2-leaf topology
- BGP underlay (eBGP between tiers)
- Each leaf connects to both spines
- Spines are interconnected

You have tools to:
- Check device status (uptime, version, role)
- Query BGP neighbors and session state
- Check interface status
- Ping devices
- Execute show commands
- Get topology information

When troubleshooting:
1. Gather information systematically
2. Check multiple devices if needed
3. Correlate data across the topology
4. Provide clear, actionable insights

Be concise and technical. Focus on facts from device output."""
    
    def chat(self, user_message: str, verbose: bool = True) -> str:
        """
        Send a message and let the agent autonomously solve the problem.
        
        Args:
            user_message: User's question or instruction
            verbose: Print tool calls as they happen
        
        Returns:
            Agent's final response
        """
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # Agentic loop - agent can call tools multiple times
        while True:
            # Call LLM with tools
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=4096,
                system=self.system_prompt,
                tools=self.tools,
                messages=self.conversation_history
            )
            
            # Check what the LLM wants to do
            if response.stop_reason == "end_turn":
                # Agent is done - has final answer
                final_text = self._extract_text(response.content)
                
                # Add to history
                self.conversation_history.append({
                    "role": "assistant",
                    "content": response.content
                })
                
                return final_text
            
            elif response.stop_reason == "tool_use":
                # Agent wants to call tools
                self.conversation_history.append({
                    "role": "assistant",
                    "content": response.content
                })
                
                # Execute all requested tools
                tool_results = []
                
                for block in response.content:
                    if block.type == "tool_use":
                        tool_name = block.name
                        tool_input = block.input
                        
                        if verbose:
                            print(f"\n🔧 Agent calling: {tool_name}({json.dumps(tool_input, indent=2)})")
                        
                        # Execute the tool
                        try:
                            tool_func = self.tools_map[tool_name]
                            result = tool_func(**tool_input)
                            
                            if verbose:
                                print(f"✅ Result: {json.dumps(result, indent=2)}")
                            
                            tool_results.append({
                                "type": "tool_result",
                                "tool_use_id": block.id,
                                "content": json.dumps(result)
                            })
                        
                        except Exception as e:
                            if verbose:
                                print(f"❌ Error: {e}")
                            
                            tool_results.append({
                                "type": "tool_result",
                                "tool_use_id": block.id,
                                "content": json.dumps({"error": str(e)}),
                                "is_error": True
                            })
                
                # Send tool results back to the agent
                self.conversation_history.append({
                    "role": "user",
                    "content": tool_results
                })
                
                # Loop continues - agent will process results and either:
                # 1. Call more tools, OR
                # 2. Provide final answer
    
    def _extract_text(self, content) -> str:
        """Extract text from response content blocks."""
        for block in content:
            if hasattr(block, 'text'):
                return block.text
        return ""
    
    def reset(self):
        """Clear conversation history."""
        self.conversation_history = []


# =============================================================================
# DEMO & TEST SCENARIOS
# =============================================================================

def demo_simple_query():
    """Demo 1: Simple device query"""
    print("\n" + "="*70)
    print("DEMO 1: Simple Device Query")
    print("="*70)
    
    bot = AgenticNetworkBot()
    
    response = bot.chat("What's the status of spine1?")
    
    print("\n📝 Agent Response:")
    print("-"*70)
    print(response)


def demo_multi_device_query():
    """Demo 2: Query across multiple devices"""
    print("\n" + "="*70)
    print("DEMO 2: Multi-Device Query (Autonomous)")
    print("="*70)
    
    bot = AgenticNetworkBot()
    
    response = bot.chat("Are all BGP sessions up in the network?")
    
    print("\n📝 Agent Response:")
    print("-"*70)
    print(response)


def demo_troubleshooting():
    """Demo 3: Multi-step troubleshooting"""
    print("\n" + "="*70)
    print("DEMO 3: Troubleshooting (Multi-Step Reasoning)")
    print("="*70)
    
    bot = AgenticNetworkBot()
    
    response = bot.chat(
        "I notice leaf2 has an interface down. "
        "Can you investigate and tell me which interface and what it connects to?"
    )
    
    print("\n📝 Agent Response:")
    print("-"*70)
    print(response)


def demo_topology_analysis():
    """Demo 4: Topology analysis"""
    print("\n" + "="*70)
    print("DEMO 4: Topology Analysis")
    print("="*70)
    
    bot = AgenticNetworkBot()
    
    response = bot.chat(
        "Which device has the most BGP peers and why?"
    )
    
    print("\n📝 Agent Response:")
    print("-"*70)
    print(response)


def interactive_mode():
    """Interactive chat with the agent"""
    print("\n" + "="*70)
    print("🤖 Interactive Agentic Network Bot")
    print("="*70)
    print("\nAvailable devices: spine1, spine2, leaf1, leaf2")
    print("Type 'quit' to exit, 'reset' to clear history\n")
    print("="*70)
    
    bot = AgenticNetworkBot()
    
    while True:
        try:
            user_input = input("\n👤 You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if user_input.lower() == 'reset':
                bot.reset()
                print("🔄 Conversation reset")
                continue
            
            # Let the agent respond
            print()  # Blank line for tool output
            response = bot.chat(user_input, verbose=True)
            
            print(f"\n🤖 Agent: {response}")
        
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


# =============================================================================
# CHALLENGES
# =============================================================================

def challenge_1():
    """
    Challenge 1: Device Inventory
    
    Goal: Ask the agent to create a device inventory report with
    hostname, role, version, and uptime for all devices.
    
    Expected: Agent should call get_device_status() for all 4 devices
    """
    print("\n" + "="*70)
    print("CHALLENGE 1: Device Inventory Report")
    print("="*70)
    
    bot = AgenticNetworkBot()
    
    response = bot.chat(
        "Create a device inventory report for all devices in the topology. "
        "Include hostname, role, software version, and uptime."
    )
    
    print("\n📝 Agent Response:")
    print("-"*70)
    print(response)


def challenge_2():
    """
    Challenge 2: BGP Health Check
    
    Goal: Full BGP health assessment across the topology
    
    Expected: Agent should check BGP on all devices and correlate results
    """
    print("\n" + "="*70)
    print("CHALLENGE 2: BGP Health Check")
    print("="*70)
    
    bot = AgenticNetworkBot()
    
    response = bot.chat(
        "Perform a complete BGP health check. Tell me if any sessions are down "
        "and which devices are affected."
    )
    
    print("\n📝 Agent Response:")
    print("-"*70)
    print(response)


def challenge_3():
    """
    Challenge 3: Find the Problem
    
    Goal: Identify which device has an issue and what it is
    
    Expected: Agent should systematically check devices and find leaf2 Ethernet3 is down
    """
    print("\n" + "="*70)
    print("CHALLENGE 3: Find the Problem")
    print("="*70)
    
    bot = AgenticNetworkBot()
    
    response = bot.chat(
        "Something is wrong with one of the devices. "
        "Can you investigate and tell me what the issue is?"
    )
    
    print("\n📝 Agent Response:")
    print("-"*70)
    print(response)


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    # Check for API key
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("="*70)
        print("⚠️  ANTHROPIC_API_KEY not set")
        print("="*70)
        print("\nTo run this lab:")
        print("1. Get API key from https://console.anthropic.com/")
        print("2. Set it: export ANTHROPIC_API_KEY=your-key-here")
        print("3. Run this script again")
        print("\nOr use the mock device simulator directly:")
        print("  python mock_network_devices.py")
        print("="*70)
    else:
        # Run demos
        print("\n🎯 Lab 4: Agentic Network Bot")
        print("="*70)
        print("\nThis lab demonstrates an AI agent that can autonomously")
        print("operate network devices using tool calling.")
        print("="*70)
        
        # Uncomment demos you want to run:
        
        demo_simple_query()
        # demo_multi_device_query()
        # demo_troubleshooting()
        # demo_topology_analysis()
        
        # Or run interactive mode:
        # interactive_mode()
        
        # Or try the challenges:
        # challenge_1()
        # challenge_2()
        # challenge_3()
        
        print("\n" + "="*70)
        print("✅ Lab 4 Complete!")
        print("="*70)
        print("\n💡 Key Takeaways:")
        print("  1. Agents can autonomously decide which tools to call")
        print("  2. Multi-step reasoning enables complex troubleshooting")
        print("  3. Tool calling connects LLMs to real infrastructure")
        print("  4. Same code works with real devices (just change the tool functions)")
        print("="*70)
