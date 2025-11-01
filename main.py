"""
Milo's Cozy Adventures - A Cozy Idle Game
Main entry point for the game
"""

import pygame
import sys
from src.game import Game

def main():
    """Main entry point for Milo's Cozy Adventures"""
    pygame.init()

    # Create and run the game
    game = Game()
    game.run()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
