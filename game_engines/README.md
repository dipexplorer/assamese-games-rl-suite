# game_engines/

## What is this?
Pure Python game logic — completely **independent of any RL framework**.

## Why does it exist?
The game engine is the **foundation of the entire project**. Before we teach an AI to play a game, the game itself must work perfectly.

This folder contains:
- Board representation
- Game rules (movement, capture, turn logic)
- Move validation (legal vs illegal moves)
- Win/loss/draw detection
- A way to simulate full games between two rule-based players

## Why separate from RL?
Because the game engine should work even without Gymnasium or Stable-Baselines3.
If the game logic is wrong, the AI will learn the wrong game.

## Files (will be added)
```
game_engines/
└── kori_khel/
    ├── board.py       ← Board state representation
    ├── rules.py       ← All game rules
    ├── game.py        ← Full game loop
    └── players.py     ← Human / random / rule-based players
```

## Resume value
Shows that you can architect software in **layers** — 
game logic → RL wrapper → AI agent. This is professional software design.
