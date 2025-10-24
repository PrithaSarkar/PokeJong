#!/usr/bin/env python3
"""
PokeJong - A Pokemon-themed 2-player Mahjong game.

Main entry point for the game.
"""

from game import PokeJongGame


def get_player_names():
    """Get player names from user input."""
    print("\n" + "="*60)
    print("POKEJONG - Pokemon Mahjong")
    print("="*60)
    print("\nA 2-player Pokemon-themed Mahjong game!")
    print("Match 3 identical Pokemon tiles to form melds and score points.")
    print("\nGame Rules:")
    print("- Each player starts with 13 tiles")
    print("- On your turn: Draw 1 tile, optionally form melds, then discard 1 tile")
    print("- Form melds by matching 3 identical Pokemon tiles")
    print("- Pokemon earn 5 points (ID 1-50) or 10 points (ID 51+)")
    print("- Win by forming 4 melds (12 tiles) with 1 tile remaining")
    print("- Or win by having the highest score when tiles run out!")
    print()
    
    player1 = input("Enter name for Player 1 (or press Enter for 'Player 1'): ").strip()
    player2 = input("Enter name for Player 2 (or press Enter for 'Player 2'): ").strip()
    
    if not player1:
        player1 = "Player 1"
    if not player2:
        player2 = "Player 2"
    
    return player1, player2


def display_menu():
    """Display the action menu."""
    print("\nActions:")
    print("  1. Form a meld (match 3 identical tiles)")
    print("  2. Discard a tile and end turn")
    print("  3. Show game state")
    print("  4. Quit game")


def play_turn(game: PokeJongGame):
    """
    Play a single turn.
    
    Args:
        game: The PokeJongGame instance
        
    Returns:
        True if turn completed normally, False if player quits
    """
    # Draw a tile
    if not game.draw_tile():
        print("\nNo more tiles to draw!")
        game.check_draw_condition()
        return True
    
    # Show current state
    game.show_game_state()
    
    # Player actions loop
    while True:
        display_menu()
        choice = input("\nChoose action (1-4): ").strip()
        
        if choice == "1":
            # Form a meld
            print("\nEnter 3 tile indices to form a meld (space-separated):")
            indices_input = input("Indices: ").strip()
            try:
                indices = [int(x) for x in indices_input.split()]
                if len(indices) != 3:
                    print("Error: You must select exactly 3 tiles!")
                    continue
                
                if game.form_meld(indices):
                    print("✓ Meld formed successfully!")
                    print(game.current_player.show_melds())
                    
                    # Check win condition
                    if game.check_win_condition():
                        return True
                else:
                    print("✗ Could not form meld. Tiles must all match!")
            except (ValueError, IndexError):
                print("Invalid input. Please enter valid tile indices.")
        
        elif choice == "2":
            # Discard a tile
            print("\nEnter tile index to discard:")
            try:
                tile_index = int(input("Index: ").strip())
                if game.discard_tile(tile_index):
                    return True
                else:
                    print("Invalid tile index!")
            except (ValueError, IndexError):
                print("Invalid input. Please enter a valid tile index.")
        
        elif choice == "3":
            # Show game state
            game.show_game_state()
        
        elif choice == "4":
            # Quit
            print("\nQuitting game...")
            return False
        
        else:
            print("Invalid choice. Please enter 1-4.")


def main():
    """Main game loop."""
    # Get player names
    player1_name, player2_name = get_player_names()
    
    # Initialize game
    game = PokeJongGame(player1_name, player2_name)
    
    try:
        # Setup game (this will fetch Pokemon from API)
        game.setup_game(num_pokemon=20)
    except Exception as e:
        print(f"\nError setting up game: {e}")
        print("Please check your internet connection and try again.")
        return
    
    print("\nGame starting!")
    print(f"{game.current_player.name} goes first!")
    
    # Main game loop
    while not game.game_over:
        if not play_turn(game):
            # Player quit
            break
        
        if game.game_over:
            break
        
        # Switch turns
        game.switch_turn()
        input("\nPress Enter to continue to next turn...")
    
    # Show final scores
    if game.game_over:
        game.show_final_scores()
    
    print("\nThanks for playing PokeJong!")


if __name__ == "__main__":
    main()
