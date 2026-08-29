# evaluation/

## What is this?
Scripts and results for measuring how well the trained AI performs.

## Why does it exist?
Training an agent is only half the job. You must also **prove it works**.
This folder contains:
- Scripts to run the trained agent against a random opponent
- Win rate measurements
- Performance comparison between PPO agent vs random agent vs rule-based agent

## Files (will be added)
```
evaluation/
└── kori_khel/
    ├── evaluate.py              ← Run trained agent, measure win rate
    ├── benchmark_results.md     ← PPO vs Random vs Rule-Based comparison
    └── plots/
        ├── win_rate.png         ← Win rate over evaluation episodes
        └── reward_curve.png     ← Training reward over time
```

## Resume value
**This is what goes in your abstract, report, and resume.**
"Our PPO agent achieved a 78% win rate against a random baseline after 500k training steps."
That's a result. Results are what recruiters and evaluators want to see.
