"""
Handles player state and actions.
"""

from typing import List, Optional  
from collections import Counter
from pokemon_tile import PokemonTile


class Player:
    """Represents a player in the PokeJong game."""
    
    def __init__(self, name: str, player_id: int):
        """
        Initialize a player.
        
        Args:
            name: Player's name
            player_id: Player number (1 or 2)
        """
        self.name = name
        self.player_id = player_id
        self.hand: List[PokemonTile] = [] # Hidden tiles
        self.discards: List[PokemonTile] = [] # Discarded tiles
        self.melds: List[List[PokemonTile]] = []  # Matched tiles
        self.score: int = 0
    
    def draw_tile(self, tile: PokemonTile):
        """Add a tile to the player's hand."""
        self.hand.append(tile)
        self.sort_hand()

    def sort_hand(self):
        """Sorts the hand for easier visualization/logic."""
        # Sorting by ID ensures identical tiles are grouped.
        self.hand.sort(key=lambda tile: tile.pokemon_id)
    
    def discard_tile(self, tile_index: int) -> PokemonTile:
        """
        Remove and return a tile from the player's hand.
        
        Args:
            tile_index: Index of tile to discard
            
        Returns:
            The discarded tile
        """
        try:
            if 0 <= tile_index < len(self.hand):
                discarded_tile = self.hand.pop(tile_index)
                self.discards.append(discarded_tile)
                return discarded_tile
            else:
                return None
        except Exception as e:
            return None
        
    def get_status(self) -> str:
        """Return a string with the player's current status."""
        return f"| {self.name} (P{self.player_id}) | Score: {self.score} | Discards: {len(self.discards)}"
    
    def show_hand(self) -> str:
        """Return a string representation of the player's current hand."""
        return f"Hand ({len(self.hand)} tiles): {self.hand}"
    
    def show_melds(self) -> str:
        """Return a string representation of the player's melds."""
        return f"Melds ({len(self.melds)}): {self.melds}"
    
    def form_meld(self, tile_indices: List[int]) -> bool:
        """
        Form a meld (set of 3 matching tiles) from the player's hand.
        This version is for PUNG/KONG calls *from the hand*.
        """
        # 1. Get the tiles to check
        if len(tile_indices) != 3:
            return False # Must be 3 tiles for a Pung

        # Extract tiles based on provided indices. Create a copy of the hand for safe removal.
        temp_hand = [self.hand[i] for i in tile_indices]
        
        # 2. Check if all 3 tiles are identical
        first_id = temp_hand[0].pokemon_id
        if not all(tile.pokemon_id == first_id for tile in temp_hand):
            return False # Not a matching set

        # 3. If they match, remove them from the hand and add to melds
        new_meld = []
        for index in sorted(tile_indices, reverse=True): # Remove in reverse order to keep indices correct
            new_meld.append(self.hand.pop(index))
        
        self.melds.append(new_meld)
        self.score += sum(t.points for t in new_meld) # Add score for the new meld
        self.sort_hand()
        return True

    def claim_meld(self, claimed_tile: PokemonTile, supporting_tiles: List[PokemonTile], meld_type: str):
        """Helper for Pung/Kong calls on a discarded tile."""
        new_meld = [claimed_tile] + supporting_tiles
        
        # Remove supporting tiles from hand
        for tile in supporting_tiles:
            # Need to find and remove the actual tile object from hand
            for i, hand_tile in enumerate(self.hand):
                if hand_tile == tile:
                    self.hand.pop(i)
                    break
        
        self.melds.append(new_meld)
        self.sort_hand()

        meld_points = sum(t.points for t in new_meld)
        if meld_type == 'KONG':
            meld_points *= 2  # bonus points

        self.score += meld_points
        print(f"** {self.name} called {meld_type} on {claimed_tile} - Gained {meld_points} points **")