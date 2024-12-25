
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
        # Screen settings.
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (40, 160, 200)

        # Ship settings.
        self.ship_speed = 3
        self.ship_limit = 3

        # Bullet settings.
        self.bullet_speed = 2.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # Alien settings.
        self.alien_speed = 2.0
        self.fleet_drop_speed = 10
        # fleet_direction of 1 represents right; -1 represents left
        self.fleet_direction = 1
