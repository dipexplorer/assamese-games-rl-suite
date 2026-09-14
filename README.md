# Computational Formalization and Reinforcement Learning Baselines for Assamese Traditional Games: A Case Study on Kori Khel

Official implementation of the Gymnasium environment and reinforcement learning baselines for **Kori Khel**, a 4-player stochastic cowrie-shell board game native to Assam, India.

This repository accompanies the paper:  
**"Computational Formalization and Reinforcement Learning Baselines for Assamese Traditional Games: A Case Study on Kori Khel"** (*IndoML 2026*).

---

## 📌 Key Highlights

- **Gymnasium Environment (`KoriKhelEnv-v0`)**: Maps physical 2D cross-shaped board geometry into a 73-state 1D Markov Decision Process (MDP) per player.
- **Stochastic Roll Modeling**: Models cowrie-shell throws via $K \sim \text{Binomial}(6, p=0.5)$ with asymmetric landing rules (*Jagowa*, *Pochi*, *Mudra*).
- **Feature Engineering**: Incorporates a 30-dimensional observation vector $\mathbf{o} \in \mathbb{Z}^{30}$ capturing raw positions, dice roll, bonus turn status, projected captures, safe zone landings, and rear threat distances.
- **Invalid Action Masking**: Solves severe entry-state bottlenecks ($s=0 \to 1$) where standard unmasked policy gradient methods fail.

---

## 📊 Empirical Evaluation & Benchmark Results

We benchmarked **Standard PPO** (1M timesteps) against **Maskable PPO** (2M timesteps) over a statistically rigorous 1,000-game head-to-head evaluation against rule-compliant heuristic opponents.

### 1,000-Game Benchmark Summary

| Metric | Standard PPO (1M Steps) | Maskable PPO (2M Steps) | Relative Advantage |
| :--- | :---: | :---: | :---: |
| **Win Rate (%)** | 28.30% | **36.20%** | **+27.9% Relative Gain** |
| **Rule Adherence (%)** | 72.80% | **100.00%** | **Perfect Policy Validity** |
| **Average Episode Length** | 94.2 turns | **59.5 turns** | **~37% Faster Completion** |
| **Average Episode Reward** | +80.93 pts | **+108.90 pts** | **+34.6% Reward Efficiency** |

### Benchmark Visualization

![Head-to-Head Benchmark Comparison](evaluation/kori_khel/plots/ppo_vs_maskable_comparison.png)  
*Figure 1: Head-to-Head 1,000-Game Benchmark Comparison across Win Rate (%), Rule Adherence (%), and Average Episode Reward (pts).*

![Training Trajectories Comparison](evaluation/kori_khel/plots/training_curves_comparison.png)  
*Figure 2: Training Trajectory Comparison over 2 million timesteps showing moving average reward and episode length convergence.*

---

## 🛠️ Repository Architecture

```
.
├── environments/               # OpenAI Gymnasium Environment Definitions
│   └── kori_khel_env.py        # 73-state 1D MDP Kori Khel environment
├── game_engines/               # Core Python Engine & Rules Logic
│   └── kori_khel_engine.py     # 4-player game state engine
├── training/                   # Baseline Training Scripts
│   └── kori_khel/
│       ├── train_ppo.py        # Standard unmasked PPO trainer
│       └── train_maskable_ppo.py # Maskable PPO trainer
├── evaluation/                 # Evaluation & Plot Generation
│   └── kori_khel/
│       ├── evaluate_maskable_ppo.py # 1,000-game head-to-head benchmark
│       ├── generate_benchmark_plots.py # Publication-grade plot renderer
│       └── plots/              # Benchmark plots (PNG)
├── visualization/              # Web GUI & Renderer
│   ├── gui_server.py           # Flask web server
│   └── templates/index.html    # Interactive HTML5/JS canvas board
└── docs/                       # Research Abstract & TeX Source
    ├── indoml_abstract.tex     # Camera-ready IndoML LaTeX source
    └── indoml_abstract.md      # Extended abstract markdown
```

---

## 🚀 Quickstart & Usage

### 1. Installation

Requires Python 3.10 or higher.

```bash
git clone https://github.com/dipexplorer/assamese-games-rl-suite.git
cd assamese-games-rl-suite

python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

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

### 3. Evaluation & Plot Generation

Run 1,000-game head-to-head evaluation benchmark:
```bash
python -m evaluation.kori_khel.evaluate_maskable_ppo
```

Re-generate benchmark plots:
```bash
python -m evaluation.kori_khel.generate_benchmark_plots
```

### 4. Interactive Web GUI

Launch the interactive web board renderer to visually step through matches:
```bash
python -m visualization.gui_server
```
Open `http://127.0.0.1:5000` in your browser.

---

## 👥 Authors & Affiliation

- **Dipjyoti Das**
- **Simanta Sharma**
- **Rupam Bhattacharyya (Advisor)**

*Department of Information Technology, Gauhati University, Assam, India*
