"""Rendering system for all game entities."""

import pygame
import math
from core.settings import Settings


class Renderer:
    """Handles rendering of all game entities."""

    def __init__(self, screen):
        self.screen = screen

    def render_entities(self, screen, glow_surface, ship, asteroids, bullets,
                        ufos, ufo_bullets, particle_system, shake_offset):
        """Render all game entities."""
        # Apply shake offset
        offset_x, offset_y = shake_offset

        # Render asteroids
        for asteroid in asteroids:
            self._render_asteroid(screen, glow_surface, asteroid, offset_x, offset_y)

        # Render ship
        if ship and ship.alive:
            self._render_ship(screen, glow_surface, ship, offset_x, offset_y)

        # Render bullets
        for bullet in bullets:
            self._render_bullet(screen, glow_surface, bullet, offset_x, offset_y)

        # Render UFO bullets
        for bullet in ufo_bullets:
            self._render_bullet(screen, glow_surface, bullet, offset_x, offset_y)

        # Render UFOs
        for ufo in ufos:
            self._render_ufo(screen, glow_surface, ufo, offset_x, offset_y)

        # Render particles
        for particle in particle_system.particles:
            self._render_particle(screen, particle, offset_x, offset_y)

    def _render_ship(self, screen, glow_surface, ship, offset_x, offset_y):
        """Render the ship with glow."""
        if not ship.alive:
            return

        # Blink when invincible
        if ship.invincible:
            blink = int(pygame.time.get_ticks() / 100) % 2 == 0
            if not blink:
                return

        points = [(x + offset_x, y + offset_y) for x, y in ship.get_rotated_points()]

        # Glow layer
        glow_points = [(x + offset_x, y + offset_y) for x, y in ship.get_rotated_points()]
        # pygame.draw.polygon(glow_surface, (0, 255, 255, 60), glow_points, 0)
        pygame.draw.polygon(glow_surface, (0, 255, 255, 120), glow_points, 1)

        # Main ship
        # pygame.draw.polygon(screen, Settings.NEON_CYAN, points, 0)
        pygame.draw.polygon(screen, Settings.NEON_CYAN, points, 1)

    def _render_asteroid(self, screen, glow_surface, asteroid, offset_x, offset_y):
        """Render asteroid with glow."""
        vertices = [(x + offset_x, y + offset_y) for x, y in asteroid.get_rotated_vertices()]

        # Glow
        # pygame.draw.polygon(glow_surface, asteroid.glow_color + (40,), vertices, 0)
        pygame.draw.polygon(glow_surface, asteroid.glow_color + (80,), vertices, 1)

        # Main asteroid
        # pygame.draw.polygon(screen, asteroid.color, vertices, 0)
        pygame.draw.polygon(screen, asteroid.color, vertices, 1)

    def _render_bullet(self, screen, glow_surface, bullet, offset_x, offset_y):
        """Render bullet with glow."""
        x, y = bullet.get_position()
        x += offset_x
        y += offset_y

        # Fade based on lifetime
        lifetime_ratio = bullet.get_lifetime_ratio()
        alpha = int(255 * lifetime_ratio)

        # Glow
        glow_radius = bullet.glow_size * (0.5 + 0.5 * lifetime_ratio)
        for i in range(3):
            glow_alpha = int((40 - i * 10) * lifetime_ratio)
            radius = int(glow_radius - i * 2)
            if radius > 0 and glow_alpha > 0:
                pygame.draw.circle(glow_surface, bullet.glow_color[:3] + (glow_alpha,),
                                (x, y), radius)

        # Main bullet
        if alpha > 0:
            color = bullet.color[:3] + (alpha,)
            surf = pygame.Surface((bullet.size * 2 + 4, bullet.size * 2 + 4), pygame.SRCALPHA)
            pygame.draw.circle(surf, color, (bullet.size + 2, bullet.size + 2), bullet.size)
            screen.blit(surf, (x - bullet.size - 2, y - bullet.size - 2))

            # White core
            if lifetime_ratio > 0.3:
                core_alpha = int(255 * min(1, lifetime_ratio * 2))
                pygame.draw.circle(screen, Settings.NEON_WHITE[:3] + (core_alpha,),
                                (x, y), bullet.size // 2)

    def _render_ufo(self, screen, glow_surface, ufo, offset_x, offset_y):
        """Render UFO with glow."""
        if not ufo.alive:
            return

        points = [(x + offset_x, y + offset_y) for x, y in ufo.get_rotated_points()]

        # Glow
        pygame.draw.polygon(glow_surface, ufo.glow_color + (40,), points, 0)
        pygame.draw.polygon(glow_surface, ufo.glow_color + (80,), points, 2)

        # Main UFO
        pygame.draw.polygon(screen, ufo.color, points, 0)
        pygame.draw.polygon(screen, Settings.NEON_WHITE, points, 1)

        # UFO light
        light_pos = (int(ufo.position[0] + offset_x),
                    int(ufo.position[1] - ufo.size * 0.6 + offset_y))
        pygame.draw.circle(screen, Settings.NEON_YELLOW, light_pos, 3)
        pygame.draw.circle(glow_surface, (255, 255, 0, 60), light_pos, 10)

    def _render_particle(self, screen, particle, offset_x, offset_y):
        """Render a single particle."""
        if not particle.alive:
            return

        x, y = particle.get_position()
        x += offset_x
        y += offset_y

        alpha = particle.get_alpha()
        size = max(1, int(particle.size))
        color = particle.color + (alpha,)

        # Create surface for alpha blending
        surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        pygame.draw.circle(surf, color, (size, size), size)
        screen.blit(surf, (x - size, y - size))

    def render_hud(self, screen, score, high_score, wave, invincible, alive):
        """Render HUD elements."""
        font = pygame.font.Font(None, 28)
        small_font = pygame.font.Font(None, 18)

        # Score
        score_text = font.render(f"SCORE {score:06d}", True, Settings.NEON_CYAN)
        screen.blit(score_text, (15, 15))

        # High score
        high_text = font.render(f"BEST {high_score:06d}", True, Settings.NEON_MAGENTA)
        screen.blit(high_text, (15, 45))

        # Wave
        wave_text = font.render(f"WAVE {wave}", True, Settings.NEON_GREEN)
        screen.blit(wave_text, (Settings.SCREEN_WIDTH - 120, 15))

        # Controls hint
        controls = small_font.render("W/A/D/Space/R/ESC", True, Settings.NEON_WHITE)
        controls_rect = controls.get_rect()
        controls_rect.centerx = Settings.SCREEN_WIDTH // 2
        controls_rect.bottom = Settings.SCREEN_HEIGHT - 15
        screen.blit(controls, controls_rect)

        # Ship status
        if not alive:
            status = small_font.render("RESPAWNING...", True, Settings.NEON_RED)
            status_rect = status.get_rect()
            status_rect.centerx = Settings.SCREEN_WIDTH // 2
            status_rect.centery = Settings.SCREEN_HEIGHT // 2 - 40
            screen.blit(status, status_rect)
        elif invincible:
            status = small_font.render("INVINCIBLE", True, Settings.NEON_GREEN)
            status_rect = status.get_rect()
            status_rect.centerx = Settings.SCREEN_WIDTH // 2
            status_rect.centery = Settings.SCREEN_HEIGHT // 2 - 40
            screen.blit(status, status_rect)