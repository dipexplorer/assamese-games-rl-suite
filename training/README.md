# Training Module

Contains policy training scripts, TensorBoard logging configurations, and hyperparameter schedules.

## Module Structure

```
training/
└── kori_khel/
    ├── train_ppo.py           # Standard PPO baseline training (1.0M timesteps)
    ├── train_maskable_ppo.py  # Tuned Maskable PPO training (2.0M timesteps)
    ├── logs/                  # Standard PPO Monitor & TensorBoard logs
    └── logs_maskable/         # Maskable PPO Monitor & TensorBoard logs
```

## Running Training

```bash
# Train Maskable PPO Agent
python -m training.kori_khel.train_maskable_ppo

# Train Standard PPO Baseline Agent
python -m training.kori_khel.train_ppo
```
