import sys
import os
import random

# Add project root to path so we can import game_engines
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game_engines.kori_khel.engine import KoriKhelEngine, roll_kori, GLOBAL_SAFE_ZONES

def run_simulation(max_turns=1000):
    """
    Simulates a full game of Kori Khel between 4 random players
    to validate transitions, captures, and win logic.
    """
    print("Starting Kori Khel Random Play Simulation...")
    print("=" * 60)
    
    engine = KoriKhelEngine()
    turn_count = 0
    total_rolls = 0
    total_captures = 0
    
    while not engine.game_over and turn_count < max_turns:
        player_id = engine.current_player
        
        # Roll the dice
        steps, bonus_turn, uburis = roll_kori()
        total_rolls += 1
        
        # Get list of valid tokens that can move
        valid_tokens = engine.get_valid_moves(player_id, steps)
        
        action_taken = "No Valid Move"
        capture_msg = ""
        
        if valid_tokens:
            # Randomly select a valid token to move
            chosen_token_id = random.choice(valid_tokens)
            old_pos = engine.players[player_id].tokens[chosen_token_id].position
            
            # Execute move
            res = engine.make_move(player_id, chosen_token_id, steps)
            new_pos = res["new_position"]
            action_taken = f"Moved T{chosen_token_id} from {old_pos} -> {new_pos}"
            
            # Check for captures
            if res["captured"]:
                total_captures += 1
                opp_id = res["captured"]["player"]
                opp_token = res["captured"]["token"]
                capture_msg = f"⚔️ CAPTURED Opponent P{opp_id} T{opp_token} (sent back to 0)!"
                
            # Integrity check: Positions must stay between 0 and 73
            assert 0 <= new_pos <= 73, f"Integrity check failed: Token position {new_pos} out of bounds."
        
        # Print turn summary
        bonus_text = "+" if bonus_turn else " "
        print(f"Turn {turn_count:3d} | Player {player_id} | Roll: {steps:2d} ({uburis} Uburis){bonus_text} | Action: {action_taken:<25} | {capture_msg}")
        
        # If player does NOT get a bonus turn, switch to next player
        if not bonus_turn or not valid_tokens:
            engine.next_turn()
            turn_count += 1

    print("=" * 60)
    if engine.game_over:
        print(f"🏆 GAME OVER! Player {engine.winner} wins the game!")
    else:
        print(f"Simulation stopped after reaching max limit of {max_turns} turns.")
        
    print(f"Total Turns Played: {turn_count}")
    print(f"Total Dice Rolls: {total_rolls}")
    print(f"Total Captures (Khua) occurred: {total_captures}")
    print("=" * 60)

if __name__ == "__main__":
    # Seed random for repeatability check
    random.seed(42)
    run_simulation()
