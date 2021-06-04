class Settings:
    "A class to store all settings for AI"

    def __init__(self) -> None:
        """initialize game settings"""

        #screen
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230,230,230)

        #ship settings
        self.ship_speed = 1.5
        self.bullets_allowed = 3

        #bullet settings
        self.bullet_speed = 1.0
        self.bullet_width = 1
        self.bullet_height = 15
        self.bullet_color = (60,60,60)

