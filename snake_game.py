"""
Snake game module containing the main game logic and classes.
Using PyGame for graphics and input handling.
"""
import pygame
import random
import time
import os
from config import *

# Initialize Pygame
pygame.init()

class Snake:
    """
    Class representing the snake in the game.
    """
    def __init__(self):
        """Initialize the snake with its starting position and length."""
        self.length = INITIAL_SNAKE_LENGTH
        # Start the snake in the middle of the screen, moving right
        self.positions = [
            (WIDTH_PYGAME // 2, HEIGHT_PYGAME // 2 + i) 
            for i in range(self.length)
        ]
        self.direction = RIGHT  # Start moving right
        self.next_direction = RIGHT  # Track the next direction change
        self.last_auto_growth = time.time()
        
    def get_head_position(self):
        """Return the position of the snake's head."""
        return self.positions[0]
    
    def update(self):
        """Update the snake's position based on its direction."""
        # Update the current direction to the next direction
        self.direction = self.next_direction
        
        # Calculate new head position
        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x, head_y + dir_y)
        
        # Check if the snake hits itself
        if new_head in self.positions[1:]:
            return False  # Game over
        
        # Check if the snake hits the wall
        if (new_head[0] == 0 or new_head[0] == WIDTH_PYGAME - 1 or 
            new_head[1] == 0 or new_head[1] == HEIGHT_PYGAME - 1):
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
        Prevents changing to the opposite direction and ensures right-angle turns.
        """
        # Don't allow moving in the opposite direction
        if (direction[0] * -1, direction[1] * -1) == self.direction:
            return
            
        # Only allow right-angle turns
        if (direction[0] != 0 and self.direction[0] != 0) or \
           (direction[1] != 0 and self.direction[1] != 0):
            return
            
        # Update the next direction
        self.next_direction = direction


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
                random.randint(1, WIDTH_PYGAME - 2),
                random.randint(1, HEIGHT_PYGAME - 2)
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
        # Initialize pygame display
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption("Snake Game")
        
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
        for x in range(WIDTH_PYGAME):
            walls.append((x, 0))
            walls.append((x, HEIGHT_PYGAME - 1))
            
        # Left and right walls
        for y in range(1, HEIGHT_PYGAME - 1):
            walls.append((0, y))
            walls.append((WIDTH_PYGAME - 1, y))
            
        return walls
    
    def handle_events(self):
        """Handle key events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return False
                if self.game_over and event.key == pygame.K_r:
                    self.reset_game()
        return True
    
    def update(self):
        """Update game state."""
        if not self.game_over:
            # Handle movement keys
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.snake.change_direction(UP)
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.snake.change_direction(DOWN)
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.snake.change_direction(LEFT)
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.snake.change_direction(RIGHT)
            
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
        """Draw the game state to the Pygame window."""
        # Clear the screen
        self.screen.fill(BLACK)
        
        # Draw walls
        for x, y in self.walls:
            pygame.draw.rect(self.screen, WHITE, 
                           (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        
        # Draw candy
        x, y = self.candy.position
        pygame.draw.rect(self.screen, RED,
                        (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        
        # Draw snake
        for i, (x, y) in enumerate(self.snake.positions):
            color = GREEN if i == 0 else (0, 200, 0)  # Head is slightly brighter
            pygame.draw.rect(self.screen, color,
                           (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        
        # Draw score and game info
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, WHITE)
        speed_text = font.render(f'Speed: {self.speed:.1f}', True, WHITE)
        length_text = font.render(f'Length: {self.snake.length}', True, WHITE)
        
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(speed_text, (10, 40))
        self.screen.blit(length_text, (10, 70))
        
        # Draw game over message
        if self.game_over:
            game_over_font = pygame.font.Font(None, 48)
            game_over_text = game_over_font.render('Game Over! Press R to restart', True, WHITE)
            text_rect = game_over_text.get_rect(center=(WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2))
            self.screen.blit(game_over_text, text_rect)
        
        # Update the display
        pygame.display.flip()
    
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
            # Handle events (quit and restart)
            running = self.handle_events()
            
            # Update game state
            self.update()
            
            # Draw the game state
            self.draw()
            
            # Control game speed
            clock.tick(self.speed)
        
        pygame.quit()
        print("Thanks for playing!")
