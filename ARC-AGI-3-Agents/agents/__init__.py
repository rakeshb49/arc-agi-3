# ARC-AGI-3-Agents/agents/__init__.py
import os
import sys
from typing import Type, cast

from dotenv import load_dotenv

# Import only the absolute core framework classes
from .agent import Agent, Playback
from .recorder import Recorder
from .swarm import Swarm

# Inject BOTH paths:
# 1. 'src/' so that solution_agent can find 'utils.grid_parsers'
# 2. 'src/agents/' so we can import solution_agent directly without namespace conflicts
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src/agents"))
)

# Import directly from the file name to avoid shadowing the framework's 'agents' package
from solution_agent import AdvancedReasoningAgent

load_dotenv()

# Build the baseline dictionary dynamically using registered subclasses
AVAILABLE_AGENTS: dict[str, Type[Agent]] = {
    cls.__name__.lower(): cast(Type[Agent], cls)
    for cls in Agent.__subclasses__()
    if cls.__name__ != "Playback"
}

# Explicitly inject your clean snake_case command line key
AVAILABLE_AGENTS["advanced_reasoning"] = AdvancedReasoningAgent

# Add all the recording files as valid agent names
for rec in Recorder.list():
    AVAILABLE_AGENTS[rec] = Playback

__all__ = [
    "Swarm",
    "Agent",
    "Recorder",
    "Playback",
    "AVAILABLE_AGENTS",
    "AdvancedReasoningAgent",
]
