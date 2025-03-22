"""
Snake game module using the curses library for terminal-based gameplay.
This is an alternative implementation that doesn't require pygame.
"""
import curses
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
    Main game class that manages the game state and rendering (using curses).
    """
    def __init__(self, stdscr):
        """Initialize the game with its starting state."""
        self.stdscr = stdscr
        
        # Configure curses
        curses.curs_set(0)  # Hide cursor
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)      # Snake
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)    # Walls and Candy
        
        # Calculate the size of the window
        self.height, self.width = stdscr.getmaxyx()
        
        # Create a game window
        self.game_win = curses.newwin(GRID_SIZE + 2, GRID_SIZE * 2 + 2, 0, 0)
        self.game_win.keypad(1)  # Enable keypad
        self.game_win.timeout(100)  # Set input timeout (ms)
        
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
    
    def handle_input(self):
        """Handle keyboard input."""
        # Set timeout based on game speed
        self.game_win.timeout(int(1000 / self.speed))
        
        # Get input
        key = self.game_win.getch()
        
        # Process key
        if key == curses.KEY_UP:
            self.snake.change_direction(UP)
        elif key == curses.KEY_DOWN:
            self.snake.change_direction(DOWN)
        elif key == curses.KEY_LEFT:
            self.snake.change_direction(LEFT)
        elif key == curses.KEY_RIGHT:
            self.snake.change_direction(RIGHT)
        # Handle 'q' to quit
        elif key == ord('q'):
            return False
        # Handle 'r' to restart when game over
        elif key == ord('r') and self.game_over:
            self.reset_game()
            
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
        """Draw the game state to the curses window."""
        self.game_win.clear()
        
        # Draw border
        self.game_win.border(0)
        
        # Draw walls
        for x, y in self.walls:
            self.game_win.addch(y + 1, x * 2 + 1, '#', curses.color_pair(2))
        
        # Draw candy
        x, y = self.candy.position
        self.game_win.addch(y + 1, x * 2 + 1, '*', curses.color_pair(2))
        
        # Draw snake
        for i, (x, y) in enumerate(self.snake.positions):
            char = 'O' if i == 0 else 'o'
            self.game_win.addch(y + 1, x * 2 + 1, char, curses.color_pair(1))
        
        # Draw score
        score_text = f" Score: {self.score} | Speed: {self.speed:.1f} | Length: {self.snake.length} "
        self.game_win.addstr(0, (self.width - len(score_text)) // 2, score_text)
        
        # Draw game over message
        if self.game_over:
            game_over_text = " Game Over! Press 'r' to restart or 'q' to quit "
            self.game_win.addstr(GRID_SIZE // 2, (GRID_SIZE * 2 - len(game_over_text)) // 2, game_over_text)
        
        # Refresh the window
        self.game_win.refresh()
    
    def run(self):
        """Main game loop."""
        # Show welcome message
        self.game_win.clear()
        self.game_win.border(0)
        welcome_text = "Welcome to Snake Game!"
        controls_text = "Use arrow keys to move"
        quit_text = "Press 'q' to quit, 'r' to restart"
        start_text = "Press any key to start..."
        
        self.game_win.addstr(GRID_SIZE // 2 - 2, (GRID_SIZE * 2 - len(welcome_text)) // 2, welcome_text)
        self.game_win.addstr(GRID_SIZE // 2 - 1, (GRID_SIZE * 2 - len(controls_text)) // 2, controls_text)
        self.game_win.addstr(GRID_SIZE // 2, (GRID_SIZE * 2 - len(quit_text)) // 2, quit_text)
        self.game_win.addstr(GRID_SIZE // 2 + 2, (GRID_SIZE * 2 - len(start_text)) // 2, start_text)
        self.game_win.refresh()
        self.game_win.getch()  # Wait for any key press
        
        running = True
        while running:
            running = self.handle_input()
            self.update()
            self.draw()
            
        return self.score


def main(stdscr):
    """Main function to run the game."""
    game = Game(stdscr)
    return game.run()


if __name__ == "__main__":
    # Initialize curses
    final_score = curses.wrapper(main)
    print(f"Final Score: {final_score}")
    print("Thanks for playing!")