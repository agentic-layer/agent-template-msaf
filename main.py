import os

from agent_framework import Agent
from agent_framework_openai import OpenAIChatCompletionClient
from agenticlayer.msaf import create_metrics_middleware
from agenticlayer.msaf.agent_to_a2a import to_a2a
from agenticlayer.msaf.otel import setup_otel
from agenticlayer.shared.config import parse_sub_agents, parse_tools
from dotenv import load_dotenv

from loguru_config import setup_logging

# Load environment variables from .env file
load_dotenv()

# Set up logging
setup_logging()

if os.environ.get("AGENT_OTEL_ENABLED", "true").lower() == "true":
    setup_otel()

# The agent url is needed for the agent card to tell other agents how to reach this agent.
# We can only guess the host and port here, as it may be set differently by Uvicorn at runtime.
# If running in k8s or similar, the host and port may also be different.
port = os.environ.get("UVICORN_PORT", 8000)

app = to_a2a(
    agent=Agent(
        client=OpenAIChatCompletionClient(
            model=os.environ.get("AGENT_MODEL", "gemini-2.5-flash"),
            base_url=os.environ.get("LITELLM_PROXY_API_BASE"),
            api_key=os.environ.get("LITELLM_PROXY_API_KEY"),
        ),
        name=os.environ.get("AGENT_NAME", "root_agent"),
        instructions=os.environ.get("AGENT_INSTRUCTION", ""),
        middleware=create_metrics_middleware(),
    ),
    name=os.environ.get("AGENT_NAME", "root_agent"),
    description=os.environ.get("AGENT_DESCRIPTION", ""),
    rpc_url=os.environ.get("AGENT_A2A_RPC_URL", f"http://localhost:{port}"),
    sub_agents=parse_sub_agents(os.environ.get("SUB_AGENTS", "{}")),
    tools=parse_tools(os.environ.get("AGENT_TOOLS", "{}")),
)
