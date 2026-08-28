"""Collision detection system."""

import math
import numpy as np


class CollisionSystem:
    """Handles collision detection between entities."""

    @staticmethod
    def check_circle_collision(a_pos, a_radius, b_pos, b_radius):
        """Check collision between two circles."""
        dx = a_pos[0] - b_pos[0]
        dy = a_pos[1] - b_pos[1]
        distance = math.sqrt(dx * dx + dy * dy)
        return distance < (a_radius + b_radius)

    @staticmethod
    def check_bullet_asteroid(bullet, asteroid):
        """Check collision between bullet and asteroid."""
        return CollisionSystem.check_circle_collision(
            bullet.position, bullet.get_radius(),
            asteroid.position, asteroid.get_radius()
        )

    @staticmethod
    def check_ship_asteroid(ship, asteroid):
        """Check collision between ship and asteroid."""
        if ship.invincible or not ship.alive:
            return False
        return CollisionSystem.check_circle_collision(
            ship.position, ship.get_radius(),
            asteroid.position, asteroid.get_radius()
        )

    @staticmethod
    def check_ship_ufo(ship, ufo):
        """Check collision between ship and UFO."""
        if ship.invincible or not ship.alive or not ufo.alive:
            return False
        return CollisionSystem.check_circle_collision(
            ship.position, ship.get_radius(),
            ufo.position, ufo.get_radius()
        )

    @staticmethod
    def check_bullet_ufo(bullet, ufo):
        """Check collision between bullet and UFO."""
        if bullet.owner != "player" or not ufo.alive:
            return False
        return CollisionSystem.check_circle_collision(
            bullet.position, bullet.get_radius(),
            ufo.position, ufo.get_radius()
        )

    @staticmethod
    def check_ufo_bullet_ship(ufo_bullet, ship):
        """Check collision between UFO bullet and ship."""
        if ship.invincible or not ship.alive:
            return False
        return CollisionSystem.check_circle_collision(
            ufo_bullet.position, ufo_bullet.get_radius(),
            ship.position, ship.get_radius()
        )