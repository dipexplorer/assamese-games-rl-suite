import numpy as np

# --- GAME CONSTANTS ---
NUM_PLAYERS = 4
TOKENS_PER_PLAYER = 4
BOARD_LENGTH = 73  # Cells 1 to 72 are track, 73 is Paka (Goal). 0 is Base.

# --- COORDINATE MAPPING LOGIC ---

# Exactly 8 Safe Zone cells on the shared 64-cell perimeter track:
# Row 4 X-marks on all 8 outer columns (2 per arm x 4 arms = 8 total)
GLOBAL_SAFE_ZONES = [5, 12, 21, 28, 37, 44, 53, 60]

def coords_to_global_pos(arm_id, side, row):
    """
    Translates physical 2D board coordinates to global 1D index cells (1-64).
    Supports anti-clockwise track traversal around the perimeter.
    
    arm_id: 0 (Bottom), 1 (Right), 2 (Top), 3 (Left)
    side: 'right', 'left', 'top', 'bottom', or 'middle'
    row: 1 (innermost near center) to 8 (outermost at tip)
    """
    # Direct mapping helper based on continuous anti-clockwise loop:
    if arm_id == 0:  # Bottom Arm
        if side in ['right', 'outer_right']:
            return [8 - row + 1]  # Row 8 -> Cell 1, Row 1 -> Cell 8
        elif side in ['left', 'outer_left']:
            return [56 + row]     # Row 1 -> Cell 57, Row 8 -> Cell 64
    elif arm_id == 1:  # Right Arm
        if side in ['bottom', 'outer_bottom']:
            return [8 + row]      # Row 1 -> Cell 9, Row 8 -> Cell 16
        elif side in ['top', 'outer_top']:
            return [16 + (8 - row + 1)]  # Row 8 -> Cell 17, Row 1 -> Cell 24
    elif arm_id == 2:  # Top Arm
        if side in ['right', 'outer_right']:
            return [24 + row]     # Row 1 -> Cell 25, Row 8 -> Cell 32
        elif side in ['left', 'outer_left']:
            return [32 + (8 - row + 1)]  # Row 8 -> Cell 33, Row 1 -> Cell 40
    elif arm_id == 3:  # Left Arm
        if side in ['top', 'outer_top']:
            return [40 + row]     # Row 1 -> Cell 41, Row 8 -> Cell 48
        elif side in ['bottom', 'outer_bottom']:
            return [48 + (8 - row + 1)]  # Row 8 -> Cell 49, Row 1 -> Cell 56

    return []


# --- KORI (DICE) LOGIC ---
def roll_kori():
    """
    Simulates throwing 6 cowrie shells based on final Kori Khel specification.
    Returns: steps (int), bonus_turn (bool), uburi_count (int)
    """
    uburi_count = np.random.binomial(6, 0.5) # number of closed shells (0 to 6)
    
    if uburi_count == 1:    # 5 open, 1 closed -> Jagowa (10 pts + Extra Turn)
        return 10, True, uburi_count
    elif uburi_count == 5:  # 1 open, 5 closed -> Pochi (25 pts + Extra Turn)
        return 25, True, uburi_count
    elif uburi_count == 0:  # 6 open, 0 closed -> Mudra (12 pts + Extra Turn)
        return 12, True, uburi_count
    elif uburi_count == 4:  # 2 open, 4 closed -> 2 pts
        return 2, False, uburi_count
    elif uburi_count == 3:  # 3 open, 3 closed -> 3 pts
        return 3, False, uburi_count
    elif uburi_count == 2:  # 4 open, 2 closed -> 4 pts
        return 4, False, uburi_count
    elif uburi_count == 6:  # 0 open, 6 closed -> 6 pts (Standard, no bonus)
        return 6, False, uburi_count
    else:
        raise ValueError(f"Invalid cowrie throw: {uburi_count}")


# --- STATE CLASSES ---

class Token:
    """Represents a single playing piece (Goti)."""
    def __init__(self, token_id):
        self.id = token_id
        self.position = 0  # 0: Base, 1-64: Perimeter, 65-72: Home Column, 73: Paka

    @property
    def is_paka(self):
        return self.position == BOARD_LENGTH

    def __repr__(self):
        return f"T{self.id}(Pos:{self.position})"


class Player:
    """Represents a player and their 4 tokens."""
    def __init__(self, player_id):
        self.id = player_id
        self.tokens = [Token(i) for i in range(TOKENS_PER_PLAYER)]

    @property
    def has_won(self):
        return all(t.is_paka for t in self.tokens)

    def __repr__(self):
        return f"P{self.id}{self.tokens}"


# --- GAME ENGINE CLASS ---

class KoriKhelEngine:
    """The pure game engine handling all rules and state transitions."""
    def __init__(self):
        self.players = [Player(i) for i in range(NUM_PLAYERS)]
        self.current_player = 0
        self.game_over = False
        self.winner = None

    def get_global_position(self, player_id, local_pos):
        """
        Maps a player's local position (1-64) to a global perimeter index (1-64).
        Each player starting point is offset by 16 cells (Ludo-style).
        """
        if 1 <= local_pos <= 64:
            return (local_pos - 1 + player_id * 16) % 64 + 1
        return None  # Base or Home Column/Goal are not on the shared perimeter

    def get_valid_moves(self, player_id, steps):
        """
        Returns a list of token IDs that are allowed to move for the given roll.
        """
        valid_token_ids = []
        player = self.players[player_id]

        for token in player.tokens:
            # Rule A: Goti at base (0) can ONLY enter on a roll of 10 (Jagowa)
            if token.position == 0:
                if steps == 10:
                    valid_token_ids.append(token.id)
            # Rule B: Goti on track can always move (overshooting rolls are capped at 73 to prevent deadlocks)
            elif token.position < BOARD_LENGTH:
                valid_token_ids.append(token.id)
                    
        return valid_token_ids

    def make_move(self, player_id, token_id, steps):
        """
        Moves the chosen token, handles captures, and returns status info.
        """
        if self.game_over:
            return {"status": "game_over"}

        player = self.players[player_id]
        token = player.tokens[token_id]

        # Validate move inline — avoids calling get_valid_moves() a second time
        # (env.step already validated before calling make_move)
        if token.position >= BOARD_LENGTH or (token.position == 0 and steps != 10):
            return {"status": "invalid_move"}

        captured_token_info = None

        # Move token
        if token.position == 0:
            token.position = 1  # Enter board
        else:
            token.position = min(BOARD_LENGTH, token.position + steps)

        # Handle captures (Khua) if landing on the shared perimeter (1-64)
        if 1 <= token.position <= 64:
            landing_global = self.get_global_position(player_id, token.position)

            # Check capture only if landing cell is NOT a safe zone
            if landing_global not in GLOBAL_SAFE_ZONES:
                for opp_id, opponent in enumerate(self.players):
                    if opp_id == player_id:
                        continue
                    
                    # Count opponent tokens on this global cell to check blocking pairs
                    opp_tokens_on_cell = [
                        t for t in opponent.tokens 
                        if self.get_global_position(opp_id, t.position) == landing_global
                    ]

                    # Capture if there is exactly 1 opponent token (no blocking pair)
                    if len(opp_tokens_on_cell) == 1:
                        opp_token = opp_tokens_on_cell[0]
                        opp_token.position = 0  # Send back to base
                        captured_token_info = {"player": opp_id, "token": opp_token.id}
                        break

        # Check win condition
        if player.has_won:
            self.game_over = True
            self.winner = player_id

        return {
            "status": "success",
            "captured": captured_token_info,
            "new_position": token.position,
            "won": player.has_won
        }

    def next_turn(self):
        """Passes turn to the next player (0 -> 1 -> 2 -> 3 -> 0)."""
        self.current_player = (self.current_player + 1) % NUM_PLAYERS


# --- SELF CHECK ---
if __name__ == "__main__":
    print("Kori Khel Engine — Self Check")
    print(f"Safe Zones ({len(GLOBAL_SAFE_ZONES)} total): {GLOBAL_SAFE_ZONES}")
    steps, bonus, uburi = roll_kori()
    print(f"Sample roll → steps={steps}, bonus={bonus}, uburi={uburi}")
    engine = KoriKhelEngine()
    print(f"Engine initialized: {engine.players}")
