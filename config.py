"""
Configuration file for the Snake game.
Contains all the constants and settings for the game.
"""

# Window configuration
BLOCK_SIZE = 20  # Size of each block in pixels

# Grid dimensions for simple console version
WIDTH_SIMPLE = 30  # Number of blocks horizontally
HEIGHT_SIMPLE = 16  # Number of blocks vertically

# Grid dimensions for pygame version
WIDTH_PYGAME = 30  # Number of blocks horizontally
HEIGHT_PYGAME = 30  # Number of blocks vertically

# Window size for pygame version
WINDOW_SIZE = (BLOCK_SIZE * WIDTH_PYGAME, BLOCK_SIZE * HEIGHT_PYGAME)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Game settings
INITIAL_SNAKE_LENGTH = 3  # Initial length of the snake in blocks
INITIAL_SNAKE_SPEED = 10  # Initial speed of the snake (frames per second)
SPEED_INCREASE = 0.5      # How much the speed increases each time
AUTO_GROWTH_INTERVAL = 5  # Time in seconds before the snake grows automatically

# Direction constants
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
