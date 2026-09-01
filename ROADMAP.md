# Project Roadmap: Assamese Traditional Games RL Suite

## ✅ Completed Milestones
- [x] **Kori Khel Rules & Board Formalization:** Exact 73-state anti-clockwise spiral MDP geometry & cowrie binomial probability model finalized.
- [x] **Pure Game Engine:** `game_engines/kori_khel/engine.py` built and tested.
- [x] **Gymnasium Environment:** `KoriKhelEnv` (`environments/kori_khel_env.py`) wrapped and action-masking supported.
- [x] **RL Agent Training:** Maskable PPO trained for 1,000,000 steps (`train_maskable_ppo.py`).
- [x] **Benchmark Evaluation:** Evaluated 100 benchmark matches (**30.00% Win Rate**, 100% Rule Adherence).
- [x] **Interactive Web Visualizer:** Flask multi-game hub and live interactive board UI with physical cowrie tray.
- [x] **IndoML 2026 Submission Draft:** 2-Page Extended Abstract (`.tex` & `.md`) with TikZ diagrams and LaTeX code.

## 🔄 Multi-Game Framework Pipeline (Upcoming Modules)
- [ ] **Game 2 — Dhop Khel (ঢোপ খেল):** Formalize 2D physical pursuit MDP & Gymnasium environment.
- [ ] **Game 3 — Tekeli Bhonga (টেকেলী ভঙা):** Formalize POMDP spatial navigation environment.
- [ ] **Game 4 — Koni Juj (কণী যুঁজ):** Formalize discrete collision mechanics environment.
- [ ] **Game 5 — Ha-Doo-Doo (হা-ডু-ডু):** Formalize continuous territory control environment.
- [ ] **IndoML 2026 UG Forum Submission:** Submit 2-Page Extended Abstract + Signed Faculty Endorsement before Sept 15, 2026.

