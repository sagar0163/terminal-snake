# Terminal Snake 🐍

Classic Snake game for Linux terminal - inspired by the iconic Nokia Snake game.

## Features

- 🎮 Classic snake gameplay
- 🍎 Multiple fruit types with different point values
- 📊 Score tracking with persistent high score
- ⚡ Speed increases as you grow
- 🎨 Colorful terminal UI
- ⌨️ WASD and Arrow key support

## Screenshots

```
 ███████╗ ██╗  ██╗ ██████╗ ███████╗██████╗ ████████╗██╗ ██████╗
 ██╔════╝ ██║  ██║██╔════╝ ██╔════╝██╔══██╗╚══██╔══╝██║██╔════╝
 █████╗   ███████║██║  ███╗█████╗  ██████╔╝   ██║   ██║██║     
 ██╔══╝   ██╔══██║██║   ██║██╔══╝  ██╔══██╗   ██║   ██║██║     
 ██║     ██║  ██║╚██████╔╝███████╗██║  ██║   ██║   ██║╚██████╗
 ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝ ╚═════╝
```

## Installation

```bash
# Clone the repository
git clone https://github.com/sagar0163/terminal-snake.git
cd terminal-snake

# No dependencies needed - uses Python's built-in curses library!
```

## How to Play

```bash
# Run the game
python3 snake.py
```

### Controls

| Key | Action |
|-----|--------|
| `↑` `↓` `←` `→` | Move snake |
| `W` `A` `S` `D` | Move snake (alternative) |
| `P` | Pause game |
| `Q` | Quit game |
| `SPACE` | Restart after game over |

### Fruits

| Fruit | Points | Rarity |
|-------|--------|--------|
| 🍎 Apple | 10 | Common |
| 🍊 Orange | 15 | Uncommon |
| 🍇 Grapes | 20 | Rare |
| 💎 Diamond | 50 | Very Rare |

## Requirements

- Python 3.6+
- Linux terminal (curses support)

### Windows / macOS

For non-Linux systems, use the alternative version:

```bash
pip install windows-curses  # Windows
# macOS usually has curses built-in
```

Then run:
```bash
python3 snake.py
```

## Files

```
terminal-snake/
├── snake.py    # Main game file
├── README.md   # This file
└── LICENSE    # MIT License
```

## How It Works

1. **Snake Movement**: The snake moves in the current direction
2. **Eating**: When the snake head hits food, it grows and score increases
3. **Collision**: Game ends if snake hits walls or itself
4. **Speed**: Game gets faster as the snake grows longer
5. **High Score**: Automatically saved to `~/.snake_highscore`

## License

MIT License - feel free to modify and share!

## Author

Created by Sagar Jadhav
