# Architecture Document: Terminal Snake

## 1. System Overview

Terminal Snake is a Python-based arcade game using the curses library for terminal rendering. It implements a classic snake game loop with power-ups, achievements, and special fruit mechanics.

## 2. Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      Main Game Loop                          │
│                    (snake.py)                               │
└─────────────────────┬───────────────────────────────────────┘
                      │
    ┌─────────────────┼─────────────────┐
    ▼                 ▼                 ▼
┌─────────┐     ┌───────────┐     ┌──────────┐
│ Input   │     │  Game     │     │ Display  │
│ Handler │     │  Logic    │     │ (Curses) │
└─────────┘     └───────────┘     └──────────┘
    │                 │                 │
    │                 ▼                 │
    │          ┌───────────┐            │
    │          │  Snake   │            │
    │          │  Entity  │            │
    │          └───────────┘            │
    │                 │                 │
    │                 ▼                 │
    │          ┌───────────┐            │
    │          │  Fruits  │            │
    │          │ & Powerups│            │
    │          └───────────┘            │
    │                 │                 │
    │                 ▼                 │
    │          ┌───────────┐            │
    │          │Collision │            │
    │          │ Detection│            │
    │          └───────────┘            │
    │                                   │
    └───────────────────────────────────┘
```

## 3. Core Components

### Game Loop
- Handles input, updates game state, and renders display at ~15 FPS
- Manages game states: playing, paused, game over

### Snake Entity
- Manages snake segments (list of coordinates)
- Handles movement, growth, and collision detection
- Supports power-up effects (shield, cut, slow)

### Fruits & Power-ups
- Spawns fruits at random positions
- Different fruit types with unique effects
- Power-up timer management

### Achievement System
- Tracks player milestones
- Unlocks achievements based on score/length

## 4. File Structure

```
terminal-snake/
├── snake.py           # Main game
├── specs/             # Documentation
└── README.md
```

---

*Document Version: 1.0*  
*Created: 2026-03-17*
