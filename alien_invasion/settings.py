
"""
settings.py

This module defines the Settings class, which stores all configuration settings 
for the Alien Invasion game.

Classes:
    Settings: Stores game settings, including screen dimensions and background color.
"""


class Settings:
    """A class to store all settings for Alien Invasion"""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (40, 160, 200)
