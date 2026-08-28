"""Particle system for managing effects."""

import random
import math
import numpy as np
from core.settings import Settings
from entities.particle import Particle


class ParticleSystem:
    """Manages particle effects."""

    def __init__(self):
        self.particles = []
        self.max_particles = Settings.PARTICLE_MAX_COUNT

    def update(self, dt):
        """Update all particles."""
        # Remove dead particles
        self.particles = [p for p in self.particles if p.alive]

        for particle in self.particles:
            particle.update(dt)

        # Limit particle count
        if len(self.particles) > self.max_particles:
            self.particles = self.particles[:self.max_particles]

    def emit(self, x, y, count, **kwargs):
        """Emit particles at position."""
        for _ in range(count):
            if len(self.particles) >= self.max_particles:
                break

            particle = Particle(x, y, **kwargs)
            self.particles.append(particle)

    def emit_thruster(self, positions, color=None):
        """Emit thruster particles from ship."""
        if color is None:
            color = Settings.NEON_CYAN

        for pos in positions:
            # Emit multiple particles per thruster point
            for _ in range(2):
                velocity = np.random.normal(0, 15, 2)
                velocity[0] += random.uniform(-30, -10) * (pos[0] / Settings.SCREEN_WIDTH)
                velocity[1] += random.uniform(-30, -10) * (pos[1] / Settings.SCREEN_HEIGHT)

                self.emit(
                    pos[0], pos[1], 1,
                    velocity=velocity,
                    color=color,
                    size=random.uniform(1, 3),
                    lifetime=random.uniform(0.1, 0.4)
                )

    def emit_explosion(self, x, y, count, colors=None, spread=200):
        """Emit explosion particles."""
        if colors is None:
            colors = [
                Settings.NEON_ORANGE,
                Settings.NEON_RED,
                Settings.NEON_YELLOW,
                Settings.NEON_WHITE,
            ]

        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(50, spread)
            velocity = np.array([math.cos(angle), math.sin(angle)]) * speed

            self.emit(
                x, y, 1,
                velocity=velocity,
                color=random.choice(colors),
                size=random.uniform(2, 8),
                lifetime=random.uniform(0.3, 1.5)
            )

    def emit_ship_explosion(self, x, y):
        """Emit ship explosion with more particles."""
        colors = [
            Settings.NEON_CYAN,
            Settings.NEON_BLUE,
            Settings.NEON_WHITE,
            Settings.NEON_ORANGE,
        ]
        self.emit_explosion(x, y, 60, colors, 300)

    def emit_asteroid_explosion(self, x, y, color=None):
        """Emit asteroid explosion."""
        if color is None:
            color = random.choice(Settings.ASTEROID_COLORS)
        colors = [color, tuple(min(c + 80, 255) for c in color), Settings.NEON_WHITE]
        self.emit_explosion(x, y, 25, colors, 150)

    def emit_ufo_explosion(self, x, y):
        """Emit UFO explosion."""
        colors = [
            Settings.NEON_PURPLE,
            Settings.NEON_MAGENTA,
            Settings.NEON_WHITE,
        ]
        self.emit_explosion(x, y, 35, colors, 180)

    def clear(self):
        """Clear all particles."""
        self.particles.clear()