# Kori Khel — Final RL Specification (v2.0)

This is the **Final Master Rulebook** for our Reinforcement Learning environment. Every rule here is backed by academic research, mathematical deduction from visual evidence, and final clarifications.

---

## 1. Players & Board Topology
* **Players:** 4 Players (Playing against each other).
* **Tokens (Gotis):** 4 tokens per player.
* **The Physical Board (Visual Render):** 
  The environment represents the exact cross-shaped board. It consists of a center square and 4 arms. Each arm has 3 columns and 8 rows. Safe zones (X marks) are placed on the 3rd and 8th (tip) rows of the arms.
* **The Board Path (Mathematical Abstraction for AI):** 
  While the game *looks* like a 2D cross to humans, to make it easy for an AI to learn, each token's journey is mathematically modeled as a **1D track from 0 to 73**.
  * `0`: **Base/Home** (Inactive, waiting to enter).
  * `1 to 64`: **Outer Perimeter**. This is a shared track where tokens from different players can cross paths and capture each other.
  * `65 to 72`: **Home Column**. A private 8-cell track for each player. Opponents cannot enter here.
  * `73`: **Paka (Goal)**. Token is successfully completed.
* **Safe Zones (X Marks):** Specific cells on the 1-64 outer perimeter are designated as "Safe Zones". If a token is on a Safe Zone, it cannot be captured by opponents. Multiple tokens can share a Safe Zone.

---

## 2. The Dice (6 Cowries) & Transition Logic
At each turn, a player throws 6 cowrie shells. The number of shells that land face down ("Uburi") determines the steps and whether the player gets a bonus turn.

| Combination | Traditional Name | Steps | Bonus Turn? | Probability |
|-------------|-----------------|-------|-------------|-------------|
| **1 Uburi** | Jagowa / Jageowa | 10 | ✅ YES | ~9.4% |
| **2 Uburi** | - | 2 | ❌ NO | ~23.4% |
| **3 Uburi** | - | 3 | ❌ NO | ~31.3% |
| **4 Uburi** | - | 4 | ❌ NO | ~23.4% |
| **5 Uburi** | Pachi | 25 | ✅ YES | ~9.4% |
| **6 Uburi** | Full Marks | 6 | ✅ YES | ~1.6% |
| **0 Uburi** (6 Chit) | Mudra | 6 | ✅ YES | ~1.6% |

---

## 3. Game Mechanics

### A. Entry Rule
A token sitting at Base (`0`) cannot move freely. The player **must roll a 10 (Jagowa)** to unlock a token. Rolling a 10 moves the token from `0` to the starting square `1`. Since Jagowa grants a bonus turn, the player then throws again to advance that token further.

### B. Movement Choice
If a player has multiple active tokens on the board, they can **choose which token to move**. (This is where the AI's strategy will come in).

### C. Capture (Khua)
If a player's token lands exactly on a cell (between 1-64) occupied by an opponent's token, and that cell is **not a Safe Zone**, the opponent's token is **"Khua" (Eaten)**. The captured token is immediately sent back to Base (`0`).

### D. Winning Condition
The game ends when a player successfully navigates all 4 of their tokens to cell `73` (Paka). That player is the Winner.

---

## 4. RL Reward Engineering
This is not a traditional rule, but the mathematical incentive system we will feed to the PPO algorithm to make it learn the game quickly and aggressively:

* **Win the Game:** +100
* **Token reaches Paka (73):** +30 *(Incentivizes finishing tokens, not just wandering)*
* **Capture an Opponent:** +20 *(Incentivizes aggressive play)*
* **Token gets Captured:** -20 *(Incentivizes defensive play and using Safe Zones)*
* **Valid Step Progress:** +0.1 per step forward *(Helps AI understand that moving forward is good)*
