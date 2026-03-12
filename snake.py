#!/usr/bin/env python3
"""
Classic Snake Game - Enhanced Edition v2.0
==========================================
A retro-style Snake game for Linux terminal with power-ups and achievements.

Controls:
- Arrow Keys or WASD to move
- Q to quit
- P to pause
- SPACE to restart after game over

Version 2.0 Features:
- Power-ups system
- Achievements
- Visual effects
- Enhanced scoring
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
HEIGHT = 22
SNAKE_CHAR = 'o'
SNAKE_HEAD = 'O'
FOOD_CHAR = '*'
WALL_CHAR = '█'

# Fruit types with different effects
FRUITS = {
    '🍎': {'points': 10, 'color': 1, 'effect': 'none'},
    '🍊': {'points': 15, 'color': 2, 'effect': 'none'},
    '🍇': {'points': 20, 'color': 3, 'effect': 'none'},
    '💎': {'points': 50, 'color': 4, 'effect': 'bonus'},
    '⭐': {'points': 30, 'color': 5, 'effect': 'speed'},
    '🐢': {'points': 10, 'color': 6, 'effect': 'slow'},
}

# Power-ups
POWERUPS = {
    '🛡️': {'duration': 5, 'desc': 'Shield - pass through walls'},
    '✂️': {'duration': 8, 'desc': 'Cut - halve snake length'},
    '⏰': {'duration': 10, 'desc': 'Slow - slow down for points'},
}


class SnakeGame:
    """Enhanced Snake Game v2.0"""
    
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.score = 0
        self.high_score = self.load_high_score()
        self.paused = False
        self.game_over = False
        
        # Initialize snake (center of screen)
        self.snake = deque([(HEIGHT//2, WIDTH//2)])
        self.direction = (0, -1)
        self.next_direction = (0, -1)
        
        # Food
        self.food = None
        self.fruit_type = '🍎'
        self.place_food()
        
        # Power-ups
        self.powerup = None
        self.powerup_timer = 0
        self.active_powerup = None
        
        # Speed
        self.base_speed = 0.12
        self.current_speed = self.base_speed
        
        # Achievements tracking
        self.achievements = set()
        
        # Visual effects
        self.effects = []
        
        self.setup_colors()
    
    def setup_colors(self):
        """Initialize curses colors"""
        if curses.has_colors():
            curses.start_color()
            curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
            curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
            curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
            curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)
            curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_BLACK)
            curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_BLACK)
            curses.init_pair(7, curses.COLOR_BLUE, curses.COLOR_BLACK)
    
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
        attempts = 0
        while attempts < 100:
            row = random.randint(1, HEIGHT - 2)
            col = random.randint(1, WIDTH - 2)
            if (row, col) not in self.snake:
                self.food = (row, col)
                
                # Random fruit selection
                rand = random.random()
                if rand < 0.05:
                    self.fruit_type = '💎'
                elif rand < 0.15:
                    self.fruit_type = '⭐'
                elif rand < 0.25:
                    self.fruit_type = '🐢'
                elif rand < 0.45:
                    self.fruit_type = '🍇'
                elif rand < 0.65:
                    self.fruit_type = '🍊'
                else:
                    self.fruit_type = '🍎'
                break
            attempts += 1
    
    def place_powerup(self):
        """Place power-up randomly"""
        if random.random() < 0.1 and not self.powerup:  # 10% chance
            attempts = 0
            while attempts < 50:
                row = random.randint(1, HEIGHT - 2)
                col = random.randint(1, WIDTH - 2)
                if (row, col) not in self.snake and (row, col) != self.food:
                    self.powerup = (row, col)
                    self.powerup_type = random.choice(list(POWERUPS.keys()))
                    break
                attempts += 1
    
    def apply_powerup(self, ptype):
        """Apply power-up effect"""
        self.active_powerup = ptype
        self.powerup_timer = POWERUPS[ptype]['duration']
        
        if ptype == '✂️':
            # Cut snake in half
            new_len = max(1, len(self.snake) // 2)
            while len(self.snake) > new_len:
                self.snake.pop()
            self.score += 50
        
        elif ptype == '⏰':
            # Slow mode - temporary speed reduction
            self.current_speed = self.base_speed * 1.5
    
    def update_powerup(self):
        """Update power-up timers"""
        if self.powerup_timer > 0:
            self.powerup_timer -= 1
            if self.powerup_timer == 0:
                self.active_powerup = None
                self.current_speed = max(0.05, self.base_speed - len(self.snake) * 0.003)
    
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
    
    def check_achievements(self):
        """Check for achievements"""
        if len(self.snake) >= 5 and 'first_5' not in self.achievements:
            self.achievements.add('first_5')
            self.effects.append('🎉 Got 5 segments!')
        
        if len(self.snake) >= 10 and 'first_10' not in self.achievements:
            self.achievements.add('first_10')
            self.effects.append('🌟 Got 10 segments!')
        
        if self.score >= 100 and 'score_100' not in self.achievements:
            self.achievements.add('score_100')
            self.effects.append('💯 Score 100!')
        
        if self.score >= 500 and 'score_500' not in self.achievements:
            self.achievements.add('score_500')
            self.effects.append('🏆 Score 500!')
    
    def update(self):
        """Update game state"""
        if self.paused or self.game_over:
            return
        
        # Update direction
        self.direction = self.next_direction
        
        # Move snake
        head = self.snake[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        
        # Wall collision (with shield powerup)
        if (new_head[0] <= 0 or new_head[0] >= HEIGHT - 1 or
            new_head[1] <= 0 or new_head[1] >= WIDTH - 1):
            if self.active_powerup == '🛡️':
                # Wrap around
                new_head = (new_head[0] % (HEIGHT - 1), new_head[1] % (WIDTH - 1))
                new_head = (max(1, min(HEIGHT - 2, new_head[0])), 
                           max(1, min(WIDTH - 2, new_head[1])))
            else:
                self.game_over = True
                return
        
        # Self collision
        if new_head in self.snake:
            self.game_over = True
            return
        
        # Add new head
        self.snake.appendleft(new_head)
        
        # Check food
        if new_head == self.food:
            points = FRUITS[self.fruit_type]['points']
            effect = FRUITS[self.fruit_type]['effect']
            
            # Apply fruit effect
            if effect == 'speed':
                self.current_speed = max(0.03, self.current_speed - 0.02)
                self.effects.append('⚡ Speed boost!')
            elif effect == 'slow':
                self.current_speed = min(0.2, self.current_speed + 0.03)
                self.effects.append('🐢 Slow mode')
            elif effect == 'bonus':
                self.effects.append('💎 Bonus points!')
            
            self.score += points
            self.check_achievements()
            self.place_food()
            self.place_powerup()
        else:
            self.snake.pop()
        
        # Check powerup
        if new_head == self.powerup and self.powerup:
            self.apply_powerup(self.powerup_type)
            self.effects.append(f'{self.powerup_type} {POWERUPS[self.powerup_type]["desc"]}!')
            self.powerup = None
        
        # Update powerup
        self.update_powerup()
        
        # Update speed
        self.current_speed = max(0.05, self.base_speed - len(self.snake) * 0.003)
        
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
        for i, (row, col) in enumerate(self.snake):
            char = SNAKE_HEAD if i == 0 else SNAKE_CHAR
            color = curses.color_pair(7) if i == 0 else curses.color_pair(5)
            self.stdscr.attron(color)
            self.stdscr.addch(row, col, char)
            self.stdscr.attroff(color)
        
        # Draw food
        if self.food:
            color = FRUITS[self.fruit_type]['color']
            self.stdscr.attron(curses.color_pair(color))
            self.stdscr.addch(self.food[0], self.food[1], self.fruit_type)
            self.stdscr.attroff(curses.color_pair(color))
        
        # Draw powerup
        if self.powerup:
            self.stdscr.attron(curses.color_pair(4) | curses.A_BOLD)
            self.stdscr.addch(self.powerup[0], self.powerup[1], self.powerup_type)
            self.stdscr.attroff(curses.color_pair(4) | curses.A_BOLD)
        
        # Draw UI
        score_text = f" Score: {self.score} "
        high_text = f" High: {self.high_score} "
        len_text = f" Length: {len(self.snake)} "
        
        self.stdscr.addstr(HEIGHT, 1, score_text, curses.color_pair(3) | curses.A_BOLD)
        self.stdscr.addstr(HEIGHT, 20, len_text, curses.color_pair(5))
        self.stdscr.addstr(HEIGHT, 40, high_text, curses.color_pair(4))
        
        # Draw active powerup
        if self.active_powerup and self.powerup_timer > 0:
            power_text = f" {self.active_powerup} {self.powerup_timer}s "
            self.stdscr.addstr(HEIGHT, 1, power_text, curses.color_pair(2) | curses.A_BOLD)
        
        # Draw effects
        if self.effects:
            effect_text = self.effects[-1]
            self.stdscr.addstr(1, WIDTH - len(effect_text) - 2, effect_text, curses.color_pair(3))
        
        # Controls
        controls = "WASD/Arrows: Move | P: Pause | Q: Quit"
        self.stdscr.addstr(HEIGHT + 1, (WIDTH - len(controls)) // 2, controls, curses.color_pair(6))
        
        # Pause overlay
        if self.paused:
            self.draw_overlay("⏸️ PAUSED", "Press P to continue")
        
        # Game over overlay
        if self.game_over:
            final_text = f"Final Score: {self.score}"
            len_text = f"Length: {len(self.snake)}"
            self.draw_overlay("💀 GAME OVER", final_text, len_text, "Press SPACE to restart")
            
            if self.score >= self.high_score:
                self.save_high_score()
                self.stdscr.addstr(HEIGHT // 2 - 3, (WIDTH - 15) // 2, "🏆 NEW HIGH SCORE!", 
                                  curses.color_pair(4) | curses.A_BOLD)
        
        self.stdscr.refresh()
    
    def draw_overlay(self, *lines):
        """Draw overlay with centered text"""
        # Darken background
        for y in range(1, HEIGHT - 1):
            for x in range(1, WIDTH - 1):
                try:
                    char = self.stdscr.inch(y, x)
                    if char & 0xFF not in [ord(WALL_CHAR), ord(' ')]:
                        self.stdscr.addch(y, x, char & 0xFF, curses.A_DIM)
                except:
                    pass
        
        # Draw text
        start_y = HEIGHT // 2 - len(lines) // 2
        for i, line in enumerate(lines):
            y = start_y + i
            x = (WIDTH - len(line)) // 2
            self.stdscr.attron(curses.color_pair(6) | curses.A_BOLD)
            self.stdscr.addstr(y, x, line)
            self.stdscr.attroff(curses.color_pair(6) | curses.A_BOLD)
    
    def run(self):
        """Main game loop"""
        curses.curs_set(0)
        self.stdscr.nodelay(True)
        
        last_update = time.time()
        
        while True:
            action = self.get_input()
            
            if action == 'quit':
                break
            elif action == 'pause':
                self.paused = not self.paused
            elif action == 'restart' and self.game_over:
                self.__init__(self.stdscr)
            
            if not self.paused and not self.game_over:
                if time.time() - last_update >= self.current_speed:
                    self.update()
                    last_update = time.time()
            
            self.draw()
            time.sleep(0.01)


def main(stdscr):
    """Main entry point"""
    curses.curs_set(0)
    stdscr.clear()
    
    # Title screen
    stdscr.nodelay(False)
    title = """
    ╔═══════════════════════════════════════╗
    ║                                       ║
    ║    🐍 SNAKE GAME v2.0 🐍              ║
    ║                                       ║
    ║    Enhanced with Power-ups!           ║
    ║                                       ║
    ╚═══════════════════════════════════════╝
    
    """
    y = 3
    for line in title.split('\n'):
        stdscr.addstr(y, (WIDTH - len(line)) // 2, line, curses.color_pair(3))
        y += 1
    
    stdscr.addstr(y + 2, (WIDTH - 26) // 2, "Press any key to start...", curses.color_pair(6))
    stdscr.addstr(y + 4, (WIDTH - 24) // 2, "Q: Quit | P: Pause | SPACE: Restart")
    stdscr.refresh()
    stdscr.getch()
    
    game = SnakeGame(stdscr)
    game.run()


if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)
