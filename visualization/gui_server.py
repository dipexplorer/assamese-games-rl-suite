import os
import sys
import numpy as np
from flask import Flask, jsonify, render_template, request

# Resolve project root dynamically (two levels up from script)
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from environments.kori_khel_env import KoriKhelEnv
from stable_baselines3 import PPO
from sb3_contrib import MaskablePPO
from sb3_contrib.common.wrappers import ActionMasker

app = Flask(__name__, template_folder="templates")

# Global environment and model pointers
env = None
model = None
model_type = None  # "masked" or "unmasked"

def mask_fn(e):
    return e.action_masks()

@app.route("/")
def index():
    """Serves the main board UI visualization page."""
    return render_template("index.html")

@app.route("/reset", methods=["POST"])
def reset_game():
    """Resets the environment and loads the selected AI model configuration."""
    global env, model, model_type
    data = request.get_json() or {}
    model_type = data.get("model", "masked")
    
    raw_env = KoriKhelEnv()
    
    if model_type == "masked":
        # Wrap environment with ActionMasker for Maskable PPO
        env = ActionMasker(raw_env, mask_fn)
        model_path = os.path.join(project_root, "agents", "kori_khel", "maskable_ppo_kori_khel.zip")
        if os.path.exists(model_path):
            model = MaskablePPO.load(model_path)
        else:
            model = None
    else:
        # Use raw environment for Standard PPO
        env = raw_env
        model_path = os.path.join(project_root, "agents", "kori_khel", "ppo_kori_khel.zip")
        if os.path.exists(model_path):
            model = PPO.load(model_path)
        else:
            model = None

    obs, info = env.reset()
    raw = env.unwrapped
    
    return jsonify({
        "status": "initialized",
        "roll": int(raw.current_roll),
        "valid_moves": [int(x) for x in raw.engine.get_valid_moves(0, raw.current_roll)],
        "positions": get_positions(raw),
        "current_player": int(raw.engine.current_player),
        "winner": raw.engine.winner,
        "game_over": raw.engine.game_over,
        "bonus_turn": bool(raw.bonus_turn)
    })

@app.route("/step", methods=["POST"])
def step_game():
    """Performs a single step (AI action execution) and returns updated board state."""
    global env, model, model_type
    if env is None:
        return jsonify({"error": "Game not initialized. Call /reset first."}), 400
        
    raw = env.unwrapped
    if raw.engine.game_over:
        return jsonify({
            "game_over": True,
            "winner": raw.engine.winner,
            "positions": get_positions(raw)
        })

    if model is None:
        # Fallback if no model is found (take random valid move)
        valid_moves = raw.engine.get_valid_moves(0, raw.current_roll)
        if valid_moves:
            action = int(np.random.choice(valid_moves))
        else:
            action = 0
    else:
        # Get current state observation
        obs = env._get_obs()
        
        # Predict action
        if model_type == "masked":
            action_mask = env.action_masks()
            action, _states = model.predict(obs, action_masks=action_mask, deterministic=False)
        else:
            action, _states = model.predict(obs, deterministic=False)
        action = int(action)
        
    # Capture state values before step
    old_pos = int(raw.engine.players[0].tokens[action].position)
    roll = int(raw.current_roll)
    valid_moves = [int(x) for x in raw.engine.get_valid_moves(0, roll)]
    
    # Step environment
    obs, reward, terminated, truncated, info = env.step(action)
    new_pos = int(raw.engine.players[0].tokens[action].position)
    
    # Check invalid flag for unmasked PPO
    is_invalid = "invalid" in info
    
    return jsonify({
        "roll": int(raw.current_roll),
        "valid_moves": [int(x) for x in raw.engine.get_valid_moves(0, raw.current_roll)],
        "positions": get_positions(raw),
        "action_token": action,
        "old_pos": old_pos,
        "new_pos": new_pos,
        "action_roll": roll,
        "action_valid_moves": valid_moves,
        "reward": float(reward),
        "is_invalid": is_invalid,
        "current_player": int(raw.engine.current_player),
        "winner": raw.engine.winner,
        "game_over": raw.engine.game_over,
        "bonus_turn": bool(raw.bonus_turn)
    })

def get_positions(raw):
    """Formats player token positions into a JSON-friendly dict."""
    positions = {}
    for p_id in range(4):
        positions[f"p{p_id}"] = [int(t.position) for t in raw.engine.players[p_id].tokens]
    return positions

if __name__ == "__main__":
    print("------------------------------------------------------------")
    print("📈 KORI KHEL WEB INTERACTIVE DASHBOARD SERVER")
    print("------------------------------------------------------------")
    app.run(host="0.0.0.0", port=5000, debug=True)
