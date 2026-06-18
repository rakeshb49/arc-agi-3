# ruff: noqa: E402
import argparse
import json
import logging
import os
import signal
import sys
import threading
from functools import partial
from pathlib import Path
from types import FrameType
from typing import Optional

import requests
from dotenv import load_dotenv

APP_DIR = Path(__file__).resolve().parent
PRESET_ARC_API_KEY = os.environ.get("ARC_API_KEY")

load_dotenv(dotenv_path=APP_DIR / ".env.example")
load_dotenv(dotenv_path=APP_DIR / ".env", override=True)

if PRESET_ARC_API_KEY:
    os.environ["ARC_API_KEY"] = PRESET_ARC_API_KEY
if os.environ.get("ARC_BASE_URL"):
    os.environ["ARC_BASE_URL"] = os.environ["ARC_BASE_URL"].rstrip("/")
if os.environ.get("ARC_API_KEY") == "your_arc_api_key_here":
    os.environ.pop("ARC_API_KEY")

# -------------------------------------------------------------------------
# Dynamic Environment Guard: Probe connection to see if we are offline.
# -------------------------------------------------------------------------
logger = logging.getLogger()
IS_ONLINE = True

try:
    # Quick low-timeout ping to verify if the official server is reachable
    requests.get("https://three.arcprize.org", timeout=3)
except requests.exceptions.RequestException:
    IS_ONLINE = False

if not IS_ONLINE:
    if not os.environ.get("ARC_API_KEY"):
        os.environ["ARC_API_KEY"] = "offline_evaluation_placeholder"
    if not os.environ.get("ONLINE_ONLY"):
        os.environ["ONLINE_ONLY"] = "False"
elif os.environ.get("ARC_API_KEY"):
    os.environ.setdefault("ONLINE_ONLY", "True")
    os.environ.setdefault("OPERATION_MODE", "online")
    os.environ.setdefault("SCHEME", "https")
    os.environ.setdefault("HOST", "three.arcprize.org")
    os.environ.setdefault("PORT", "443")
# -------------------------------------------------------------------------

from agents import AVAILABLE_AGENTS, Swarm
from agents.tracing import initialize as init_agentops

SCHEME = os.environ.get("SCHEME", "http")
HOST = os.environ.get("HOST", "localhost")
PORT = os.environ.get("PORT", 8001)

# Hide standard ports in URL
if (SCHEME == "http" and str(PORT) == "80") or (
    SCHEME == "https" and str(PORT) == "443"
):
    ROOT_URL = f"{SCHEME}://{HOST}"
else:
    ROOT_URL = f"{SCHEME}://{HOST}:{PORT}"
HEADERS = {
    "X-API-Key": os.getenv("ARC_API_KEY", ""),
    "Accept": "application/json",
}


def run_agent(swarm: Swarm) -> None:
    swarm.main()
    os.kill(os.getpid(), signal.SIGINT)


def cleanup(
    swarm: Swarm,
    signum: Optional[int],
    frame: Optional[FrameType],
) -> None:
    logger.info("Received SIGINT, exiting...")
    card_id = swarm.card_id
    if card_id:
        scorecard = swarm.close_scorecard(card_id)
        if scorecard:
            logger.info("--- EXISTING SCORECARD REPORT ---")
            logger.info(json.dumps(scorecard.model_dump(), indent=2))
            swarm.cleanup(scorecard)

        # Provide web link to scorecard
        if card_id:
            scorecard_url = f"{ROOT_URL}/scorecards/{card_id}"
            logger.info(f"View your scorecard online: {scorecard_url}")

    sys.exit(0)


def main() -> None:
    log_level = logging.INFO
    if os.environ.get("DEBUG", "False") == "True":
        log_level = logging.DEBUG

    logger.setLevel(log_level)
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(log_level)
    stdout_handler.setFormatter(formatter)

    file_handler = logging.FileHandler("logs.log", mode="w")
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stdout_handler)

    if not IS_ONLINE:
        logger.info(
            "Offline environment detected. Enabled automated local framework fallback triggers."
        )

    parser = argparse.ArgumentParser(description="ARC-AGI-3-Agents")
    parser.add_argument(
        "-a",
        "--agent",
        choices=AVAILABLE_AGENTS.keys(),
        help="Choose which agent to run.",
    )
    parser.add_argument(
        "-g",
        "--game",
        help="Choose a specific game_id for the agent to play. If none specified, an agent swarm will play all available games.",
    )
    parser.add_argument(
        "-t",
        "--tags",
        type=str,
        help="Comma-separated list of tags for the scorecard (e.g., 'experiment,v1.0')",
        default=None,
    )

    args = parser.parse_args()

    if not args.agent:
        logger.error("An Agent must be specified")
        return

    print(f"{ROOT_URL}/api/games")

    # Get the list of games from the API
    full_games = []
    try:
        with requests.Session() as session:
            session.headers.update(HEADERS)
            r = session.get(f"{ROOT_URL}/api/games", timeout=10)

        if r.status_code == 200:
            try:
                full_games = [g["game_id"] for g in r.json()]
            except (ValueError, KeyError) as e:
                logger.error(f"Failed to parse games response: {e}")
                logger.error(f"Response content: {r.text[:200]}")
        else:
            logger.error(
                f"API request failed with status {r.status_code}: {r.text[:200]}"
            )

    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to connect to API server: {e}")

    # For playback agents, we can derive the game from the recording filename
    if not full_games and args.agent and args.agent.endswith(".recording.jsonl"):
        from agents.recorder import Recorder

        game_prefix = Recorder.get_prefix_one(args.agent)
        full_games = [game_prefix]
        logger.info(
            f"Using game '{game_prefix}' derived from playback recording filename"
        )

    # -------------------------------------------------------------------------
    # Offline Fallback Engine
    # When isolated from the API server, seed games from arguments or datasets
    # -------------------------------------------------------------------------
    if not full_games:
        if args.game:
            full_games = args.game.split(",")
            logger.info(
                f"Offline Mode: Seeded game indices from CLI parameters: {full_games}"
            )
        else:
            env_dir = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "../environment_files")
            )
            if os.path.exists(env_dir):
                full_games = [
                    os.path.splitext(f)[0]
                    for f in os.listdir(env_dir)
                    if f.endswith(".json")
                ]
                logger.info(
                    f"Offline Mode: Detected {len(full_games)} local game frames inside environment_files/"
                )
    # -------------------------------------------------------------------------

    games = full_games[:]
    if args.game:
        filters = args.game.split(",")
        games = [
            gid
            for gid in full_games
            if any(gid.startswith(prefix) for prefix in filters)
        ]

    logger.info(f"Game list: {games}")

    if not games:
        if full_games:
            logger.error(
                f"The specified game '{args.game}' does not exist or is not available with your API key. Please try a different game."
            )
        else:
            logger.error(
                "No games available to play. Check API connection or recording file."
            )
        return

    # Start with Empty tags, "agent" and agent name will be added by the Swarm later
    tags: list[str] = []

    # Append user-provided tags if any
    if args.tags:
        user_tags = [tag.strip() for tag in args.tags.split(",")]
        tags.extend(user_tags)

    # Initialize AgentOps client
    init_agentops(api_key=os.getenv("AGENTOPS_API_KEY"), log_level=log_level)

    swarm = Swarm(
        args.agent,
        ROOT_URL,
        games,
        tags=tags,
    )
    agent_thread = threading.Thread(target=partial(run_agent, swarm))
    agent_thread.daemon = True  # die when the main thread dies
    agent_thread.start()

    signal.signal(signal.SIGINT, partial(cleanup, swarm))  # handler for Ctrl+C

    try:
        while agent_thread.is_alive():
            agent_thread.join(timeout=5)  # Check every 5 seconds
    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt received in main thread")
        cleanup(swarm, signal.SIGINT, None)
    except Exception as e:
        logger.error(f"Unexpected error in main thread: {e}")
        cleanup(swarm, None, None)


if __name__ == "__main__":
    os.environ["TESTING"] = "False"
    main()
