"""
Snake game module with a pure Python implementation.
This is a simplified version that works in any terminal.
"""
import random
import time
import os
import sys
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
        
        # Calculate new head position
        new_x = head_x + dir_x
        new_y = head_y + dir_y
        new_head = (new_x, new_y)
        
        # Check if the snake hits the wall
        if (new_x == 0 or new_x == GRID_SIZE - 1 or 
            new_y == 0 or new_y == GRID_SIZE - 1):
            return False  # Game over
        
        # Check if the snake hits itself
        if new_head in self.positions[1:]:
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
            
        # Print game control information
        if self.game_over:
            print("\nGame Over!")
            print("Press 'r' to restart or 'q' to quit.")
        else:
            print("\nControls:")
            print("w = Up, s = Down, a = Left, d = Right")
            print("q = Quit")
    
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
    
    def run(self):
        """Main game loop with simple input handling."""
        print("Welcome to Snake Game!")
        print("Controls: w=Up, s=Down, a=Left, d=Right, q=Quit")
        print("Game starts in 3 seconds...")
        time.sleep(3)
        
        running = True
        last_update = time.time()
        
        # This is a very simplified version of the game that shows one frame
        # and then waits for input, rather than having smooth continuous movement
        while running:
            # Draw the current state
            self.draw()
            
            # Get input
            key = input("Enter command: ").lower()
            
            # Process input
            if key == 'q':
                running = False
            elif self.game_over and key == 'r':
                self.reset_game()
            elif not self.game_over:
                # Change direction based on input
                if key == 'w':
                    self.snake.change_direction(UP)
                elif key == 's':
                    self.snake.change_direction(DOWN)
                elif key == 'a':
                    self.snake.change_direction(LEFT)
                elif key == 'd':
                    self.snake.change_direction(RIGHT)
            
            # Update the game state
            if not self.game_over:
                self.update()
            
        print("Thanks for playing!")


if __name__ == "__main__":
    # Run the game
    game = Game()
    game.run()