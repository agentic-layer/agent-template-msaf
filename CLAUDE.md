# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

**For general usage instructions, Docker examples, and environment configuration:**

@./README.md

## Architecture Overview

### Core Components
- **main.py**: Entry point that creates and configures the root agent using the Microsoft Agent Framework (MSAF)
- **Agent Configuration**: The root agent is configured via environment variables and supports:
  - Dynamic sub-agent loading from URL-based agent cards
  - MCP (Model Context Protocol) toolset integration
  - OpenAI-compatible model integration via LiteLLM proxy

### Agent System Design
- **Root Agent**: Main agent created with `Agent()` class from `agent_framework`
- **Sub-Agents**: Remote A2A (Agent-to-Agent) agents loaded from environment configuration
- **Tools**: MCP toolsets that provide external functionality via HTTP connections
- **Model Integration**: Uses OpenAI-compatible clients supporting various LLM providers via gateway

### Configuration Pattern
The application uses a JSON-based configuration system through environment variables:
- `SUB_AGENTS`: Maps agent names to configuration objects with URLs
- `AGENT_TOOLS`: Maps tool names to configuration objects with connection parameters
- Both configurations are parsed from JSON and have error handling for invalid JSON

### Deployment
- Multi-stage Docker build using Python 3.14 with uv for dependency management
- Exposes port 8000 by default
- Supports multi-platform builds (linux/arm64, linux/amd64)

### Dependencies
- **agentic-layer-sdk-msaf**: Core MSAF functionality for agent creation
- **agent-framework**: Microsoft Agent Framework
- **uvicorn**: ASGI server for serving the agent API
- **OpenAI-compatible gateway**: Model abstraction layer (e.g. LiteLLM proxy)
- **MCP integration**: For external tool connectivity

The codebase follows a template pattern for creating configurable agents that can be extended with sub-agents and tools through environment configuration rather than code changes.
