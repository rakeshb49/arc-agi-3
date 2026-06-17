import os
import sys
from typing import Type, cast

from dotenv import load_dotenv

from .agent import Agent, Playback
from .recorder import Recorder
from .swarm import Swarm
from .templates.langgraph_functional_agent import LangGraphFunc, LangGraphTextOnly
from .templates.langgraph_random_agent import LangGraphRandom
from .templates.langgraph_thinking import LangGraphThinking
from .templates.llm_agents import LLM, FastLLM, GuidedLLM, ReasoningLLM
from .templates.multimodal import MultiModalLLM
from .templates.random_agent import Random
from .templates.reasoning_agent import ReasoningAgent
from .templates.smolagents import SmolCodingAgent, SmolVisionAgent

# 1. Inject the local src directory path and import your agent first
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))
from agents.solution_agent import AdvancedReasoningAgent

load_dotenv()

# 2. Build the baseline dictionary dynamically using registered subclasses
AVAILABLE_AGENTS: dict[str, Type[Agent]] = {
    cls.__name__.lower(): cast(Type[Agent], cls)
    for cls in Agent.__subclasses__()
    if cls.__name__ != "Playback"
}

# 3. Explicitly inject your clean snake_case command line key
AVAILABLE_AGENTS["advanced_reasoning"] = AdvancedReasoningAgent

# 4. Add all the recording files as valid agent names
for rec in Recorder.list():
    AVAILABLE_AGENTS[rec] = Playback

# 5. Handle explicit template updates
AVAILABLE_AGENTS["reasoningagent"] = ReasoningAgent

__all__ = [
    "Swarm",
    "Random",
    "LangGraphFunc",
    "LangGraphTextOnly",
    "LangGraphThinking",
    "LangGraphRandom",
    "LLM",
    "FastLLM",
    "ReasoningLLM",
    "GuidedLLM",
    "ReasoningAgent",
    "SmolCodingAgent",
    "SmolVisionAgent",
    "Agent",
    "Recorder",
    "Playback",
    "AVAILABLE_AGENTS",
    "MultiModalLLM",
    "AdvancedReasoningAgent",  # Expose your agent cleanly in the module namespace
]
