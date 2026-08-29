# visualization/

## What is this?
Code for rendering the game board and displaying the AI playing in real time.

## Why does it exist?
A working AI that you can **actually see playing** is 10x more impressive than
just a number on a graph. This folder contains the board renderer — 
either a terminal ASCII view or a simple Pygame/Matplotlib GUI.

## Files (will be added)
```
visualization/
└── kori_khel/
    ├── renderer.py         ← Draw the cross board with token positions
    └── demo.py             ← Watch the trained agent play a full game
```

## Usage (after training)
```bash
python visualization/kori_khel/demo.py
# Watch the AI play Kori Khel step by step
```

## Resume value
**A demo is worth a thousand graphs.**
If you can show a recruiter a live demo of your AI playing an ancient Indian board game,
that is an unforgettable impression. It also makes excellent demo material for the
IndoML poster presentation.
