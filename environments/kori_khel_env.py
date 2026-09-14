import gymnasium as gym
from gymnasium import spaces
import numpy as np
import sys
import os

# Add project root to path so we can import game_engines
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game_engines.kori_khel.engine import (
    KoriKhelEngine, roll_kori, BOARD_LENGTH, NUM_PLAYERS, GLOBAL_SAFE_ZONES
)

# =============================================================================
# CONSTANTS
# =============================================================================

# Agent is always Player 0 throughout the environment
AGENT_ID = 0

# Total number of features the agent receives every step
N_OBS_FEATURES = 30

# Named index map — documents exactly what each position in the obs vector means.
# Use this anywhere in code instead of raw integers (e.g. obs[OBS_INDEX["dice_roll"]])
OBS_INDEX = {
    "p0_tokens":        slice(0, 4),    # Player 0 token positions (0–73)
    "p1_tokens":        slice(4, 8),    # Player 1 token positions (0–73)
    "p2_tokens":        slice(8, 12),   # Player 2 token positions (0–73)
    "p3_tokens":        slice(12, 16),  # Player 3 token positions (0–73)
    "dice_roll":        16,             # Current roll value (0–25)
    "bonus_turn":       17,             # Will agent roll again? (0 or 1)
    "capture_flags":    slice(18, 22),  # Will token i capture an opponent? (0 or 1)
    "safe_landing":     slice(22, 26),  # Will token i land on a safe zone? (0 or 1)
    "threat_distances": slice(26, 30),  # Steps until nearest enemy reaches token i (0–64)
}

# Per-feature minimum values — all features have min 0
OBS_LOW = np.zeros(N_OBS_FEATURES, dtype=np.int32)

# Per-feature maximum values — each feature group has its own correct ceiling
OBS_HIGH = np.concatenate([
    np.full(16, 73),  # 16 token positions       → max 73 (Paka/Goal cell)
    [25, 1],          # dice_roll → 25, bonus_turn → 1
    np.ones(8),       # 4 capture flags + 4 safe-landing flags → max 1
    np.full(4, 64),   # 4 threat distances        → max 64 (full circular track)
]).astype(np.int32)


class KoriKhelEnv(gym.Env):
    """
    Gymnasium Environment wrapper for Kori Khel (Assamese traditional board game).

    Agent: Player 0 (trained via MaskablePPO).
    Opponents: Players 1, 2, 3 — simulated with a heuristic priority policy.

    Observation vector (30 features, see OBS_INDEX above):
      [0–15]  Raw token positions for all 4 players (4 tokens each)
      [16]    Current dice roll value
      [17]    Bonus turn flag (1 = agent gets another roll after this move)
      [18–21] Capture opportunity flags (1 = moving token i will cut an opponent)
      [22–25] Safe-landing flags (1 = moving token i will land on a safe zone)
      [26–29] Threat distances (steps until nearest enemy reaches each of agent's tokens)

    Action space: Discrete(4) — choose which of agent's 4 tokens to move.
    """
    metadata = {"render_modes": ["ansi"]}

    def __init__(self):
        super(KoriKhelEnv, self).__init__()

        # --- ACTION SPACE ---
        # Agent picks one of 4 tokens (0, 1, 2, 3) to move each turn.
        # Invalid actions are masked out by action_masks() so MaskablePPO
        # never attempts an illegal move.
        self.action_space = spaces.Discrete(4)

        # --- OBSERVATION SPACE ---
        # shape= is NOT passed explicitly. When low & high are numpy arrays,
        # Gymnasium automatically infers shape from their size.
        self.observation_space = spaces.Box(
            low=OBS_LOW,
            high=OBS_HIGH,
            dtype=np.int32
        )

        self.engine = None
        self.current_roll = 0
        self.bonus_turn = False

    # =========================================================================
    # OBSERVATION BUILDER
    # =========================================================================

    def _get_landing_global(self, player_id, token, steps):
        """
        Computes the projected global perimeter cell after moving token by steps.
        Returns None if the move is invalid (base + non-10 roll) or lands off
        the shared perimeter track (cells 1–64).
        Shared by _will_capture, _will_land_safe, and _get_obs to avoid
        recomputing get_global_position for the same token twice.
        """
        if token.position == 0 and steps != 10:
            return None
        new_local = 1 if token.position == 0 else min(BOARD_LENGTH, token.position + steps)
        if not (1 <= new_local <= 64):
            return None
        return self.engine.get_global_position(player_id, new_local)

    def _get_obs(self):
        """
        Builds the 30-feature observation vector for the agent.
        All features are documented in OBS_INDEX above.
        _get_landing_global() is called ONCE per token and reused for both
        capture and safe-landing flags to avoid duplicate computation.
        """
        obs = np.zeros(N_OBS_FEATURES, dtype=np.int32)

        # --- Indices 0–15: Raw token positions for all 4 players ---
        idx = 0
        for p_id in range(NUM_PLAYERS):
            for token in self.engine.players[p_id].tokens:
                obs[idx] = token.position
                idx += 1

        # --- Index 16: Current dice roll ---
        obs[16] = self.current_roll

        # --- Index 17: Bonus turn flag ---
        obs[17] = int(self.bonus_turn)

        # --- Indices 18–29: Strategic computed features (per agent token) ---
        # landing_global computed once per token and reused for both capture
        # and safe-landing checks (avoids calling get_global_position twice).
        for i, token in enumerate(self.engine.players[AGENT_ID].tokens):
            landing_global = self._get_landing_global(AGENT_ID, token, self.current_roll)
            obs[18 + i] = int(self._capture_at(AGENT_ID, landing_global))
            obs[22 + i] = int(landing_global is not None and landing_global in GLOBAL_SAFE_ZONES)
            obs[26 + i] = self._nearest_threat(AGENT_ID, token)

        return obs

    # =========================================================================
    # STRATEGIC HELPER METHODS (shared by observation builder & heuristic policy)
    # =========================================================================

    def _capture_at(self, player_id, landing_global):
        """
        Returns True if a token landing on `landing_global` will capture an opponent.
        Expects landing_global already computed (None = no capture possible).
        """
        if landing_global is None or landing_global in GLOBAL_SAFE_ZONES:
            return False
        for opp_id, opponent in enumerate(self.engine.players):
            if opp_id == player_id:
                continue
            opp_on_cell = [
                t for t in opponent.tokens
                if (1 <= t.position <= 64 and
                    self.engine.get_global_position(opp_id, t.position) == landing_global)
            ]
            # Single opponent token on that cell = capturable (pair blocks capture)
            if len(opp_on_cell) == 1:
                return True
        return False

    def _will_capture(self, player_id, token, steps):
        """Returns True if moving this token by steps will capture an opponent token."""
        return self._capture_at(player_id, self._get_landing_global(player_id, token, steps))

    def _will_land_safe(self, player_id, token, steps):
        """Returns True if moving this token by steps will land on a safe zone (X mark)."""
        landing_global = self._get_landing_global(player_id, token, steps)
        return landing_global is not None and landing_global in GLOBAL_SAFE_ZONES

    def _nearest_threat(self, player_id, token):
        """
        Returns how many steps behind the nearest opponent token is.
        Small value = danger (enemy close behind); 64 = no threat on shared track.
        Only meaningful while token is on the shared perimeter (positions 1–64).
        """
        if not (1 <= token.position <= 64):
            return 64  # Not on shared track — no threat applicable
        my_global = self.engine.get_global_position(player_id, token.position)
        min_dist = 64
        for opp_id, opponent in enumerate(self.engine.players):
            if opp_id == player_id:
                continue
            for opp_token in opponent.tokens:
                if not (1 <= opp_token.position <= 64):
                    continue
                opp_global = self.engine.get_global_position(opp_id, opp_token.position)
                # Circular distance: how many steps for opponent to reach my cell
                dist = (my_global - opp_global) % 64
                if 0 < dist < min_dist:
                    min_dist = dist
        return min_dist

    # =========================================================================
    # ACTION MASKING
    # =========================================================================

    def action_masks(self) -> np.ndarray:
        """
        Returns a boolean array of size 4 indicating which token choices are valid.
        MaskablePPO uses this to zero-out illegal actions before sampling.
        """
        if self.engine is None or self.engine.game_over:
            return np.ones(self.action_space.n, dtype=bool)

        valid_moves = self.engine.get_valid_moves(AGENT_ID, self.current_roll)
        mask = np.zeros(self.action_space.n, dtype=bool)
        for action in valid_moves:
            mask[action] = True

        # SB3-contrib requires at least one True to avoid division-by-zero
        if not np.any(mask):
            mask[0] = True
        return mask

    # =========================================================================
    # RESET
    # =========================================================================

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        self.engine = KoriKhelEngine()
        self.current_roll, self.bonus_turn, _ = roll_kori()

        return self._get_obs(), {}

    # =========================================================================
    # HEURISTIC OPPONENT POLICY
    # =========================================================================

    def _choose_heuristic_move(self, opp_id, valid_tokens, steps):
        """
        Chooses the best token for an opponent using priority-based heuristic.
        Single-pass loop: landing_global computed once per token, reused for
        both capture (Priority 1) and safe-zone (Priority 2) checks.
          1. Capture an opponent token if possible (aggressive)  — return immediately
          2. Land on a safe zone if possible (defensive)         — remember, keep scanning
          3. Move the token that is furthest advanced toward goal (progress)
        """
        safe_candidate = None  # First safe-zone landing found (Priority 2)

        for tid in valid_tokens:
            token = self.engine.players[opp_id].tokens[tid]
            landing_global = self._get_landing_global(opp_id, token, steps)

            # Priority 1: Capture — return immediately, highest priority
            if self._capture_at(opp_id, landing_global):
                return tid

            # Priority 2: Safe zone — remember first match, keep scanning for a capture
            if safe_candidate is None and landing_global is not None and landing_global in GLOBAL_SAFE_ZONES:
                safe_candidate = tid

        # Return safe candidate if found, else most advanced token (Priority 3)
        if safe_candidate is not None:
            return safe_candidate
        return max(valid_tokens,
                   key=lambda tid: self.engine.players[opp_id].tokens[tid].position)

    def _run_opponents(self):
        """
        Simulates turns for opponent players (1, 2, 3) using the heuristic policy
        until the turn rotates back to Player 0.
        """
        while self.engine.current_player != AGENT_ID and not self.engine.game_over:
            opp_id = self.engine.current_player
            steps, opp_bonus, _ = roll_kori()

            valid_tokens = self.engine.get_valid_moves(opp_id, steps)
            if valid_tokens:
                chosen_token = self._choose_heuristic_move(opp_id, valid_tokens, steps)
                self.engine.make_move(opp_id, chosen_token, steps)

            # Hand turn to next player unless opponent earned a bonus roll
            if not opp_bonus or not valid_tokens:
                self.engine.next_turn()

    # =========================================================================
    # STEP (Agent takes one action)
    # =========================================================================

    def step(self, action):
        """Executes one step: agent moves a token, opponents respond, rewards computed."""
        reward = 0.0
        terminated = False
        truncated = False
        info = {}

        # Guard: game already ended (e.g. opponent won during reset skipping)
        if self.engine.game_over:
            terminated = True
            if self.engine.winner != AGENT_ID:
                reward -= 100.0
            return self._get_obs(), reward, terminated, truncated, info

        # Validate action
        valid_moves = self.engine.get_valid_moves(AGENT_ID, self.current_roll)
        if not valid_moves:
            # Agent has no valid moves for this roll (e.g. base token with non-10 roll).
            # Pass turn to opponents and roll new dice for agent.
            self.engine.next_turn()
            self._run_opponents()
            if self.engine.game_over:
                terminated = True
                if self.engine.winner != AGENT_ID:
                    reward -= 100.0
            else:
                self.current_roll, self.bonus_turn, _ = roll_kori()
            return self._get_obs(), reward, terminated, truncated, info

        if action not in valid_moves:
            reward -= 2.0
            return self._get_obs(), reward, terminated, truncated, {"invalid": True}

        # Snapshot state before move for reward computation
        chosen_token = self.engine.players[AGENT_ID].tokens[action]
        old_position = chosen_token.position
        landing_global_old = self.engine.get_global_position(AGENT_ID, old_position)
        was_safe = landing_global_old is not None and landing_global_old in GLOBAL_SAFE_ZONES
        threat_before = self._nearest_threat(AGENT_ID, chosen_token)
        will_land_safe = self._will_land_safe(AGENT_ID, chosen_token, self.current_roll)

        # Execute the chosen move
        move_result = self.engine.make_move(AGENT_ID, action, self.current_roll)
        new_position = move_result["new_position"]

        # --- REWARD SHAPING ---
        # 1. Progress reward: 0.1 per step moved forward
        reward += 0.1 * (new_position - old_position)

        # 2. Private Home Stretch Sprint Bonus (cells 65-72): +0.5 extra per step in home column
        if new_position >= 65:
            steps_in_home = new_position - max(64, old_position)
            reward += 0.5 * steps_in_home

        # 3. Capture reward: opponent token sent back to base
        if move_result["captured"]:
            reward += 20.0

        # 4. Safe-zone landing bonus: strategic positioning
        if will_land_safe:
            reward += 5.0

        # 5. Strategic Threat Avoidance: penalty for recklessly leaving a safe zone under close threat
        if was_safe and threat_before <= 6 and not will_land_safe and new_position <= 64 and not move_result["captured"]:
            reward -= (6.0 / max(1, threat_before))

        # 6. Token reached Goal (Paka)
        if new_position == BOARD_LENGTH and old_position < BOARD_LENGTH:
            reward += 30.0

        # 7. Game won (engine already set game_over inside make_move)
        if move_result["won"]:
            reward += 100.0
            terminated = True

        # Snapshot agent token positions AFTER our move but BEFORE opponents play
        # Used below to detect which of our tokens got captured by opponents
        my_positions_after_my_move = [t.position for t in self.engine.players[AGENT_ID].tokens]

        # --- TURN ROUTING ---
        if self.bonus_turn and not move_result["won"]:
            # Bonus roll (Jagowa / Pochi / Mudra): agent goes again immediately
            self.current_roll, self.bonus_turn, _ = roll_kori()
        else:
            # Normal: pass turn to opponents
            self.engine.next_turn()
            self._run_opponents()

            # Penalise for any of agent's tokens captured during opponent turns
            for t_idx, token in enumerate(self.engine.players[AGENT_ID].tokens):
                if token.position == 0 and my_positions_after_my_move[t_idx] > 0:
                    reward -= 20.0

            # Check if an opponent won
            if self.engine.game_over:
                terminated = True
                if self.engine.winner != AGENT_ID:
                    reward -= 100.0

            # Roll for agent's next turn
            if not self.engine.game_over:
                self.current_roll, self.bonus_turn, _ = roll_kori()

        # Skip agent turns where no valid move exists
        while not self.engine.game_over and not self.engine.get_valid_moves(AGENT_ID, self.current_roll):
            self.engine.next_turn()
            self._run_opponents()

            if self.engine.game_over:
                terminated = True
                if self.engine.winner != AGENT_ID:
                    reward -= 100.0
                break

            self.current_roll, self.bonus_turn, _ = roll_kori()

        return self._get_obs(), reward, terminated, truncated, info

    # =========================================================================
    # RENDER
    # =========================================================================

    def render(self):
        """ASCII board state for console debugging."""
        output = ["=== Kori Khel Board State ==="]
        for p_id in range(NUM_PLAYERS):
            tokens_str = ", ".join(
                [f"T{t.id}:{t.position}" for t in self.engine.players[p_id].tokens]
            )
            output.append(f"Player {p_id}: [{tokens_str}]")
        output.append(f"Current Roll: {self.current_roll}")
        output.append(f"Bonus Turn:   {self.bonus_turn}")
        return "\n".join(output)


# =============================================================================
# SELF-CHECK
# =============================================================================
if __name__ == "__main__":
    env = KoriKhelEnv()
    obs, info = env.reset()
    print("Environment initialized successfully!")
    print(f"Observation shape : {env.observation_space.shape}")
    print(f"\nOBS_INDEX breakdown:")
    for name, idx in OBS_INDEX.items():
        print(f"  {name:20s} → {obs[idx]}")
