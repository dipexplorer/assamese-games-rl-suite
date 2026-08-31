import os
import sys
import time

# Resolve project root dynamically (three levels up from script)
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from environments.kori_khel_env import KoriKhelEnv
from sb3_contrib import MaskablePPO
from sb3_contrib.common.wrappers import ActionMasker

def mask_fn(env):
    """Callback function that returns the action mask from the environment."""
    return env.action_masks()

def watch_game():
    """Loads the trained Maskable PPO model and plays a single game step-by-step in the console."""
    # Instantiate and wrap the environment
    raw_env = KoriKhelEnv()
    env = ActionMasker(raw_env, mask_fn)
    
    model_path = os.path.join(project_root, "agents", "kori_khel", "maskable_ppo_kori_khel.zip")
    if not os.path.exists(model_path):
        print(f"Error: Model not found at {model_path}. Please train it first.")
        return
        
    print(f"Loading trained Maskable PPO model from: {model_path}")
    model = MaskablePPO.load(model_path)
    
    # Reset environment
    obs, info = env.reset()
    
    print("\n============================================================")
    print("🏆 KORI KHEL INTERACTIVE VISUAL WATCH SCRIPT 🏆")
    print("============================================================")
    print(raw_env.render())
    print("============================================================\n")
    
    step_count = 0
    terminated = False
    truncated = False
    
    while not terminated and not truncated:
        step_count += 1
        input(f"👉 [Step {step_count}] Press Enter to see AI's move...")
        
        # Extract current state details for printing
        roll = raw_env.current_roll
        valid_moves = raw_env.engine.get_valid_moves(0, roll)
        
        # Predict action (using stochastic mode for organic play)
        action_mask = env.action_masks()
        action, _states = model.predict(obs, action_masks=action_mask, deterministic=False)
        action = int(action)
        
        # Get movement details before stepping
        old_position = raw_env.engine.players[0].tokens[action].position
        
        # Step the environment
        obs, reward, terminated, truncated, info = env.step(action)
        
        new_position = raw_env.engine.players[0].tokens[action].position
        
        # Print description of the move
        print("\n------------------------------------------------------------")
        print(f"🤖 AI (Player 0) rolled {roll} | Valid tokens: {valid_moves}")
        print(f"🎯 Action: Selected Token {action} | Moved: Cell {old_position} -> Cell {new_position}")
        
        # Display capture/goal notices
        if new_position == 73:
            print("🎉 Success: Token reached the Goal (Paka)!")
        
        # Render the updated board state
        print("------------------------------------------------------------")
        print(raw_env.render())
        print("------------------------------------------------------------\n")
        
        time.sleep(0.5)
        
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
