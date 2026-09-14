# Evaluation & Benchmarking

Scripts and tools for benchmarking trained RL policies against heuristic opponents.

## Directory Structure

```
evaluation/
└── kori_khel/
    ├── evaluate.py                  # 1,000-game evaluation for Standard PPO
    ├── evaluate_maskable_ppo.py     # 1,000-game evaluation for Maskable PPO
    ├── generate_benchmark_plots.py  # Publication plot generator script
    ├── benchmark_results.md         # Quantitative evaluation summary (PPO)
    ├── benchmark_results_maskable.md# Quantitative evaluation summary (Maskable PPO)
    └── plots/
        ├── ppo_vs_maskable_comparison.png
        └── training_curves_comparison.png
```

## Running Benchmarks

```bash
# Evaluate Maskable PPO model (1,000 games)
python -m evaluation.kori_khel.evaluate_maskable_ppo

# Evaluate Standard PPO model (1,000 games)
python -m evaluation.kori_khel.evaluate

# Generate publication plots
python -m evaluation.kori_khel.generate_benchmark_plots
```
