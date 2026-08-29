# training/

## What is this?
Training scripts and configuration files for running RL experiments.

## Why does it exist?
This folder contains the scripts that actually run the training loop —
setting hyperparameters, choosing algorithms, logging progress.

Separating training config from the game code means you can easily
run different experiments (e.g., PPO vs DQN, different reward functions)
without changing the game environment.

## Files (will be added)
```
training/
└── kori_khel/
    ├── train_ppo.py        ← Run PPO training
    ├── config_ppo.yaml     ← Hyperparameters (lr, steps, gamma...)
    └── train_dqn.py        ← Compare with DQN
```

## Resume value
Shows you understand **reproducible ML** — a core skill in any ML/AI job.
Separating config from code is standard industry practice.
