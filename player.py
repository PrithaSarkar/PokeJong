"""
Player module for PokeJong game.
Handles player state and actions.
"""

from typing import List
from pokemon_tile import PokemonTile


class Player:
    """Represents a player in the PokeJong game."""
    
    def __init__(self, name: str, player_number: int):
        """
        Initialize a player.
        
        Args:
            name: Player's name
            player_number: Player number (1 or 2)
        """
        self.name = name
        self.player_number = player_number
        self.hand: List[PokemonTile] = []
        self.melds: List[List[PokemonTile]] = []  # Sets of matched tiles
        self.score = 0
    
    def draw_tile(self, tile: PokemonTile):
        """Add a tile to the player's hand."""
        self.hand.append(tile)
    
    def discard_tile(self, tile_index: int) -> PokemonTile:
        """
        Remove and return a tile from the player's hand.
        
        Args:
            tile_index: Index of tile to discard
            
        Returns:
            The discarded tile
        """
        if 0 <= tile_index < len(self.hand):
            return self.hand.pop(tile_index)
        return None
    
    def form_meld(self, tile_indices: List[int]) -> bool:
        """
        Form a meld (set of 3 matching tiles) from the player's hand.
        
        Args:
            tile_indices: List of indices of tiles to form a meld
            
        Returns:
            True if meld was successfully formed, False otherwise
        """
        if len(tile_indices) != 3:
            return False
        
        # Check if indices are valid
        if any(idx < 0 or idx >= len(self.hand) for idx in tile_indices):
            return False
        
        # Get tiles
        tiles = [self.hand[idx] for idx in sorted(tile_indices, reverse=True)]
        
        # Check if all tiles match
        if not (tiles[0] == tiles[1] == tiles[2]):
            return False
        
        # Remove tiles from hand and add to melds
        meld = []
        for idx in sorted(tile_indices, reverse=True):
            meld.append(self.hand.pop(idx))
        
        self.melds.append(meld)
        
        # Add points for the meld
        self.score += sum(tile.points for tile in meld)
        
        return True
    
    def show_hand(self) -> str:
        """Return a string representation of the player's hand."""
        hand_str = f"\n{self.name}'s Hand:\n"
        for idx, tile in enumerate(self.hand):
            hand_str += f"  {idx}: {tile}\n"
        return hand_str
    
    def show_melds(self) -> str:
        """Return a string representation of the player's melds."""
        if not self.melds:
            return f"{self.name}'s Melds: None\n"
        
        melds_str = f"{self.name}'s Melds:\n"
        for idx, meld in enumerate(self.melds):
            meld_points = sum(tile.points for tile in meld)
            melds_str += f"  Meld {idx + 1}: {' '.join(str(t) for t in meld)} ({meld_points} pts)\n"
        return melds_str
    
    def get_status(self) -> str:
        """Return a string with the player's current status."""
        return f"{self.name} - Score: {self.score} pts | Hand size: {len(self.hand)} | Melds: {len(self.melds)}"
