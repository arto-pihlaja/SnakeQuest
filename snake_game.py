"""
Snake game module containing the main game logic and classes.
"""
import pygame
import random
import time
from config import *

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
            
    def draw(self, surface):
        """Draw the snake on the game surface."""
        for i, position in enumerate(self.positions):
            rect = pygame.Rect(
                position[0] * BLOCK_SIZE, 
                position[1] * BLOCK_SIZE, 
                BLOCK_SIZE, BLOCK_SIZE
            )
            pygame.draw.rect(surface, RED, rect)
            # Draw a darker outline for better visibility
            pygame.draw.rect(surface, BLACK, rect, 1)


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
        
    def draw(self, surface):
        """Draw the candy on the game surface."""
        rect = pygame.Rect(
            self.position[0] * BLOCK_SIZE,
            self.position[1] * BLOCK_SIZE,
            BLOCK_SIZE, BLOCK_SIZE
        )
        pygame.draw.rect(surface, WHITE, rect)


class Game:
    """
    Main game class that manages the game state and rendering.
    """
    def __init__(self):
        """Initialize the game with its starting state."""
        pygame.init()
        
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption('Snake Game')
        
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 20)
        
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
        """Handle pygame events."""
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
        """Draw the game state to the screen."""
        self.screen.fill(BLACK)
        
        # Draw walls
        for position in self.walls:
            rect = pygame.Rect(
                position[0] * BLOCK_SIZE,
                position[1] * BLOCK_SIZE,
                BLOCK_SIZE, BLOCK_SIZE
            )
            pygame.draw.rect(self.screen, WHITE, rect)
        
        # Draw candy
        self.candy.draw(self.screen)
        
        # Draw snake
        self.snake.draw(self.screen)
        
        # Draw score
        score_text = self.font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Draw game over screen
        if self.game_over:
            game_over_text = self.font.render('Game Over! Press R to Restart', True, WHITE)
            self.screen.blit(game_over_text, (WINDOW_SIZE // 2 - 150, WINDOW_SIZE // 2))
        
        pygame.display.update()
    
    def run(self):
        """Main game loop."""
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.speed)
        
        pygame.quit()
