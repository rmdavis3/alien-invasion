"""
alien_invasion.py

This module implements the Alien Invasion game, a classic arcade-style game where
the player controls a spaceship to defend against waves of alien invaders.

The player uses keyboard controls to move the spaceship left or right and shoot
bullets to destroy aliens. The game tracks the player's score, level, and remaining
ships, with progressively challenging waves of aliens as levels increase.

Modules:
    - settings: Contains game configuration settings.
    - game_stats: Tracks game statistics such as score, level, and remaining ships.
    - scoreboard: Handles the visual display of scores, levels, and ships.
    - button: Manages the Play button functionality.
    - ship: Represents the player's ship and its movement.
    - bullet: Defines the bullets fired by the player's ship.
    - alien: Represents the alien invaders and their behavior.

Classes:
    AlienInvasion: The main class that manages the game initialization, event handling,
    game updates, and rendering.

Usage:
    Run this script to start the Alien Invasion game:
        $ python alien_invasion.py
"""

import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    """
    Overall class to manage game assets and behavior for the Alien Invasion game.

    This class initializes the game, sets up its resources, and handles the main
    game loop, including event handling, updating game states, and rendering
    visuals.

    Attributes:
        clock (pygame.time.Clock): Regulates the game's frame rate.
        settings (Settings): Stores game settings, including screen dimensions,
            ship speed, bullet speed, and alien behavior.
        screen (pygame.Surface): Represents the main game display surface.
        stats (GameStats): Tracks game statistics such as score, level, and remaining ships.
        scoreboard (Scoreboard): Manages the display of scores, levels, and remaining ships.
        ship (Ship): Represents the player's ship.
        bullets (pygame.sprite.Group): Group for managing active bullets in the game.
        aliens (pygame.sprite.Group): Group for managing aliens in the fleet.
        game_active (bool): Indicates whether the game is currently active.
        play_button (Button): The Play button displayed at the start or after a game ends.

    Methods:
        __init__(): Initializes the game and sets up resources.
        run_game(): Starts the main game loop.
        _check_events(): Handles user input events (keyboard and mouse).
        _check_play_button(mouse_pos): Starts a new game when the Play button is clicked.
        _check_keydown_events(event): Handles key press events.
        _check_keyup_events(event): Handles key release events.
        _fire_bullet(): Fires a bullet if under the allowed limit.
        _udpate_bullets(): Updates bullet positions and handles collisions with aliens.
        _check_bullet_alien_collisions(): Handles bullet-alien collisions, updates scores,
            and generates a new fleet if necessary.
        _ship_hit(): Responds to the player's ship being hit by an alien.
        _update_aliens(): Updates alien positions and checks for collisions with the ship or
            the screen bottom.
        _check_aliens_bottom(): Handles the case where aliens reach the bottom of the screen.
        _create_fleet(): Creates a fleet of aliens to attack the player.
        _create_alien(x_position, y_position): Creates an alien and positions it.
        _check_fleet_edges(): Changes direction of the alien fleet when it reaches screen edges.
        _change_fleet_direction(): Drops the fleet and changes its direction.
        _update_screen(): Draws all game elements and updates the screen display.
    """

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()  # pylint: disable=no-member
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        # Create an instance to store game statistics.
        self.stats = GameStats(self)

        # Create an instance
        self.scoreboard = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Start Alien Invasion in an active state.
        self.game_active = False

        # Make the Play button.
        self.play_button = Button(self, "Play")

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()

            if self.game_active:
                self.ship.update()
                self._udpate_bullets()
                self._update_aliens()

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
            elif event.type == pygame.MOUSEBUTTONDOWN:  # pylint: disable=no-member
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            # Reset the game settings.
            self.settings.initialize_dynamic_settings()

            # Reset the game statistics.
            self.stats.reset_stats()
            self.scoreboard.prep_score()
            self.scoreboard.prep_level()
            self.scoreboard.prep_ships()
            self.game_active = True

            # Get rid of any remaining bullets and aliens.
            self.bullets.empty()
            self.aliens.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:  # pylint: disable=no-member
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:  # pylint: disable=no-member
            self.ship.moving_left = True
        elif event.key == pygame.K_q:  # pylint: disable=no-member
            pygame.quit()  # pylint: disable=no-member
            sys.exit()
        elif self.game_active and event.key == pygame.K_SPACE:  # pylint: disable=no-member
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
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Remove any bullets and aliens that have collided.
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                # Add points for all aliens hit by a single bullet
                self.stats.score += self.settings.alien_points * len(aliens)
            self.scoreboard.prep_score()
            self.scoreboard.check_high_score()

        if not self.aliens:
            # Destory existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase level.
            self.stats.level += 1
            self.scoreboard.prep_level()

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:
            # Decrement ships_left, and update scoreboard.
            self.stats.ships_left -= 1
            self.scoreboard.prep_ships()

            # Get rid of any remaining bullets and aliens.
            self.bullets.empty()
            self.aliens.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Pause.
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _update_aliens(self):
        """Check if the fleet is at an edge, then update positions."""
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break

    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create an alien and keep adding aliens until there's no more room left.
        # Spacing between aliens is one alien width and one alien height.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        current_x, current_y = alien_width, alien_height + 22
        while current_y < (self.settings.screen_height - 14 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width

            # Finished a row; reset x value, and increment y value.
            current_x = alien_width
            current_y += 2 * alien_height

    def _create_alien(self, x_position, y_position):
        """Create an alien and place it in a row"""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)

        # Draw the score information.
        self.scoreboard.show_score()

        # Draw the play button if the game is inactive.
        if not self.game_active:
            self.play_button.draw_button()

        # Make the most recently drawn screen visible.
        pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
