"""Asteroid entity with procedural generation."""

import math
import random
import numpy as np
from core.settings import Settings


class Asteroid:
    """Procedurally generated asteroid with irregular shape."""

    def __init__(self, x, y, generation=0):
        self.position = np.array([x, y], dtype=float)
        self.velocity = np.array([0.0, 0.0], dtype=float)
        self.generation = generation
        self.rotation = 0.0
        self.rotation_speed = random.uniform(-60.0, 60.0)

        # Determine size based on generation
        if generation == 0:
            self.radius = Settings.LARGE_RADIUS
            self.score = Settings.SCORE_LARGE_ASTEROID
        elif generation == 1:
            self.radius = Settings.MEDIUM_RADIUS
            self.score = Settings.SCORE_MEDIUM_ASTEROID
        else:
            self.radius = Settings.SMALL_RADIUS
            self.score = Settings.SCORE_SMALL_ASTEROID

        # Generate irregular shape
        self.vertices = self._generate_vertices()

        # Color
        self.color = random.choice(Settings.ASTEROID_COLORS)
        self.glow_color = tuple(min(c + 80, 255) for c in self.color)

        # Random velocity
        speed = random.uniform(
            Settings.ASTEROID_BASE_SPEED * 0.5,
            Settings.ASTEROID_BASE_SPEED * (1.0 + generation * 0.3)
        )
        angle = random.uniform(0, 2 * math.pi)
        self.velocity = np.array([math.cos(angle), math.sin(angle)]) * speed

        # Add some randomness to velocity
        self.velocity += np.random.normal(0, 20, 2)

        # Mark for destruction
        self.destroyed = False

    def _generate_vertices(self):
        """Generate irregular polygon vertices."""
        num_vertices = random.randint(6, 10)
        vertices = []

        for i in range(num_vertices):
            # Random angle
            angle = (i / num_vertices) * 2 * math.pi + random.uniform(-0.1, 0.1)

            # Random radius with irregularity
            radius_mult = random.uniform(0.65, 1.0)
            r = self.radius * radius_mult

            x = math.cos(angle) * r
            y = math.sin(angle) * r
            vertices.append((x, y))

        return vertices

    def update(self, dt):
        """Update asteroid state."""
        self.position += self.velocity * dt
        self.rotation += self.rotation_speed * dt
        self._wrap()

    def _wrap(self):
        """Wrap around screen edges."""
        w, h = Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT
        if self.position[0] < -self.radius * 2:
            self.position[0] = w + self.radius * 2
        elif self.position[0] > w + self.radius * 2:
            self.position[0] = -self.radius * 2
        if self.position[1] < -self.radius * 2:
            self.position[1] = h + self.radius * 2
        elif self.position[1] > h + self.radius * 2:
            self.position[1] = -self.radius * 2

    def get_rotated_vertices(self):
        """Get rotated vertices for rendering."""
        rad = math.radians(self.rotation)
        cos_a, sin_a = math.cos(rad), math.sin(rad)

        vertices = []
        for x, y in self.vertices:
            rx = x * cos_a - y * sin_a
            ry = x * sin_a + y * cos_a
            vertices.append((
                int(self.position[0] + rx),
                int(self.position[1] + ry)
            ))

        return vertices

    def get_radius(self):
        """Get collision radius."""
        return self.radius * 0.8

    def should_split(self):
        """Check if asteroid should split into smaller ones."""
        return self.generation < 2

    def get_split_asteroids(self):
        """Create smaller asteroids from this one."""
        if not self.should_split():
            return []

        asteroids = []
        num_split = random.randint(2, 3)

        for _ in range(num_split):
            angle = random.uniform(0, 2 * math.pi)
            distance = self.radius * 0.5
            pos = self.position + np.array([
                math.cos(angle) * distance,
                math.sin(angle) * distance
            ])

            ast = Asteroid(pos[0], pos[1], self.generation + 1)
            ast.velocity = self.velocity + np.random.normal(0, 30, 2)
            asteroids.append(ast)

        return asteroids