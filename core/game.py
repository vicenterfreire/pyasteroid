"""Main game class."""

import pygame
import math
import random
import numpy as np
from core.settings import Settings
from core.game_data import GameData
from entities.ship import Ship
from entities.asteroid import Asteroid
from entities.bullet import Bullet
from entities.ufo import UFO
from systems.collision import CollisionSystem
from systems.particle_system import ParticleSystem
from systems.sound_system import SoundSystem
from rendering.renderer import Renderer
from rendering.background import Background


class Game:
    """Main game controller."""

    def __init__(self):
        self.screen = pygame.display.set_mode(
            (Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT)
        )
        pygame.display.set_caption("Neon Asteroids")
        self.clock = pygame.time.Clock()
        self.running = True

        # Game data
        self.game_data = GameData()

        # Systems
        self.particle_system = ParticleSystem()
        self.sound_system = SoundSystem()
        self.renderer = Renderer(self.screen)
        self.background = Background(self.screen, self.game_data)

        # Game state
        self.score = 0
        self.wave = 1
        self.wave_timer = 0
        self.game_over = False
        self.respawn_timer = 0
        self.shake_intensity = 0

        # Entities
        self.ship = None
        self.asteroids = []
        self.bullets = []
        self.ufos = []
        self.ufo_bullets = []

        # Spawn timers
        self.asteroid_spawn_timer = 0
        self.ufo_spawn_timer = 0
        self.ufo_spawn_interval = Settings.UFO_SPAWN_INTERVAL

        # Initialize
        self.reset_game()

    def reset_game(self):
        """Reset game state."""
        self.score = 0
        self.wave = 1
        self.wave_timer = 0
        self.game_over = False
        self.respawn_timer = 0
        self.shake_intensity = 0

        self.asteroids = []
        self.bullets = []
        self.ufos = []
        self.ufo_bullets = []
        self.particle_system.clear()

        self.ship = Ship(
            Settings.SCREEN_WIDTH // 2,
            Settings.SCREEN_HEIGHT // 2
        )

        self.asteroid_spawn_timer = 0
        self.ufo_spawn_timer = 0
        self.ufo_spawn_interval = Settings.UFO_SPAWN_INTERVAL

        self.spawn_initial_asteroids()

    def spawn_initial_asteroids(self):
        """Spawn initial wave of asteroids."""
        count = 3 + self.wave
        for _ in range(count):
            self.spawn_asteroid()

    def spawn_asteroid(self):
        """Spawn a single asteroid away from ship."""
        if len(self.asteroids) >= Settings.WAVE_MAX_ASTEROIDS:
            return

        # Try to spawn away from ship
        for _ in range(10):
            x = random.randint(50, Settings.SCREEN_WIDTH - 50)
            y = random.randint(50, Settings.SCREEN_HEIGHT - 50)

            if self.ship:
                dist = math.sqrt((x - self.ship.position[0])**2 +
                               (y - self.ship.position[1])**2)
                if dist > Settings.ASTEROID_SPAWN_DISTANCE:
                    asteroid = Asteroid(x, y, 0)
                    self.asteroids.append(asteroid)
                    return

        # Fallback
        asteroid = Asteroid(
            random.randint(50, Settings.SCREEN_WIDTH - 50),
            random.randint(50, Settings.SCREEN_HEIGHT - 50),
            0
        )
        self.asteroids.append(asteroid)

    def spawn_ufo(self):
        """Spawn a UFO."""
        if len(self.ufos) >= Settings.UFO_MAX_SPAWN:
            return

        # Spawn from edge
        side = random.randint(0, 3)
        if side == 0:  # Top
            x = random.randint(0, Settings.SCREEN_WIDTH)
            y = -Settings.UFO_SIZE
        elif side == 1:  # Bottom
            x = random.randint(0, Settings.SCREEN_WIDTH)
            y = Settings.SCREEN_HEIGHT + Settings.UFO_SIZE
        elif side == 2:  # Left
            x = -Settings.UFO_SIZE
            y = random.randint(0, Settings.SCREEN_HEIGHT)
        else:  # Right
            x = Settings.SCREEN_WIDTH + Settings.UFO_SIZE
            y = random.randint(0, Settings.SCREEN_HEIGHT)

        advanced = self.wave > 3 and random.random() < 0.3
        ufo = UFO(x, y, advanced)
        self.ufos.append(ufo)

    def shoot(self):
        """Shoot a bullet from the ship."""
        if not self.ship or not self.ship.alive:
            return

        direction = self.ship.get_direction()
        bullet_velocity = direction * Settings.BULLET_SPEED + self.ship.velocity

        bullet = Bullet(
            self.ship.position[0],
            self.ship.position[1],
            bullet_velocity,
            "player"
        )
        self.bullets.append(bullet)

        # Play sound
        self.sound_system.play_shoot()

    def handle_input(self):
        """Handle keyboard input."""
        keys = pygame.key.get_pressed()

        # Ship controls
        if self.ship and self.ship.alive:
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                self.ship.rotation = -1
            elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                self.ship.rotation = 1
            else:
                self.ship.rotation = 0

            if keys[pygame.K_w] or keys[pygame.K_UP]:
                self.ship.is_accelerating = True
            else:
                self.ship.is_accelerating = False

    def update(self, dt):
        """Update game state."""
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_r:
                    self.reset_game()
                elif event.key == pygame.K_SPACE and self.ship and self.ship.alive:
                    if not hasattr(self, '_last_shoot'):
                        self._last_shoot = 0
                    if pygame.time.get_ticks() - self._last_shoot > Settings.BULLET_COOLDOWN * 1000:
                        self.shoot()
                        self._last_shoot = pygame.time.get_ticks()

        # Handle continuous input
        self.handle_input()

        # Update ship
        if self.ship:
            self.ship.update(dt)

            # Thruster particles
            if self.ship.alive and self.ship.is_accelerating:
                positions = self.ship.get_thruster_positions()
                self.particle_system.emit_thruster(positions)
                if self.sound_system.sounds.get('thruster'):
                    self.sound_system.play_thruster()
            else:
                self.sound_system.stop_thruster()

        # Update asteroids
        for asteroid in self.asteroids[:]:
            asteroid.update(dt)

        # Update bullets
        for bullet in self.bullets[:]:
            bullet.update(dt)
            if not bullet.alive:
                self.bullets.remove(bullet)

        # Update UFO bullets
        for bullet in self.ufo_bullets[:]:
            bullet.update(dt)
            if not bullet.alive:
                self.ufo_bullets.remove(bullet)

        # Update UFOs
        for ufo in self.ufos[:]:
            if ufo.shoot_timer is not None:
                if ufo.update(dt, self.ship.position if self.ship else None):
                    # UFO shoots
                    if self.ship and self.ship.alive:
                        direction = ufo.get_shoot_direction(self.ship.position)
                        bullet_velocity = direction * (Settings.BULLET_SPEED * 0.7)
                        bullet = Bullet(
                            ufo.position[0],
                            ufo.position[1],
                            bullet_velocity,
                            "ufo"
                        )
                        bullet.color = Settings.NEON_ORANGE
                        self.ufo_bullets.append(bullet)
                        self.sound_system.play_ufo_shoot()

        # Spawn asteroids
        self.asteroid_spawn_timer += dt
        if self.asteroid_spawn_timer >= Settings.ASTEROID_SPAWN_RATE:
            self.asteroid_spawn_timer = 0
            if len(self.asteroids) < Settings.ASTEROID_MAX_SPAWN + self.wave * 2:
                self.spawn_asteroid()

        # Spawn UFOs
        self.ufo_spawn_timer += dt
        if self.ufo_spawn_timer >= self.ufo_spawn_interval:
            self.ufo_spawn_timer = 0
            if random.random() < Settings.UFO_SPAWN_CHANCE:
                self.spawn_ufo()

        # Check collisions
        self.check_collisions()

        # Update particles
        self.particle_system.update(dt)

        # Update screen shake
        self.shake_intensity *= Settings.SHAKE_DECAY
        if self.shake_intensity < 0.1:
            self.shake_intensity = 0

        # Check respawn
        if self.ship and not self.ship.alive:
            self.respawn_timer += dt
            if self.respawn_timer >= 2.0:
                self.ship.reset(
                    Settings.SCREEN_WIDTH // 2,
                    Settings.SCREEN_HEIGHT // 2
                )
                self.respawn_timer = 0

        # Wave progression
        self.wave_timer += dt
        if self.wave_timer >= 30.0:  # New wave every 30 seconds
            self.wave_timer = 0
            self.wave += 1

            # Increase difficulty
            self.ufo_spawn_interval = max(
                Settings.WAVE_UFO_INTERVAL_MIN,
                self.ufo_spawn_interval - Settings.WAVE_UFO_INTERVAL_DECREASE
            )

            # Spawn bonus asteroids for new wave
            for _ in range(Settings.WAVE_ASTEROID_INCREMENT):
                self.spawn_asteroid()

    def check_collisions(self):
        """Check all collisions."""
        # Bullets vs Asteroids
        for bullet in self.bullets[:]:
            for asteroid in self.asteroids[:]:
                if CollisionSystem.check_bullet_asteroid(bullet, asteroid):
                    # Destroy asteroid
                    self.score += asteroid.score
                    self.game_data.update_high_score(self.score)

                    # Spawn particles
                    self.particle_system.emit_asteroid_explosion(
                        asteroid.position[0],
                        asteroid.position[1],
                        asteroid.color
                    )

                    # Screen shake
                    self.shake_intensity = min(
                        self.shake_intensity + 3,
                        Settings.SHAKE_MAX_INTENSITY
                    )

                    # Split asteroid
                    new_asteroids = asteroid.get_split_asteroids()
                    self.asteroids.extend(new_asteroids)

                    # Remove asteroid and bullet
                    self.asteroids.remove(asteroid)
                    bullet.alive = False
                    break

        # Bullets vs UFOs
        for bullet in self.bullets[:]:
            for ufo in self.ufos[:]:
                if CollisionSystem.check_bullet_ufo(bullet, ufo):
                    self.score += ufo.score
                    self.game_data.update_high_score(self.score)

                    self.particle_system.emit_ufo_explosion(
                        ufo.position[0],
                        ufo.position[1]
                    )

                    self.shake_intensity = min(
                        self.shake_intensity + 5,
                        Settings.SHAKE_MAX_INTENSITY
                    )

                    self.ufos.remove(ufo)
                    bullet.alive = False
                    self.sound_system.play_explosion()
                    break

        # Ship vs Asteroids
        if self.ship and self.ship.alive:
            for asteroid in self.asteroids[:]:
                if CollisionSystem.check_ship_asteroid(self.ship, asteroid):
                    self.destroy_ship()
                    break

        # Ship vs UFOs
        if self.ship and self.ship.alive:
            for ufo in self.ufos[:]:
                if CollisionSystem.check_ship_ufo(self.ship, ufo):
                    self.destroy_ship()
                    break

        # UFO bullets vs Ship
        if self.ship and self.ship.alive:
            for bullet in self.ufo_bullets[:]:
                if CollisionSystem.check_ufo_bullet_ship(bullet, self.ship):
                    self.destroy_ship()
                    bullet.alive = False
                    break

    def destroy_ship(self):
        """Destroy the ship."""
        if not self.ship or not self.ship.alive:
            return

        self.ship.alive = False

        # Explosion
        self.particle_system.emit_ship_explosion(
            self.ship.position[0],
            self.ship.position[1]
        )

        # Screen shake
        self.shake_intensity = min(
            self.shake_intensity + 8,
            Settings.SHAKE_MAX_INTENSITY
        )

        self.sound_system.play_explosion()
        self.respawn_timer = 0

    def render(self):
        """Render the game."""
        # Get shake offset
        shake_offset = (0, 0)
        if self.shake_intensity > 0:
            shake_offset = (
                random.randint(-int(self.shake_intensity), int(self.shake_intensity)),
                random.randint(-int(self.shake_intensity), int(self.shake_intensity))
            )

        # Clear screen
        self.background.render(shake_offset)

        # Create glow surface
        glow_surface = pygame.Surface(
            (Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT),
            pygame.SRCALPHA
        )

        # Render entities
        self.renderer.render_entities(
            self.screen,
            glow_surface,
            self.ship,
            self.asteroids,
            self.bullets,
            self.ufos,
            self.ufo_bullets,
            self.particle_system,
            shake_offset
        )

        # Apply glow
        self.screen.blit(glow_surface, (0, 0))

        # Render HUD
        self.renderer.render_hud(
            self.screen,
            self.score,
            self.game_data.high_score,
            self.wave,
            self.ship.invincible if self.ship else False,
            self.ship.alive if self.ship else False
        )

        # Update display
        pygame.display.flip()

    def run(self):
        """Main game loop."""
        dt = 0

        while self.running:
            dt = self.clock.tick(Settings.FPS) / 1000.0

            self.update(dt)
            self.render()

        # Save on exit
        self.game_data.save()