class GameStats():
    """Track statistics for Space Invaders."""

    def __init__(self, si_settings):
        """Initialize statistics."""
        self.si_settings = si_settings
        self.reset_stats()

        # Start Alien Invasion in an active state.
        self.game_active = False

        # High score should never be reset.
        self.high_score = 0

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.si_settings.ship_limit
        self.score = 0
        self.level = 1
