import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import io
import requests
from typing import List, Optional
from game import PokeJongGame 
from player import Player
from pokemon_tile import PokemonTile
from game import get_tile_counts

# --- Global UI Constants ---
TILE_WIDTH, TILE_HEIGHT = 80, 100
HIDDEN_TILE_IMAGE_URL = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/items/poke-ball.png"


class GameUI:
    """Manages the Tkinter Graphical User Interface for PokeJong."""

    def __init__(self, master: tk.Tk, game: PokeJongGame):
        self.master = master
        self.game = game
        self.master.title("PokeJong - Pokémon Mahjong")
        
        self.tile_images = {} 
        self.hidden_tile_image = self._load_image_from_url(HIDDEN_TILE_IMAGE_URL, TILE_WIDTH, TILE_HEIGHT)
        
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

        # --- Row 0: Game Status ---
        self.status_label = ttk.Label(main_frame, text="Game Status: Setting Up...", font=('Arial', 12, 'bold'))
        self.status_label.grid(row=0, column=0, columnspan=2, pady=10)

        # --- Row 1: Player Status Area (FIXED MISSING FRAMES) ---
        player_status_frame = ttk.Frame(main_frame)
        player_status_frame.grid(row=1, column=0, columnspan=2, pady=5, sticky="ew")

        # Frame for Player 1 (Ash) - Defined here
        self.ash_frame = ttk.LabelFrame(player_status_frame, text=self.game.player1.name, padding="10")
        self.ash_frame.pack(side="left", expand=True, fill="both", padx=10)
        self.ash_score_label = ttk.Label(self.ash_frame, text=f"Score: {self.game.player1.score}")
        self.ash_score_label.pack()

        # Frame for Player 2 (Joy/Gary) - Defined here
        self.joy_frame = ttk.LabelFrame(player_status_frame, text=self.game.player2.name, padding="10")
        self.joy_frame.pack(side="right", expand=True, fill="both", padx=10)
        self.joy_score_label = ttk.Label(self.joy_frame, text=f"Score: {self.game.player2.score}")
        self.joy_score_label.pack()
        
        # --- Row 2: Opponent's Hand Display ---
        self.opponent_hand_frame = ttk.LabelFrame(main_frame, text="Opponent's Hand", padding="10")
        self.opponent_hand_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")

        # --- Row 3: Discard/Wall Area (FIXED GRID ROW) ---
        center_frame = ttk.LabelFrame(main_frame, text="Draw Pile / Discards", padding="10")
        center_frame.grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")
        
        self.wall_label = ttk.Label(center_frame, text="Wall: 0 tiles")
        self.wall_label.grid(row=0, column=0, padx=10)
        self.discard_label = ttk.Label(center_frame, text="Discards: None")
        self.discard_label.grid(row=0, column=1, padx=10)

        # --- Row 4: Action Buttons (FIXED GRID ROW) ---
        button_frame = ttk.Frame(main_frame, padding="10")
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Form Meld (Pung)", command=self._handle_meld).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Discard Selected", command=self._handle_discard).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Show Opponent's Discards", command=self._show_opponent_discards).grid(row=0, column=2, padx=5)
        
        # --- Row 5: Current Player Hand Display (FIXED GRID ROW) ---
        self.current_player_hand_frame = ttk.LabelFrame(main_frame, text="Your Hand", padding="10")
        self.current_player_hand_frame.grid(row=5, column=0, columnspan=2, pady=10, sticky="ew")
    
    def _draw_hand(self, player: Player, target_frame : ttk.LabelFrame, is_current_player: bool):
        """Draws a player's hand, fully visible for testing purposes."""
        # 1. Clear the frame
        for widget in target_frame.winfo_children():
            widget.destroy()

        hand = player.hand
        # Update label text to clearly show whose hand it is
        turn_status = "ACTIVE TURN ➡️" if is_current_player else "Opponent"
        target_frame.config(text=f"{player.name}'s Hand ({len(hand)} Tiles) - {turn_status}")

        # Reset selection if it's the current player's frame
        if is_current_player:
            self.selected_indices = []

        # 2. Draw the tiles
        for i, tile in enumerate(hand):
            # FIX: Always set is_exposed = True for testing without masking
            is_exposed = True 
            image = self.get_tile_image(tile, is_exposed=is_exposed)

            tile_label = ttk.Label(target_frame, image=image, relief="raised", borderwidth=1)
            tile_label.grid(row=0, column=i, padx=2)

            # Only the current player's tiles should be interactive for discard/meld
            if is_current_player:
                tile_label.bind("<Button-1>", lambda event, index=i, label=tile_label: self._toggle_selection(index, label))

        # 3. Draw Melds (placed below the tiles)
        meld_text_parts = []
        for meld in player.melds:
            meld_names = ", ".join(t.name for t in meld)
            meld_text_parts.append(f"({meld_names})")

        meld_text = "Melds: " + " | ".join(meld_text_parts)

        # Place the meld display label
        # Use a large columnspan to prevent cutoff
        ttk.Label(target_frame, text=meld_text).grid(row=1, column=0, columnspan=len(hand) + 5, pady=5)

    def _update_ui(self):
        """Refreshes all UI elements based on the current game state."""
        current_player = self.game.current_player
        opponent = self.game.other_player
        
        # 1. Update Status Label
        status_text = f"Tiles Left: {len(self.game.draw_pile)}"
        if self.game.game_over:
             status_text = f"GAME OVER! Winner: {self.game.winner.name if self.game.winner else 'None'}"
        self.status_label.config(text=status_text)

        # 2. Update Draw/Discard Area
        player1 = self.game.player1
        player2 = self.game.player2

        self.ash_frame.config(borderwidth=2, relief="groove", text=self.game.player1.name)
        self.joy_frame.config(borderwidth=2, relief="groove", text=self.game.player1.name)
        
        self.ash_score_label.config(text=f"Score: {player1.score}")
        self.joy_score_label.config(text=f"Score: {player2.score}")

        # Apply highlight to the current player
        if current_player == player1:
            self.ash_frame.config(relief="solid", borderwidth=4, text=f"{player1.name} (YOUR TURN ➡️)")
        else:
            self.joy_frame.config(relief="solid", borderwidth=4, text=f"{player2.name} (YOUR TURN ➡️)")

        # 3. Redraw Player Hand -> Clear old tiles and reset selections
        self._draw_hand(opponent, self.opponent_hand_frame, is_current_player=False)
        self._draw_hand(current_player, self.current_player_hand_frame, is_current_player=True)
        
        # 4. Update Draw/Discard Area
        self.wall_label.config(text=f"Wall: {len(self.game.draw_pile)} tiles")
        last_discard = self.game.discard_pile[-1] if self.game.discard_pile else "None"
        self.discard_label.config(text=f"Last Discard: {last_discard}")


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
        self._draw_hand(self.game.current_player, self.current_player_hand_frame, is_current_player=True)

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