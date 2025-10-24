# PokeJong - Example Gameplay

## Starting the Game

```bash
$ python main.py

============================================================
POKEJONG - Pokemon Mahjong
============================================================

A 2-player Pokemon-themed Mahjong game!
Match 3 identical Pokemon tiles to form melds and score points.

Game Rules:
- Each player starts with 13 tiles
- On your turn: Draw 1 tile, optionally form melds, then discard 1 tile
- Form melds by matching 3 identical Pokemon tiles
- Pokemon earn 5 points (ID 1-50) or 10 points (ID 51+)
- Win by forming 4 melds (12 tiles) with 1 tile remaining
- Or win by having the highest score when tiles run out!

Enter name for Player 1 (or press Enter for 'Player 1'): Alice
Enter name for Player 2 (or press Enter for 'Player 2'): Bob

Setting up PokeJong game...
Fetching Pokemon data from PokeAPI...
Game setup complete! 54 tiles remaining in draw pile.

Game starting!
Alice goes first!
```

## Example Turn

```
============================================================
CURRENT TURN: Alice
============================================================

Tiles remaining in draw pile: 54
Tiles in discard pile: 0

Alice - Score: 0 pts | Hand size: 14 | Melds: 0
Bob - Score: 0 pts | Hand size: 13 | Melds: 0

Alice's Hand:
  0: [Bulbasaur:5pts]
  1: [Bulbasaur:5pts]
  2: [Bulbasaur:5pts]
  3: [Pikachu:5pts]
  4: [Charmander:5pts]
  5: [Squirtle:5pts]
  6: [Pidgey:5pts]
  7: [Rattata:5pts]
  8: [Eevee:5pts]
  9: [Mewtwo:10pts]
  10: [Articuno:10pts]
  11: [Moltres:10pts]
  12: [Zapdos:10pts]
  13: [Jigglypuff:5pts]

Alice's Melds: None

Actions:
  1. Form a meld (match 3 identical tiles)
  2. Discard a tile and end turn
  3. Show game state
  4. Quit game

Choose action (1-4): 1

Enter 3 tile indices to form a meld (space-separated):
Indices: 0 1 2
✓ Meld formed successfully!
Alice's Melds:
  Meld 1: [Bulbasaur:5pts] [Bulbasaur:5pts] [Bulbasaur:5pts] (15 pts)

Choose action (1-4): 2

Enter tile index to discard:
Index: 10
Alice discarded: [Articuno:10pts]

Press Enter to continue to next turn...
```

## Example Winning Scenario

```
============================================================
CURRENT TURN: Alice
============================================================

Alice - Score: 60 pts | Hand size: 1 | Melds: 4
Bob - Score: 45 pts | Hand size: 5 | Melds: 3

Alice's Hand:
  0: [Pikachu:5pts]

Alice's Melds:
  Meld 1: [Bulbasaur:5pts] [Bulbasaur:5pts] [Bulbasaur:5pts] (15 pts)
  Meld 2: [Charmander:5pts] [Charmander:5pts] [Charmander:5pts] (15 pts)
  Meld 3: [Squirtle:5pts] [Squirtle:5pts] [Squirtle:5pts] (15 pts)
  Meld 4: [Mewtwo:10pts] [Mewtwo:10pts] [Mewtwo:10pts] (30 pts)

============================================================
GAME OVER!
============================================================

Alice: 60 points
Alice's Melds:
  Meld 1: [Bulbasaur:5pts] [Bulbasaur:5pts] [Bulbasaur:5pts] (15 pts)
  Meld 2: [Charmander:5pts] [Charmander:5pts] [Charmander:5pts] (15 pts)
  Meld 3: [Squirtle:5pts] [Squirtle:5pts] [Squirtle:5pts] (15 pts)
  Meld 4: [Mewtwo:10pts] [Mewtwo:10pts] [Mewtwo:10pts] (30 pts)

Bob: 45 points
Bob's Melds:
  Meld 1: [Pikachu:5pts] [Pikachu:5pts] [Pikachu:5pts] (15 pts)
  Meld 2: [Eevee:5pts] [Eevee:5pts] [Eevee:5pts] (15 pts)
  Meld 3: [Jigglypuff:5pts] [Jigglypuff:5pts] [Jigglypuff:5pts] (15 pts)

🎉 Alice WINS! 🎉

Thanks for playing PokeJong!
```

## Running the Demo

For a quick demonstration of game mechanics without playing:

```bash
$ python demo.py

============================================================
POKEJONG DEMO
============================================================

This demo shows how the game mechanics work.
In a real game, players would interact via the CLI.

Creating players and tiles...

--- Initial Setup ---

Alice's Hand:
  0: [Pikachu:5pts]
  1: [Pikachu:5pts]
  2: [Pikachu:5pts]
  3: [Bulbasaur:5pts]
  4: [Charmander:5pts]

--- Player 1's Turn ---
Alice notices they have 3 matching Pikachu tiles!
Forming a meld with tiles at indices 0, 1, 2...
✓ Meld formed successfully!
Alice's Melds:
  Meld 1: [Pikachu:5pts] [Pikachu:5pts] [Pikachu:5pts] (15 pts)

Current score: 15 points

--- Demo Complete ---
```

## Running Tests

```bash
$ python test_game.py

============================================================
Running PokeJong Tests
============================================================
Testing PokemonTile...
✓ PokemonTile tests passed!

Testing PokemonTileFactory...
✓ PokemonTileFactory tests passed!

Testing Player...
✓ Player tests passed!

Testing PokeJongGame initialization...
✓ PokeJongGame initialization tests passed!

Testing game setup...
✓ Game setup tests passed!

============================================================
ALL TESTS PASSED! ✓
============================================================
```

## Strategy Tips

1. **Look for matching sets**: Before discarding, check if you can form any melds
2. **Prioritize high-value Pokemon**: Melds with 10-point Pokemon are worth more
3. **Track discarded tiles**: Remember what your opponent discards
4. **Plan ahead**: Try to collect Pokemon that are close to forming melds
5. **Balance speed and points**: Sometimes it's better to form lower-point melds quickly
