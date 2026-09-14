# Computational Formalization and Reinforcement Learning Baselines for Assamese Traditional Games

This repository contains the official implementation of the computational formalization and OpenAI Gymnasium environments for Assamese traditional games. The codebase establishes baseline reinforcement learning (RL) policies for these environments, focusing on Kori Khel.

## Overview

Standard RL benchmark suites predominantly feature Western board games. Indigenous multi-agent games, characterized by asymmetric stochastic dynamics and complex topological constraints, remain largely unmodeled. This repository provides:

1. **`KoriKhelEnv-v0`**: A 73-state 1D Markov Decision Process (MDP) implementation of the 4-player cowrie-shell game Kori Khel.
2. **Policy Gradient Baselines**: Training and evaluation scripts for Proximal Policy Optimization (PPO) and Maskable PPO.
3. **Action Masking**: Implementations addressing severe action-space bottlenecks caused by strict game entry rules.

Empirical results demonstrate that standard PPO fails to maintain legal play (72.8% rule adherence) due to entry-state penalty minima, whereas Maskable PPO achieves 100% rule adherence, an average episode reward of +108.90, and a 36.20% win rate against rule-compliant opponents in a 4-player setting (25.0% random baseline).

## Installation

The codebase requires Python 3.10 or higher.

```bash
git clone https://github.com/dipexplorer/assamese-games-rl-suite.git
cd assamese-games-rl-suite

python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

pip install -e .
```

## Usage

### 1. Training Baselines

Train Maskable PPO (2.0M timesteps):
```bash
python -m training.kori_khel.train_maskable_ppo
```

Train Standard PPO Baseline (1.0M timesteps):
```bash
python -m training.kori_khel.train_ppo
```

Training logs are output to `training/kori_khel/logs_maskable/` and `training/kori_khel/logs/` and can be visualized using TensorBoard.

### 2. Evaluation & Plot Generation

Evaluate Maskable PPO over 1,000 games:
```bash
python -m evaluation.kori_khel.evaluate_maskable_ppo
```

Generate head-to-head benchmark comparison figures:
```bash
python -m evaluation.kori_khel.generate_benchmark_plots
```

### 3. Interactive Web GUI

Launch the Flask board renderer to step through games interactively:

```bash
python -m visualization.gui_server
```

Access the rendering interface at `http://127.0.0.1:5000`.

## Authors

- **Dipjyoti Das**
- **Simanta Sharma**
- **Rupam Bhattacharyya (Advisor)**

*Department of Information Technology, Gauhati University, Assam, India*
