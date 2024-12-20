import pygame


class Ship:
    """A class to manage the ship."""

    def __init__(self, ai_game):
        """Initialize the ship and set its starting position"""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.moving_right = False

        # Load the ship image and get its rect.
        self.image = pygame.image.load('images/DurrrSpaceShip.bmp')
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

    def update(self):
        """Update the ship's position based on the movement flag."""
        if self.moving_right is True:
            self.rect.x += 1

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)
