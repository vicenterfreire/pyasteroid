"""Game data persistence with JSON."""

import json
import os
from pathlib import Path


class GameData:
    """Handles loading and saving game data to JSON."""

    def __init__(self, data_path="data/game.json"):
        self.data_path = Path(data_path)
        self.high_score = 0
        self.background_path = None
        self.load()

    def load(self):
        """Load data from JSON file."""
        try:
            if not self.data_path.exists():
                self._create_default()
                return

            with open(self.data_path, 'r') as f:
                data = json.load(f)

            self.high_score = data.get('high_score', 0)
            self.background_path = data.get('background', None)

            # Validate background path
            if self.background_path and not Path(self.background_path).exists():
                self.background_path = None

        except (json.JSONDecodeError, IOError):
            self._create_default()

    def save(self):
        """Save data to JSON file."""
        try:
            # Ensure directory exists
            self.data_path.parent.mkdir(parents=True, exist_ok=True)

            with open(self.data_path, 'w') as f:
                json.dump({
                    'high_score': self.high_score,
                    'background': self.background_path
                }, f, indent=4)
        except IOError:
            pass

    def _create_default(self):
        """Create default data."""
        self.high_score = 0
        self.background_path = None
        self.save()

    def update_high_score(self, score):
        """Update high score if score is higher."""
        if score > self.high_score:
            self.high_score = score
            self.save()
            return True
        return False