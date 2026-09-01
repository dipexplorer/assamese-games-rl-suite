import numpy as np

# --- GAME CONSTANTS ---
NUM_PLAYERS = 4
TOKENS_PER_PLAYER = 4
BOARD_LENGTH = 73  # Cells 1 to 72 are track, 73 is Paka (Goal). 0 is Base.

# --- COORDINATE MAPPING LOGIC ---

def coords_to_global_pos(arm_id, side, row):
    """
    Translates physical 2D board coordinates to global 1D index cells (1-64).
    Supports 'right', 'left', and 'middle' columns to map X marks accurately.
    
    Args:
        arm_id (int): 0, 1, 2, or 3 (clockwise).
        side (str): 'right', 'left', or 'middle'.
        row (int): 1 (innermost row) to 8 (outermost row).
    Returns:
        list of int: The mapped 1D cell indices.
    """
    base_offset = arm_id * 16
    if side == 'right':
        # Right column goes from Row 1 to Row 8
        return [base_offset + row]
    elif side == 'left':
        # Left column goes from Row 8 down to Row 1
        return [base_offset + 8 + (8 - row + 1)]
    elif side == 'middle':
        if row == 8:
            # Row 8 of the middle column is the physical tip of the arm.
            # In our 64-cell loop, the goti turns at the tip from right col to left col.
            # Thus, both cell 8 (end of right) and cell 9 (start of left) represent this tip.
            return [base_offset + 8, base_offset + 9]
        else:
            # Rows 1-7 of the middle column are private home columns, not on the shared track.
            return []
    else:
        raise ValueError("Side must be 'right', 'left', or 'middle'")

# Programmatically generate safe zones using verified physical coordinates
GLOBAL_SAFE_ZONES = []
for arm in range(NUM_PLAYERS):
    # Rule: X marks are at Row 3 on both side columns, and Row 8 at the middle column tip
    GLOBAL_SAFE_ZONES.extend(coords_to_global_pos(arm, 'right', 4))   # Row 4 Right Column
    GLOBAL_SAFE_ZONES.extend(coords_to_global_pos(arm, 'middle', 8))  # Row 8 Middle Column (Tip)
    GLOBAL_SAFE_ZONES.extend(coords_to_global_pos(arm, 'left', 4))    # Row 4 Left Column

# Sort for consistency
GLOBAL_SAFE_ZONES.sort()


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
    def is_active(self):
        return 0 < self.position < BOARD_LENGTH

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

        # Double check if move is valid
        valid_moves = self.get_valid_moves(player_id, steps)
        if token_id not in valid_moves:
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


# --- TEST PLAY ---
if __name__ == "__main__":
    print("Testing Part C: Kori Khel Game Engine (Corrected Coordinate Mapping)")
    print("-" * 70)
    print("Programmatically Generated Global Safe Zones:")
    for idx, cell in enumerate(GLOBAL_SAFE_ZONES):
        found = False
        for arm in range(4):
            for side in ['right', 'left', 'middle']:
                for row in range(1, 9):
                    if cell in coords_to_global_pos(arm, side, row):
                        print(f"Safe Zone {idx+1:2d}: 1D Index {cell:2d} -> Arm {arm}, {side:6s} column, Row {row}")
                        found = True
                        break
                if found: break
            if found: break
