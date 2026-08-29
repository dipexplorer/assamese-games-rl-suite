# environments/

## What is this?
Gymnasium-compatible wrappers that connect the game engine to the RL framework.

## Why does it exist?
Gymnasium is the industry-standard API for RL environments (used at OpenAI, DeepMind, etc.).
This folder contains the `gym.Env` subclass for each game — the layer that turns a game into something an AI can train on.

## What it defines
- `observation_space` — What the AI can "see" (board state)
- `action_space` — What moves the AI can make
- `reset()` — Start a new game
- `step(action)` — AI makes a move, environment returns new state + reward

## Files (will be added)
```
environments/
└── kori_khel_env.py   ← Wraps game_engine → Gymnasium API
```

## Resume value
Shows you understand the **standard ML engineering interface** used across the industry.
Any ML engineer will immediately recognise a Gymnasium environment.
