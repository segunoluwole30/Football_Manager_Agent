# Autonomous Tactics Agent for Football Manager 2024

## Overview
This repository contains the source code for an autonomous tactical decision-making agent for Football Manager 2024. Built without the luxury of an open API, this agent utilizes a combination of Large Language Model (LLM) reasoning, Vision-Language Model (VLM) screenshot interpretation, and simulated GUI interactions to act as an automated football manager. 

The system analyzes your team's squad depth, attributes, and opponent scouting reports to intelligently generate and apply tactical presets, formations, and mentalities directly in-game.

## Key Features
* **Vision-Based Data Pipeline:** Utilizes GPT-4 Vision to capture in-game screenshots (like Squad Planners and Scouting Reports) and extract structured textual data.
* **Centralized Orchestrator:** An autonomous controller script manages the entire lifecycle, from taking screenshots to physically applying tactics in the game interface.
* **Structured Tactical Reasoning:** A robust prompt-engineering framework acts as a "Tactical Analyst," ensuring the agent only selects valid tactical combinations recognized by the game engine (e.g., ensuring selected formations match a chosen pressing style).
* **Hardcoded UI Navigation:** Uses precise, resolution-specific (1920x1080) hardcoded coordinates for reliable GUI navigation, bypassing the unreliability of purely visual grounding models in low-contrast interfaces.

## System Architecture
The agent operates through a sequential, 4-phase pipeline managed by a central orchestrator:

* **Phase 1: Visual Data Collection:** Automatically navigates the FM24 interface and captures screenshots of the Squad Overview, Squad Planner, and Opponent Scouting Report using `pyautogui`.
* **Phase 2: Analysis:** Images are batched and processed by GPT-4 Vision (`opponent_image_extractor.py`) to generate raw text. The text is then summarized into compact tactical briefs (`summarize_team_report.py`).
* **Phase 3: Reasoning:** The `strategy_reasoning.py` module evaluates the tactical briefs to formulate a game plan. It outputs a strict JSON plan containing the chosen Formation, Tactical Preset (e.g., Gegenpress), and Mentality.
* **Phase 4: Execution:** The `apply_tactics.py` module parses the generated JSON plan and uses PyAutoGUI to simulate human mouse clicks, mapping them to the game interface to apply the tactics.

# Core Modules & Files
* `agent_main.py`: The main orchestrator script that runs the agent loop, handling conditional executions like "match-day mode" to skip redundant data gathering.
* `opponent_image_extractor.py`: Converts images to Base64 and interfaces with GPT-4 Vision to extract opponent key players, weaknesses, and depth.
* `strategy_reasoning.py`: Generates the tactical JSON plan and enforces logic to prevent hallucinated tactical combinations.
* `apply_tactics.py`: Executes the final tactical plan by translating it into physical mouse clicks.
* `ui_coordinates.py`: Contains a dictionary of hardcoded coordinate points mapped to a 1920x1080 screen resolution for reliable UI clicking.

## Performance & Evaluation
The agent was benchmarked against a human manager over 5 identical fixtures.

* **Expected Goals (xG):** The agent achieved a highly comparable xG to the human manager (1.93 vs 1.91), proving its capability to generate high-quality tactical scoring chances.
* **Points & Results:** While the agent slightly lagged behind the human in raw points (8 vs 13) and mean goals scored (0.8 vs 2.4), this was largely attributed to unlucky stochastic finishing events within the game engine rather than poor tactical creation.

## Limitations
* **Stochastic In-Game Events:** The agent operates strictly in the "Match Setup" phase. It currently cannot react to mid-game random events like red cards or injuries, which require complex drag-and-drop substitutions.
* **Cost Constraints:** Running the full pipeline costs roughly $0.29 per run. While manageable for match-day setups (approx $0.05 per run using cached team reports), full-season Monte Carlo simulations are prohibitively expensive due to API token usage.

## Future Work
* **Dynamic Coordinate OCR:** Upgrading from hardcoded GUI coordinates to an object detection model (like YOLO) to dynamically find UI buttons across different screen resolutions.
* **In-Match Feedback Loops:** Enabling the agent to read half-time scores and adapt tactics mid-match (e.g., switching to "Park the Bus" when defending a lead).

## Author
**Oluwasegun Oluwole** Texas A&M University  
Developed for CSCE 689: Programming Large Language Models 
