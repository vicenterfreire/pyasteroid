"""Background rendering with optional image support."""

import pygame
from core.settings import Settings


class Background:
    """Handles background rendering."""

    def __init__(self, screen, game_data):
        self.screen = screen
        self.game_data = game_data
        self.background_image = None
        self.image_loaded = False

        # Load background if available
        if game_data.background_path:
            self._load_background(game_data.background_path)

    def _load_background(self, path):
        """Load background image."""
        try:
            self.background_image = pygame.image.load(path)
            self.background_image = pygame.transform.scale(
                self.background_image,
                (Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT)
            )
            self.image_loaded = True
        except (pygame.error, FileNotFoundError):
            self.image_loaded = False

    def render(self, shake_offset):
        """Render background."""
        offset_x, offset_y = shake_offset

        if self.image_loaded and self.background_image:
            # Draw background image with shake offset
            self.screen.blit(self.background_image, (offset_x, offset_y))
        else:
            # Default dark background with subtle grid
            self.screen.fill((10, 10, 20))

            # Draw subtle grid lines
            grid_color = (30, 30, 50)
            width, height = Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT

            # Vertical lines
            for x in range(0, width, 50):
                pygame.draw.line(self.screen, grid_color,
                               (x + offset_x, 0 + offset_y),
                               (x + offset_x, height + offset_y), 1)

            # Horizontal lines
            for y in range(0, height, 50):
                pygame.draw.line(self.screen, grid_color,
                               (0 + offset_x, y + offset_y),
                               (width + offset_x, y + offset_y), 1)

            # Random stars
            import random
            star_color = (60, 60, 80)
            for _ in range(100):
                x = random.randint(0, width)
                y = random.randint(0, height)
                size = random.randint(1, 2)
                brightness = random.randint(40, 80)
                pygame.draw.circle(self.screen, (brightness, brightness, brightness + 20),
                                 (x + offset_x, y + offset_y), size)