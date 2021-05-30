import pygame

class Ship:
    """A class to manage the ship"""

    def __init__(self,ai_game) -> None:
        """Initialize the ship and set its starting position"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Load the ship image and get its rect.
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # start each new ship at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom

    def blitme(self):
        """draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)