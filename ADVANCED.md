# Snake Game - Advanced Features

## Controls

| Key | Action |
|-----|--------|
| Arrow Keys | Move snake |
| Space | Pause/Resume |
| Q | Quit |

## Game Modes

### Classic
- Standard snake gameplay
- Grow on eating food
- Die on wall/self collision

### Speed Run
- Timer-based
- Collect maximum food in limited time

### Infinite
- No walls (wrap around)
- Survival mode

## Scoring

- Food: +10 points
- Speed bonus: +5 points per level
- Time bonus: +1 point per second

## Customization

```bash
# Custom speed
python snake.py --speed 0.1

# Custom size
python snake.py --width 30 --height 20

# Dark mode
python snake.py --theme dark
```
