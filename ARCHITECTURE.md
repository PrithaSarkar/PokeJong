# PokeJong Architecture

## Project Structure

```
PokeJong/
├── main.py             # Main entry point with CLI interface
├── game.py             # Core game logic and state management
├── player.py           # Player class with hand and meld management
├── pokemon_tile.py     # Pokemon tile class and PokeAPI integration
├── demo.py             # Demo script showing game mechanics
├── test_game.py        # Test suite
├── requirements.txt    # Python dependencies
└── README.md          # User documentation
```

## Core Components

### PokemonTile (pokemon_tile.py)
- Represents a single Pokemon-themed Mahjong tile
- Stores Pokemon ID, name, and point value (5 or 10)
- Implements equality checking for matching tiles

### PokemonTileFactory (pokemon_tile.py)
- Fetches Pokemon data from PokeAPI
- Creates tiles with appropriate point values based on Pokemon ID
- Generates complete tile sets for the game (20 Pokemon × 4 copies)
- Has fallback mechanism if API is unavailable

### Player (player.py)
- Manages player's hand (tiles held)
- Tracks formed melds (sets of 3 matching tiles)
- Calculates score based on melds
- Handles drawing and discarding tiles

### PokeJongGame (game.py)
- Main game controller
- Manages game state and turn-based flow
- Handles draw pile and discard pile
- Implements win conditions:
  - Form 4 melds (12 tiles) + 1 remaining tile
  - Highest score when draw pile is empty
- Switches turns between players

## Game Flow

```
1. Game Setup
   ├── Fetch 20 Pokemon from PokeAPI
   ├── Create 4 copies of each (80 tiles total)
   ├── Shuffle tiles
   └── Deal 13 tiles to each player (54 tiles remaining)

2. Turn Cycle (repeat until game over)
   ├── Current player draws 1 tile
   ├── Player can form melds (optional, multiple)
   │   └── Each meld: 3 identical Pokemon tiles
   ├── Player discards 1 tile
   └── Switch to other player

3. Win Conditions
   ├── Player forms 4 melds with 1 tile remaining
   └── OR draw pile empties (winner = highest score)
```

## Point System

- Pokemon with ID 1-50: **5 points** per tile
- Pokemon with ID 51+: **10 points** per tile
- Score is accumulated when forming melds
- Example: Meld of 3 Pikachu (ID 25) = 3 × 5 = **15 points**

## Technical Details

### Dependencies
- **requests**: For PokeAPI HTTP requests
- **Python 3.6+**: Core language

### API Integration
- Uses PokeAPI (https://pokeapi.co/api/v2/pokemon/{id})
- Fetches Pokemon name and ID
- Has fallback for offline mode (generates placeholder tiles)

### Testing
- Unit tests for all core components
- Integration test for game setup
- Demo script for showcasing mechanics

## Future Enhancements
- Add special tiles (wild cards, bonus Pokemon)
- Implement different point values based on Pokemon rarity
- Add GUI using pygame or tkinter
- Support for more than 2 players
- Save/load game state
- Online multiplayer support
