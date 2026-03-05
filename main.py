import os

from agent_framework import Agent
from agenticlayer.config import parse_sub_agents, parse_tools
from agenticlayer.msaf.agent_to_a2a import to_a2a
from agenticlayer.msaf.client import create_openai_client
from agenticlayer.msaf.otel import setup_otel
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
        client=create_openai_client(
            model_id=os.environ.get("AGENT_MODEL"),
        ),
        name=os.environ.get("AGENT_NAME", "root_agent"),
        instructions=os.environ.get("AGENT_INSTRUCTION", ""),
    ),
    name=os.environ.get("AGENT_NAME", "root_agent"),
    description=os.environ.get("AGENT_DESCRIPTION", ""),
    rpc_url=os.environ.get("AGENT_A2A_RPC_URL", f"http://localhost:{port}"),
    sub_agents=parse_sub_agents(os.environ.get("SUB_AGENTS", "{}")),
    tools=parse_tools(os.environ.get("AGENT_TOOLS", "{}")),
)
