"""UFO entity with procedural design."""

import math
import random
import numpy as np
from core.settings import Settings


class UFO:
    """Enemy UFO with procedural design."""

    def __init__(self, x, y, advanced=False):
        self.position = np.array([x, y], dtype=float)
        self.velocity = np.array([0.0, 0.0], dtype=float)
        self.advanced = advanced
        self.alive = True
        self.size = Settings.UFO_SIZE

        # Movement
        angle = random.uniform(0, 2 * math.pi)
        speed = Settings.UFO_SPEED * (1.2 if advanced else 1.0)
        self.velocity = np.array([math.cos(angle), math.sin(angle)]) * speed

        # Shooting
        self.shoot_timer = random.uniform(0, Settings.UFO_SHOOT_COOLDOWN)
        self.shoot_cooldown = Settings.UFO_SHOOT_COOLDOWN * (0.7 if advanced else 1.0)

        # Color
        self.color = Settings.NEON_PURPLE if advanced else Settings.NEON_MAGENTA
        self.glow_color = tuple(min(c + 80, 255) for c in self.color)

        # Accuracy
        self.accuracy_error = Settings.UFO_ACCURACY_ERROR * (0.6 if advanced else 1.0)

        # Generate UFO shape
        self.shape = self._generate_shape()

        # Score
        self.score = Settings.SCORE_UFO * (1.5 if advanced else 1.0)
        self.score = int(self.score)

    def _generate_shape(self):
        """Generate UFO shape points."""
        vertices = []
        size = self.size

        # Main body (ellipse-like polygon)
        num_points = 12
        for i in range(num_points):
            angle = (i / num_points) * 2 * math.pi
            rx = size * (1 + 0.2 * math.sin(angle * 2))
            ry = size * 0.6 * (1 + 0.2 * math.cos(angle * 2))
            vertices.append((math.cos(angle) * rx, math.sin(angle) * ry))

        # Top dome
        dome_points = 6
        for i in range(dome_points + 1):
            t = i / dome_points
            angle = math.pi * 0.8 * t + math.pi * 0.1
            x = math.sin(angle) * size * 0.5
            y = -math.cos(angle) * size * 0.7 - size * 0.4
            vertices.append((x, y))

        return vertices

    def update(self, dt, player_pos=None):
        """Update UFO state."""
        if not self.alive:
            return

        # Move
        self.position += self.velocity * dt

        # Slight wobble
        self.position[1] += math.sin(self.position[0] * 0.02 + self.position[1] * 0.02) * 10 * dt

        self._wrap()

        # Shooting
        if player_pos is not None:
            self.shoot_timer -= dt
            if self.shoot_timer <= 0:
                self.shoot_timer = self.shoot_cooldown
                return True

        return False

    def _wrap(self):
        """Wrap around screen edges."""
        w, h = Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT
        margin = self.size * 2
        if self.position[0] < -margin:
            self.position[0] = w + margin
        elif self.position[0] > w + margin:
            self.position[0] = -margin
        if self.position[1] < -margin:
            self.position[1] = h + margin
        elif self.position[1] > h + margin:
            self.position[1] = -margin

    def get_rotated_points(self):
        """Get shape points for rendering."""
        return [(int(self.position[0] + x), int(self.position[1] + y))
                for x, y in self.shape]

    def get_position(self):
        """Get position as tuple."""
        return (int(self.position[0]), int(self.position[1]))

    def get_radius(self):
        """Get collision radius."""
        return self.size * 0.8

    def get_shoot_direction(self, player_pos):
        """Get direction to shoot with random error."""
        if player_pos is None:
            return np.array([0.0, 0.0])

        dx = player_pos[0] - self.position[0]
        dy = player_pos[1] - self.position[1]
        angle = math.atan2(dy, dx)

        # Add random error
        angle += random.uniform(-self.accuracy_error, self.accuracy_error)

        return np.array([math.cos(angle), math.sin(angle)])