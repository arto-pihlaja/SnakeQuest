"""
Main entry point for the Snake game.
Allows the user to choose between different implementations.
"""
import os
import sys

if __name__ == "__main__":
    print("Welcome to Snake Game!")
    print("Please choose a game implementation:")
    print("1. Console-based version (uses PyGame in the background)")
    print("2. Simple pure Python version (most compatible)")
    print("3. Curses version (works well in terminal)")
    
    choice = input("Enter your choice (1-3): ")
    
    if choice == "1":
        from snake_game import Game
        game = Game()
        game.run()
    elif choice == "2":
        from snake_game_simple import Game
        game = Game()
        game.run()
    elif choice == "3":
        import curses
        import snake_game_curses
        curses.wrapper(snake_game_curses.main)
    else:
        print("Invalid choice. Please run again and select a valid option.")
        sys.exit(1)
