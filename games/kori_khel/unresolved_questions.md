## KORI KHEL — UNRESOLVED QUESTIONS

These are open research questions that MUST be answered
before implementation can proceed. Do NOT invent answers.

Format:
  Q: Question
  Status: [Blocking / Non-blocking]
  Impact: What implementation step this affects
  Evidence so far: What partial evidence exists

==================================================

Q1: What is the exact value of Suda (6 cowries same orientation)?
Status: Blocking (for complete dice table)
Impact: Transition function in game engine
Evidence: Suda name is documented but value is not.

---

Q2: What is the complete and verified throw → movement mapping?
Status: Blocking (for game engine)
Impact: step() function, transition logic
Evidence: Jagora=10, Pachi=25 verified. 2/3/4 uburi are
          engineering decisions. Suda unknown.

---

Q3: What is the exact physical board layout and path topology?
Status: Blocking (for render() and path validation)
Impact: Board rendering, movement path
Evidence: Cross-shape inferred from photographs.
          Exact cell count and path not textually confirmed.

---

Q4: What is the verified starting arrangement of tokens?
Status: Blocking (for reset() function)
Impact: Initial state
Evidence: No source found.

---

Q5: Are safe zones (X marks) explicitly documented in any source?
Status: Blocking (for capture logic)
Impact: Capture rule implementation
Evidence: X marks visible in photographs. No textual rule found.

---

Q6: Is capture (khua) explicitly described for the six-cowrie
    Dhal/Chaal version?
Status: Blocking (for capture logic)
Impact: step() capture branch
Evidence: "Khua" concept mentioned in Assamese Wikipedia
          but mechanics for this specific variant not confirmed.

---

Q7: Is the entry rule (must roll Jagora to enter) textually
    confirmed for the six-cowrie Dhal/Chaal version?
Status: Non-blocking (user expert confirmed, but no text source)
Impact: Entry logic in step()
Evidence: Expert clarification only.

---

Q8: What is the exact path direction (clockwise / anti-clockwise)?
Status: Blocking (for movement direction in engine)
Impact: Path topology
Evidence: No verified source.

---

Q9: What happens when the home column cells are reached — can
    an opponent guti ever access the home column?
Status: Blocking (for safe zone logic)
Impact: Capture rule
Evidence: Inferred as "safe" from structure but not verified.

---

Q10: Is a "blocking pair" rule (two same-player tokens on same
     cell = immune to capture) documented for Kori Khel?
Status: Non-blocking (common in related games)
Impact: Capture logic
Evidence: No verified source for Kori Khel specifically.
