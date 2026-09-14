# Deterministic Game Engines

Pure Python implementations of game rules and state transition mechanics for Assamese traditional games. The game engines are decoupled from Gymnasium and RL dependencies.

## Module Layout

```
game_engines/
└── kori_khel/
    └── engine.py   # Core Kori Khel game state, movement, safe zones, and roll rules
```

## Key Engine Components (`KoriKhelEngine`)

* **Board Layout**: 64-cell global perimeter track + 8 private home corridor cells + Ghai ($s=73$).
* **Safe Zones**: 8 sanctuary cells ($s \in \{5, 12, 21, 28, 37, 44, 53, 60\}$).
* **Dice Mechanics**: Binomial model $K \sim \text{Binomial}(6, p=0.5)$ for 6 cowrie shells.
* **Captures**: Opponent collision on non-safe cells sends captured token back to base ($s=0$).
