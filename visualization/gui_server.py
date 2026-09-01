import os
import sys
import numpy as np
from flask import Flask, jsonify, render_template

# Resolve project root dynamically (two levels up from script)
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from environments.kori_khel_env import KoriKhelEnv
from game_engines.kori_khel.engine import KoriKhelEngine, roll_kori
from sb3_contrib import MaskablePPO
from sb3_contrib.common.wrappers import ActionMasker

app = Flask(__name__, template_folder="templates")

# Global UI engine and RL model
ui_engine = None
current_roll = 0
bonus_turn = False
consecutive_bonus = 0
current_uburi = 0
model = None

# We keep a dummy KoriKhelEnv instance just to format observations for the AI model
dummy_env = KoriKhelEnv()

def get_positions(engine):
    """Formats player token positions into a JSON-friendly dict."""
    positions = {}
    for p_id in range(4):
        positions[f"p{p_id}"] = [int(t.position) for t in engine.players[p_id].tokens]
    return positions

@app.route("/")
def index():
    """Serves the Kori Khel interactive board visualization page."""
    return render_template("index.html")

@app.route("/reset", methods=["POST"])
def reset_game():
    """Resets the environment for step-by-step UI visualization."""
    global ui_engine, current_roll, bonus_turn, consecutive_bonus, current_uburi, model
    
    # 1. Initialize pure game engine (no RL skipping)
    temp_engine = KoriKhelEngine()
    
    # 2. Roll for the first player (Player 0)
    roll, bonus, uburi = roll_kori()
    
    # 3. Load model if needed
    model_path = os.path.join(project_root, "agents", "kori_khel", "maskable_ppo_kori_khel.zip")
    if os.path.exists(model_path):
        temp_model = MaskablePPO.load(model_path)
    else:
        temp_model = None

    # Commit state
    ui_engine = temp_engine
    current_roll = roll
    bonus_turn = bonus
    consecutive_bonus = 0
    current_uburi = uburi
    model = temp_model
    
    return jsonify({
        "status": "initialized",
        "roll": int(current_roll),
        "uburi": int(current_uburi),
        "valid_moves": [int(x) for x in ui_engine.get_valid_moves(0, current_roll)],
        "positions": get_positions(ui_engine),
        "current_player": int(ui_engine.current_player),
        "winner": ui_engine.winner,
        "game_over": ui_engine.game_over,
        "bonus_turn": bool(bonus_turn)
    })

@app.route("/step", methods=["POST"])
def step_game():
    """Executes exactly ONE player's turn (AI or Opponent)."""
    global ui_engine, current_roll, bonus_turn, consecutive_bonus, current_uburi, model
    
    if ui_engine is None:
        return jsonify({"error": "Game not initialized. Call /reset first."}), 400
        
    if ui_engine.game_over:
        return jsonify({
            "game_over": True,
            "winner": ui_engine.winner,
            "positions": get_positions(ui_engine)
        })

    player_id = ui_engine.current_player
    valid_moves = ui_engine.get_valid_moves(player_id, current_roll)
    action_token = -1
    
    if len(valid_moves) > 0:
        if player_id == 0 and model is not None:
            # Inject UI state into dummy_env for prediction
            dummy_env.engine = ui_engine
            dummy_env.current_roll = current_roll
            obs = dummy_env._get_obs()
            action_mask = dummy_env.action_masks()
            
            action, _ = model.predict(obs, action_masks=action_mask, deterministic=False)
            action_token = int(action)
        else:
            action_token = int(np.random.choice(valid_moves))
            
        # Execute move
        ui_engine.make_move(player_id, action_token, current_roll)
        passed = False
    else:
        # Pass turn
        passed = True

    # Capture state for UI return
    executed_roll = current_roll
    executed_uburi = current_uburi
    
    # Determine next player and roll
    if bonus_turn and not passed:
        consecutive_bonus += 1
    else:
        consecutive_bonus = 0
        
    if consecutive_bonus >= 3:
        # 3-Blow Rule triggered! 3 consecutive extra turns cancel turn!
        passed = True
        consecutive_bonus = 0
        bonus_turn = False
        ui_engine.next_turn()
    elif passed or not bonus_turn:
        ui_engine.next_turn()
        
    current_roll, bonus_turn, current_uburi = roll_kori()

    return jsonify({
        "action_player": int(player_id),
        "action_roll": int(executed_roll),
        "action_uburi": int(executed_uburi),
        "action_token": int(action_token),
        "passed": bool(passed),
        "positions": get_positions(ui_engine),
        "next_player": int(ui_engine.current_player),
        "next_roll": int(current_roll),
        "next_uburi": int(current_uburi),
        "winner": ui_engine.winner,
        "game_over": ui_engine.game_over
    })

if __name__ == "__main__":
    print("------------------------------------------------------------")
    print("📈 KORI KHEL WEB INTERACTIVE DASHBOARD SERVER")
    print("------------------------------------------------------------")
    app.run(host="0.0.0.0", port=5000, debug=True)
