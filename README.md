# Assamese Traditional Games RL Suite

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Computational Formalization and Reinforcement Learning Baselines for Assamese Traditional Games.**

This repository contains the codebase for our ongoing research to map indigenous, asymmetric multi-agent games of Assam into standard Markov Decision Process (MDP) frameworks. The project provides `OpenAI Gymnasium` environments to benchmark policy gradient algorithms (like PPO) against complex topological constraints and skewed stochastic mechanics that are absent in standard Western board game benchmarks (like Chess or Go).

*This project is targeting the **IndoML 2026 (Undergraduate Forum)**.*

---

## 🕹️ Current Environments

### 1. Kori Khel (`KoriKhelEnv-v0`)
A 4-player stochastic cowrie-shell race game featuring a 73-state continuous track per player, asymmetric binomial dice rolls (where $P(\text{Jagowa}) \approx 9.38\%$), safe-zone sanctuaries, and capture mechanics.

**Key RL Challenge:** The strict entry constraint (requiring an exact roll of 10 to leave the Base) creates a severe action bottleneck. Standard PPO fails to learn legal play (46% rule adherence) due to this penalty minimum, making Kori Khel a highly effective testbed for **invalid action masking**. 

*Our Maskable PPO baseline achieves 100% legal play and a 30% win rate against a 4-player random baseline.*

## 🚀 Installation

Clone the repository and install the required dependencies:

```bash
git clone https://github.com/dipexplorer/assamese-games-rl-suite.git
cd assamese-games-rl-suite

# It is recommended to use a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate

pip install -r requirements.txt
```

## 🎮 Running the Environments

### 1. Training the Maskable PPO Baseline
To train the Maskable PPO agent on the Kori Khel environment:
```bash
python -m training.kori_khel.train_maskable
```

### 2. Launching the Interactive Web UI
We provide a Flask-based interactive web board to visualize agent evaluation in real-time.
```bash
python visualization/gui_server.py
```
Then navigate to `http://127.0.0.1:5000` in your browser.

## 🗺️ Roadmap (Future Modules)

This suite is being actively developed. The following games are slated for future formalization:

- **[In Progress] Dhop Khel (ঢোপ খেল):** Transitioning from discrete board MDPs to continuous 2D spatial coordinate systems with multi-agent ball-possession and tagging dynamics under partial observability.
- **Tekeli Bhonga (টেকেলী ভঙা):** Spatial awareness and precision targeting game modeling POMDP spatial navigation constraints.
- **Koni Juj (কণী যুঁজ):** Tactical collision MDP testing shell structural integrity prediction.
- **Ha-Doo-Doo (হা-ডু-ডু):** High-density continuous territory-control modeling breath-duration constraint tagging.

## 📖 Citation

If you use these environments or baselines in your research, please cite our IndoML 2026 paper:

```bibtex
@inproceedings{das2026korikhel,
  title={Computational Formalization and Reinforcement Learning Baselines for Assamese Traditional Games: A Case Study on Kori Khel},
  author={Das, Dipjyoti and Sharma, Simanata and Bhattacharyya, Rupam},
  booktitle={7th Indian Symposium on Machine Learning (IndoML) - Undergraduate Forum},
  year={2026},
  address={Kolkata, India}
}
```

## 👨‍💻 Authors & Affiliation
- **Dipjyoti Das**
- **Simanta Sharma**
- **Rupam Bhattacharyya (Advisor)**

*Department of Information Technology, Gauhati University, Assam, India*
