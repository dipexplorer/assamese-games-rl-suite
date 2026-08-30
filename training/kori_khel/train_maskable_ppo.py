import os
import sys
import matplotlib.pyplot as plt
import numpy as np

# Add project root to path so we can import environments (three levels up)
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from environments.kori_khel_env import KoriKhelEnv
from sb3_contrib import MaskablePPO
from sb3_contrib.common.wrappers import ActionMasker
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.results_plotter import load_results, ts2xy

def mask_fn(env):
    """Callback function that returns the action mask from the environment."""
    return env.action_masks()

def train_maskable_agent(total_timesteps=200000):
    """
    Trains a MaskablePPO agent on the Kori Khel environment using action masking.
    Saves the model and the training learning curve graph.
    """
    # Create directories for saving models and logs (dynamically resolved to project root)
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    log_dir = os.path.join(project_root, "training", "kori_khel", "logs_maskable")
    model_dir = os.path.join(project_root, "agents", "kori_khel")
    plot_dir = os.path.join(project_root, "evaluation", "kori_khel", "plots")
    
    os.makedirs(log_dir, exist_ok=True)
    os.makedirs(model_dir, exist_ok=True)
    os.makedirs(plot_dir, exist_ok=True)

    print("Setting up Gymnasium Environment with ActionMasker wrapper...")
    # Instantiate raw environment
    raw_env = KoriKhelEnv()
    # Wrap it with ActionMasker
    wrapped_env = ActionMasker(raw_env, mask_fn)
    # Monitor wrapper to log episodic rewards/steps
    env = Monitor(wrapped_env, log_dir)

    print("Configuring MaskablePPO Model (MLP Policy)...")
    # Initialize MaskablePPO model
    model = MaskablePPO(
        "MlpPolicy",
        env,
        learning_rate=3e-4,
        n_steps=2048,
        batch_size=64,
        n_epochs=10,
        gamma=0.99,
        gae_lambda=0.95,
        clip_range=0.2,
        ent_coef=0.01,
        verbose=1,
        tensorboard_log=os.path.join(log_dir, "tb")
    )

    print(f"Starting training for {total_timesteps} timesteps...")
    model.learn(total_timesteps=total_timesteps)

    # Save model weights
    model_path = os.path.join(model_dir, "maskable_ppo_kori_khel.zip")
    model.save(model_path)
    print(f"🏆 Maskable Model saved successfully to: {model_path}")

    # Generate Learning Curve Plot
    print("Generating learning curve plot...")
    try:
        x, y = ts2xy(load_results(log_dir), 'timesteps')
        if len(x) > 0:
            # Smooth the rewards
            window = min(50, len(y))
            y_smoothed = np.convolve(y, np.ones(window)/window, mode='valid')
            x_smoothed = x[window-1:]
            
            plt.figure(figsize=(10, 5))
            plt.plot(x, y, alpha=0.2, color='green', label='Raw Episode Reward')
            plt.plot(x_smoothed, y_smoothed, color='darkgreen', linewidth=2, label='Smoothed Reward (Moving Avg)')
            plt.title("Kori Khel Maskable PPO Training Learning Curve")
            plt.xlabel("Timesteps")
            plt.ylabel("Episode Reward")
            plt.grid(True)
            plt.legend()
            
            plot_path = os.path.join(plot_dir, "maskable_reward_curve.png")
            plt.savefig(plot_path)
            plt.close()
            print(f"📈 Learning curve graph saved to: {plot_path}")
        else:
            print("Warning: No training results found to plot.")
    except Exception as e:
        print(f"Error plotting learning curve: {e}")

if __name__ == "__main__":
    # Train for 1,000,000 steps (1M) with masking for strategic convergence
    train_maskable_agent(total_timesteps=1000000)
