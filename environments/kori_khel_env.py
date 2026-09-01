import gymnasium as gym
from gymnasium import spaces
import numpy as np
import sys
import os

# Add project root to path so we can import game_engines
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game_engines.kori_khel.engine import KoriKhelEngine, roll_kori, BOARD_LENGTH, NUM_PLAYERS

class KoriKhelEnv(gym.Env):
    """
    Gymnasium Environment wrapper for Kori Khel.
    The agent always plays as Player 0. Opponents (Players 1, 2, 3) are simulated
    internally using a random policy.
    """
    metadata = {"render_modes": ["ansi"]}

    def __init__(self):
        super(KoriKhelEnv, self).__init__()

        # --- ACTION SPACE ---
        # The agent chooses which of their 4 tokens to move (0, 1, 2, or 3)
        self.action_space = spaces.Discrete(4)

        # --- OBSERVATION SPACE ---
        # Flat Box of size 17:
        # [0-3]: Player 0's token positions (local 0-73)
        # [4-7]: Player 1's token positions (relative to Player 0)
        # [8-11]: Player 2's token positions (relative to Player 0)
        # [12-15]: Player 3's token positions (relative to Player 0)
        # [16]: Current dice roll value (0 to 25)
        self.observation_space = spaces.Box(
            low=0,
            high=73,
            shape=(17,),
            dtype=np.int32
        )

        self.engine = None
        self.current_roll = 0
        self.bonus_turn = False
        self.turn_history = []  # Added to track intermediate moves for UI

    def _get_obs(self):
        """Helper to build the symmetric observation vector for Player 0."""
        obs = np.zeros(17, dtype=np.int32)
        
        # Add positions of all players in order (Player 0 first)
        idx = 0
        for p_id in range(NUM_PLAYERS):
            for token in self.engine.players[p_id].tokens:
                obs[idx] = token.position
                idx += 1
                
        # Add current roll at the end
        obs[16] = self.current_roll
        return obs

    def action_masks(self) -> np.ndarray:
        """Returns a boolean array indicating which actions are valid (True) or invalid (False)."""
        if self.engine is None or self.engine.game_over:
            return np.ones(self.action_space.n, dtype=bool)  # Return all True if game over to prevent crash

        valid_moves = self.engine.get_valid_moves(0, self.current_roll)
        mask = np.zeros(self.action_space.n, dtype=bool)
        for action in valid_moves:
            mask[action] = True
        
        # SB3-contrib requires at least one valid action to avoid zero probability division errors
        if not np.any(mask):
            mask[0] = True
        return mask

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        
        # Initialize pure game engine
        self.engine = KoriKhelEngine()
        
        # Start turn for Player 0 (the agent)
        # Roll kori for the agent
        self.current_roll, self.bonus_turn, _ = roll_kori()
        
        valid_moves = self.engine.get_valid_moves(0, self.current_roll)
        while not valid_moves:
            # Player 0 passes turn, run opponents
            self.engine.next_turn()
            self._run_opponents()
            
            # Roll again for Player 0
            self.current_roll, self.bonus_turn, _ = roll_kori()
            valid_moves = self.engine.get_valid_moves(0, self.current_roll)
            
            if self.engine.game_over:
                break

        return self._get_obs(), {}

    def _run_opponents(self):
        """Simulates turns for opponent players (1, 2, 3) until it is Player 0's turn."""
        while self.engine.current_player != 0 and not self.engine.game_over:
            opp_id = self.engine.current_player
            steps, opp_bonus, _ = roll_kori()
            
            valid_tokens = self.engine.get_valid_moves(opp_id, steps)
            if valid_tokens:
                # Opponent takes a random valid move
                chosen_token = np.random.choice(valid_tokens)
                self.engine.make_move(opp_id, chosen_token, steps)
            
            # If no bonus turn, pass to next player
            if not opp_bonus or not valid_tokens:
                self.engine.next_turn()

    def step(self, action):
        """Executes one step in the environment."""
        reward = 0.0
        terminated = False
        truncated = False
        info = {}

        player_id = 0  # The agent is always Player 0
        
        # Guard check: If game is already over (e.g. opponent won during reset/skipping)
        if self.engine.game_over:
            terminated = True
            if self.engine.winner != player_id:
                reward -= 100.0  # Lose penalty
            return self._get_obs(), reward, terminated, truncated, info

        # Check if the chosen action is valid
        valid_moves = self.engine.get_valid_moves(player_id, self.current_roll)
        
        if action not in valid_moves:
            # Penalty for invalid action (shaping reward to teach legal actions)
            reward -= 2.0
            # Return current state without advancing, but let agent try again
            return self._get_obs(), reward, terminated, truncated, {"invalid": True}

        # Save old position for reward shaping
        old_position = self.engine.players[player_id].tokens[action].position
        
        # Execute move
        move_result = self.engine.make_move(player_id, action, self.current_roll)
        new_position = move_result["new_position"]

        # --- REWARD SHAPING (ENGINEERING DECISIONS) ---
        # 1. Base step reward (0.1 per step forward)
        reward += 0.1 * (new_position - old_position)
        
        # 2. Capture reward (+20 for capturing opponent)
        if move_result["captured"]:
            reward += 20.0
            
        # 3. Token reached Goal (+30)
        if new_position == BOARD_LENGTH and old_position < BOARD_LENGTH:
            reward += 30.0

        # 4. Game won (+100)
        if move_result["won"]:
            reward += 100.0
            terminated = True
            self.engine.game_over = True

        # Check if any opponent tokens captured the agent's tokens during opponent turns
        # We need to scan if our tokens got captured
        my_token_positions_before = [t.position for t in self.engine.players[player_id].tokens]

        # --- TURN ROUTING ---
        if self.bonus_turn and not move_result["won"]:
            # Player 0 gets to roll again immediately
            self.current_roll, self.bonus_turn, _ = roll_kori()
        else:
            # Pass turn to opponents
            self.engine.next_turn()
            self._run_opponents()
            
            # Once opponents finish, check if agent's tokens were captured
            for t_idx, token in enumerate(self.engine.players[player_id].tokens):
                if token.position == 0 and my_token_positions_before[t_idx] > 0:
                    # Token was captured! Apply -20 penalty
                    reward -= 20.0

            # If opponent won, game ends
            if self.engine.game_over:
                terminated = True
                if self.engine.winner != player_id:
                    reward -= 100.0  # Lose penalty

            # Start Player 0's turn again by rolling
            if not self.engine.game_over:
                self.current_roll, self.bonus_turn, _ = roll_kori()

        # Handle turn skipping if Player 0 has no valid moves
        while not self.engine.game_over and not self.engine.get_valid_moves(player_id, self.current_roll):
            # No valid moves, pass turn to opponents
            self.engine.next_turn()
            self._run_opponents()
            
            if self.engine.game_over:
                terminated = True
                if self.engine.winner != player_id:
                    reward -= 100.0
                break
                
            # Roll again for Player 0
            self.current_roll, self.bonus_turn, _ = roll_kori()

        return self._get_obs(), reward, terminated, truncated, info

    def render(self):
        # ASCII representation of game state for console debugging
        output = []
        output.append("=== Kori Khel Board State ===")
        for p_id in range(NUM_PLAYERS):
            tokens_str = ", ".join([f"T{t.id}:{t.position}" for t in self.engine.players[p_id].tokens])
            output.append(f"Player {p_id}: [{tokens_str}]")
        output.append(f"Current Roll: {self.current_roll}")
        return "\n".join(output)

# Self-check if gym environment loads
if __name__ == "__main__":
    env = KoriKhelEnv()
    obs, info = env.reset()
    print("Environment initialized successfully!")
    print("Initial observation vector:", obs)
    print("Observation shape:", env.observation_space.shape)
