# Kori Khel — Final RL Specification (v2.0)

> **Status: APPROVED ✅** — All rules verified via academic sources + visual evidence + expert clarification.

---

## 1. Overview
Kori Khel is a traditional Assamese board game played using cowrie shells as dice and coins/tokens as pieces. It is a **4-player, turn-based, stochastic strategy game**.

---

## 2. Board Topology

**Physical Shape:** Cross-shaped board drawn on cloth or ground.
**Structure:** 4 arms extending from a central hub. Each arm = 3 columns × 8 rows.

**Mathematical Abstraction (for RL):**
Each token's journey is modeled as a linear track from 0 → 73:

| Cell Range | Zone | Description |
|------------|------|-------------|
| `0` | **Base** | Token is inactive (off-board) |
| `1 – 64` | **Outer Perimeter** | Shared track. Captures can happen here. |
| `65 – 72` | **Home Column** | Private 8-cell safe track. No captures. |
| `73` | **Paka (Goal)** | Token is completed. |

**Safe Zones (X Marks):**
Certain cells on the Outer Perimeter (1–64) are marked with X. A token on a Safe Zone **cannot be captured**.

---

## 3. Players & Tokens

| Parameter | Value |
|-----------|-------|
| Players | 4 |
| Tokens per player | 4 |
| Total tokens on board | 16 |

---

## 4. Dice System — 6 Cowries

| Combination | Name | Steps | Bonus Turn | Probability |
|-------------|------|-------|------------|-------------|
| 1 Uburi + 5 Chit | **Jagowa / Jageowa** | 10 | ✅ YES | ~9.4% |
| 2 Uburi + 4 Chit | — | 2 | ❌ | ~23.4% |
| 3 Uburi + 3 Chit | — | 3 | ❌ | ~31.3% |
| 4 Uburi + 2 Chit | — | 4 | ❌ | ~23.4% |
| 5 Uburi + 1 Chit | **Pachi** | 25 | ✅ YES | ~9.4% |
| 6 Uburi + 0 Chit | **Full Marks** | 6 | ✅ YES | ~1.6% |
| 0 Uburi + 6 Chit | **Mudra** | 6 | ✅ YES | ~1.6% |

---

## 5. Game Mechanics

### A. Entry Rule (Kori Gaja)
A token at Base (`0`) can only enter the board when the player rolls **Jagowa (10)**. The token moves from `0` → `1`. Since Jagowa grants a bonus turn, the player throws again.

### B. Movement Choice
If multiple tokens are active, the player **chooses which token to move** with the rolled value.

### C. Capture (Khua)
- If a player lands **exactly on a cell (1–64)** occupied by an opponent's token, and that cell is **NOT a Safe Zone**, the opponent's token is **eaten (Khua)**.
- The captured token returns to **Base (0)** and must re-enter with a Jagowa roll.
- A token on a **Safe Zone** cannot be captured.

### D. Blocking
If **2+ tokens of the same player** are on the same cell, they form a pair and **cannot be captured**.

### E. Winning Condition
The **first player to move all 4 tokens to cell 73 (Paka)** wins. The game ends immediately.

---

## 6. RL Environment Specification

### State / Observation
```python
# 16-element array: [p1_t1, p1_t2, p1_t3, p1_t4, p2_t1, ..., p4_t4]
# Each value: 0 (base) to 73 (paka)
observation_space = Box(low=0, high=73, shape=(16,), dtype=np.int32)
```

### Action Space
```python
# Choose which of your 4 tokens to move (0, 1, 2, or 3)
action_space = Discrete(4)
```

### Reward Function

| Event | Reward |
|-------|--------|
| Win (all 4 tokens Paka) | **+100** |
| Lose | **-100** |
| Token reaches Paka (73) | **+30** |
| Capture an opponent | **+20** |
| Token gets captured | **-20** |
| Valid step forward | **+0.1 per step** |
| Invalid move (no valid token to move) | **-2** |
