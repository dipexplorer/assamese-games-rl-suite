## ROADMAP

Current Phase: PHASE 1 — GAME RESEARCH AND RULE DISCOVERY

==================================================
PHASE 1 — Game Discovery + Rule Research      [CURRENT]
==================================================
[ ] Confirm the 5 target Assamese traditional games
[ ] Create a structured research profile for each game
[ ] Collect and record sources for each game
[ ] Classify all rules: [VERIFIED / SUPPORTED / INFERRED /
    ENGINEERING DECISION / UNKNOWN]
[ ] Complete evidence matrix for Kori Khel
[ ] Document unresolved questions for each game

==================================================
PHASE 2 — Source Verification + Variant Resolution
==================================================
[ ] Cross-reference multiple sources per game
[ ] Identify regional variants for each game
[ ] Maintain separate variant documents
[ ] Resolve or explicitly flag conflicts

==================================================
PHASE 3 — Formal Game Specification
==================================================
[ ] For each game, write a formal_spec.md answering:
    - What is the state?
    - What is observable?
    - Who acts?
    - What actions are legal / illegal?
    - What is the transition?
    - Where does randomness occur?
    - What ends the game?
    - What constitutes a win / loss / draw?

==================================================
PHASE 4 — Pure Game Engine
==================================================
[ ] Implement board, state, players, pieces, turns
[ ] Implement move validation
[ ] Implement transitions, scoring, termination
[ ] Game engine works independently of any RL framework

==================================================
PHASE 5 — Game Engine Validation
==================================================
[ ] Unit tests for every verified rule
[ ] Random-play simulations
[ ] Confirm no impossible game states are produced

==================================================
PHASE 6 — Gymnasium Environment
==================================================
[ ] Define observation_space and action_space
[ ] Implement reset(), step()
[ ] Define reward, terminated, truncated, info
[ ] Pass gymnasium.utils.env_checker

==================================================
PHASE 7 — Baseline Agents
==================================================
[ ] Random Agent
[ ] Rule-Based Agent
[ ] Test against validated environment

==================================================
PHASE 8 — RL Algorithm Selection
==================================================
[ ] Analyze action space, observation space, stochasticity
[ ] Evaluate PPO, DQN, SAC and other candidates
[ ] Justify algorithm choice with reasoning

==================================================
PHASE 9 — RL Training
==================================================
[ ] Train selected algorithm
[ ] Log: seed, hyperparameters, steps, metrics
[ ] Save checkpoints and training curves

==================================================
PHASE 10 — Evaluation
==================================================
[ ] Evaluate trained agent vs Random Agent
[ ] Evaluate trained agent vs Rule-Based Agent
[ ] Record win rates, episode lengths, reward curves

==================================================
PHASE 11 — Visualization
==================================================
[ ] 2D renderer for the game board
[ ] Training result graphs

==================================================
PHASE 12 — Cross-Game Analysis
==================================================
[ ] Compare RL learning across all implemented games
[ ] Investigate whether game structure affects learning

==================================================
PHASE 13 — Research Paper / Final Report
==================================================
[ ] Write IndoML 2026 abstract (Deadline: 15 Sep 2026)
[ ] Write full Final Year Project report
[ ] Final presentation
