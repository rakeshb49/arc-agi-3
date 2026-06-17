# Repository Architecture & Core Mechanics

## Target Challenge
- All code generation must align with the parameters defined in the `arc_prize_2026_project_description.md` file.
- Refer to `arc_prize_2026_project_description.md` verbatim for details on interactive game loops, 64x64 grid tracking, valid action vocabularies, and squared-efficiency scoring metrics.

## Development Constraints
- **Zero Local Execution**: The local machine and Jules's temporary cloud VMs lack runtime execution compute and environment dependencies. Never attempt to execute `main.py` or run training loops locally. Treat the local workspace strictly as a read/write environment for static files.
- **Dependency Isolation**: Missing package errors on a local machine (e.g., `langsmith`, `langgraph`) are expected, normal, and must be ignored. Do not introduce verbose try-except hacks to bypass them. Code verification occurs exclusively on the remote RTX 6000 compute node.
- **Deployment Protocol**: Code sync is purely Git-driven. No custom sync scripts or local transport daemons are permitted. Changes must be committed and pushed to GitHub locally, then pulled or cloned down on the remote cluster for verification execution.
- **Modularity & Base Class**: Custom solutions must exclusively inherit from the official `Agent` base class located inside `ARC-AGI-3-Agents/agents/agent.py`. Custom logic belongs completely inside `src/agents/solution_agent.py`. Avoid editing internal template files or baseline orchestrator structures.

# Google Jules Operational Manual

## Framework Dependencies
- `ARC-AGI-3-Agents/` is the official repository code provided by the competition organizers. Treat this directory as read-only, except for the explicit registration hook.
- **Registration Protocol**: To introduce our agent to the Swarm orchestrator, append the import path and the string key dictionary entry (`AVAILABLE_AGENTS["advanced_reasoning"] = AdvancedReasoningAgent`) to the *absolute bottom* of `ARC-AGI-3-Agents/agents/__init__.py`. Do not alter any other lines in the initialization block.
- `environment_files/` contains the 25 static public game configurations. Use them strictly as mock structural reference maps for designing 2D spatial grid transformation matrices.

## Development Strategy
- **Framework Ingestion**: To implement our solution, import `Agent` from `agents.agent` alongside the typed state wrappers `FrameData`, `GameAction`, and `GameState` from the core binary backend `arcengine`.
- **Interface Implementation**: Implement your logic inside `src/agents/solution_agent.py` by adhering to the explicit framework signatures:
  - `is_done(frames: list[FrameData], latest_frame: FrameData) -> bool`
  - `choose_action(frames: list[FrameData], latest_frame: FrameData) -> GameAction`
- **Action Type Strictness**: The `choose_action` function must always return a valid `GameAction` enum instance (such as `GameAction.ACTION1` or `GameAction.RESET`). Returning raw python strings (e.g., `"ACTION1"`) is invalid and will cause runtime execution failures.
