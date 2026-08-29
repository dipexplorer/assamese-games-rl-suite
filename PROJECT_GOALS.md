## PROJECT GOALS

==================================================
OBJECTIVE A — Cultural / Game Preservation
==================================================

- Identify traditional Assamese games
- Document their rules and gameplay from reliable sources
- Preserve important game knowledge digitally
- Record regional variations where they exist
- Acknowledge conflicting or incomplete information

==================================================
OBJECTIVE B — Machine Learning / RL
==================================================

- Formalize game mechanics computationally
- Design RL-compatible environments (Gymnasium)
- Implement a pure game engine before any RL layer
- Train RL agents on validated environments
- Evaluate agent behaviour and performance
- Investigate whether different game structures affect RL learning

==================================================
WHAT THIS PROJECT IS NOT
==================================================

This project is NOT simply:
  "Train PPO on Kori Khel."

That is only one possible later experiment.

The project is primarily about:
  Research → Documentation → Formalization → Computation → RL

==================================================
SUCCESS CRITERIA
==================================================

Phase 1 (Research):
  - Each selected game has a structured research profile
  - Evidence matrix is complete with source classifications
  - Unresolved questions are explicitly documented

Phase 2–3 (Formalization):
  - Each game has a formal game specification
  - Rules are classified [VERIFIED / SUPPORTED / INFERRED /
    ENGINEERING DECISION / UNKNOWN]

Phase 4–5 (Game Engine):
  - Pure game engine works independently of RL
  - All verified rules are unit-tested

Phase 6 (Gymnasium):
  - Valid Gymnasium environment
  - Passes environment checker

Phase 7 (Baseline):
  - Random agent and rule-based agent implemented

Phase 8–10 (RL):
  - Suitable algorithm selected with justification
  - Training results reproducible
  - Agent evaluated against baselines

Phase 11–13 (Analysis):
  - Visualization of results
  - Cross-game analysis (if multiple games implemented)
  - Research paper / final report
