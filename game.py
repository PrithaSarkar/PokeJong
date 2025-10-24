"""
Main game module for PokeJong.
Handles game state, rules, and turn-based gameplay.
"""

from typing import List, Optional
from pokemon_tile import PokemonTile, PokemonTileFactory
from player import Player


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
    
    def check_win_condition(self) -> bool:
        """
        Check if the current player has won.
        Win condition: Form 4 melds (12 tiles) + 1 tile remaining = complete hand
        
        Returns:
            True if player has won
        """
        if len(self.current_player.melds) >= 4 and len(self.current_player.hand) == 1:
            self.game_over = True
            self.winner = self.current_player
            return True
        return False
    
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
