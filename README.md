# PokeJong
A Pokémon themed 2-player Mahjong game.

## Description
PokeJong is a simplified 2-player Mahjong game with Pokemon-themed tiles. Each Pokemon tile carries either 5 points (Pokemon ID 1-50) or 10 points (Pokemon ID 51+). The game uses the PokeAPI to fetch real Pokemon data.

## Features
- 2-player turn-based gameplay
- Pokemon-themed tiles fetched from PokeAPI
- Point system: 5 points for lower ID Pokemon, 10 points for higher ID Pokemon
- Form melds (sets of 3 matching Pokemon tiles) to score points
- Win by forming 4 melds or having the highest score when tiles run out

## Installation

1. Clone the repository:
```bash
git clone https://github.com/PrithaSarkar/PokeJong.git
cd PokeJong
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## How to Play

Run the game:
```bash
python main.py
```

### Game Rules
1. Each player starts with 13 Pokemon tiles
2. On your turn:
   - Draw 1 tile from the draw pile
   - Optionally form melds (3 matching Pokemon tiles)
   - Discard 1 tile to end your turn
3. Form melds to score points:
   - Each meld must contain 3 identical Pokemon tiles
   - Points are awarded based on the Pokemon's point value
4. Win conditions:
   - Form 4 melds (12 tiles) with 1 tile remaining in hand
   - OR have the highest score when the draw pile is empty

### Pokemon Point Values
- Pokemon with ID 1-50: 5 points each
- Pokemon with ID 51+: 10 points each

## Game Components

- `main.py` - Main game entry point with CLI interface
- `game.py` - Core game logic and state management
- `player.py` - Player class handling hand, melds, and scores
- `pokemon_tile.py` - Pokemon tile class and PokeAPI integration

## Requirements
- Python 3.6+
- Internet connection (for PokeAPI access)
- requests library

## Example Gameplay
```
Player 1's turn:
- Draw a Pikachu tile
- Form a meld with 3 Bulbasaur tiles (15 points)
- Discard a Charmander tile

Player 2's turn:
- Draw a Squirtle tile
- No melds available
- Discard a Pidgey tile
```

## License
MIT License 
