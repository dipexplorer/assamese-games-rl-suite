# Computational Formalization and Reinforcement Learning Baselines for Assamese Traditional Games

This repository contains the official implementation of the computational formalization and OpenAI Gymnasium environments for Assamese traditional games. The codebase establishes baseline reinforcement learning (RL) policies for these environments, currently focusing on Kori Khel. 

This work is intended for the **IndoML 2026 Undergraduate Forum**.

## Overview

Standard RL benchmark suites predominantly feature Western board games. Indigenous multi-agent games, characterized by asymmetric stochastic dynamics and complex topological constraints, remain largely unmodeled. This repository provides:

1. **`KoriKhelEnv-v0`**: A 73-state 1D Markov Decision Process (MDP) implementation of the 4-player cowrie-shell game Kori Khel.
2. **Policy Gradient Baselines**: Training and evaluation scripts for Proximal Policy Optimization (PPO).
3. **Action Masking**: Implementations addressing severe action-space bottlenecks caused by strict game entry rules.

Empirical results demonstrate that standard PPO fails to learn legal play (46% rule adherence) due to entry-state penalty minima, whereas Maskable PPO achieves 100% rule adherence and a 30% win rate against a uniform random baseline.

## Installation

The codebase requires Python 3.10 or higher. It is recommended to use an isolated virtual environment.

```bash
git clone https://github.com/dipexplorer/assamese-games-rl-suite.git
cd assamese-games-rl-suite

python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

## Usage

### 1. Training Baselines
To train the Maskable PPO agent on the Kori Khel environment:

```bash
python -m training.kori_khel.train_maskable
```
Training logs are output to `training/kori_khel/logs_maskable/` and can be visualized using TensorBoard.

### 2. Environment Visualization
The repository includes a Flask-based board renderer for agent evaluation and policy visualization.

```bash
python visualization/gui_server.py
```
Access the rendering interface at `http://127.0.0.1:5000`.

## Future Work

The formalization framework is actively being extended to other regional games, including:
- **Dhop Khel**: Transitioning to continuous 2D spatial coordinate systems with multi-agent tagging dynamics.
- **Tekeli Bhonga**: POMDP spatial navigation constraints under partial observability.
- **Koni Juj**: Discrete collision MDPs for structural integrity prediction.
- **Ha-Doo-Doo**: Continuous territory-control modeling.

## Citation

If you utilize this codebase or environment in your research, please cite the associated paper:

```bibtex
@inproceedings{das2026korikhel,
  title={Computational Formalization and Reinforcement Learning Baselines for Assamese Traditional Games: A Case Study on Kori Khel},
  author={Das, Dipjyoti and Sharma, Simanata and Bhattacharyya, Rupam},
  booktitle={7th Indian Symposium on Machine Learning (IndoML) - Undergraduate Forum},
  year={2026},
  address={Kolkata, India}
}
```

## Authors
- **Dipjyoti Das**
- **Simanta Sharma**
- **Rupam Bhattacharyya (Advisor)**

*Department of Information Technology, Gauhati University, Assam, India*
