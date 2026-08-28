"""Procedural sound generation using NumPy."""

import pygame
import numpy as np
import random
from core.settings import Settings


class SoundSystem:
    """Generates procedural sounds with NumPy."""

    def __init__(self):
        self.mixer_available = False
        self.sounds = {}
        self.thruster_channel = None
        self._init_mixer()

        # Generate all sounds
        if self.mixer_available:
            self._generate_sounds()
            self.thruster_channel = pygame.mixer.find_channel()

    def _init_mixer(self):
        """Initialize pygame mixer."""
        try:
            pygame.mixer.init(
                frequency=Settings.SAMPLE_RATE,
                size=-16,
                channels=Settings.AUDIO_CHANNELS
            )
            self.mixer_available = True
        except pygame.error:
            self.mixer_available = False

    def _generate_sounds(self):
        """Generate all procedural sounds."""
        self.sounds['shoot'] = self._generate_shoot_sound()
        self.sounds['explosion'] = self._generate_explosion_sound()
        self.sounds['thruster'] = self._generate_thruster_sound()
        self.sounds['ufo_shoot'] = self._generate_ufo_shoot_sound()
        self.sounds['ufo_hum'] = self._generate_ufo_hum_sound()

    def _generate_shoot_sound(self):
        """Generate laser shoot sound."""
        sample_rate = Settings.SAMPLE_RATE
        duration = 0.08
        samples = int(sample_rate * duration)

        t = np.linspace(0, duration, samples)
        freq = 800 - 600 * (t / duration)
        wave = np.sin(2 * np.pi * freq * t)

        envelope = np.exp(-t * 30)
        wave = wave * envelope

        wave = (wave * 32767).astype(np.int16)
        return pygame.sndarray.make_sound(wave)

    def _generate_explosion_sound(self):
        """Generate explosion sound with noise."""
        sample_rate = Settings.SAMPLE_RATE
        duration = random.uniform(0.3, 0.6)
        samples = int(sample_rate * duration)

        noise = np.random.normal(0, 1, samples)
        t = np.linspace(0, duration, samples)
        envelope = np.exp(-t * 8)
        wave = noise * envelope

        wave += np.sin(2 * np.pi * 200 * t) * np.exp(-t * 10) * 0.3

        # Normalize
        wave = wave / np.max(np.abs(wave))
        wave = (wave * 32767).astype(np.int16)
        return pygame.sndarray.make_sound(wave)

    def _generate_thruster_sound(self):
        """Generate thruster sound."""
        sample_rate = Settings.SAMPLE_RATE
        duration = 0.5
        samples = int(sample_rate * duration)

        t = np.linspace(0, duration, samples)

        # Low frequency rumble with noise
        wave = np.sin(2 * np.pi * 60 * t) * 0.7
        wave += np.random.normal(0, 0.3, samples)
        wave *= np.exp(-t * 2)

        wave = (wave * 16384).astype(np.int16)
        return pygame.sndarray.make_sound(wave)

    def _generate_ufo_shoot_sound(self):
        """Generate UFO shoot sound."""
        sample_rate = Settings.SAMPLE_RATE
        duration = 0.1
        samples = int(sample_rate * duration)

        t = np.linspace(0, duration, samples)
        freq = 400 + 200 * (t / duration)
        wave = np.sin(2 * np.pi * freq * t)

        envelope = np.exp(-t * 20)
        wave = wave * envelope

        wave = (wave * 32767).astype(np.int16)
        return pygame.sndarray.make_sound(wave)

    def _generate_ufo_hum_sound(self):
        """Generate UFO humming sound."""
        sample_rate = Settings.SAMPLE_RATE
        duration = 1.0
        samples = int(sample_rate * duration)

        t = np.linspace(0, duration, samples)

        # Oscillating tone
        wave = np.sin(2 * np.pi * 200 * t) * 0.5
        wave += np.sin(2 * np.pi * 240 * t) * 0.3
        wave += np.sin(2 * np.pi * 180 * t + t * 50) * 0.2

        wave = (wave * 16384).astype(np.int16)
        return pygame.sndarray.make_sound(wave)

    def play_shoot(self):
        """Play shoot sound."""
        if self.mixer_available and 'shoot' in self.sounds:
            self.sounds['shoot'].play()

    def play_explosion(self):
        """Play explosion sound with slight variation."""
        if self.mixer_available:
            sound = self._generate_explosion_sound()
            sound.play()

    def play_thruster(self):
        """Play thruster sound."""
        if self.mixer_available and self.thruster_channel:
            if not self.thruster_channel.get_busy():
                self.thruster_channel.play(self.sounds['thruster'], loops=-1)

    def stop_thruster(self):
        """Stop thruster sound."""
        if self.mixer_available and self.thruster_channel:
            if self.thruster_channel.get_busy():
                self.thruster_channel.stop()

    def play_ufo_shoot(self):
        """Play UFO shoot sound."""
        if self.mixer_available and 'ufo_shoot' in self.sounds:
            self.sounds['ufo_shoot'].play()

    def play_ufo_hum(self):
        """Play UFO hum sound."""
        if self.mixer_available and 'ufo_hum' in self.sounds:
            self.sounds['ufo_hum'].play()