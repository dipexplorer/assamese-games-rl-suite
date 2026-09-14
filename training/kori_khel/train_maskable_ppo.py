import os
import sys
import matplotlib.pyplot as plt
import numpy as np

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from environments.kori_khel_env import KoriKhelEnv
from sb3_contrib import MaskablePPO
from sb3_contrib.common.wrappers import ActionMasker
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.results_plotter import load_results, ts2xy


def mask_fn(env):
    """Returns the boolean action mask from the Gymnasium environment."""
    return env.action_masks()


def linear_schedule(initial_value: float, final_value: float = 5e-5):
    """Linear learning rate decay schedule."""
    def func(progress_remaining: float) -> float:
        return final_value + progress_remaining * (initial_value - final_value)
    return func


def train_maskable_agent(total_timesteps=2_000_000):
    """Trains a MaskablePPO agent on Kori Khel with invalid action masking."""
    log_dir   = os.path.join(PROJECT_ROOT, "training", "kori_khel", "logs_maskable")
    model_dir = os.path.join(PROJECT_ROOT, "agents", "kori_khel")
    plot_dir  = os.path.join(PROJECT_ROOT, "evaluation", "kori_khel", "plots")

    os.makedirs(log_dir,   exist_ok=True)
    os.makedirs(model_dir, exist_ok=True)
    os.makedirs(plot_dir,  exist_ok=True)

    print("Setting up Gymnasium Environment with ActionMasker wrapper...")
    raw_env     = KoriKhelEnv()
    wrapped_env = ActionMasker(raw_env, mask_fn)
    env         = Monitor(wrapped_env, log_dir)

    print("Configuring MaskablePPO Model (MLP Policy)...")
    model = MaskablePPO(
        "MlpPolicy",
        env,
        learning_rate=linear_schedule(3e-4, 5e-5),
        n_steps=2048,
        batch_size=64,
        n_epochs=10,
        gamma=0.995,
        gae_lambda=0.95,
        clip_range=0.2,
        ent_coef=0.005,
        verbose=1,
        tensorboard_log=os.path.join(log_dir, "tb")
    )

    print(f"Starting training for {total_timesteps} timesteps...")
    model.learn(total_timesteps=total_timesteps)

    model_path = os.path.join(model_dir, "maskable_ppo_kori_khel.zip")
    model.save(model_path)
    print(f"Model saved to: {model_path}")


if __name__ == "__main__":
    train_maskable_agent(total_timesteps=2_000_000)
