"""Game settings and constants."""

class Settings:
    # Screen
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    FPS = 60

    # Colors (neon palette)
    NEON_CYAN = (0, 255, 255)
    NEON_BLUE = (0, 150, 255)
    NEON_PURPLE = (180, 0, 255)
    NEON_MAGENTA = (255, 0, 200)
    NEON_GREEN = (0, 255, 100)
    NEON_ORANGE = (255, 120, 0)
    NEON_RED = (255, 50, 50)
    NEON_YELLOW = (255, 255, 0)
    NEON_WHITE = (230, 230, 255)

    # Ship
    SHIP_ACCELERATION = 200.0
    SHIP_MAX_SPEED = 300.0
    SHIP_FRICTION = 0.98
    SHIP_ROTATION_SPEED = 200.0
    SHIP_SIZE = 20
    SHIP_INVINCIBILITY_TIME = 2.0
    SHIP_BLINK_INTERVAL = 0.1

    # Bullets
    BULLET_SPEED = 500.0
    BULLET_LIFETIME = 2.0
    BULLET_SIZE = 4
    BULLET_COOLDOWN = 0.15
    BULLET_GLOW_SIZE = 12

    # Asteroids
    ASTEROID_BASE_SPEED = 60.0
    ASTEROID_MAX_SPEED = 150.0
    ASTEROID_SPAWN_RATE = 3.0
    ASTEROID_MAX_SPAWN = 15
    ASTEROID_SPAWN_DISTANCE = 150

    # Asteroid sizes
    LARGE_RADIUS = 45
    MEDIUM_RADIUS = 25
    SMALL_RADIUS = 12

    # Asteroid colors
    ASTEROID_COLORS = [
        (0, 255, 255),   # cyan
        (0, 150, 255),   # blue
        (180, 0, 255),   # purple
        (255, 0, 200),   # magenta
        (0, 255, 100),   # green
    ]

    # UFO
    UFO_SPAWN_INTERVAL = 8.0
    UFO_SPAWN_CHANCE = 0.7
    UFO_SPEED = 120.0
    UFO_SIZE = 25
    UFO_SHOOT_COOLDOWN = 1.5
    UFO_ACCURACY_ERROR = 0.3
    UFO_MAX_SPAWN = 2

    # Particles
    PARTICLE_MAX_COUNT = 200
    PARTICLE_FADE_RATE = 0.98
    PARTICLE_SHRINK_RATE = 0.98

    # Scoring
    SCORE_LARGE_ASTEROID = 20
    SCORE_MEDIUM_ASTEROID = 50
    SCORE_SMALL_ASTEROID = 100
    SCORE_UFO = 250

    # Screen shake
    SHAKE_MAX_INTENSITY = 15
    SHAKE_DECAY = 0.9

    # Waves
    WAVE_ASTEROID_INCREMENT = 2
    WAVE_SPEED_INCREMENT = 1.05
    WAVE_UFO_INTERVAL_DECREASE = 0.5
    WAVE_UFO_INTERVAL_MIN = 3.0
    WAVE_MAX_ASTEROIDS = 30

    # Audio
    SAMPLE_RATE = 44100
    AUDIO_CHANNELS = 1

    # Glow
    GLOW_LAYER_ALPHA = 60