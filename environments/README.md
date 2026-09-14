# Gymnasium Environments

This module implements Gymnasium-compatible environment wrappers for Assamese traditional games.

## Module Layout

```
environments/
└── kori_khel_env.py   # KoriKhelEnv-v0 implementation (OpenAI Gymnasium API)
```

## Environment Specifications (`KoriKhelEnv`)

* **Observation Space**: `Box(low=0, high=73, shape=(17,), dtype=int32)`
  * `obs[0..3]`: Absolute scalar positions of active agent's 4 tokens ($s \in [0, 73]$).
  * `obs[4..15]`: Relative positions of 12 opponent tokens (3 opponents $\times$ 4 tokens).
  * `obs[16]`: Current dice roll value ($r \in [0, 25]$).
* **Action Space**: `Discrete(4)` — Select which token index ($0, 1, 2, 3$) to advance.
* **Action Masking**: Exposes `action_masks()` returning a boolean array of length 4 indicating legal moves.
