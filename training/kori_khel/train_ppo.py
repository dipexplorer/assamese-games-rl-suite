import os
import sys
import matplotlib.pyplot as plt
import numpy as np

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from environments.kori_khel_env import KoriKhelEnv
from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.results_plotter import load_results, ts2xy


def train_agent(total_timesteps=1_000_000):
    """Trains a baseline PPO agent on the Kori Khel environment."""
    log_dir   = os.path.join(PROJECT_ROOT, "training", "kori_khel", "logs")
    model_dir = os.path.join(PROJECT_ROOT, "agents", "kori_khel")
    plot_dir  = os.path.join(PROJECT_ROOT, "evaluation", "kori_khel", "plots")

    os.makedirs(log_dir,   exist_ok=True)
    os.makedirs(model_dir, exist_ok=True)
    os.makedirs(plot_dir,  exist_ok=True)

    print("Setting up Gymnasium Environment...")
    env = Monitor(KoriKhelEnv(), log_dir)

    print("Configuring PPO Model (MLP Policy)...")
    model = PPO(
        "MlpPolicy",
        env,
        verbose=1,
        learning_rate=3e-4,
        n_steps=2048,
        batch_size=64,
        n_epochs=10,
        gamma=0.99,
        gae_lambda=0.95,
        clip_range=0.2,
        tensorboard_log=os.path.join(log_dir, "tb")
    )

    print(f"Starting training for {total_timesteps} timesteps...")
    model.learn(total_timesteps=total_timesteps)

    model_path = os.path.join(model_dir, "ppo_kori_khel.zip")
    model.save(model_path)
    print(f"Model saved to: {model_path}")

    _plot_results(log_dir, plot_dir)


def _plot_results(log_dir, plot_dir):
    """Loads monitor logs and plots smoothed training reward curve."""
    try:
        x, y = ts2xy(load_results(log_dir), "timesteps")
    except (FileNotFoundError, ValueError) as e:
        print(f"Could not generate plot: {e}")
        return

    window = min(50, len(y))
    if len(y) > window:
        y_smoothed = np.convolve(y, np.ones(window) / window, mode="valid")
        x_smoothed = x[window - 1:]
    else:
        y_smoothed, x_smoothed = y, x

    plt.figure(figsize=(10, 5))
    plt.plot(x, y, alpha=0.2, color="blue", label="Raw Episode Reward")
    plt.plot(x_smoothed, y_smoothed, color="red", linewidth=2, label="Smoothed Reward (Moving Avg)")
    plt.title("Kori Khel PPO — Training Learning Curve")
    plt.xlabel("Timesteps")
    plt.ylabel("Episode Reward")
    plt.grid(True)
    plt.legend()

    plot_path = os.path.join(plot_dir, "reward_curve.png")
    plt.savefig(plot_path)
    plt.close()
    print(f"Learning curve saved to: {plot_path}")


if __name__ == "__main__":
    train_agent(total_timesteps=1_000_000)
