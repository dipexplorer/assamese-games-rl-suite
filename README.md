# Computational Formalization & RL Suite for Assamese Traditional Games

**Final Year Project** | Department of Information Technology, Gauhati University | 2026  
**Target Submission:** IndoML 2026 (7th Indian Symposium on Machine Learning) — Undergraduate Forum

> A systematic computational framework to formalize traditional Assamese games into OpenAI Gymnasium environments and benchmark Reinforcement Learning algorithms.

---

## 🎮 Suite Games & Status

| Game | Domain / Dynamics | Status | RL Benchmark | Win Rate |
| :--- | :--- | :---: | :---: | :---: |
| **Kori Khel** (কড়ি খেল) | Stochastic 4-Player Board | 🟢 **Complete** | Maskable PPO | **30.00%** (100% Legal Play) |
| **Dhop Khel** (ঢোপ খেল) | Multi-Agent Pursuit & Tagging | 🟡 In Formalization | TBD | Pending |
| **Tekeli Bhonga** (টেকেলী ভঙa) | POMDP Spatial Awareness | 🟡 In Formalization | TBD | Pending |
| **Koni Juj** (কণী যুঁজ) | Discrete Collision Mechanics | 🟡 In Formalization | TBD | Pending |
| **Ha-Doo-Doo** (হা-ডু-ডু) | Continuous Territory Control | 🟡 In Formalization | TBD | Pending |

---

## 📁 Architecture (Modular 5-Game Layered Design)

```
PROJECT/
├── game_engines/    ← Pure Python game logic (kori_khel, dhop_khel, etc.)
├── environments/    ← OpenAI Gymnasium wrappers (KoriKhelEnv, etc.)
├── training/        ← Training pipelines (train_maskable_ppo.py)
├── agents/          ← Saved trained model weights (.zip)
├── evaluation/      ← 100-game benchmark scripts & win-rate metrics
├── visualization/   ← Flask Web Dashboard (Multi-game Hub & interactive boards)
├── docs/            ← IndoML 2026 2-Page Extended Abstract (.tex / .md) & rulebooks
├── tests/           ← Unit tests for mechanics and state transitions
└── experiments/     ← Training logs & Tensorboard events
```

---

## 🚀 Quick Start

### 1. Run Interactive Web Visualizer
```bash
python visualization/gui_server.py
```
Open `http://localhost:5000` in your browser to launch the Multi-Game Hub or play Kori Khel live!

### 2. Train Maskable PPO Agent (1M Steps)
```bash
.venv/bin/python training/kori_khel/train_maskable_ppo.py
```

### 3. Run Benchmark Evaluation
```bash
.venv/bin/python evaluation/kori_khel/evaluate_maskable_ppo.py
```

