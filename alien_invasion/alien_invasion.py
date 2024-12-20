"""
alien_invasion.py

This module implements the Alien Invasion game, a simple arcade game where the
player must defend against waves of aliens.

Classes:
    AlienInvasion: Manages game initialization, resources, and the main game loop.
"""

import sys
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    """Overall class to manage game asets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()  # pylint: disable=no-member
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            self.ship.update()
            self._udpate_bullets()
            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # pylint: disable=no-member
                pygame.quit()  # pylint: disable=no-member
                sys.exit()
            elif event.type == pygame.KEYDOWN:  # pylint: disable=no-member
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:  # pylint: disable=no-member
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:  # pylint: disable=no-member
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:  # pylint: disable=no-member
            self.ship.moving_left = True
        elif event.key == pygame.K_q:  # pylint: disable=no-member
            pygame.quit()  # pylint: disable=no-member
            sys.exit()
        elif event.key == pygame.K_SPACE:  # pylint: disable=no-member
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:  # pylint: disable=no-member
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:  # pylint: disable=no-member
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _udpate_bullets(self):
        """Update position of bullets and get rod of old bullets."""
        # Update bullet positions
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create an alien and keep adding aliens until there's no more room left.
        # Spacing between aliens is one alien width.
        alien = Alien(self)
        alien_width = alien.rect.width

        current_x = alien_width
        while current_x < (self.settings.screen_width - 2 * alien_width):
            new_alien = Alien(self)
            new_alien.x = current_x
            new_alien.rect.x = current_x
            self.aliens.add(new_alien)
            current_x += 2 * alien_width

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)
        # Make the most recently drawn screen visible.
        pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
