"""Particle entity for effects."""

import math
import random
import numpy as np
from core.settings import Settings


class Particle:
    """Single particle with physics and lifetime."""

    def __init__(self, x, y, velocity=None, color=None, size=None, lifetime=None):
        self.position = np.array([x, y], dtype=float)

        if velocity is None:
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(30, 150)
            self.velocity = np.array([math.cos(angle), math.sin(angle)]) * speed
        else:
            self.velocity = np.array(velocity, dtype=float)

        self.lifetime = lifetime if lifetime is not None else random.uniform(0.3, 1.5)
        self.max_lifetime = self.lifetime

        if color is None:
            colors = [
                Settings.NEON_CYAN,
                Settings.NEON_BLUE,
                Settings.NEON_PURPLE,
                Settings.NEON_MAGENTA,
                Settings.NEON_GREEN,
                Settings.NEON_ORANGE,
                Settings.NEON_RED,
            ]
            self.color = random.choice(colors)
        else:
            self.color = color

        self.size = size if size is not None else random.uniform(2, 6)
        self.initial_size = self.size

        self.alive = True

        # Random initial variation
        self.velocity += np.random.normal(0, 20, 2)

    def update(self, dt):
        """Update particle state."""
        if not self.alive:
            return

        self.position += self.velocity * dt
        self.velocity *= Settings.PARTICLE_FADE_RATE

        self.lifetime -= dt
        self.size *= Settings.PARTICLE_SHRINK_RATE

        if self.lifetime <= 0 or self.size < 0.5:
            self.alive = False

    def get_alpha(self):
        """Get current alpha based on lifetime."""
        if self.max_lifetime <= 0:
            return 255
        return int(255 * (self.lifetime / self.max_lifetime))

    def get_position(self):
        """Get position as tuple."""
        return (int(self.position[0]), int(self.position[1]))