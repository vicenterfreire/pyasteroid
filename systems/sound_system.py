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

        # Normalize to prevent clipping
        max_val = np.max(np.abs(wave))
        if max_val > 0:
            wave = wave / max_val

        wave = (wave * 32767).astype(np.int16)
        return self._make_sound(wave)

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
        max_val = np.max(np.abs(wave))
        if max_val > 0:
            wave = wave / max_val
        wave = (wave * 32767).astype(np.int16)
        return self._make_sound(wave)

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

        # Normalize
        max_val = np.max(np.abs(wave))
        if max_val > 0:
            wave = wave / max_val
        wave = (wave * 16384).astype(np.int16)
        return self._make_sound(wave)

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

        # Normalize
        max_val = np.max(np.abs(wave))
        if max_val > 0:
            wave = wave / max_val
        wave = (wave * 32767).astype(np.int16)
        return self._make_sound(wave)

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

        # Normalize
        max_val = np.max(np.abs(wave))
        if max_val > 0:
            wave = wave / max_val
        wave = (wave * 16384).astype(np.int16)
        return self._make_sound(wave)

    def _make_sound(self, wave):
        """Convert numpy array to pygame sound safely."""
        try:
            # Ensure wave is int16
            wave = wave.astype(np.int16)

            # Check if mixer is initialized
            if not pygame.mixer.get_init():
                return None

            # Get mixer settings safely
            mixer_init = pygame.mixer.get_init()
            if mixer_init is None:
                return None

            frequency, size, channels = mixer_init

            # Convert mono to stereo if needed
            if channels == 2 and wave.ndim == 1:
                wave = np.column_stack((wave, wave))

            return pygame.sndarray.make_sound(wave)
        except Exception as e:
            # Silently fail - sound just won't play
            return None

    def _play_sound(self, sound_key):
        """Safely play a sound by key."""
        if not self.mixer_available:
            return

        sound = self.sounds.get(sound_key)
        if sound is not None:
            try:
                sound.play()
            except Exception:
                pass  # Silently fail

    def play_shoot(self):
        """Play shoot sound."""
        self._play_sound('shoot')

    def play_explosion(self):
        """Play explosion sound with slight variation."""
        if not self.mixer_available:
            return

        try:
            sound = self._generate_explosion_sound()
            if sound is not None:
                sound.play()
        except Exception:
            pass

    def play_thruster(self):
        """Play thruster sound."""
        if not self.mixer_available or self.thruster_channel is None:
            return

        try:
            if not self.thruster_channel.get_busy():
                sound = self.sounds.get('thruster')
                if sound is not None:
                    self.thruster_channel.play(sound, loops=-1)
        except Exception:
            pass

    def stop_thruster(self):
        """Stop thruster sound."""
        if not self.mixer_available or self.thruster_channel is None:
            return

        try:
            if self.thruster_channel.get_busy():
                self.thruster_channel.stop()
        except Exception:
            pass

    def play_ufo_shoot(self):
        """Play UFO shoot sound."""
        self._play_sound('ufo_shoot')

    def play_ufo_hum(self):
        """Play UFO hum sound."""
        self._play_sound('ufo_hum')