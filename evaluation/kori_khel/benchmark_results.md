# Kori Khel PPO Agent Evaluation Benchmark (2,000,000 Steps)

This benchmark evaluates our trained model-free PPO agent against simulated random opponents over 100 full games.

---

## 📊 Final Evaluation Metrics

* **Total Games Played:** 100
* **PPO Agent Win Rate:** 22.00% (22/100 games)
* **Opponents Win Rate:** 78.00%
* **Average Steps per Game:** 43.5
* **Average Episode Reward:** 44.14
* **AI Rule Adherence Rate:** 46.3%

---

## 🔍 Key Research Insights (Post-2M Training)

1. **Rule Adherence Bottleneck**:
   Our PPO agent trained for 2M steps achieved a **46.3% rule adherence rate**, which is comparable to the 100k step baseline (49.8%). This indicates a learning plateau. 
   
2. **State-Action Traps**:
   Because standard PPO does not support action masking out-of-the-box, when the agent selects an invalid move (e.g. choosing a locked token), it receives a `-2.0` penalty and the environment state remains unchanged. 
   
   Since the state and the dice roll do not change, the policy network frequently gets stuck in a loop selecting the same invalid move multiple times during a single game, inflating the episode length and accumulating negative reward gradients.

3. **Critical Recommendations for Abstract**:
   - To achieve 100% rule adherence and exceed the random win-rate baseline, future work must utilize **Action Masking** (e.g. using `MaskablePPO` from SB3-Contrib) to completely prevent the policy network from selecting illegal actions.
   - Self-play training is also recommended to allow the agent to learn advanced defensive strategies around the verified Safe Zones.
