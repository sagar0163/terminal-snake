# Business Requirements Document (BRD)

## Project Overview
- **Project Name**: Terminal Snake
- **Type**: Classic Snake Game for Linux Terminal
- **Core Functionality**: Enhanced snake game with power-ups, achievements, and visual effects
- **Target Users**: Linux users looking for a fun terminal-based game

## Features
1. **Classic Snake Gameplay** - Control snake to eat food and grow
2. **Power-Ups System** - Shield, Cut, Slow abilities with timed effects
3. **Special Fruits** - Apple, Orange, Grapes, Star (speed boost), Diamond (bonus), Turtle (slow)
4. **Achievements System** - Unlock achievements (5 segments, 10 segments, 100pts, 500pts)
5. **Wall Wrap** - Pass through walls with shield power-up
6. **Visual Effects** - On-screen effects and feedback
7. **Enhanced UI** - Better score display and controls
8. **Pause/Resume** - P to pause, Q to quit, SPACE to restart

## Tech Stack
- **Language**: Python 3
- **Library**: curses (terminal UI)
- **Platform**: Linux terminal

## User Stories
1. As a player, I want to control the snake direction so that I can eat food
2. As a player, I want power-ups so that I can get special abilities
3. As a player, I want achievements so that I have goals to achieve
4. As a player, I want different fruits with different effects so that the game is varied

## Requirements
- Python 3.6+
- Linux terminal with curses support

## Future Enhancements
- Multiplayer mode
- High score persistence
- Level system
- Sound effects
- Custom themes/skins
