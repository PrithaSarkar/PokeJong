"""
Simple tests for PokeJong game components.
"""

import sys
from pokemon_tile import PokemonTile, PokemonTileFactory
from player import Player
from game import PokeJongGame


def test_pokemon_tile():
    """Test PokemonTile creation."""
    print("Testing PokemonTile...")
    tile1 = PokemonTile(1, "Bulbasaur", 5)
    tile2 = PokemonTile(1, "Bulbasaur", 5)
    tile3 = PokemonTile(2, "Ivysaur", 5)
    
    assert tile1 == tile2, "Equal tiles should match"
    assert tile1 != tile3, "Different tiles should not match"
    assert tile1.name == "Bulbasaur", "Name should be capitalized"
    assert tile1.points == 5, "Points should be set correctly"
    print("✓ PokemonTile tests passed!")


def test_pokemon_tile_factory():
    """Test PokemonTileFactory."""
    print("\nTesting PokemonTileFactory...")
    
    # Test single tile creation
    tile = PokemonTileFactory.create_tile(1)
    assert tile is not None, "Should create a tile"
    assert tile.pokemon_id == 1, "Pokemon ID should match"
    assert tile.points in [5, 10], "Points should be 5 or 10"
    print(f"  Created tile: {tile}")
    
    # Test tile set creation
    tiles = PokemonTileFactory.create_tile_set(num_pokemon=5, num_copies=4)
    assert len(tiles) == 20, "Should create 5 Pokemon x 4 copies = 20 tiles"
    
    # Count occurrences of each Pokemon
    pokemon_counts = {}
    for tile in tiles:
        pokemon_counts[tile.pokemon_id] = pokemon_counts.get(tile.pokemon_id, 0) + 1
    
    for pokemon_id, count in pokemon_counts.items():
        assert count == 4, f"Each Pokemon should appear 4 times, but {pokemon_id} appears {count} times"
    
    print("✓ PokemonTileFactory tests passed!")


def test_player():
    """Test Player functionality."""
    print("\nTesting Player...")
    player = Player("TestPlayer", 1)
    
    # Test drawing tiles
    tile1 = PokemonTile(1, "Bulbasaur", 5)
    tile2 = PokemonTile(1, "Bulbasaur", 5)
    tile3 = PokemonTile(1, "Bulbasaur", 5)
    tile4 = PokemonTile(2, "Ivysaur", 5)
    
    player.draw_tile(tile1)
    player.draw_tile(tile2)
    player.draw_tile(tile3)
    player.draw_tile(tile4)
    
    assert len(player.hand) == 4, "Player should have 4 tiles"
    
    # Test forming a meld
    result = player.form_meld([0, 1, 2])
    assert result == True, "Should successfully form a meld"
    assert len(player.hand) == 1, "Player should have 1 tile left"
    assert len(player.melds) == 1, "Player should have 1 meld"
    assert player.score == 15, "Player should have 15 points (3 tiles x 5 points)"
    
    # Test discarding
    discarded = player.discard_tile(0)
    assert discarded == tile4, "Should discard the correct tile"
    assert len(player.hand) == 0, "Player should have no tiles left"
    
    print("✓ Player tests passed!")


def test_game_initialization():
    """Test PokeJongGame initialization."""
    print("\nTesting PokeJongGame initialization...")
    game = PokeJongGame("Alice", "Bob")
    
    assert game.player1.name == "Alice", "Player 1 name should be set"
    assert game.player2.name == "Bob", "Player 2 name should be set"
    assert game.current_player == game.player1, "Player 1 should go first"
    assert game.game_over == False, "Game should not be over initially"
    
    print("✓ PokeJongGame initialization tests passed!")


def test_game_setup():
    """Test game setup with tile creation."""
    print("\nTesting game setup...")
    game = PokeJongGame("Alice", "Bob")
    
    print("  Fetching Pokemon data from PokeAPI (this may take a moment)...")
    # Use 10 Pokemon for testing: 10 x 4 copies = 40 tiles
    # 13 + 13 = 26 tiles dealt to players, 14 remaining in draw pile
    game.setup_game(num_pokemon=10)
    
    # Each player should have 13 tiles
    assert len(game.player1.hand) == 13, "Player 1 should have 13 tiles"
    assert len(game.player2.hand) == 13, "Player 2 should have 13 tiles"
    
    # Draw pile should have remaining tiles: 40 - 26 = 14
    assert len(game.draw_pile) == 14, f"Draw pile should have 14 tiles, but has {len(game.draw_pile)}"
    
    print("✓ Game setup tests passed!")


def run_all_tests():
    """Run all tests."""
    print("="*60)
    print("Running PokeJong Tests")
    print("="*60)
    
    try:
        test_pokemon_tile()
        test_pokemon_tile_factory()
        test_player()
        test_game_initialization()
        test_game_setup()
        
        print("\n" + "="*60)
        print("ALL TESTS PASSED! ✓")
        print("="*60)
        return 0
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
