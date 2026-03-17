# Architecture Document

## System Architecture

```
┌─────────────────────────────────────────────┐
│           Terminal Snake Game                │
├─────────────────────────────────────────────┤
│  ┌─────────────┐  ┌──────────────────────┐ │
│  │ Game Engine │◄─┤  Renderer (curses)    │ │
│  │ - Snake     │  │  - Screen refresh     │ │
│  │ - Food      │  │  - UI elements        │ │
│  │ - Collision │  └──────────────────────┘ │
│  └─────────────┘                             │
│         │                                     │
│  ┌───────▼────────┐                          │
│  │ Power-Up Sys  │                          │
│  │ - Shield      │                          │
│  │ - Cut         │                          │
│  │ - Slow        │                          │
│  └───────────────┘                          │
│         │                                    │
│  ┌───────▼────────┐                         │
│  │ Achievement    │                         │
│  │ Tracker       │                         │
│  └───────────────┘                         │
└─────────────────────────────────────────────┘
```

## Components

### 1. Game Engine
- Snake movement and growth logic
- Food spawning and collision detection
- Boundary handling (wall wrap)

### 2. Power-Up System
- Shield: Allows passing through walls (5 seconds)
- Cut: Halves snake length, adds 50 points
- Slow: Reduces game speed

### 3. Achievement System
- Tracks player milestones
- Unlocks at 5 segments, 10 segments, 100pts, 500pts

### 4. Renderer (curses)
- Terminal screen management
- UI rendering (score, achievements, effects)

## Data Structures

```python
snake = [(x, y), ...]        # List of body segments
food = (x, y, type)          # Food position and type
powerups = {type: timer}     # Active power-ups
achievements = [unlocked]    # Unlocked achievements
```

## Game Loop

1. Process Input (WASD/P arrows)
2. Update Snake Position
3. Check Collisions (food, walls, self)
4. Update Power-Up Timers
5. Check Achievements
6. Render Frame
7. Sleep (control game speed)

## File Structure

```
terminal-snake/
├── snake.py       # Main game
├── README.md      # Documentation
└── specs/
    ├── BRD.md
    └── ARCHITECTURE.md
```
