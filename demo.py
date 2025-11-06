#!/usr/bin/env python3
"""
Demo script for PokeJong - shows how the game mechanics work.
This runs a simulated game with pre-scripted actions.
"""

from pokemon_tile import PokemonTile
from player import Player
from game import PokeJongGame


def demo_game():
    """Run a demonstration of the game mechanics."""
    print("\n" + "="*60)
    print("POKEJONG DEMO")
    print("="*60)
    print("\nThis demo shows how the game mechanics work.")
    print("In a real game, players would interact via the CLI.\n")
    
    # Create a simplified demo with pre-made tiles
    print("Creating players and tiles...")
    player1 = Player("Player 1", 1)
    player2 = Player("Player 2", 2)
    
    # Create some Pokemon tiles manually for the demo
    pikachu = PokemonTile(25, "Pikachu", 5)
    bulbasaur = PokemonTile(1, "Bulbasaur", 5)
    charmander = PokemonTile(4, "Charmander", 5)
    squirtle = PokemonTile(7, "Squirtle", 5)
    
    # Give Player 1 some tiles including a matching set
    print("\n--- Initial Setup ---")
    for tile in [pikachu, pikachu, pikachu, bulbasaur, charmander]:
        player1.draw_tile(tile)
    
    for tile in [squirtle, squirtle, squirtle, bulbasaur, charmander]:
        player2.draw_tile(tile)
    
    print(player1.show_hand())
    print(player2.show_hand())
    
    # Player 1 forms a meld
    print("\n--- Player 1's Turn ---")
    print(f"{player1.name} notices they have 3 matching Pikachu tiles!")
    print("Forming a meld with tiles")
    
    if player1.form_meld([0, 1, 2]):
        print("✓ Meld formed successfully!")
        print(player1.show_melds())
        print(f"Current score: {player1.score} points")
    
    print(player1.show_hand())
    
    # Player 2 forms a meld
    print("\n--- Player 2's Turn ---")
    print(f"{player2.name} has 3 matching Squirtle tiles!")
    print("Forming a meld with tiles")
    
    if player2.form_meld([0, 1, 2]):
        print("✓ Meld formed successfully!")
        print(player2.show_melds())
        print(f"Current score: {player2.score} points")
    
    print(player2.show_hand())
    
    # Show final status
    print("\n--- Game Status ---")
    print(player1.get_status())
    print(player2.get_status())
    
    print("\n--- Explanation ---")
    print("• Each player formed a meld (3 matching Pokemon tiles)")
    print("• Each Pikachu and Squirtle is worth 5 points")
    print("• Each meld earned 15 points (3 tiles × 5 points)")
    print("• In a full game, players continue until someone forms 4 melds")
    print("  or the draw pile runs out")
    print("\n--- Demo Complete ---\n")


if __name__ == "__main__":
    demo_game()
