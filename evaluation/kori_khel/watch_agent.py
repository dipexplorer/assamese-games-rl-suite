import os
import sys
import time

# Resolve project root dynamically (three levels up from script)
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from environments.kori_khel_env import KoriKhelEnv
from stable_baselines3 import PPO
from sb3_contrib import MaskablePPO
from sb3_contrib.common.wrappers import ActionMasker

def mask_fn(env):
    """Callback function that returns the action mask from the environment."""
    return env.action_masks()

def watch_game():
    """Loads either Maskable PPO or Standard PPO and runs a step-by-step game demo."""
    print("\n============================================================")
    print("🏆 KORI KHEL MODEL WATCHER 🏆")
    print("============================================================")
    print("Select AI Algorithm to watch:")
    print("1. Maskable PPO (Masked Model - 100% Rule Compliance)")
    print("2. Standard PPO (Unmasked Model - Baseline)")
    print("============================================================")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    raw_env = KoriKhelEnv()
    
    if choice == "1":
        # Wrap environment with ActionMasker for Maskable PPO
        env = ActionMasker(raw_env, mask_fn)
        model_path = os.path.join(project_root, "agents", "kori_khel", "maskable_ppo_kori_khel.zip")
        if not os.path.exists(model_path):
            print(f"Error: Model file not found at {model_path}. Please train it first.")
            return
        print(f"\nLoading Maskable PPO model from: {model_path}")
        model = MaskablePPO.load(model_path)
        is_masked = True
    elif choice == "2":
        # Use raw environment for Standard PPO
        env = raw_env
        model_path = os.path.join(project_root, "agents", "kori_khel", "ppo_kori_khel.zip")
        if not os.path.exists(model_path):
            print(f"Error: Model file not found at {model_path}. Please train it first.")
            return
        print(f"\nLoading Standard PPO model from: {model_path}")
        model = PPO.load(model_path)
        is_masked = False
    else:
        print("Invalid choice. Exiting.")
        return

    # Reset environment
    obs, info = env.reset()
    
    print("\n============================================================")
    print("GAME INITIALIZED")
    print("============================================================")
    print(raw_env.render())
    print("============================================================\n")
    
    step_count = 0
    terminated = False
    truncated = False
    
    while not terminated and not truncated:
        step_count += 1
        input(f"👉 [Step {step_count}] Press Enter to see AI's move...")
        
        roll = raw_env.current_roll
        valid_moves = raw_env.engine.get_valid_moves(0, roll)
        
        # Predict action based on chosen model configuration
        if is_masked:
            action_mask = env.action_masks()
            action, _states = model.predict(obs, action_masks=action_mask, deterministic=False)
        else:
            action, _states = model.predict(obs, deterministic=False)
            
        action = int(action)
        
        # Save old position for reporting
        old_position = raw_env.engine.players[0].tokens[action].position
        
        # Step the environment
        obs, reward, terminated, truncated, info = env.step(action)
        
        new_position = raw_env.engine.players[0].tokens[action].position
        
        # Print description of the step
        print("\n------------------------------------------------------------")
        print(f"🤖 AI rolled {roll} | Valid tokens: {valid_moves}")
        
        if not is_masked and "invalid" in info:
            print(f"❌ Action: Selected Token {action} (ILLEGAL MOVE!) | Penalty: -2.0")
        else:
            print(f"🎯 Action: Selected Token {action} | Moved: Cell {old_position} -> Cell {new_position}")
            
        if new_position == 73 and old_position < 73:
            print("🎉 Success: Token reached the Goal (Paka)!")
        
        # Render current state
        print("------------------------------------------------------------")
        print(raw_env.render())
        print("------------------------------------------------------------\n")
        
        time.sleep(0.3)
        
    print("============================================================")
    print("🏁 GAME OVER 🏁")
    print("============================================================")
    winner = raw_env.engine.winner
    if winner == 0:
        print("🏆 Congratulations! AI (Player 0) WON the game!")
    else:
        print(f"💀 AI Lost. Opponent Player {winner} won the game.")
    print("============================================================\n")

if __name__ == "__main__":
    watch_game()
