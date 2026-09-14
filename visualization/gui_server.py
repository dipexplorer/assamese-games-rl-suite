import os
import sys
from flask import Flask, jsonify, render_template

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)

from environments.kori_khel_env import KoriKhelEnv, AGENT_ID
from game_engines.kori_khel.engine import KoriKhelEngine, roll_kori
from sb3_contrib import MaskablePPO

app = Flask(__name__, template_folder="templates")

# Global UI game state
ui_engine        = None
current_roll     = 0
bonus_turn       = False
consecutive_bonus = 0
current_uburi    = 0
model            = None

# Single shared env instance — used to build observations and action masks for the AI model.
# Its .engine and .current_roll are updated each step to reflect the UI game state.
# This avoids creating a new env object on every /step call.
shared_env = KoriKhelEnv()


def get_positions(engine):
    """Formats player token positions into a JSON-friendly dict."""
    return {
        f"p{p_id}": [int(t.position) for t in engine.players[p_id].tokens]
        for p_id in range(4)
    }


@app.route("/")
def index():
    """Serves the Kori Khel interactive board visualization page."""
    return render_template("index.html")


@app.route("/reset", methods=["POST"])
def reset_game():
    """Resets the environment for step-by-step UI visualization."""
    global ui_engine, current_roll, bonus_turn, consecutive_bonus, current_uburi, model

    ui_engine = KoriKhelEngine()
    roll, bonus, uburi = roll_kori()

    model_path = os.path.join(PROJECT_ROOT, "agents", "kori_khel", "maskable_ppo_kori_khel.zip")
    model = MaskablePPO.load(model_path) if os.path.exists(model_path) else None

    current_roll      = roll
    bonus_turn        = bonus
    consecutive_bonus = 0
    current_uburi     = uburi

    return jsonify({
        "status":         "initialized",
        "roll":           int(current_roll),
        "uburi":          int(current_uburi),
        "valid_moves":    [int(x) for x in ui_engine.get_valid_moves(AGENT_ID, current_roll)],
        "positions":      get_positions(ui_engine),
        "current_player": int(ui_engine.current_player),
        "winner":         ui_engine.winner,
        "game_over":      ui_engine.game_over,
        "bonus_turn":     bool(bonus_turn),
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
            "winner":    ui_engine.winner,
            "positions": get_positions(ui_engine),
        })

    player_id   = ui_engine.current_player
    valid_moves = ui_engine.get_valid_moves(player_id, current_roll)
    action_token = -1

    if valid_moves:
        # Sync shared_env with current UI state (done once, used by both branches)
        shared_env.engine       = ui_engine
        shared_env.current_roll = current_roll
        shared_env.bonus_turn   = bonus_turn

        if player_id == AGENT_ID and model is not None:
            # Build observation and mask for the AI model
            obs         = shared_env._get_obs()
            action_mask = shared_env.action_masks()
            action, _ = model.predict(obs, action_masks=action_mask, deterministic=False)
            action_token = int(action)
        else:
            # Use heuristic policy for opponents — consistent with training conditions
            action_token = int(shared_env._choose_heuristic_move(player_id, valid_moves, current_roll))

        ui_engine.make_move(player_id, action_token, current_roll)
        passed = False
    else:
        passed = True

    # Capture executed state before advancing turn
    executed_roll  = current_roll
    executed_uburi = current_uburi

    # Apply 3-bonus-turn rule: 3 consecutive bonus turns cancel the turn
    if bonus_turn and not passed:
        consecutive_bonus += 1
    else:
        consecutive_bonus = 0

    if consecutive_bonus >= 3:
        passed            = True
        consecutive_bonus = 0
        bonus_turn        = False
        ui_engine.next_turn()
    elif passed or not bonus_turn:
        ui_engine.next_turn()

    current_roll, bonus_turn, current_uburi = roll_kori()

    return jsonify({
        "action_player": int(player_id),
        "action_roll":   int(executed_roll),
        "action_uburi":  int(executed_uburi),
        "action_token":  int(action_token),
        "passed":        bool(passed),
        "positions":     get_positions(ui_engine),
        "next_player":   int(ui_engine.current_player),
        "next_roll":     int(current_roll),
        "next_uburi":    int(current_uburi),
        "winner":        ui_engine.winner,
        "game_over":     ui_engine.game_over,
    })


if __name__ == "__main__":
    print("------------------------------------------------------------")
    print("KORI KHEL — WEB INTERACTIVE DASHBOARD SERVER")
    print("------------------------------------------------------------")
    app.run(host="0.0.0.0", port=5000, debug=True)
