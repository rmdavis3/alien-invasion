"""
game_stats.py

"""


class GameStats:
    """Tracks statistics for Alien Invasion."""

    def __init(self, ai_game):
        """Initialize statistics."""
        self.settings = ai_game.settings
        self.reset_stats()

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_lef = self.settings.ship_limit
