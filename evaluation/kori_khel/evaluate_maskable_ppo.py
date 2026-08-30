import os
import sys
import numpy as np

# Add project root to path so we can import environments (three levels up)
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from environments.kori_khel_env import KoriKhelEnv
from sb3_contrib import MaskablePPO
from sb3_contrib.common.wrappers import ActionMasker

def mask_fn(env):
    """Callback function that returns the action mask from the environment."""
    return env.action_masks()

def get_env_mask(env):
    """Robust helper to extract the action mask by traversing any wrapper chain."""
    current_env = env
    while not hasattr(current_env, 'action_masks'):
        if hasattr(current_env, 'env'):
            current_env = current_env.env
        else:
            break
    return current_env.action_masks()

def evaluate_maskable_agent(model_path, num_episodes=100):
    """
    Evaluates the trained MaskablePPO agent against random opponents over 100 games
    and prints the average win rate, steps, and reward metrics.
    """
    print(f"Loading trained Maskable PPO model from: {model_path}")
    if not os.path.exists(model_path):
        print(f"Error: Model file not found at {model_path}")
        return

    # Load the model
    model = MaskablePPO.load(model_path)
    
    # Create and wrap evaluation environment
    raw_env = KoriKhelEnv()
    env = ActionMasker(raw_env, mask_fn)
    
    ppo_wins = 0
    opponent_wins = 0
    total_steps = 0
    total_rewards = 0.0
    fallback_actions_count = 0
    total_actions_count = 0

    print(f"Starting evaluation of {num_episodes} games...")
    print("=" * 60)

    for ep in range(num_episodes):
        obs, info = env.reset()
        terminated = False
        truncated = False
        ep_reward = 0.0
        ep_steps = 0
        
        while not terminated and not truncated:
            valid_moves = raw_env.engine.get_valid_moves(0, obs[16])
            
            # Guard check: If no valid moves are available (e.g. if game is over)
            if not valid_moves:
                action = 0  # Dummy action, will trigger the step() game_over check
            else:
                # Extract action mask for the current state
                action_mask = get_env_mask(env)
                
                # Predict action utilizing the action mask (stochastic evaluation for stochastic board games)
                action, _states = model.predict(obs, action_masks=action_mask, deterministic=False)
                action = int(action)
                
                total_actions_count += 1
                
                # Double check if PPO's masked output is legally valid
                if action not in valid_moves:
                    # This should NEVER happen with Action Masking
                    fallback_actions_count += 1
                    action = int(np.random.choice(valid_moves))
                
            obs, reward, terminated, truncated, info = env.step(action)
            ep_reward += reward
            ep_steps += 1
            
        total_steps += ep_steps
        total_rewards += ep_reward
        
        # Check who won
        if raw_env.engine.winner == 0:
            ppo_wins += 1
        else:
            opponent_wins += 1
            
        if (ep + 1) % 10 == 0:
            print(f"Games played: {ep+1:3d}/{num_episodes} | PPO Wins: {ppo_wins:2d} | Win Rate: {(ppo_wins/(ep+1))*100:5.1f}%")

    # Final calculations
    win_rate = (ppo_wins / num_episodes) * 100
    avg_steps = total_steps / num_episodes
    avg_reward = total_rewards / num_episodes
    rule_adherence = ((total_actions_count - fallback_actions_count) / total_actions_count) * 100

    print("=" * 60)
    print("🏆 FINAL MASKABLE PPO EVALUATION RESULTS 🏆")
    print("=" * 60)
    print(f"PPO Agent Win Rate    : {win_rate:.2f}% ({ppo_wins}/{num_episodes} games)")
    print(f"Opponents Win Rate    : {(opponent_wins/num_episodes)*100:.2f}%")
    print(f"Average Steps per Game: {avg_steps:.1f}")
    print(f"Average Episode Reward: {avg_reward:.2f}")
    print(f"AI Rule Adherence Rate: {rule_adherence:.1f}%")
    print("-" * 60)
    print(f"Rule Adherence Note: The Maskable agent chose legally valid actions {rule_adherence:.1f}% of the time.")
    print("============================================================\n")

    # Save results to markdown for reference
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    results_path = os.path.join(project_root, "evaluation", "kori_khel", "benchmark_results_maskable.md")
    os.makedirs(os.path.dirname(results_path), exist_ok=True)
    with open(results_path, "w") as f:
        f.write(f"# Kori Khel Maskable PPO Agent Evaluation Benchmark\n\n")
        f.write(f"- **Total Games Played:** {num_episodes}\n")
        f.write(f"- **Maskable PPO Agent Win Rate:** {win_rate:.2f}%\n")
        f.write(f"- **Average steps per game:** {avg_steps:.1f}\n")
        f.write(f"- **Average episode reward:** {avg_reward:.2f}\n")
        f.write(f"- **AI Rule Adherence:** {rule_adherence:.1f}% (Expected: 100.0%)\n")
    print(f"Results saved to: {results_path}")

if __name__ == "__main__":
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    model_path = os.path.join(project_root, "agents", "kori_khel", "maskable_ppo_kori_khel.zip")
    evaluate_maskable_agent(model_path, num_episodes=100)
