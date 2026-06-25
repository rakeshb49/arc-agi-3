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
NVIDIA RTX PRO 6000 Blackwell GPU (`g4-standard-48`) is available for this competition. Final-inference hardware profile: **48 vCPUs; 96GB GDDR7 GPU memory**. Note this budget applies to **final inference only** (≤9h, internet disabled, single GPU); **training, experimentation, and testing are unconstrained** and must be performed offline ahead of submission.

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

> **RHAE consequence (load-bearing):** A level scores **0 unless completed**; once completed, every wasted or dead-end **live-board** action is punished **quadratically** via the Relative Human Action Efficiency formula $(\frac{\text{Human Actions}}{\text{AI Actions}})^2$. Completion is the gate; **live-action** efficiency is the squared multiplier. There is therefore **no acceptable "exploratory" live move** — probing the live API to learn a game (e.g., spending live actions to discover what `ACTION6` does) permanently caps that level's score before the real solution begins.

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

### ARC-AGI-3 Preview Findings: Architectural Primitives for 2026

The July–August 2025 Preview Competition (won by StochasticGoose at 12.58%) \[1\]\[2\] proved that scaling standard RL or injecting raw grid frames into LLMs fails due to sample inefficiency and context limits \[3\]. When the preview winner was later evaluated on the full 2026 benchmark, its score plummeted to 0.25% \[3\]. This drop-off cleanly isolates **patched exploits that MUST NOT be used (SCRAP)** from **optional priors that may be reused, refined, or superseded only if empirically best (KEEP)**.

#### 1\. The Perception Layer (KEEP — optional: 4-Layer CNN Vision Prior)

Frontier Vision-Language Models (VLMs) are too slow for the 9-hour Kaggle inference limits and struggle with precise spatial relationships. A strong perception **baseline** (not a mandate) is the CNN architecture from the preview \[2\]:

* **Input Representation:** 16-channel one-hot encoded frames (64x64 grids).  
* **Backbone:** A lightweight 4-layer CNN (32→64→128→256 channels).  
* **Advantage:** Fast inference, highly sample-efficient, and perfectly preserves the 2D spatial inductive biases of the grid environments.
* **Optionality:** Adopt, refine, or replace this only if it wins ablations. Actively research stronger alternatives (object-centric/slot encoders, GNNs over interaction graphs, neural cellular automata, learned-equivalence state abstraction).

#### 2\. The Action Filter (KEEP — optional: Binary Effect Prediction)

Training an agent directly on environment rewards (win/loss) fails due to long horizons. Instead, a perception model may be trained on a localized binary classification task \[2\]:

* **Objective:** Predict (state, action) \-\> frame\_changed.  
* **Application:** This acts as an **internal simulator**. The agent "imagines" interacting with a coordinate; if the model predicts no state change, the action is pruned from the search tree **inside the world model — never by probing the live board**.  
* **2026 Necessity:** Effect-based pruning is critical to survive the squared RHAE penalty, where dead-end **live** actions quadratically destroy your score: $(\frac{\text{Human Actions}}{\text{AI Actions}})^2$ \[4\].

#### 3\. State Space Compression (KEEP — optional: Heuristic Masking)

Raw frame hashing causes state-space explosions in ARC-AGI-3 (e.g., an in-game timer ticking every turn registers as a novel state, breaking experience buffers).

* **Implementation:** Build programmatic heuristic masks to detect and obscure status bars, timers, and non-interactive UI elements before state hashing.  
* **Buffer Management:** Enforce strict hash-based deduplication in your experience buffer to remain within Kaggle's memory and compute constraints \[2\].

#### 4\. Decision-Making (SCRAP — hard prohibition: Stochastic Sampling)

The fatal flaw of the preview agents—and why they failed the 2026 benchmark—was relying on sigmoid probabilities (Stochastic Sampling) to blindly pick from the pool of valid actions \[2\]. **The following are patched exploits and MUST NOT be used:**

* **Stochastic sigmoid action sampling / random walks** over valid actions.
* **Naive RL reward-scaling** on win/loss over long horizons.
* **Raw-grid-into-LLM/VLM** pipelines (sample-inefficient, context-limited, too slow for ≤9h).
* **Live-board epistemic foraging** — using the live evaluation API as a scientific testing ground (see the firewall below).

* **2026 Redesign:** Perception/effect models should only **identify** interactive nodes and build the graph of valid interactions; action **selection** must be handed to a **deterministic reasoning layer** (e.g., Monte Carlo Tree Search or inference-time compute via a reasoning LLM) capable of multi-step hypothesis testing and long-horizon planning \[3\].

#### 5\. Exploration Discipline (Latent-Space Exploration Firewall — mandatory)

Because RHAE squares **live-board** action counts, all curiosity-driven, hypothesis-testing exploration (Active Inference, intrinsic curiosity, count/novelty bonuses, epistemic-reward shaping) **MUST execute entirely inside the agent's internal simulated world model (in VRAM)** — built offline and updated only from **passively observed** frames at inference — and **NEVER on the live evaluation board**. The agent must deduce each game's action semantics, level structure, and win conditions **internally via simulated rollouts**, then emit **live** actions **only** when executing a mathematically verified solution trajectory. To the Kaggle scorer the agent must appear as a **near-zero-shot, flawless executor** whose live-action count approaches the human baseline (efficiency ratio → 1.0).

#### References

\[1\] ARC Prize Foundation. (2025). *ARC‑AGI‑3 Preview Agent Competition*. Retrieved from https://arcprize.org/competitions/arc-agi-3-preview-agents/archive

\[2\] Smit, D. (2025). *StochasticGoose: ARC-AGI-3 Developer Preview Agent Competition Submission*. GitHub. Retrieved from https://github.com/DriesSmit/ARC3-solution

\[3\] ARC Prize Foundation. (2026). *ARC-AGI-3: A New Challenge for Frontier Agentic Intelligence*. arXiv preprint arXiv:2603.24621. Retrieved from https://arxiv.org/abs/2603.24621

\[4\] ARC Prize Foundation. (2026). *ARC Prize 2026 \- ARC-AGI-3 Competition*. Retrieved from https://arcprize.org/competitions/2026/arc-agi-3
