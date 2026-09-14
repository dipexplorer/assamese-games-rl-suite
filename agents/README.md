# Saved Reinforcement Learning Models

This directory contains trained model weights for the Kori Khel environment in Stable-Baselines3 `.zip` format.

## Structure

```
agents/
└── kori_khel/
    ├── maskable_ppo_kori_khel.zip  # Tuned Maskable PPO model (2.0M timesteps)
    └── ppo_kori_khel.zip           # Baseline PPO model (1.0M timesteps)
```

## Loading Checkpoints

```python
from sb3_contrib import MaskablePPO
from stable_baselines3 import PPO

# Load Maskable PPO model
maskable_model = MaskablePPO.load("agents/kori_khel/maskable_ppo_kori_khel.zip")

# Load Standard PPO model
ppo_model = PPO.load("agents/kori_khel/ppo_kori_khel.zip")
```
