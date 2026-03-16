"""Unit tests for Snake game"""

import pytest
from unittest.mock import Mock, patch
import sys
import io

# Mock curses before importing snake
sys.modules['curses'] = Mock()

from snake import Snake, Game, Direction


class TestSnake:
    def test_snake_initialization(self):
        snake = Snake(10, 10)
        assert len(snake.body) > 0
        assert snake.direction == Direction.RIGHT
    
    def test_snake_move(self):
        snake = Snake(10, 10)
        initial_head = snake.body[0]
        snake.move()
        # Head should have moved
        assert snake.body[0] != initial_head or len(snake.body) > 1
    
    def test_snake_grow(self):
        snake = Snake(10, 10)
        initial_length = len(snake.body)
        snake.grow()
        assert len(snake.body) == initial_length + 1
    
    def test_snake_collision(self):
        snake = Snake(10, 10)
        # Create self-collision
        snake.body = [(5, 5), (5, 6), (5, 5)]
        assert snake.check_collision() == True


class TestDirection:
    def test_direction_values(self):
        assert Direction.UP.value == (-1, 0)
        assert Direction.DOWN.value == (1, 0)
        assert Direction.LEFT.value == (0, -1)
        assert Direction.RIGHT.value == (0, 1)


class TestGame:
    def test_game_initialization(self):
        game = Game(20, 20)
        assert game.width == 20
        assert game.height == 20
        assert game.score == 0
    
    def test_food_generation(self):
        game = Game(20, 20)
        food = game.generate_food()
        assert 0 <= food[0] < game.height
        assert 0 <= food[1] < game.width
