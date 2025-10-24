"""
Main game module for PokeJong.
Handles game state, rules, and turn-based gameplay.
"""

from typing import Dict, List, Optional
from pokemon_tile import PokemonTile, PokemonTileFactory
from player import Player
from collections import Counter

def get_tile_counts(tiles: List[PokemonTile]) -> Dict[int, int]:
        """Converts a list of PokemonTile objects into a frequency map using pokemon_id"""
        return Counter(tile.pokemon_id for tile in tiles)
    
def _check_recursive(counts: Dict[int, int], has_pair: bool) -> bool:
    """Recursive function to check for 4 Melds (Pung/Kong) + 1 Pair in tile counts."""
    # Base Case 1: All the tiles have been consumed and a pair has been found = WIN!!
    if all(count == 0 for count in counts.values()):
        return has_pair
    
    # Find the next tile ID to process (smallest ID with count > 0)
    current_tile_id = min((tile_id for tile_id, count in counts.items() if count > 0), default = None)
    if current_tile_id is None:
        return False
    
    original_count = counts[current_tile_id]
    # Try to form the PAIR / THE EYE
    if not has_pair and original_count >= 2:
        test_counts = counts.copy()
        test_counts[current_tile_id] -= 2
        if _check_recursive(test_counts, has_pair=True):
            return True
        
    # Try to form a PUNG (Triplet: 3 identical tiles)
    if original_count >= 3:
        test_counts = counts.copy()
        test_counts[current_tile_id] -= 3
        if _check_recursive(test_counts, has_pair):
            return True
        
    return False


class PokeJongGame:
    """Main game class for PokeJong - a 2-player Pokemon-themed Mahjong game."""
    
    def __init__(self, player1_name: str = "Player 1", player2_name: str = "Player 2"):
        """
        Initialize the game.
        
        Args:
            player1_name: Name of player 1
            player2_name: Name of player 2
        """
        self.player1 = Player(player1_name, 1)
        self.player2 = Player(player2_name, 2)
        self.current_player: Player = self.player1
        self.other_player: Player = self.player2
        self.draw_pile: List[PokemonTile] = []
        self.discard_pile: List[PokemonTile] = []
        self.game_over = False
        self.winner: Optional[Player] = None
        
    def setup_game(self, num_pokemon: int = 20):
        """
        Set up the game by creating tiles and dealing initial hands.
        
        Args:
            num_pokemon: Number of different Pokemon to use (default 20)
        """
        print("Setting up PokeJong game...")
        print("Fetching Pokemon data from PokeAPI...")
        
        # Create tile set (20 Pokemon x 4 copies = 80 tiles)
        self.draw_pile = PokemonTileFactory.create_tile_set(num_pokemon, num_copies=4)
        
        # Deal initial hands (13 tiles each, like in Mahjong)
        for _ in range(13):
            self.player1.draw_tile(self.draw_pile.pop())
            self.player2.draw_tile(self.draw_pile.pop())
        
        print(f"Game setup complete! {len(self.draw_pile)} tiles remaining in draw pile.")
    
    def switch_turn(self):
        """Switch the current player."""
        self.current_player, self.other_player = self.other_player, self.current_player
    
    def draw_tile(self) -> bool:
        """
        Current player draws a tile from the draw pile.
        
        Returns:
            True if tile was drawn, False if draw pile is empty
        """
        if not self.draw_pile:
            return False
        
        tile = self.draw_pile.pop()
        self.current_player.draw_tile(tile)
        print(f"{self.current_player.name} drew: {tile}")
        return True


    def discard_tile(self, tile_index: int) -> bool:
        """
        Current player discards a tile.
        
        Args:
            tile_index: Index of tile to discard
            
        Returns:
            True if tile was discarded successfully
        """
        tile = self.current_player.discard_tile(tile_index)
        if tile:
            self.discard_pile.append(tile)
            print(f"{self.current_player.name} discarded: {tile}")
            return True
        return False
    
    def form_meld(self, tile_indices: List[int]) -> bool:
        """
        Current player attempts to form a meld.
        
        Args:
            tile_indices: List of 3 tile indices to form a meld
            
        Returns:
            True if meld was formed successfully
        """
        return self.current_player.form_meld(tile_indices)
    
    def check_win_condition(self, player: Optional[Player]=None, claimed_tile: Optional[PokemonTile] = None) -> bool:
        """
        Check if the specified player has a winning hand (4 Melds + 1 Pair).
        
        If claimed_tile is provided, it's a Ron check (13 tiles in hand + claimed tile).
        If not, it's a Tsumo check (14 tiles in hand).
        """
        player = player or self.current_player

        tiles_to_check = player.hand.copy()
        for meld in player.melds:
            tiles_to_check.extend(meld)

        if claimed_tile:
            tiles_to_check.append(claimed_tile)

        if len(tiles_to_check) != 14:
            return False
        
        tile_counts = get_tile_counts(tiles_to_check)

        if _check_recursive(tile_counts, has_pair=False):
            self.game_over = True
            self.winner = player

            winning_tile = claimed_tile if claimed_tile else player.hand[-1]
            win_type = 'Ron' if claimed_tile else 'Tsumo'
            self.calculate_win_score(player, winning_tile, win_type)
            return True
        
        return False
    
    def check_opponent_action(self, discarded_tile: PokemonTile) -> bool:
        """Checks if other_player can call Ron (Win) or Pung/ Kong
        
        Priority : Ron > Pung > Kong.

        Returns:
            True if action (win or meld) was taken, False otherwise.
        """
        opponent = self.other_player

        # Check for Ron (Win)
        if self.check_win_condition(player=opponent, claimed_tile=discarded_tile):
            print(f"{opponent.name} calls RON on {discarded_tile} and wins the game!")
            return True # GAME OVER
        
        # Check for Pung (3 identical tiles)
        hand_counts = get_tile_counts(opponent.hand)
        discard_id = discarded_tile.pokemon_id
        current_count = hand_counts.get(discard_id, 0)

        if current_count >= 2:
            # Player can call PUNG (2 matching in hand) or KONG (3 matching in hand)
            call_type = 'KONG' if current_count == 3 else 'PUNG'

            # Find the actual tile objects from the hand
            supporting_tiles = [t for t in opponent.hand if t.pokemon_id == discard_id][:current_count]

            print(f"\n📢 {opponent.name} can call {call_type} on {discarded_tile}. (Y/N)")

            # --- SIMPLIFIED AUTO-CALL LOGIC (REPLACE WITH UI INPUT LATER) ---
            # For now, we'll auto-call Pung/Kong
            if True: 
                opponent.claim_meld(discarded_tile, supporting_tiles, call_type)
                
                # The tile is removed from the discard pile (now in meld)
                self.discard_pile.pop() 
                
                # Switch turn to the meld caller (opponent) to discard
                self.switch_turn() 
                
                print(f"** Turn now passes to {opponent.name} to discard. **")
                return True

        return False # No action taken, continue normal turn flow

    def run_game_loop(self):
        """The main loop, running until the game ends."""
        while not self.game_over:

            if self.check_win_condition(player=self.current_player):
                print(f"{self.current_player.name} calls TSUMO and wins the game!")
                return #GAME IS OVER
            
            if not self.draw_tile():
                self.check_draw_condition()
                continue

            self.show_game_state()

    def check_draw_condition(self) -> bool:
        """
        Check if the game ends in a draw (no more tiles to draw).
        
        Returns:
            True if game is a draw
        """
        if not self.draw_pile:
            self.game_over = True
            # Winner is player with higher score
            if self.player1.score > self.player2.score:
                self.winner = self.player1
            elif self.player2.score > self.player1.score:
                self.winner = self.player2
            else:
                self.winner = None  # Tie
            return True
        
        return False
    
    def calculate_win_score(self, winner: Player, winning_tile: PokemonTile, win_type: str):
        """Calculate the final score for the winning player.
        
        Args:
            winner: The Player who won.
            winning_title: The 14th tile that completed the win.
            win_type: 'Tsumo' or 'Ron'"""
        
        # 1. Base Score (Points from all tiles, including the winning tile)
        base_points = sum(t.points for t in winner.hand) # Hand is the remaining 13 tiles after melds
        base_points += sum(sum(t.points for t in meld) for meld in winner.melds)
        base_points += winning_tile.points

        # 2. Add Win Bonus (Simplified Fan/Yaku)
        win_bonus = 0

        # Check for a "Pung-Heavy Hand" (Toitoi or All Pungs) - if 4 melds are already Pungs/Kongs
        if len(winner.melds) == 4 and all(len(meld) == 3 or len(meld) == 4 for meld in winner.melds):
            win_bonus += 50 
            print(f"[{winner.name}] Awarded 50 bonus points for All Pungs hand.")

        # 3. Apply Win Type Multiplier
        if win_type == 'Tsumo':
            # Tsumo is generally more valuable as the winner takes all the points from the opponent.
            final_score = (base_points + win_bonus) * 2
            print(f"[{winner.name}] Tsumo Win Multiplier applied (x2).")
        else: # Ron
            # Ron is simpler; the winner takes the points from the discarder (or everyone in complex systems).
            final_score = (base_points + win_bonus) * 1.5 
            print(f"[{winner.name}] Ron Win Multiplier applied (x1.5).")

        # 4. Update Score
        winner.score += int(final_score)
        print(f"\n--- WINNER SCORE ---")
        print(f"Winner: {winner.name} | Win Type: {win_type}")
        print(f"Base Points: {base_points} | Final Score Gained: {int(final_score)}")
        print(f"New Total Score: {winner.score}")
        print("--------------------")


    def show_game_state(self):
        """Display the current game state."""
        print("\n" + "="*60)
        print(f"CURRENT TURN: {self.current_player.name}")
        print("="*60)
        print(f"\nTiles remaining in draw pile: {len(self.draw_pile)}")
        print(f"Tiles in discard pile: {len(self.discard_pile)}")
        if self.discard_pile:
            print(f"Last discarded: {self.discard_pile[-1]}")
        print()
        print(self.player1.get_status())
        print(self.player2.get_status())
        print()
        print(self.current_player.show_hand())
        print(self.current_player.show_melds())
    
    def show_final_scores(self):
        """Display final game scores."""
        print("\n" + "="*60)
        print("GAME OVER!")
        print("="*60)
        print(f"\n{self.player1.name}: {self.player1.score} points")
        print(self.player1.show_melds())
        print(f"{self.player2.name}: {self.player2.score} points")
        print(self.player2.show_melds())
        
        if self.winner:
            print(f"\n🎉 {self.winner.name} WINS! 🎉")
        else:
            print("\n🤝 It's a TIE! 🤝")