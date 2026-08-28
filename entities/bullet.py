"""Bullet entity."""

import math
import numpy as np
from core.settings import Settings


class Bullet:
    """Player or enemy bullet with glow effect."""

    def __init__(self, x, y, velocity, owner="player"):
        self.position = np.array([x, y], dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.owner = owner  # "player" or "ufo"
        self.lifetime = Settings.BULLET_LIFETIME
        self.alive = True
        self.size = Settings.BULLET_SIZE
        self.glow_size = Settings.BULLET_GLOW_SIZE
        self._initial_lifetime = Settings.BULLET_LIFETIME  # Store initial value

        # Color based on owner
        if owner == "player":
            self.color = Settings.NEON_CYAN
            self.glow_color = (0, 255, 255, 100)
        else:
            self.color = Settings.NEON_ORANGE
            self.glow_color = (255, 120, 0, 100)

    def update(self, dt):
        """Update bullet state."""
        self.position += self.velocity * dt
        self.lifetime -= dt

        if self.lifetime <= 0:
            self.alive = False

        self._wrap()

    def _wrap(self):
        """Wrap around screen edges."""
        w, h = Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT
        if self.position[0] < -10:
            self.position[0] = w + 10
        elif self.position[0] > w + 10:
            self.position[0] = -10
        if self.position[1] < -10:
            self.position[1] = h + 10
        elif self.position[1] > h + 10:
            self.position[1] = -10

    def get_position(self):
        """Get position as tuple."""
        return (int(self.position[0]), int(self.position[1]))

    def get_radius(self):
        """Get collision radius."""
        return self.size * 0.7

    def get_lifetime_ratio(self):
        """Get remaining lifetime ratio (0-1)."""
        if self._initial_lifetime <= 0:
            return 1.0
        return max(0, self.lifetime / self._initial_lifetime)