"""
Snake game module containing the main game logic and classes.
Using a simplified PyGame approach with reduced graphics dependency.
"""
import pygame
import random
import time
import os
from config import *

# Initialize Pygame with a software-only driver to avoid graphics driver issues
os.environ['SDL_VIDEODRIVER'] = 'dummy'

class Snake:
    """
    Class representing the snake in the game.
    """
    def __init__(self):
        """Initialize the snake with its starting position and length."""
        self.length = INITIAL_SNAKE_LENGTH
        # Start the snake in the middle of the screen
        self.positions = [
            (GRID_SIZE // 2, GRID_SIZE // 2 + i) 
            for i in range(self.length)
        ]
        self.direction = UP
        self.last_auto_growth = time.time()
        
    def get_head_position(self):
        """Return the position of the snake's head."""
        return self.positions[0]
    
    def update(self):
        """Update the snake's position based on its direction."""
        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction
        new_head = ((head_x + dir_x) % (GRID_SIZE - 2) + 1, 
                   (head_y + dir_y) % (GRID_SIZE - 2) + 1)
        
        # Check if the snake hits itself
        if new_head in self.positions[1:]:
            return False  # Game over
        
        # Check if the snake hits the wall
        if (new_head[0] == 0 or new_head[0] == GRID_SIZE - 1 or 
            new_head[1] == 0 or new_head[1] == GRID_SIZE - 1):
            return False  # Game over
        
        # Add the new head position at the beginning of the list
        self.positions.insert(0, new_head)
        
        # Remove the tail if the snake hasn't grown
        if len(self.positions) > self.length:
            self.positions.pop()
            
        return True  # Game continues
    
    def auto_grow(self):
        """Automatically grow the snake based on time interval."""
        current_time = time.time()
        if current_time - self.last_auto_growth >= AUTO_GROWTH_INTERVAL:
            self.length += 1
            self.last_auto_growth = current_time
        
    def grow(self):
        """Increase the length of the snake."""
        self.length += 1
        
    def change_direction(self, direction):
        """
        Change the direction of the snake.
        Prevents changing to the opposite direction.
        """
        # Prevent changing to the opposite direction
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.direction = direction


class Candy:
    """
    Class representing the candy in the game.
    """
    def __init__(self, snake_positions, walls):
        """Initialize a candy at a random position, avoiding the snake and walls."""
        self.position = self.generate_position(snake_positions, walls)
        
    def generate_position(self, snake_positions, walls):
        """Generate a random position for the candy that is not inside the snake or walls."""
        while True:
            # Generate a random position within the game area (excluding the walls)
            position = (
                random.randint(1, GRID_SIZE - 2),
                random.randint(1, GRID_SIZE - 2)
            )
            # Check if the position is valid (not inside the snake or walls)
            if position not in snake_positions and position not in walls:
                return position


class Game:
    """
    Main game class that manages the game state and rendering.
    """
    def __init__(self):
        """Initialize the game with its starting state."""
        # Initialize pygame in a way that doesn't require display hardware
        pygame.init()
        
        # Initialize the console-based display
        self.reset_game()
        
    def reset_game(self):
        """Reset the game to its initial state."""
        self.snake = Snake()
        self.walls = self.create_walls()
        self.candy = Candy(self.snake.positions, self.walls)
        self.speed = INITIAL_SNAKE_SPEED
        self.score = 0
        self.game_over = False
        
    def create_walls(self):
        """Create the walls around the game area."""
        walls = []
        
        # Top and bottom walls
        for x in range(GRID_SIZE):
            walls.append((x, 0))
            walls.append((x, GRID_SIZE - 1))
            
        # Left and right walls
        for y in range(1, GRID_SIZE - 1):
            walls.append((0, y))
            walls.append((GRID_SIZE - 1, y))
            
        return walls
    
    def handle_events(self):
        """Handle key events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if self.game_over:
                    if event.key == pygame.K_r:
                        self.reset_game()
                else:
                    if event.key == pygame.K_UP:
                        self.snake.change_direction(UP)
                    elif event.key == pygame.K_DOWN:
                        self.snake.change_direction(DOWN)
                    elif event.key == pygame.K_LEFT:
                        self.snake.change_direction(LEFT)
                    elif event.key == pygame.K_RIGHT:
                        self.snake.change_direction(RIGHT)
                    # Also support WASD keys
                    elif event.key == pygame.K_w:
                        self.snake.change_direction(UP)
                    elif event.key == pygame.K_s:
                        self.snake.change_direction(DOWN)
                    elif event.key == pygame.K_a:
                        self.snake.change_direction(LEFT)
                    elif event.key == pygame.K_d:
                        self.snake.change_direction(RIGHT)
        return True
    
    def update(self):
        """Update game state."""
        if not self.game_over:
            # Move the snake
            if not self.snake.update():
                self.game_over = True
                return
            
            # Check for auto growth
            self.snake.auto_grow()
            
            # Check if the snake ate the candy
            if self.snake.get_head_position() == self.candy.position:
                self.snake.grow()
                self.candy = Candy(self.snake.positions, self.walls)
                self.score += 1
                
                # Increase the speed
                self.speed += SPEED_INCREASE
    
    def draw(self):
        """Draw the game state to the console."""
        # Clear the console
        os.system('clear' if os.name == 'posix' else 'cls')
        
        # Create a grid representation
        grid = [[' ' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        
        # Place walls on the grid
        for x, y in self.walls:
            grid[y][x] = '#'
            
        # Place candy on the grid
        x, y = self.candy.position
        grid[y][x] = '*'
        
        # Place snake on the grid
        for i, (x, y) in enumerate(self.snake.positions):
            if i == 0:  # Head
                grid[y][x] = 'O'
            else:  # Body
                grid[y][x] = 'o'
        
        # Print the grid
        print(f"Snake Game - Score: {self.score}")
        print(f"Speed: {self.speed:.1f} - Snake Length: {self.snake.length}")
        for row in grid:
            print(''.join(row))
            
        # Print game over message
        if self.game_over:
            print("Game Over! Press 'r' to restart or 'q' to quit.")
        else:
            print("Use arrow keys or WASD to move. Press 'q' to quit.")
    
    def run(self):
        """Main game loop."""
        # Set up a simple clock for game timing
        clock = pygame.time.Clock()
        
        print("Welcome to Snake Game!")
        print("Controls: Use arrow keys or WASD to move")
        print("Press 'r' to restart after game over, 'q' to quit")
        print("Game starts in 3 seconds...")
        time.sleep(3)
        
        running = True
        while running:
            # Handle events
            running = self.handle_events()
            
            # Get keyboard state
            keys = pygame.key.get_pressed()
            if keys[pygame.K_q]:
                running = False
            
            # Update game state
            self.update()
            
            # Draw the game state
            self.draw()
            
            # Control game speed
            clock.tick(self.speed)
        
        pygame.quit()
        print("Thanks for playing!")
