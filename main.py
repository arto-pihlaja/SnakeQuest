"""
Main entry point for the Snake game.
Allows the user to choose between different implementations.
"""
import os
import sys

if __name__ == "__main__":
    print("Welcome to Snake Game!")
    print("Please choose a game implementation:")
    print("1. PyGame version (graphical window)")
    print("2. Simple pure Python version (console-based)")
    
    choice = input("Enter your choice (1-2): ")
    
    if choice == "1":
        from snake_game import Game
        game = Game()
        game.run()
    elif choice == "2":
        from snake_game_simple import Game
        game = Game()
        game.run()
    else:
        print("Invalid choice. Please run again and select a valid option.")
        sys.exit(1)
