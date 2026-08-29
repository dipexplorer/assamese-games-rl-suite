# experiments/

## What is this?
Log of every training run — what settings were used and what results came out.

## Why does it exist?
When you train an RL agent, you try many different settings:
- Different reward values (+10 vs +20 for capture)
- Different algorithms (PPO vs DQN)
- Different training steps (100k vs 500k)

This folder tracks each experiment so you can compare them and
explain *why* the final version works best.

## Structure (will be added)
```
experiments/
└── kori_khel/
    ├── exp_001/
    │   ├── config.yaml         ← Exact settings used
    │   ├── results.md          ← Win rate, reward stats
    │   └── reward_curve.png    ← Training graph
    ├── exp_002/
    │   └── ...
    └── comparison.md           ← Which experiment won and why
```

## Resume value
Shows **scientific thinking and iteration** — not just "I ran it once and it worked."
Comparing experiments across different reward functions or algorithms
is the kind of depth that separates a strong project from a basic one.
