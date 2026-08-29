# 🎯 Final Year Project — Assamese Traditional Games RL

## Overview
Building **Reinforcement Learning environments** for **5 Assamese Traditional Games** using the Gymnasium (Farama Foundation) library, and training RL agents (PPO/DQN) on them.

This project also serves as a submission to **IndoML 2026 Undergraduate Forum** (Deadline: 15 September 2026).

## Guide
Based on initial discussion with the project supervisor.

## Key Resources
- [Gymnasium Docs](https://gymnasium.farama.org/index.html)
- [HuggingFace Deep RL Course](https://huggingface.co/learn/deep-rl-course/en/unit0/introduction)
- [IndoML 2026 Forum](https://indoml.in/undergraduate-forum)
- ATG-VQA Research Paper (background context — 6 Assamese games + VLM evaluation)

## Project Structure
```
PROJECT/
├── README.md                  ← This file
├── TASK.md                    ← Live task tracker
├── docs/
│   ├── kori_khel_rulebook.md  ← Finalized game specification
│   └── indoml_abstract.md     ← 2-Page submission draft
├── games/
│   ├── kori_khel/             ← Primary game (most complete)
│   │   ├── env.py             ← Gymnasium environment
│   │   ├── train.py           ← Training script (PPO)
│   │   └── results/           ← Graphs, logs
│   ├── game_2/                ← TBD
│   ├── game_3/                ← TBD
│   ├── game_4/                ← TBD
│   └── game_5/                ← TBD
└── shared/
    └── utils.py               ← Shared utilities
```

## The 5 Games
| # | Game | Status |
|---|------|--------|
| 1 | **Kori Khel** (Cowrie Game) | 🟡 Rulebook Complete, Env Pending |
| 2 | TBD | ⬜ Not Started |
| 3 | TBD | ⬜ Not Started |
| 4 | TBD | ⬜ Not Started |
| 5 | TBD | ⬜ Not Started |
