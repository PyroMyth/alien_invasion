import sys
import pygame
import game_functions
from settings import Settings
from game_stats import GameStats
from actors import Ship
from pygame.sprite import Group


def main():
    pygame.init()  # Initialize game
    the_settings = Settings()
    screen = pygame.display.set_mode((the_settings.screen_width, the_settings.screen_height))
    pygame.display.set_caption('Alien Invasion')
    stats = GameStats(the_settings)  # Initialize the statistics
    ship = Ship(the_settings, screen)  # Make a ship
    bullets = Group()  # Make a group to store the bullets
    aliens = Group()  # Make a group of aliens
    while the_settings.game_active or the_settings.menu_active or \
            the_settings.options_active or the_settings.game_over_active:
        if the_settings.game_active and the_settings.new_game:
            the_settings.new_game = False
            stats = GameStats(the_settings)  # Initialize the statistics
            ship = Ship(the_settings, screen)  # Make a ship
            bullets = Group()  # Make a group to store the bullets
            aliens = Group()  # Make a group of aliens
            game_functions.create_fleet(the_settings, screen, ship, aliens)
            stats.score = 0
        elif the_settings.menu_active:
            game_functions.display_menu(screen)
        elif the_settings.options_active:
            game_functions.display_options(the_settings, screen)
        elif the_settings.game_over_active:
            game_functions.display_game_over(stats, screen)

        game_functions.check_events(the_settings, screen, ship, bullets)
        if the_settings.game_active:
            ship.update()
            game_functions.update_bullets(the_settings, stats, screen, ship, bullets, aliens)
            game_functions.update_aliens(the_settings, stats, screen, ship, aliens, bullets)
        game_functions.update_screen(the_settings, stats, screen, ship, aliens, bullets)


if __name__ == '__main__':
    main()
