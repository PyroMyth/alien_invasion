class GameStats():
    """Track statistics for Alien Invasion"""

    def __init__(self, the_settings):
        self.the_settings = the_settings
        self.reset_stats()
        self.score = 0


    def reset_stats(self):
        """Initialize statistics"""
        self.ships_left = self.the_settings.ship_limit
