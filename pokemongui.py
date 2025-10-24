# pokemongui.py

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import io
import requests
from typing import List, Optional
from game import PokeJongGame
from player import Player
from pokemon_tile import PokemonTile


# --- Global UI Constants ---
TILE_WIDTH, TILE_HEIGHT = 80, 100
HIDDEN_TILE_IMAGE_URL = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/items/poke-ball.png"


class GameUI:
    """Manages the Tkinter Graphical User Interface for PokeJong."""

    def __init__(self, master: tk.Tk, game: PokeJongGame):
        self.master = master
        self.game = game
        self.master.title("PokeJong - Pokémon Mahjong")
        
        # Image Cache to prevent garbage collection issues with Tkinter images
        self.tile_images = {} 
        self.hidden_tile_image = self._load_image_from_url(HIDDEN_TILE_IMAGE_URL, TILE_WIDTH, TILE_HEIGHT)
        
        # State tracking for player selections
        self.selected_indices = []

        self._create_widgets()
        self._update_ui()

    def _load_image_from_url(self, url: str, width: int, height: int) -> Optional[ImageTk.PhotoImage]:
        """Fetches an image from a URL and returns a PhotoImage object."""
        try:
            response = requests.get(url, stream=True, timeout=5)
            response.raise_for_status()
            image_data = response.content
            image = Image.open(io.BytesIO(image_data))
            image = image.resize((width, height), Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(image)
        except requests.RequestException as e:
            print(f"Error loading image from URL {url}: {e}")
            # Fallback to a simple colored block if image fails to load
            placeholder_image = Image.new('RGB', (width, height), color = 'grey')
            return ImageTk.PhotoImage(placeholder_image)

    def get_tile_image(self, tile: PokemonTile, is_exposed: bool = True) -> ImageTk.PhotoImage:
        """Returns the appropriate image for a tile, caching the result."""
        if not is_exposed:
            return self.hidden_tile_image
            
        if tile.pokemon_id not in self.tile_images:
    
            url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{tile.pokemon_id}.png"
            
            self.tile_images[tile.pokemon_id] = self._load_image_from_url(url, TILE_WIDTH, TILE_HEIGHT)
        
        return self.tile_images[tile.pokemon_id]

    def _create_widgets(self):
        """Sets up the main layout and interactive elements."""
        main_frame = ttk.Frame(self.master, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        # --- Game State Area (Top) ---
        self.status_label = ttk.Label(main_frame, text="Game Status: Setting Up...", font=('Arial', 12, 'bold'))
        self.status_label.grid(row=0, column=0, columnspan=2, pady=10)

        # --- Discard/Wall Area (Center) ---
        center_frame = ttk.LabelFrame(main_frame, text="Draw Pile / Discards", padding="10")
        center_frame.grid(row=1, column=0, columnspan=2, pady=10, sticky="ew")
        
        self.wall_label = ttk.Label(center_frame, text="Wall: 0 tiles")
        self.wall_label.grid(row=0, column=0, padx=10)
        self.discard_label = ttk.Label(center_frame, text="Discards: None")
        self.discard_label.grid(row=0, column=1, padx=10)

        # --- Player Hand Display ---
        self.hand_frame = ttk.LabelFrame(main_frame, text="Your Hand", padding="10")
        self.hand_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")
        
        # --- Action Buttons ---
        button_frame = ttk.Frame(main_frame, padding="10")
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Form Meld (Pung)", command=self._handle_meld).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Discard Selected", command=self._handle_discard).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Show Opponent's Discards", command=self._show_opponent_discards).grid(row=0, column=2, padx=5)


    def _update_ui(self):
        """Refreshes all UI elements based on the current game state."""
        current_player = self.game.current_player
        
        # 1. Update Status Label
        status_text = f"Current Turn: {current_player.name} | Tiles Left: {len(self.game.draw_pile)}"
        if self.game.game_over:
             status_text = f"GAME OVER! Winner: {self.game.winner.name if self.game.winner else 'None'}"
        self.status_label.config(text=status_text)
        
        # 2. Update Draw/Discard Area
        self.wall_label.config(text=f"Wall: {len(self.game.draw_pile)} tiles")
        last_discard = self.game.discard_pile[-1] if self.game.discard_pile else "None"
        self.discard_label.config(text=f"Last Discard: {last_discard}")
        
        # 3. Redraw Player Hand
        for widget in self.hand_frame.winfo_children():
            widget.destroy()
        self.selected_indices = []

        hand = current_player.hand
        for i, tile in enumerate(hand):
            image = self.get_tile_image(tile, is_exposed=True)
            
            tile_label = ttk.Label(self.hand_frame, image=image, relief="raised", borderwidth=1)
            tile_label.grid(row=0, column=i, padx=2)
            
            # Bind click event to select/deselect the tile
            tile_label.bind("<Button-1>", lambda event, index=i, label=tile_label: self._toggle_selection(index, label))

        # 4. Display Melds (Simplified)
        meld_text = "Melds: " + " | ".join([f"{[t.name for t in meld]}" for meld in current_player.melds])
        ttk.Label(self.hand_frame, text=meld_text).grid(row=1, column=0, columnspan=len(hand), pady=5)


    def _toggle_selection(self, index: int, label: ttk.Label):
        """Handles tile selection for meld/discard actions."""
        if index in self.selected_indices:
            self.selected_indices.remove(index)
            label.config(relief="raised")
        else:
            if len(self.selected_indices) < 3: # Max 3 for Pung
                self.selected_indices.append(index)
                label.config(relief="sunken")

    def _handle_meld(self):
        """Attempts to form a meld with selected tiles."""
        if len(self.selected_indices) != 3:
            print("Select exactly 3 tiles for a Pung/Kong.")
            return

        # Call the game logic
        if self.game.form_meld(self.selected_indices):
            print("Meld formed successfully! Checking for win...")
            if self.game.check_win_condition():
                self._game_over_ui()
                return

            self._update_ui()
        else:
            print("Meld failed: Tiles must match.")
        
        self.selected_indices = []

    def _handle_discard(self):
        """Discards the single selected tile and switches turn."""
        if len(self.selected_indices) != 1:
            print("Select exactly 1 tile to discard.")
            return
            
        discard_index = self.selected_indices[0]
        
        # Call the game logic for discard
        if self.game.discard_tile(discard_index):
            
            # Opponent Check (Ron/Pung/Kong) happens here
            discarded_tile = self.game.discard_pile[-1]
            action_taken = self.game.check_opponent_action(discarded_tile)
            
            if not action_taken:
                self.game.switch_turn()
            
            # Force the next player to draw when they start their turn
            self.game.draw_tile() 
            
            self._update_ui() # Refresh the UI for the new player/state
        else:
            print("Discard failed.")

    def _show_opponent_discards(self):
        """Placeholder for showing the other player's discards/melds."""
        opponent = self.game.other_player
        print(f"\n--- {opponent.name}'s Status ---")
        print(f"Discards: {opponent.discards}")
        print(f"Melds: {opponent.melds}")

    def _game_over_ui(self):
        """Displays game over message."""
        self.status_label.config(text=f"GAME OVER! {self.game.winner.name if self.game.winner else 'TIE'} WINS!")
        # Disable buttons, show final scores, etc.
        # ... (further UI cleanup for end state) ...

def start_gui():
    """Initializes the Tkinter window and starts the game."""
    root = tk.Tk()
    
    # Initialize game core logic
    game = PokeJongGame("Ash", "Gary")
    try:
        # Note: num_pokemon should be low for fast testing (e.g., 10-15)
        game.setup_game(num_pokemon=15) 
        
        # Player 1 draws the first tile to start with 14
        game.draw_tile() 

        # Initialize the GUI
        app = GameUI(root, game)
        root.mainloop()

    except requests.RequestException:
        print("\nFATAL: Failed to connect to PokeAPI. Check internet/API status.")
    except Exception as e:
        print(f"\nAn error occurred during startup: {e}")

if __name__ == '__main__':
    start_gui()