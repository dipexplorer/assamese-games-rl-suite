# Assamese Traditional Games — RL Environment

**Final Year Project** | Dibrugarh University | 2026

> Develop a systematic framework for formalizing selected traditional Assamese games as computational environments and investigate their suitability for Reinforcement Learning.

---

## 🎯 What This Project Does

This project digitally preserves and computationally implements selected traditional Assamese board games as RL environments. AI agents are then trained using algorithms like PPO to learn and play these games.

## 🎮 Games

| Game      | Status         | Algorithm | Result |
| --------- | -------------- | --------- | ------ |
| Kori Khel | 🟡 In Progress | PPO       | -      |
| Game 2    | ⬜ TBD         | -         | -      |

## 📁 Architecture (Layered Design)

The project is split into distinct functional layers. Each layer contains sub-folders for specific games (e.g., `game_engines/kori_khel/`).

```
PROJECT/
├── game_engines/    ← 1. Pure Python game logic (rules, board, validation)
├── environments/    ← 2. Gymnasium wrapper (connects logic to AI)
├── training/        ← 3. Training scripts and hyperparameter config (PPO)
├── agents/          ← 4. Saved trained models (.zip)
├── evaluation/      ← 5. Win rates and benchmark testing
├── visualization/   ← 6. Board renderer for live AI demos
└── experiments/     ← 7. Logs of different training attempts
```

## 🚀 Quick Start (Once Kori Khel is complete)

```bash
pip install -r requirements.txt
python evaluation/kori_khel/evaluate.py      # Run the trained agent
```
