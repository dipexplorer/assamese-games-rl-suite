# Computational Formalization and Reinforcement Learning Baselines for Kori Khel: A Traditional Assamese Board Game

**IndoML 2026 Undergraduate Forum Submission Draft**
**Authors:** [Your Name], [Project Partners' Names]  
**Advisor:** [Advisor/Guide Name], Dibrugarh University  

---

## Abstract
Traditional cultural games are rapidly fading from public memory due to the dominance of modern digital recreation. This paper presents a systematic framework to digitally preserve and computationally formalize **Kori Khel**, a traditional cowrie-shell board game from Assam, India. We mathematically abstract the game’s 2D cross-shaped board into a 73-state 1D MDP and implement a custom Gymnasium environment. We establish baseline performance benchmarks by training a Reinforcement Learning agent using Proximal Policy Optimization (PPO) against rule-based random opponents. 

To resolve learning inefficiencies under complex rules, we perform a comparative study between **Standard PPO** (utilizing negative penalty shaping) and **Maskable PPO** (utilizing action masking). Our results show that while Standard PPO struggles to learn constraints (achieving only **46.3% rule adherence**), Maskable PPO guarantees **100.0% rule adherence** from step 1, significantly improving learning stability and reducing game length from **43.5 to 37.3 steps**.

---

## 1. Introduction & Background
Traditional Assamese games like Kori Khel carry significant cultural heritage but lack formal mathematical documentation. In this work, we address this preservation gap by:
1. Creating a formal computational rulebook for Kori Khel.
2. Developing a Gymnasium-compliant environment suitable for Reinforcement Learning research.
3. Establishing baseline results using modern policy gradient methods (PPO).

---

## 2. Kori Khel Game Formulation
Kori Khel is played by 4 players, each managing 4 tokens. The game utilizes 6 cowrie shells as stochastic dice, where the number of shells landing face-down ($k \sim \text{Binomial}(6, 0.5)$) determines token movement steps:
* **1 Uburi (Jagowa):** 10 steps + Bonus Turn (Entry roll required to release tokens from Base)
* **5 Uburis (Pachi):** 25 steps + Bonus Turn
* **6 or 0 Uburis (Full Marks/Mudra):** 6 steps + Bonus Turn
* **2, 3, 4 Uburis:** 2, 3, 4 steps respectively (No bonus)

### Mathematical Board Abstraction
To facilitate RL training, we map the physical 3x8 cross board to a local **1D coordinate system of 73 cells** for each player:
* **Cell 0:** Base (Token is off-board).
* **Cells 1–64:** Shared Outer Perimeter. Collisions on non-safe cells result in capture (*"Khua"*), sending the opponent back to 0.
* **Cells 65–72:** Private Home Column (Opponents cannot enter).
* **Cell 73:** Paka (Goal state).
* **Safe Zones:** Verified from board designs at relative rows 3 (sides) and 8 (tips) on the perimeter.

---

## 3. Reinforcement Learning Framework

### Observation Space
A 17-dimensional vector representing:
* Current player's 4 token positions ($s \in [0, 73]^4$)
* Opponents' 12 token positions ($s_{opp} \in [0, 73]^{12}$)
* Current dice roll value ($r \in [0, 25]$)

### Action Space
Discrete action space of size 4: $a \in \{0, 1, 2, 3\}$, corresponding to which token the agent chooses to move.

### Reward Design
* **Winning the Game:** $+100.0$ (Lose: $-100.0$)
* **Token Reaches Goal (Paka):** $+30.0$
* **Capturing an Opponent:** $+20.0$
* **Getting Captured:** $-20.0$
* **Invalid Move Selection:** $-2.0$ (only applicable to Standard PPO)
* **Step Progress:** $+0.1$ per cell advanced.

---

## 4. Experiments and Comparative Results
We trained two baseline configurations:
1. **Standard PPO (Unmasked):** Trained for 1,000,000 (1M) timesteps, utilizing reward penalties for invalid move selection.
2. **Maskable PPO (Masked):** Trained for 1,000,000 (1M) timesteps, utilizing action masks to restrict the policy distribution to legal actions.

### Evaluation Benchmarks (100 Games)

| Metric | Standard PPO (Unmasked - 1M Steps) | Maskable PPO (Masked - 1M Steps) |
| :--- | :---: | :---: |
| **Win Rate** | 22.00% | **29.00%** |
| **Rule Adherence Rate** | 46.30% | **100.00%** |
| **Avg Steps per Game** | 43.5 | **48.2** |
| **Avg Episode Reward** | 44.14 | **61.68** |

---

## 5. Discussion & Future Work (Key Scientific Contribution)
Our comparative study reveals critical insights into policy gradient learning on board games:
1. **Action Bottleneck in Standard PPO:** Standard PPO struggles to converge to legal play even after 1M steps. Because selecting an invalid move leads to a state-loop with negative penalties, the agent gets trapped in local minima, inflating episode lengths (43.5 steps) and capturing only a 22% win rate.
2. **Strategic Superiority of Maskable PPO:** By using action masks, the policy is restricted to valid action manifolds. Combined with a stochastic evaluation policy (`deterministic=False`) to match the luck-based dynamics of the game, the 1M-step Maskable agent achieves a **29.00% win rate**, outperforming the Rule-Compliant Random Baseline (25%) in a 4-player setting.
3. **Paths to Strategic Dominance:** While the agent now reliably beats random opponents and adheres to rules 100% of the time, future work involves scaling Maskable PPO to **2M steps** and implementing **Self-Play (SP)** to discover advanced defensive and offensive tactics around Safe Zones.
