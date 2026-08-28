"""Player ship entity."""

import math
import pygame
import numpy as np
from core.settings import Settings


class Ship:
    """Player spaceship with neon style."""

    def __init__(self, x, y):
        self.position = np.array([x, y], dtype=float)
        self.velocity = np.array([0.0, 0.0], dtype=float)
        self.angle = -90.0  # pointing up
        self.size = Settings.SHIP_SIZE
        self.acceleration = 0.0
        self.is_accelerating = False
        self.rotation = 0.0  # -1 left, 0 none, 1 right
        self.invincible = True
        self.invincible_timer = Settings.SHIP_INVINCIBILITY_TIME
        self.blink_timer = 0.0
        self.alive = True

        # Thruster particles
        self.thruster_particles = []

        # Create ship shape (triangle)
        self.points = self._create_shape()

    def _create_shape(self):
        """Create triangular ship shape."""
        size = self.size
        points = [
            (0, -size),      # nose
            (-size * 0.7, size * 0.7),
            (-size * 0.4, size * 0.4),
            (0, size * 0.5),
            (size * 0.4, size * 0.4),
            (size * 0.7, size * 0.7),
        ]
        return points

    def update(self, dt):
        """Update ship state."""
        if not self.alive:
            return

        # Handle invincibility
        if self.invincible:
            self.invincible_timer -= dt
            if self.invincible_timer <= 0:
                self.invincible = False

        # Rotation
        if self.rotation != 0:
            self.angle += self.rotation * Settings.SHIP_ROTATION_SPEED * dt

        # Acceleration
        if self.is_accelerating:
            rad = math.radians(self.angle)
            direction = np.array([math.cos(rad), math.sin(rad)])
            self.velocity += direction * Settings.SHIP_ACCELERATION * dt

        # Friction
        self.velocity *= Settings.SHIP_FRICTION

        # Clamp speed
        speed = np.linalg.norm(self.velocity)
        max_speed = Settings.SHIP_MAX_SPEED
        if speed > max_speed:
            self.velocity = self.velocity / speed * max_speed

        # Move
        self.position += self.velocity * dt

        # Wrap around
        self._wrap()

    def _wrap(self):
        """Wrap ship around screen edges."""
        w, h = Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT
        if self.position[0] < 0:
            self.position[0] = w
        elif self.position[0] > w:
            self.position[0] = 0
        if self.position[1] < 0:
            self.position[1] = h
        elif self.position[1] > h:
            self.position[1] = 0

    def get_direction(self):
        """Get normalized direction vector."""
        rad = math.radians(self.angle+(-90))
        return np.array([math.cos(rad), math.sin(rad)])

    def get_position(self):
        """Get position as tuple."""
        return (int(self.position[0]), int(self.position[1]))

    def get_nose_position(self):
        """Get position of the ship's nose (tip)."""
        rad = math.radians(self.angle)
        direction = np.array([math.cos(rad), math.sin(rad)])
        # Move from center to nose tip (size units forward)
        nose_pos = self.position + direction #* self.size * 1.1
        return nose_pos

    def get_rotated_points(self):
        """Get rotated ship points for rendering."""
        rad = math.radians(self.angle)
        cos_a, sin_a = math.cos(rad), math.sin(rad)

        rotated = []
        for x, y in self.points:
            rx = x * cos_a - y * sin_a
            ry = x * sin_a + y * cos_a
            rotated.append((int(self.position[0] + rx), int(self.position[1] + ry)))

        return rotated

    def get_thruster_positions(self):
        """Get positions for thruster particles."""
        rad = math.radians(self.angle + 180)
        base = self.position.copy()

        # Two thruster points at the back
        offset = self.size * 0.5
        side_offset = self.size * 0.4

        left = base + np.array([
            math.cos(rad + math.radians(10)) * offset + math.cos(rad) * side_offset,
            math.sin(rad + math.radians(10)) * offset + math.sin(rad) * side_offset
        ])
        right = base + np.array([
            math.cos(rad - math.radians(10)) * offset - math.cos(rad) * side_offset,
            math.sin(rad - math.radians(10)) * offset - math.sin(rad) * side_offset
        ])

        return [left, right]

    def get_radius(self):
        """Get collision radius."""
        return self.size * 0.7

    def reset(self, x, y):
        """Reset ship position."""
        self.position = np.array([x, y], dtype=float)
        self.velocity = np.array([0.0, 0.0], dtype=float)
        self.angle = -90.0
        self.alive = True
        self.invincible = True
        self.invincible_timer = Settings.SHIP_INVINCIBILITY_TIME
        self.is_accelerating = False