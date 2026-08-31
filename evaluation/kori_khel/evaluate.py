import os
import sys
import numpy as np

# Add project root to path so we can import environments (three levels up)
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from environments.kori_khel_env import KoriKhelEnv
from stable_baselines3 import PPO

def evaluate_agent(model_path, num_episodes=100):
    """
    Evaluates the trained PPO agent against random opponents over 100 games
    and prints the average win rate, steps, and reward metrics.
    """
    print(f"Loading trained PPO model from: {model_path}")
    if not os.path.exists(model_path):
        print(f"Error: Model file not found at {model_path}")
        return

    # Load the model
    model = PPO.load(model_path)
    
    # Create evaluation environment
    env = KoriKhelEnv()
    
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
            roll = obs[16]
            valid_moves = env.engine.get_valid_moves(0, roll)
            
            # Guard check: If no valid moves are available (e.g. if game is over)
            if not valid_moves:
                action = 0  # Dummy action, will trigger the step() game_over check
            else:
                # PPO Model predicts the action (deterministic=True for evaluation)
                action, _states = model.predict(obs, deterministic=True)
                action = int(action)  # Convert numpy int to Python int
                
                total_actions_count += 1
                
                # --- EVALUATION FALLBACK ---
                # If PPO predicts an invalid move (since standard SB3 PPO doesn't support action masking out-of-the-box),
                # we apply a fallback to choose a valid action, but log it to see if PPO has learned the rules.
                if action not in valid_moves:
                    fallback_actions_count += 1
                    action = int(np.random.choice(valid_moves))
                
            obs, reward, terminated, truncated, info = env.step(action)
            ep_reward += reward
            ep_steps += 1
            
        total_steps += ep_steps
        total_rewards += ep_reward
        
        # Check who won
        if env.engine.winner == 0:
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
    print("🏆 FINAL EVALUATION RESULTS 🏆")
    print("=" * 60)
    print(f"PPO Agent Win Rate    : {win_rate:.2f}% ({ppo_wins}/{num_episodes} games)")
    print(f"Opponents Win Rate    : {(opponent_wins/num_episodes)*100:.2f}%")
    print(f"Average Steps per Game: {avg_steps:.1f}")
    print(f"Average Episode Reward: {avg_reward:.2f}")
    print(f"AI Rule Adherence Rate: {rule_adherence:.1f}%")
    print("-" * 60)
    print(f"Rule Adherence Note: The AI chose legally valid actions {rule_adherence:.1f}% of the time.")
    print("============================================================\n")

    # Save results to a markdown file for references
    results_path = "evaluation/kori_khel/benchmark_results.md"
    os.makedirs(os.path.dirname(results_path), exist_ok=True)
    with open(results_path, "w") as f:
        f.write(f"# Kori Khel PPO Agent Evaluation Benchmark\n\n")
        f.write(f"- **Total Games Played:** {num_episodes}\n")
        f.write(f"- **PPO Agent Win Rate:** {win_rate:.2f}%\n")
        f.write(f"- **Average steps per game:** {avg_steps:.1f}\n")
        f.write(f"- **Average episode reward:** {avg_reward:.2f}\n")
        f.write(f"- **AI Rule Adherence:** {rule_adherence:.1f}%\n")
    print(f"Results saved to: {results_path}")

if __name__ == "__main__":
    model_path = "agents/kori_khel/ppo_kori_khel.zip"
    evaluate_agent(model_path, num_episodes=100)
