#!/usr/bin/env python3
"""
Classic Snake Game
=================
A retro-style Snake game for Linux terminal.

Controls:
- Arrow Keys or WASD to move
- Q to quit
- P to pause
- SPACE to restart after game over

Features:
- Classic snake gameplay
- Score tracking
- High score persistence
- Speed increases as you grow
- Visual fruits with different effects
"""

import os
import sys
import time
import random
import curses
from collections import deque
from pathlib import Path

# Game constants
WIDTH = 40
HEIGHT = 20
SNAKE_CHAR = 'O'
SNAKE_HEAD = '@'
FOOD_CHAR = '*'
WALL_CHAR = '#'

# Fruit types with different effects
FRUITS = {
    '🍎': {'points': 10, 'color': 1},
    '🍊': {'points': 15, 'color': 2},
    '🍇': {'points': 20, 'color': 3},
    '💎': {'points': 50, 'color': 4},  # Bonus - rare
}


class SnakeGame:
    """Classic Snake Game"""
    
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.score = 0
        self.high_score = self.load_high_score()
        self.paused = False
        self.game_over = False
        
        # Initialize snake (center of screen)
        self.snake = deque([(HEIGHT//2, WIDTH//2)])
        self.direction = (0, -1)  # Moving left
        self.next_direction = (0, -1)
        
        # Place initial food
        self.food = None
        self.fruit_type = '🍎'
        self.place_food()
        
        # Game speed (decreases as you grow)
        self.base_speed = 0.15
        self.current_speed = self.base_speed
        
        # Colors
        self.setup_colors()
    
    def setup_colors(self):
        """Initialize curses colors"""
        if curses.has_colors():
            curses.start_color()
            curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)    # Apple
            curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Orange
            curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_BLACK) # Grapes
            curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)    # Diamond
            curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Snake
            curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_BLACK)    # Text
    
    def load_high_score(self):
        """Load high score from file"""
        try:
            score_file = Path.home() / ".snake_highscore"
            if score_file.exists():
                return int(score_file.read_text().strip())
        except:
            pass
        return 0
    
    def save_high_score(self):
        """Save high score to file"""
        try:
            score_file = Path.home() / ".snake_highscore"
            score_file.write_text(str(self.high_score))
        except:
            pass
    
    def place_food(self):
        """Place food at random position"""
        while True:
            row = random.randint(1, HEIGHT - 2)
            col = random.randint(1, WIDTH - 2)
            if (row, col) not in self.snake:
                self.food = (row, col)
                
                # Random fruit selection (diamond is rare)
                if random.random() < 0.1:  # 10% chance for diamond
                    self.fruit_type = '💎'
                elif random.random() < 0.3:
                    self.fruit_type = '🍇'
                elif random.random() < 0.5:
                    self.fruit_type = '🍊'
                else:
                    self.fruit_type = '🍎'
                break
    
    def get_input(self):
        """Get keyboard input"""
        try:
            key = self.stdscr.getch()
            
            if key == ord('q') or key == ord('Q'):
                return 'quit'
            elif key == ord('p') or key == ord('P'):
                return 'pause'
            elif key == ord(' '):
                return 'restart'
            elif key in [curses.KEY_UP, ord('w'), ord('W')]:
                if self.direction != (1, 0):
                    self.next_direction = (-1, 0)
            elif key in [curses.KEY_DOWN, ord('s'), ord('S')]:
                if self.direction != (-1, 0):
                    self.next_direction = (1, 0)
            elif key in [curses.KEY_LEFT, ord('a'), ord('A')]:
                if self.direction != (0, 1):
                    self.next_direction = (0, -1)
            elif key in [curses.KEY_RIGHT, ord('d'), ord('D')]:
                if self.direction != (0, -1):
                    self.next_direction = (0, 1)
        except:
            pass
        
        return None
    
    def update(self):
        """Update game state"""
        if self.paused or self.game_over:
            return
        
        # Update direction
        self.direction = self.next_direction
        
        # Move snake
        head = self.snake[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        
        # Check collision with walls
        if (new_head[0] <= 0 or new_head[0] >= HEIGHT - 1 or
            new_head[1] <= 0 or new_head[1] >= WIDTH - 1):
            self.game_over = True
            return
        
        # Check collision with self
        if new_head in self.snake:
            self.game_over = True
            return
        
        # Add new head
        self.snake.appendleft(new_head)
        
        # Check food
        if new_head == self.food:
            # Eat food
            points = FRUITS[self.fruit_type]['points']
            self.score += points
            
            # Speed up slightly
            self.current_speed = max(0.05, self.base_speed - len(self.snake) * 0.005)
            
            # Place new food
            self.place_food()
        else:
            # Remove tail
            self.snake.pop()
        
        # Update high score
        if self.score > self.high_score:
            self.high_score = self.score
    
    def draw(self):
        """Draw the game"""
        self.stdscr.clear()
        
        # Draw border
        self.stdscr.attron(curses.color_pair(6))
        for i in range(WIDTH):
            self.stdscr.addch(0, i, WALL_CHAR)
            self.stdscr.addch(HEIGHT - 1, i, WALL_CHAR)
        for i in range(HEIGHT):
            self.stdscr.addch(i, 0, WALL_CHAR)
            self.stdscr.addch(i, WIDTH - 1, WALL_CHAR)
        self.stdscr.attroff(curses.color_pair(6))
        
        # Draw snake
        self.stdscr.attron(curses.color_pair(5))
        for i, (row, col) in enumerate(self.snake):
            if i == 0:
                self.stdscr.addch(row, col, SNAKE_HEAD)
            else:
                self.stdscr.addch(row, col, SNAKE_CHAR)
        self.stdscr.attroff(curses.color_pair(5))
        
        # Draw food
        if self.food:
            color = FRUITS[self.fruit_type]['color']
            self.stdscr.attron(curses.color_pair(color))
            self.stdscr.addch(self.food[0], self.food[1], self.fruit_type)
            self.stdscr.attroff(curses.color_pair(color))
        
        # Draw score
        score_text = f"Score: {self.score}"
        high_text = f"High Score: {self.high_score}"
        self.stdscr.addstr(HEIGHT, 1, score_text)
        self.stdscr.addstr(HEIGHT, WIDTH - len(high_text) - 1, high_text)
        
        # Draw controls hint
        controls = "WASD/Arrows: Move | P: Pause | Q: Quit"
        self.stdscr.addstr(HEIGHT + 1, (WIDTH - len(controls)) // 2, controls)
        
        # Draw pause overlay
        if self.paused:
            self.draw_overlay("PAUSED", "Press P to continue")
        
        # Draw game over overlay
        if self.game_over:
            self.draw_overlay("GAME OVER", f"Final Score: {self.score}", "Press SPACE to restart")
            
            # Save high score
            if self.score >= self.high_score:
                self.save_high_score()
        
        self.stdscr.refresh()
    
    def draw_overlay(self, *lines):
        """Draw overlay with centered text"""
        start_y = HEIGHT // 2 - len(lines) // 2
        start_x = (WIDTH - max(len(line) for line in lines)) // 2
        
        # Darken background
        for y in range(HEIGHT):
            for x in range(WIDTH):
                try:
                    char = self.stdscr.inch(y, x)
                    if char & 0xFF not in [WALL_CHAR, ' ']:
                        self.stdscr.addch(y, x, char, curses.A_DIM)
                except:
                    pass
        
        # Draw text
        for i, line in enumerate(lines):
            y = start_y + i
            x = start_x
            self.stdscr.attron(curses.color_pair(6) | curses.A_BOLD)
            self.stdscr.addstr(y, x, line.center(WIDTH - 2))
            self.stdscr.attroff(curses.color_pair(6) | curses.A_BOLD)
    
    def run(self):
        """Main game loop"""
        curses.curs_set(0)  # Hide cursor
        self.stdscr.nodelay(True)
        
        last_update = time.time()
        
        while True:
            # Handle input
            action = self.get_input()
            
            if action == 'quit':
                break
            elif action == 'pause':
                self.paused = not self.paused
            elif action == 'restart' and self.game_over:
                # Reset game
                self.__init__(self.stdscr)
            
            # Update game
            if not self.paused and not self.game_over:
                if time.time() - last_update >= self.current_speed:
                    self.update()
                    last_update = time.time()
            
            # Draw
            self.draw()
            time.sleep(0.01)


def main(stdscr):
    """Main entry point"""
    # Setup terminal
    curses.curs_set(0)
    stdscr.clear()
    
    # Show title screen
    stdscr.nodelay(False)
    title = """
    ██████╗ ██╗  ██╗ ██████╗ ███████╗██████╗ ████████╗██╗ ██████╗
    ██╔══██╗██║  ██║██╔════╝ ██╔════╝██╔══██╗╚══██╔══╝██║██╔════╝
    ██████╔╝███████║██║  ███╗█████╗  ██████╔╝   ██║   ██║██║     
    ██╔═══╝ ██╔══██║██║   ██║██╔══╝  ██╔══██╗   ██║   ██║██║     
    ██║     ██║  ██║╚██████╔╝███████╗██║  ██║   ██║   ██║╚██████╗
    ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝ ╚═════╝
    
    """
    y = 2
    for line in title.split('\n'):
        stdscr.addstr(y, (WIDTH - len(line)) // 2, line)
        y += 1
    
    stdscr.addstr(y + 2, (WIDTH - 28) // 2, "Press any key to start...")
    stdscr.addstr(y + 4, (WIDTH - 20) // 2, "Q: Quit | P: Pause")
    stdscr.refresh()
    stdscr.getch()
    
    # Run game
    game = SnakeGame(stdscr)
    game.run()


if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"\nError: {e}")
        print("Make sure you're running in a terminal that supports curses.")
        sys.exit(1)
