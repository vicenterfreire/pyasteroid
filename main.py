"""Neon Asteroids - Main entry point."""

import sys
import pygame
from core.game import Game


def main():
    """Initialize and run the game."""
    pygame.init()

    try:
        game = Game()
        game.run()
    except Exception as e:
        print(f"Error starting game: {e}")
        import traceback
        traceback.print_exc()
    finally:
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    main()