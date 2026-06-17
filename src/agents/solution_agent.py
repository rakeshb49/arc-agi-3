# src/agents/solution_agent.py
import os
import sys
from typing import Any, Optional

# Ensure the official local framework copy is in the Python path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../ARC-AGI-3-Agents"))
)

# Import type declarations and the base class directly from the framework
from agents.agent import Agent
from arcengine import FrameData, GameAction, GameState

# Import the custom 2D grid representation utility implemented in Step 2
from utils.grid_parsers import ARCGrid


class AdvancedReasoningAgent(Agent):
    def __init__(
        self, config: Optional[dict[str, Any]] = None, *args: Any, **kwargs: Any
    ) -> None:
        """
        Initializes the agent. Accepts *args and **kwargs to allow the
        official Swarm orchestrator to pass telemetry hooks smoothly.
        """
        super().__init__(*args, **kwargs)
        # Store your custom model parameters or search space limits
        self.config = config or {}

    def is_done(self, frames: list[FrameData], latest_frame: FrameData) -> bool:
        """
        Decide if the agent should stop playing or not.
        Returning True early stops the action loop to maximize efficiency scores.
        """
        # Baseline check: Stop immediately if a WIN or GAME_OVER state is encountered
        if latest_frame.state in [GameState.WIN, GameState.GAME_OVER]:
            return True

        # Example early-stopping check to protect your efficiency penalty score
        if len(frames) > self.config.get("max_steps_allowed", 60):
            return True

        return False

    def choose_action(
        self, frames: list[FrameData], latest_frame: FrameData
    ) -> GameAction:
        """
        Main step function mapping the grid to an action space.
        Returns an explicit GameAction enum wrapper.
        """
        # Framework rule: If the environment hasn't started or has crashed, reset it
        if latest_frame.state in [GameState.NOT_PLAYED, GameState.GAME_OVER]:
            return GameAction.RESET

        # --- Step 3: Environment Input Parsing ---
        # Parse the 64x64 grid state list of lists into our Rigid 2D Grid Engine
        grid_env = ARCGrid(latest_frame.frame)

        # Track the valid operational action tokens provided by the interactive environment
        allowed_actions = latest_frame.available_actions

        # --- Your Custom Neuro-Symbolic / Search Engine Placement ---
        # Use grid_env properties (e.g., grid_env.matrix, grid_env.unique_colors)
        # to reason over the current state and choose an action from allowed_actions.

        # Default fallback heuristic action selection (e.g., ACTION1)
        chosen_action = GameAction.ACTION1

        # Optional: Attach reasoning strings for logging and AgentOps tracking
        chosen_action.reasoning = (
            f"Parsed 2D grid of size {grid_env.height}x{grid_env.width}. "
            f"Detected unique colors: {grid_env.unique_colors}. Executing action fallback."
        )

        # If executing coordinate-based transformations (ACTION6 requiring x,y)
        if chosen_action.is_complex():
            # Coordinate system defaults to (0,0) top-left based on competition spec
            chosen_action.set_data({"x": 0, "y": 0})

        return chosen_action
