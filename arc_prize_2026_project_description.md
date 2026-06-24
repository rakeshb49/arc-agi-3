# ARC Prize 2026 - ARC-AGI-3
**Create an AI capable of fluid intelligence**

## Overview
Build systems that learn and adapt to novel, human-solvable tasks they’ve never seen before and advance AI’s ability to learn new skills efficiently.

*   **Start Date:** March 25, 2026
*   **Close Date:** 5 months to go (as of June 2026)
*   **Status:** Featured Code Competition

---

### Description
*Note: there are three active competitions for ARC in 2026: this competition, [ARC-AGI-2](https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-2/overview), and a [paper track](https://www.kaggle.com/competitions/arc-prize-2026-paper-track), where you can document your approach for either one of the prediction competitions.*

Real intelligence isn’t about memorizing answers - it’s knowing what to do when the problem changes. Today’s AI systems excel at what they were trained to do, but often fall short when something unfamiliar comes along. Most benchmarks reward pattern recognition, not genuine problem-solving.

ARC Prize Foundation focuses on true generalization: whether a system can quickly learn new skills in unfamiliar situations. Instead of rewarding pattern recognition on known tasks, it evaluates how well systems can adapt to new problems they’ve never encountered before. The ARC-AGI-3 evaluation environment is designed so systems can't just memorize solutions. Tasks take place in hidden, interactive environments that require exploration and multi-step reasoning.

In this competition, you’ll build AI systems that adapt on the fly to new tasks in the ARC environment, and develop approaches that learn quickly, generalize well, and solve problems never seen before.

Your solution could help move AI closer to systems that learn the way people do: flexible, efficient, and able to handle new challenges.

The real test of intelligence begins when the problem changes.

---

### Evaluation
Scores for individual game range from 0 to 100%. A score of 100% represents an agent matching human-level performance, meaning it beat every game while matching the number of actions humans took. While an agent could theoretically exceed 100% by using fewer moves, scores are capped at 100%. The final score averages individual game scores across levels. Read more at the [ARC-AGI-3 Scoring Methodology page](https://docs.arcprize.org/methodology).

### Submission File
Submission files are automatically calculated. As long as the agent takes action on *any* of the games, a submission file for all of the games is created.

---

### Timeline
*   **March 25, 2026** - Start Date.
*   **October 26, 2026** - Entry Deadline. You must accept the competition rules before this date in order to compete.
*   **October 26, 2026** - Team Merger Deadline. This is the last day participants may join or merge teams.
*   **November 2, 2026** - Final Submission Deadline.
*   **December 4, 2026** - Winners announcement.

All deadlines are at 11:59 PM UTC on the corresponding day unless otherwise noted. The competition organizers reserve the right to update the contest timeline if they deem it necessary.

---

### Code Requirements
Submissions to this competition must be made through Notebooks. In order for the "Submit" button to be active after a commit, the following conditions must be met:
*   CPU/GPU Notebook <= 9 hours run-time
*   Internet access disabled
*   Freely & publicly available external data is allowed, including pre-trained models
*   Submission file will be automatically generated.

### Upgraded Accelerators
NVIDIA RTX PRO 6000 GPU (`g4-standard-48`) is available for this competition.

---

### Citation
Francois Chollet, Mike Knoop, Greg Kamradt, David Wexler, Derek Smith, Hunter Henry, Walter Reade, and María Cruz. ARC Prize 2026 - ARC-AGI-3. https://kaggle.com/competitions/arc-prize-2026-arc-agi-3, 2026. Kaggle.

---

## Dataset Description
ARC-AGI-3 is an **Interactive Reasoning Benchmark** designed to measure an AI agent's ability to generalize in novel, unseen environments. Unlike traditional static benchmarks used to evaluate LLMs and reasoning systems, ARC-AGI-3 evaluates frontier AI agent systems on exploration, memory, goal acquisition, and alignment.

Full documentation: [docs.arcprize.org](https://docs.arcprize.org/)

### Games (Environments)
ARC-AGI-3 consists of **hand-crafted interactive environments** that test abstraction and reasoning. Each game presents a unique challenge that your agent must explore, understand, and solve.

#### How Games Work
*   Your agent receives **frames** — JSON objects containing the current game state and metadata.
*   Each frame includes a **grid** (max 64×64) with integer cell values 0–15 representing different states/colors, using a (0,0) top-left coordinate system.
*   Your agent responds with **actions** to interact with the environment.
*   Each game has multiple **levels** of increasing difficulty.
*   A game can be in one of three states: NOT_FINISHED, WIN, or GAME_OVER.

#### Available Actions
Agents interact with environments using up to 7 actions:
| Action | Description |
| :--- | :--- |
| `RESET` | Start or restart the game |
| `ACTION1` – `ACTION5` | Simple actions (e.g., move up/down/left/right, interact) |
| `ACTION6` | Complex action requiring `(x, y)` coordinates |
| `ACTION7` | Additional simple action |

Each game defines which actions are available and what they do. The meaning of actions varies per game — your agent must figure out what each action does through exploration.

#### Public Games
A set of public games is available for development and practice at arcprize.org. In addition, public game files are available in the environment_files folder on this page.

*Note: Competition evaluation uses a **separate, private set of 110 games** that your agent has never seen. Half of these are used for the Public Leaderboard score, and the other half for the Private Leaderboard score.*

---

### Scoring
AI agents are scored on **two criteria**:

1. **Completion** — How many levels did the agent complete in each game?
2. **Efficiency** — How many actions did the agent take to complete each level, compared to a human baseline?

#### Scoring Method
* For each level completed, the agent's action count is compared to a human baseline (first-time test-testers).
* **Per-level score** = min(human_actions / agent_actions, 1.0), then **squared** (a raw score of 0.5 becomes 0.25).
* **Per-game score** = Weighted average of level scores (weighted by level index, 1-indexed).
* **Total score** = Average of all individual game scores.
* Final output is a score between **0%–100%**.

---

### ARC-AGI Toolkit
The [`arc-agi`](https://github.com/arcprize/arc-agi) Python package provides the core toolkit for interacting with ARC-AGI-3 environments.

### Building Agents
The [`ARC-AGI-3-Agents`](https://github.com/arcprize/ARC-AGI-3-Agents) repository provides the framework for building and running agents.

#### Agent Architecture
An agent plays ARC-AGI-3 by implementing two core methods:
*   **is_done(frames, latest_frame)** — Decide if the agent should stop playing
*   **choose_action(frames, latest_frame)** — Choose which action to take given the current game state

A **Swarm** orchestrates multiple agent instances across all available games in parallel.

#### Agent Lifecycle
1. Get the list of available games from the API
2. Open a scorecard (tracks performance)
3. For each game, RESET to start, then take actions based on the agent's strategy
4. Close the scorecard when all games are complete

---

### Files
*   **ARC-AGI-3-Agents/**: a local copy of the [ARC-AGI-3-Agents repo](https://github.com/arcprize/ARC-AGI-3-Agents).
*   **arc_agi_3_wheels/**: package wheels for the installing [ARC-AGI-3](https://github.com/arcprize/ARC-AGI-3).
*   **environment_files/**: location of the 25 public game files

**Total Size:** 48.97 MB (148 files)
**License:** [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0)

---

### [ARC-AGI-3 Preview Agent Competition](https://arcprize.org/blog/arc-agi-3-preview-30-day-learnings)
The winning solution from the 2025 Preview would score close to 0% in the current ARC Prize 2026 track.

The preview was a sandbox designed to catch exactly the kinds of shortcuts the 2025 winner used. Here is what changed and why the old meta is dead.

#### What Changed in ARC Prize 2026

The 2026 launch introduced strict countermeasures against brute-force solving and fundamentally changed the scoring math:

* **Massive Scale Increase:** The 2025 preview evaluated agents on just 3 hidden games. The 2026 competition evaluates agents against **110 hidden games**, demanding true cross-game generalization rather than narrow adaptation.
* **Anti-Brute-Force Design:** The ARC team noted in their post-mortem that the 2025 preview games were too friendly to random search. The 2026 environments are specifically designed to trap, penalize, or fail agents that rely on mindless trial-and-error.
* **Power-Law Scoring:** This is the most lethal change. In 2026, the action efficiency ratio (Human Actions / Agent Actions) is **squared**. Under a linear model, an agent taking 10x the actions of a human still gets 10% credit. Under the power-law model, taking massive amounts of exploratory actions drives the per-level score to near zero almost instantly.

#### Why the 2025 Winner Fails Today

The 2025 Preview was won by Dries Smit with an agent called **StochasticGoose**. It achieved a 12.58% score by completing 18 levels across the 3 hidden games.

StochasticGoose was effectively a highly optimized "Smart Random" reinforcement learning algorithm using a Convolutional Neural Network (CNN). It brute-forced the state space by permanently storing frame transitions in memory to avoid repeating useless moves.

It would fail the 2026 gauntlet for three reasons:

1. **Catastrophic Action Bloat:** StochasticGoose took over **255,000 actions** to solve those 18 levels. Because of the new power-law scoring math, taking 255,000 actions on levels that humans solve in roughly 500 actions guarantees a score fraction so small it effectively rounds to zero.
2. **Kaggle Compute Limits:** To brute-force the games, StochasticGoose relied on hashing and storing massive amounts of frame data in memory. The 2026 Kaggle evaluation environment runs strictly offline with tight memory limits and aggressive execution timeouts. Agents that attempt infinite-loop random exploration are rapidly hit with `SIGKILL` terminations.
3. **Lack of Semantic Understanding:** StochasticGoose didn't actually "understand" the rules of the games; it just mapped state transitions until it stumbled into a win state.
