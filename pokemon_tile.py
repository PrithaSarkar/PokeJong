"""
Pokemon Tile module for PokeJong game.
Handles fetching Pokemon data from PokeAPI and creating tiles.
"""

import requests
import random
from typing import Dict, List


class PokemonTile:
    """Represents a Pokemon-themed Mahjong tile."""
    
    def __init__(self, pokemon_id: int, name: str, points: int):
        """
        Initialize a Pokemon tile.
        
        Args:
            pokemon_id: The Pokemon's ID number
            name: The Pokemon's name
            points: Points value (5 or 10)
        """
        self.pokemon_id = pokemon_id
        self.name = name.capitalize()
        self.points = points
    
    def __repr__(self):
        return f"[{self.name}:{self.points}pts]"
    
    def __eq__(self, other):
        if not isinstance(other, PokemonTile):
            return False
        return self.pokemon_id == other.pokemon_id


class PokemonTileFactory:
    """Factory class to create Pokemon tiles using PokeAPI."""
    
    BASE_URL = "https://pokeapi.co/api/v2/pokemon"
    
    @staticmethod
    def fetch_pokemon(pokemon_id: int) -> Dict:
        """
        Fetch Pokemon data from PokeAPI.
        
        Args:
            pokemon_id: The Pokemon ID to fetch
            
        Returns:
            Dictionary containing Pokemon data
        """
        try:
            response = requests.get(f"{PokemonTileFactory.BASE_URL}/{pokemon_id}", timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching Pokemon {pokemon_id}: {e}")
            return None
    
    @staticmethod
    def create_tile(pokemon_id: int) -> PokemonTile:
        """
        Create a Pokemon tile from PokeAPI data.
        
        Args:
            pokemon_id: The Pokemon ID to create a tile for
            
        Returns:
            PokemonTile instance
        """
        data = PokemonTileFactory.fetch_pokemon(pokemon_id)
        if data:
            name = data['name']
            # Assign points based on Pokemon ID (arbitrary rule for game balance)
            # Lower ID Pokemon (1-50) get 5 points, higher ID (51+) get 10 points
            points = 5 if pokemon_id <= 50 else 10
            return PokemonTile(pokemon_id, name, points)
        else:
            # Fallback if API fails
            return PokemonTile(pokemon_id, f"Pokemon{pokemon_id}", 5)
    
    @staticmethod
    def create_tile_set(num_pokemon: int = 20, num_copies: int = 4) -> List[PokemonTile]:
        """
        Create a set of Pokemon tiles for Mahjong.
        In traditional Mahjong, each tile appears 4 times.
        
        Args:
            num_pokemon: Number of different Pokemon to use
            num_copies: Number of copies of each Pokemon tile
            
        Returns:
            List of PokemonTile instances
        """
        tiles = []
        # Use first num_pokemon Pokemon from the API
        pokemon_ids = list(range(1, num_pokemon + 1))
        
        for pokemon_id in pokemon_ids:
            tile = PokemonTileFactory.create_tile(pokemon_id)
            # Create multiple copies of each tile (like Mahjong)
            for _ in range(num_copies):
                tiles.append(PokemonTile(tile.pokemon_id, tile.name, tile.points))
        
        # Shuffle the tiles
        random.shuffle(tiles)
        return tiles
