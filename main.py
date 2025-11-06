"""
PokeJong - A Pokemon-themed 2-player Mahjong game.

Main entry point for the game.
"""

import tkinter as tk
import requests

from game import PokeJongGame
from pokemongui import GameUI

def start_gui():
    print("Starting PokéJong GUI...")

    root = tk.Tk()
    # Set default player names for the GUI
    game = PokeJongGame(player1_name="Ash Ketchum", player2_name="Nurse Joy") 
    
    try:
        # Set up the game and fetch initial Pokémon data
        # num_pokemon set to low for faster initial load
        game.setup_game(num_pokemon=20) 
        
        # Player 1 (Dealer) draws 14 tiles to start the game
        game.draw_tile() 

        # --- 2. Initialize and Run the GUI ---
        # The GameUI class is passed the Tkinter root and the game object
        app = GameUI(root, game) 
        
        # Start the Tkinter event loop - this keeps the window open and responsive
        root.mainloop() 

    except requests.RequestException:
        print("\nFATAL: Failed to connect to PokeAPI. Please check your internet connection.")
        # If API fails, destroy the empty window
        root.destroy() 
    except Exception as e:
        print(f"\nAn error occurred during GUI or Game startup: {e}")
        root.destroy()


if __name__ == "__main__":
    # This is the single entry point, launching the GUI
    start_gui()
