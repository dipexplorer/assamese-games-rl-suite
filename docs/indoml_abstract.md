# Computational Formalization and Reinforcement Learning Baselines for Assamese Traditional Games: A Case Study on Kori Khel

**Target Venue:** IndoML 2026 (7th Indian Symposium on Machine Learning) — Undergraduate Forum  
**Venue & Date:** IIT Kharagpur Kolkata Extension Centre / Research Park | December 18–20, 2026  
**Authors:** Dipjyoti Das, Simanata Sharma, Rupam Bhattacharyya (Advisor)  
**Affiliation:** Department of Information Technology, Gauhati University, Assam, India  

---

## Abstract
Reinforcement Learning (RL) benchmark environments are predominantly focused on standardized Western board and video games. Consequently, indigenous multi-agent board games with asymmetric stochastic dynamics and complex topological constraints remain unmodeled in standard RL benchmark suites. In this paper, we present a computational formalization and Gymnasium environment for **Kori Khel**, a 4-player stochastic cowrie-shell board game native to Assam, India. We abstract the 2D cross-shaped board into a 73-state 1D Markov Decision Process (MDP) per player, incorporating asymmetric binomial dice distributions, safe zones, and capture mechanics. We evaluate baseline policy gradient performance using Proximal Policy Optimization (PPO) under two regimes: standard reward-penalty shaping and invalid action masking. Across a 100-game evaluation, Standard PPO fails to learn legal play (46% rule adherence) due to entry-state bottlenecks, whereas Maskable PPO achieves 100% rule adherence and a 30% win rate against rule-compliant random opponents in a 4-player setting (25% random baseline). We analyze why action masking is necessary in games with hard entry constraints and outline a path toward a broader suite of formalized regional games.

---

## 1. Introduction
**Kori Khel** is a 4-player cowrie-shell race game played across rural Assam, structurally resembling Pachisi/Ludo but characterized by a highly skewed binomial dice distribution and a strict entry constraint: tokens remain trapped off-board ($s=0$) until an exact roll (*Jagowa*) is obtained. This entry rule induces a severely bottlenecked action space where reward-penalty shaping fails to guide unmasked policy gradient methods, making Kori Khel an ideal testbed for invalid action masking techniques.

While RL has been benchmarked extensively on Chess, Go, and StarCraft II, regional games such as Kori Khel lack computational state-space definitions. In this work, we formalize Kori Khel from scratch, establishing:
1. A formal state-space specification of Kori Khel, mapping its physical 2D cross grid to a 73-state 1D coordinate system.
2. An open-source OpenAI Gymnasium environment (`KoriKhelEnv`).
3. Comparative baseline benchmarks evaluating Standard PPO versus Maskable PPO under stochastic dice conditions.

---

## 2. Kori Khel Game Formalization

### 2.1 Asymmetric Stochastic Roll Model
Kori Khel is played with 6 cowrie shells (*kori*). The outcome of a throw is defined by the number of shells landing face-down (*uburi*), modeled as a binomial variable $K \sim \text{Binomial}(6, p=0.5)$:

$$\mathbb{P}(K = k) = \binom{6}{k} (0.5)^6$$

- **Pochi ($k=5$, 1 Open, 5 Closed):** 25 steps + Bonus Turn ($\mathbb{P} \approx 9.38\%$).
- **Jagowa ($k=1$, 5 Open, 1 Closed):** 10 steps + Bonus Turn ($\mathbb{P} \approx 9.38\%$) — *Mandatory entry roll required to release tokens from Base.*
- **Mudra ($k=0$, 6 Open, 0 Closed):** 12 steps + Bonus Turn ($\mathbb{P} \approx 1.56\%$).
- **Standard Throws ($k \in \{2, 3, 4, 6\}$):** 4, 3, 2, 6 steps respectively (No bonus turn).
- **3-Blow Rule:** Rolling 3 consecutive bonus turns invalidates all accumulated points for that turn.

### 2.2 Board Abstraction & MDP Mapping
The physical board consists of 4 arms arranged in a cross (➕), each with 3 columns of 8 cells. We map this 2D geometry into a **1D state sequence of 73 positions** for each player:
- **State $s = 0$ (Base):** Token is inactive off-board; requires a *Jagowa* (10) roll to enter state $1$.
- **States $s \in [1, 64]$ (Shared Outer Perimeter):** Shared 64-cell track traversed in a strict global **Anti-Clockwise** spiral. Collisions on non-safe cells result in capture (*"Khua"*), returning the opponent to $0$.
- **Safe Zones ($X$ Marks):** 12 designated sanctuary cells on the perimeter where collisions do not trigger capture.
- **States $s \in [65, 72]$ (Private Home Corridor):** Private 8-cell central corridor leading to the center.
- **State $s = 73$ (Ghai / Goal):** Terminal winning state (*"Pokoa"*). First player to move all 4 tokens to 73 wins.

---

## 3. Reinforcement Learning Architecture

### 3.1 Observation & Action Spaces
- **Observation Vector $\mathbf{o} \in \mathbb{Z}^{17}$:** Formatted as $[s_{0..3}, s^{\text{rel}}_{1..12}, r]$. We represent the 4 active agent token positions absolute ($s \in [0,73]$), while the 12 opponent token positions are mapped *relative* to the agent's start index to maintain rotational invariance across player seats. $r \in [0,25]$ denotes the current roll. Safe-zone status is implicitly inferred by the network from token scalar positions matching the 12 fixed sanctuary indices.
- **Action Space $a \in \{0, 1, 2, 3\}$:** Discrete action selecting which of the 4 agent tokens to advance.

### 3.2 Reward Design & Coefficient Justification
$$\mathcal{R}(s, a, s') = r_{\text{progress}} + r_{\text{event}}$$
- $r_{\text{progress}} = +0.1 \times (s' - s)$
- $r_{\text{capture}} = +20.0$ (Capturing opponent token) / $-20.0$ (Getting captured)
- $r_{\text{ghai}} = +30.0$ (Token reaching state 73)
- $r_{\text{win}} = +100.0$ (Winning the match) / $-100.0$ (Loss)
- $r_{\text{invalid}} = -2.0$ (Selecting an illegal move; Standard PPO only)

*Coefficient Justification:* Terminal match outcomes ($\pm 100$) set the primary value scale. The sub-goal reward for entering Ghai ($+30$) is scaled lower than match win ($+100$) because reaching Ghai for a single token is an intermediate milestone, not game termination. Capture incentives are symmetric ($\pm 20$) to model zero-sum tactical interactions without skewing value estimates. Step progress ($+0.1$) is an order of magnitude smaller than event rewards to prevent infinite-loop shaping exploitation, while $r_{\text{invalid}} = -2.0$ penalizes illegal moves without causing catastrophic policy collapse.

---

## 4. Empirical Evaluation & Baseline Results

We trained two agent configurations for **1,000,000 (1M) timesteps** against 3 rule-compliant random opponents:
1. **Standard PPO (Unmasked):** Relies on penalty shaping ($r_{\text{invalid}} = -2.0$) to learn valid moves.
2. **Maskable PPO (Masked):** Uses invalid-action masking to restrict policy distribution $\pi(a|s)$ to legal actions.

### 4.1 Quantitative Performance (100 Matches, Single 1M-Step Training Run)

| Metric | Standard PPO (1M Steps) | Maskable PPO (1M Steps) |
| :--- | :---: | :---: |
| **Win Rate** | 22% | **30%** |
| **Rule Adherence Rate** | 46% | **100%** |
| **Average Steps per Game** | 43.5 | **44.2** |
| **Average Episode Reward** | 44.14 | **59.49** |

### 4.2 Analytical Insights
Standard PPO fails to learn legal play (46% rule adherence) even after 1M steps. Because tokens at Base ($s=0$) require an exact roll of 10 to move, unmasked agents repeatedly sample illegal actions, getting trapped in local penalty minima. Conversely, Maskable PPO guarantees 100% legal play from step 1, achieving a **30% win rate** that outperforms the 4-player random baseline (25%). These metrics reflect a single training run per configuration; the raw curve in Fig. 1 retains expected variance due to stochastic cowrie rolls.

---

## 5. Conclusion & Future Work
This paper presented a formal MDP abstraction and Gymnasium benchmark environment for Kori Khel, proving that action masking is essential for overcoming entry-roll bottlenecks. Extending this framework to other regional games requires tailored state-space adaptations; for instance, formalizing **Dhop Khel** necessitates transitioning from our 73-state discrete single-track MDP to a continuous 2D spatial coordinate system with multi-agent ball-possession and tagging dynamics under partial observability.

---

## 6. References
1. **Berner, C., et al. (2019).** *Dota 2 with Large Scale Deep Reinforcement Learning.* arXiv:1912.06680.
2. **Huang, S., & Ontañón, S. (2022).** *A Closer Look at Invalid Action Masking in Policy Gradient Algorithms.* FLAIRS Conference.
3. **Schulman, J., et al. (2017).** *Proximal Policy Optimization Algorithms.* arXiv:1707.06347.
4. **Sutton, R. S., & Barto, A. G. (2018).** *Reinforcement Learning: An Introduction.* MIT Press.
