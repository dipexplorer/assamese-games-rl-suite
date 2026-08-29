# Assamese Traditional Games — RL Environment

**Final Year Project** | Dibrugarh University | 2026

> Building Reinforcement Learning environments for traditional Assamese board games using Python and Gymnasium.

---

## 🎯 What This Project Does
This project digitally preserves and computationally implements selected traditional Assamese board games as RL environments. AI agents are then trained using algorithms like PPO to learn and play these games.

## 🎮 Games
| Game | Status | Algorithm | Result |
|------|--------|-----------|--------|
| Kori Khel | 🟡 In Progress | PPO | - |
| Game 2 | ⬜ TBD | - | - |
| Game 3 | ⬜ TBD | - | - |
| Game 4 | ⬜ TBD | - | - |
| Game 5 | ⬜ TBD | - | - |

## 🛠️ Stack
- Python 3.x
- [Gymnasium](https://gymnasium.farama.org/) — RL Environment API
- [Stable-Baselines3](https://stable-baselines3.readthedocs.io/) — PPO/DQN
- Matplotlib — Results visualization

## 📁 Structure
```
games/
└── kori_khel/
    ├── env.py       ← Gymnasium environment
    ├── train.py     ← Train PPO agent
    ├── test_env.py  ← Verify environment works
    ├── results/     ← Training graphs, win rates
    └── tests/       ← Unit tests for game logic
tests/               ← Shared test utilities
ROADMAP.md           ← Project progress tracker
requirements.txt     ← Dependencies
```

## 🚀 Quick Start
```bash
pip install -r requirements.txt
python games/kori_khel/test_env.py   # Verify env
python games/kori_khel/train.py      # Train agent
```
