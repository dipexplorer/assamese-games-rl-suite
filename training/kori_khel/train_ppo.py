import os
import sys
import matplotlib.pyplot as plt
import numpy as np

# Add project root to path so we can import environments (three levels up)
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from environments.kori_khel_env import KoriKhelEnv
from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.results_plotter import load_results, ts2xy

def train_agent(total_timesteps=100000):
    """
    Trains a PPO agent on the Kori Khel environment and saves the model
    and the training learning curve graph.
    """
    print("Initializing training directories...")
    # Create directories for saving models and logs
    log_dir = "training/kori_khel/logs/"
    model_dir = "agents/kori_khel/"
    plot_dir = "evaluation/kori_khel/plots/"
    
    os.makedirs(log_dir, exist_ok=True)
    os.makedirs(model_dir, exist_ok=True)
    os.makedirs(plot_dir, exist_ok=True)

    print("Setting up Gymnasium Environment...")
    env = KoriKhelEnv()
    # Wrap environment to monitor and log rewards
    env = Monitor(env, log_dir)

    print("Configuring PPO Model (MLP Policy)...")
    # MLP Policy (multi-layer perceptron) fits our flat Box state representation perfectly
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
        tensorboard_log=os.path.join(log_dir, "tb/")
    )

    print(f"Starting training for {total_timesteps} timesteps...")
    model.learn(total_timesteps=total_timesteps)

    # Save the trained model
    model_path = os.path.join(model_dir, "ppo_kori_khel.zip")
    model.save(model_path)
    print(f"🏆 Model saved successfully to: {model_path}")

    # Plot the learning curve
    print("Generating learning curve plot...")
    plot_results(log_dir, plot_dir)

def plot_results(log_dir, plot_dir):
    """Loads monitor logs and plots the smoothed training reward."""
    x, y = ts2xy(load_results(log_dir), "timesteps")
    
    # Apply moving average to smooth the curve
    window = 50
    if len(y) > window:
        y_smoothed = np.convolve(y, np.ones(window)/window, mode='valid')
        x_smoothed = x[window-1:]
    else:
        y_smoothed = y
        x_smoothed = x

    plt.figure(figsize=(10, 5))
    plt.plot(x, y, alpha=0.2, color='blue', label='Raw Episode Reward')
    plt.plot(x_smoothed, y_smoothed, color='red', linewidth=2, label='Smoothed Reward (Moving Avg)')
    plt.title("Kori Khel PPO Training Learning Curve")
    plt.xlabel("Timesteps")
    plt.ylabel("Episode Reward")
    plt.grid(True)
    plt.legend()
    
    plot_path = os.path.join(plot_dir, "reward_curve.png")
    plt.savefig(plot_path)
    plt.close()
    print(f"📈 Learning curve graph saved to: {plot_path}")

if __name__ == "__main__":
    # Default is set to 10,000 for a true 1-minute quick local test.
    # Use 2,000,000 steps to reproduce research baseline results.
    train_agent(total_timesteps=10000)
