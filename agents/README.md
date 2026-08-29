# agents/

## What is this?
Saved trained RL agent models — the actual AI that learned to play the games.

## Why does it exist?
After training, the model is saved here as a `.zip` file (Stable-Baselines3 format).
Anyone can load this file and watch the trained agent play — without retraining.

## Files (will be added after training)
```
agents/
└── kori_khel/
    ├── ppo_kori_khel_v1.zip   ← Trained PPO model
    └── ppo_kori_khel_v2.zip   ← Improved version
```

## Resume value
This is **the proof that your project works**.
A recruiter or evaluator can literally run `python evaluate.py` and watch 
your AI play an ancient Assamese board game. That's impressive.
