# Assamese Traditional Games Reinforcement Learning Suite

An open-source suite of OpenAI Gymnasium environments and baseline RL algorithms for traditional indigenous games native to Assam, India.

---

## Overview

Traditional games often feature unique board layouts, random dice rolls, and strict entry rules that make them great testbeds for Reinforcement Learning (RL). 

This project aims to build RL environments for traditional Assamese games. **Kori Khel** is the first game released in this suite, with more games planned.

### Game 1: Kori Khel (`KoriKhelEnv-v0`)

Kori Khel is a 4-player board game played with 6 cowrie shells. The shells act as dice: each shell lands face-up or face-down with a 50% chance, determining how many steps a player can move.

- **Board Layout**: The board is mapped to a 73-position track for each player (Base at position 0, main perimeter from 1 to 64, home corridor from 65 to 72, and Goal at 73).
- **Entry Constraint**: Tokens start at Base (position 0) and can only enter the board when the player rolls a **Jagowa** (a roll value of 10, achieved when 5 shells land open and 1 lands closed).
- **30-Feature Observation Vector**: The environment provides 30 state features to the agent, including token positions, current dice roll, bonus turn flag, capture opportunities, safe zone landings, and threat distances.
- **Action Masking**: Because tokens cannot move from Base without a roll of 10, standard RL agents can get stuck sampling illegal moves. We use **Maskable PPO** to restrict action choices strictly to legal moves.

---

## Benchmark Results (Kori Khel)

We evaluated **Standard PPO** (trained for 2 million steps) against **Maskable PPO** (trained for 2 million steps) across 1,000 matches against rule-compliant heuristic opponents.

| Metric | Standard PPO (2M Steps) | Maskable PPO (2M Steps) | Notes |
| :--- | :---: | :---: | :--- |
| **Win Rate (%)** | 28.90% | **38.10%** | Higher win rate against 3 heuristic opponents |
| **Rule Adherence (%)** | 88.40% | **100.00%** | Maskable PPO never plays an illegal move |
| **Average Episode Length** | 53.0 turns | **59.3 turns** | Completes games faster |
| **Average Episode Reward** | +88.24 pts | **+115.15 pts** | Earns higher average game score |

### Evaluation Plots

![Head-to-Head Benchmark Comparison](evaluation/kori_khel/plots/ppo_vs_maskable_comparison.png)  
*Figure 1: Benchmark comparison showing Win Rate, Rule Adherence, and Episode Reward across 1,000 games.*

![Training Trajectories Comparison](evaluation/kori_khel/plots/training_curves_comparison.png)  
*Figure 2: Training progress over 2 million steps showing episode reward and episode length.*

---

## Repository Structure

```
.
├── environments/               # Gymnasium environment wrappers
│   └── kori_khel_env.py        # Kori Khel environment (KoriKhelEnv-v0)
├── game_engines/               # Pure Python game engine & rules
│   └── kori_khel/
│       └── engine.py           # Movement logic, safe zones, and dice mechanics
├── training/                   # Baseline training scripts
│   └── kori_khel/
│       ├── train_ppo.py        # Standard PPO training script
│       └── train_maskable_ppo.py # Maskable PPO training script
├── evaluation/                 # Benchmark evaluation & plotting scripts
│   └── kori_khel/
│       ├── evaluate_maskable_ppo.py # 1,000-game evaluation benchmark
│       ├── generate_benchmark_plots.py # Plot generation script
│       └── plots/              # Benchmark output plots
├── visualization/              # Interactive Web UI
│   ├── gui_server.py           # Flask server
│   └── templates/index.html    # Interactive board UI
└── docs/                       # Research paper source files
    ├── indoml_abstract.tex     # LaTeX source
    └── indoml_abstract.md      # Extended abstract markdown
```

---

## Quickstart & Usage

### 1. Installation

Python 3.10 or higher is required.

```bash
git clone https://github.com/dipexplorer/assamese-games-rl-suite.git
cd assamese-games-rl-suite

python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

pip install -e .
```

### 2. Train Baselines

Train Maskable PPO (2 million steps):
```bash
python -m training.kori_khel.train_maskable_ppo
```

Train Standard PPO (2 million steps):
```bash
python -m training.kori_khel.train_ppo
```

### 3. Run Benchmark & Generate Plots

Run the 1,000-game evaluation:
```bash
python -m evaluation.kori_khel.evaluate_maskable_ppo
```

Re-generate comparison plots:
```bash
python -m evaluation.kori_khel.generate_benchmark_plots
```

### 4. Interactive Web Interface

Launch the web board interface to watch or play steps:
```bash
python -m visualization.gui_server
```
Open `http://127.0.0.1:5000` in your web browser.

---

## Authors & Affiliation

- **Dipjyoti Das**
- **Simanta Sarma**
- **Rupam Bhattacharyya (Advisor)**

*Department of Information Technology, Gauhati University, Assam, India*
