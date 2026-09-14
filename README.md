# Assamese Traditional Games Reinforcement Learning Suite

Official repository for computational formalizations, OpenAI Gymnasium environments, and reinforcement learning baselines for traditional indigenous games native to Assam, India.

> **Paper**: *Computational Formalization and Reinforcement Learning Baselines for Assamese Traditional Games: A Case Study on Kori Khel*

---

## Overview

Indigenous multi-agent games feature asymmetric stochastic distributions, complex topological constraints, and non-trivial entry rules that are absent from standard RL benchmark suites. This project aims to formalize a multi-game suite of 5 traditional Assamese games into standardized Gymnasium environments.

### Suite Roadmap & Initial Case Study

* **Game 1 (Initial Release — `KoriKhelEnv-v0`)**: **Kori Khel**, a 4-player stochastic cowrie-shell race game featuring a 73-state 1D Markov Decision Process (MDP) per player, a 30D observation space, and invalid action masking to overcome severe entry bottlenecks.
* **Upcoming Environments**: Multi-agent pursuit mechanics (*Dhop Khel*), spatial navigation under partial observability (*Tekeli Bhonga*), collision dynamics (*Koni Juj*), and continuous territory control (*Ha-Doo-Doo*).

---

## Game 1: Kori Khel (`KoriKhelEnv-v0`)

Kori Khel is played with 6 cowrie shells ($K \sim \text{Binomial}(6, p=0.5)$). Tokens remain trapped off-board ($s=0$) until an exact entry roll (*Jagowa*, roll of 10) is thrown.

### Environment & Architecture

1. **`KoriKhelEnv-v0`**: Maps physical 2D cross-shaped board geometry into a 73-state 1D MDP per player.
2. **30D Feature Representation**: State vector $\mathbf{o} \in \mathbb{Z}^{30}$ capturing token positions, roll value, bonus status, projected captures, safe-zone landings, and rear threat distances.
3. **Invalid Action Masking**: Solves entry-state bottlenecks where unmasked policy gradient methods get trapped in illegal-action penalty minima.

---

## Experimental Benchmarks (Kori Khel)

Models were evaluated across a 1,000-game head-to-head benchmark against 3 rule-compliant heuristic opponents.

### Performance Comparison (1,000 Games)

| Metric | Standard PPO (1M Steps) | Maskable PPO (2M Steps) | Advantage |
| :--- | :---: | :---: | :---: |
| **Win Rate (%)** | 28.30% | **36.20%** | +27.9% relative win rate |
| **Rule Adherence (%)** | 72.80% | **100.00%** | 100% legal action selection |
| **Average Episode Length** | 94.2 turns | **59.5 turns** | ~37% faster match completion |
| **Average Episode Reward** | +80.93 pts | **+108.90 pts** | Higher reward efficiency |

### Evaluation Plots

![Head-to-Head Benchmark Comparison](evaluation/kori_khel/plots/ppo_vs_maskable_comparison.png)  
*Figure 1: Head-to-head 1,000-game benchmark metrics comparing Standard PPO and Maskable PPO.*

![Training Trajectories Comparison](evaluation/kori_khel/plots/training_curves_comparison.png)  
*Figure 2: Training trajectories over 2 million timesteps showing moving average reward and episode length.*

---

## Repository Structure

```
.
├── environments/               # Gymnasium environment wrappers
│   └── kori_khel_env.py        # Kori Khel 73-state 1D MDP environment
├── game_engines/               # Pure Python game rules & state engines
│   └── kori_khel/
│       └── engine.py           # Core movement, safe zones, and dice mechanics
├── training/                   # Policy training scripts
│   └── kori_khel/
│       ├── train_ppo.py        # Standard PPO trainer
│       └── train_maskable_ppo.py # Maskable PPO trainer
├── evaluation/                 # Benchmark evaluation & figure generation
│   └── kori_khel/
│       ├── evaluate_maskable_ppo.py # 1,000-game evaluation benchmark
│       ├── generate_benchmark_plots.py # Plot generation script
│       └── plots/              # Benchmark plots
├── visualization/              # Web GUI & interactive board renderer
│   ├── gui_server.py           # Flask server
│   └── templates/index.html    # Board rendering interface
└── docs/                       # Research paper source files
    ├── indoml_abstract.tex     # Camera-ready LaTeX paper source
    └── indoml_abstract.md      # Extended abstract markdown
```

---

## Quickstart & Usage

### 1. Installation

Requires Python 3.10 or higher.

```bash
git clone https://github.com/dipexplorer/assamese-games-rl-suite.git
cd assamese-games-rl-suite

python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

pip install -e .
```

### 2. Training Baselines

Train Maskable PPO (2M timesteps):
```bash
python -m training.kori_khel.train_maskable_ppo
```

Train Standard PPO (1M timesteps):
```bash
python -m training.kori_khel.train_ppo
```

### 3. Running Evaluation & Generating Plots

Run 1,000-game benchmark evaluation:
```bash
python -m evaluation.kori_khel.evaluate_maskable_ppo
```

Re-generate benchmark comparison plots:
```bash
python -m evaluation.kori_khel.generate_benchmark_plots
```

### 4. Interactive Web Interface

Launch the interactive web renderer to step through matches:
```bash
python -m visualization.gui_server
```
Open `http://127.0.0.1:5000` in a web browser.

---

## Authors & Affiliation

- **Dipjyoti Das**
- **Simanta Sharma**
- **Rupam Bhattacharyya (Advisor)**

*Department of Information Technology, Gauhati University, Assam, India*
