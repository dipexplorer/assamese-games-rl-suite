import sys
import os
import random

# Add project root to path so we can import environments
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from environments.kori_khel_env import KoriKhelEnv

def test_random_agent_gym_env(episodes=5):
    """
    Runs a random agent on the Gymnasium environment for a few episodes
    to verify that step transitions, rewards, and terminations work correctly.
    """
    print(f"Starting Random Agent Test on Gymnasium Environment ({episodes} episodes)...")
    print("=" * 70)

    env = KoriKhelEnv()
    
    for ep in range(episodes):
        obs, info = env.reset()
        terminated = False
        truncated = False
        step_count = 0
        total_reward = 0.0
        
        while not terminated and not truncated:
            # Check the roll from observation (last element)
            roll = obs[16]
            
            # Find valid actions manually to avoid invalid moves penalty
            # The agent can move tokens 0, 1, 2, or 3
            valid_actions = env.engine.get_valid_moves(0, roll)
            
            if not valid_actions:
                # If no valid actions are possible, the environment should have automatically
                # skipped the turn (which is handled inside reset() and step()).
                # If we are here, it means we have a roll but no valid actions, which is an error.
                raise ValueError(f"Error: Agent turn active but no valid actions for roll {roll}!")
                
            # Randomly select a valid action
            action = random.choice(valid_actions)
            
            # Step the environment
            next_obs, reward, terminated, truncated, step_info = env.step(action)
            
            total_reward += reward
            step_count += 1
            obs = next_obs
            
            # Print periodic updates
            if step_count % 50 == 0:
                print(f"Episode {ep+1} | Step {step_count:4d} | Roll: {roll:2d} | Action: {action} | Step Reward: {reward:6.2f} | Total Reward: {total_reward:6.2f}")
                
        print(f"✨ Episode {ep+1} Finished | Total Steps: {step_count} | Total Reward: {total_reward:6.2f} | Winner: Player {env.engine.winner}")
        print("-" * 70)
        
    print("Gymnasium Environment verification successful! All transitions and reward scaling worked without errors.")

if __name__ == "__main__":
    # Seed for repeatability
    random.seed(42)
    test_random_agent_gym_env()
