import sys
import pygame
from actors import Alien
from actors import Bullet
from time import sleep


# Check Events Methods
def check_events(the_settings, screen, ship, bullets):
    """Respond to keypresses and mouse events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if the_settings.game_active:
                check_game_keydown_events(event, the_settings, screen, ship, bullets)
            elif the_settings.menu_active:
                check_menu_keydown_events(event, the_settings)
            elif the_settings.options_active:
                check_opt_keydown_events(event, the_settings, screen)
            elif the_settings.game_over_active:
                check_over_keydown_events(event, the_settings)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


def check_menu_keydown_events(event, the_settings):
    if event.key == pygame.K_q:
        sys.exit()
    if event.key == pygame.K_o:
        the_settings.menu_active = False
        the_settings.options_active = True
        the_settings.game_active = False
        the_settings.game_over_active = False
    elif event.key == pygame.K_n:
        the_settings.menu_active = False
        the_settings.game_over_active = False
        the_settings.game_active = True
        the_settings.new_game = True


def check_opt_keydown_events(event, the_settings, screen):
    if event.key == pygame.K_q:
        sys.exit()
    if event.key == pygame.K_b:
        the_settings.super_bullet = not the_settings.super_bullet
    elif event.key == pygame.K_e:
        # Difficulty = Easy
        the_settings.bullet_width = 10
        the_settings.bullets_allowed = 100
        the_settings.alien_speed_factor = 1
        the_settings.fleet_drop_speed = 10
    elif event.key == pygame.K_n:
        # Difficulty = Normal
        the_settings.bullet_width = 3
        the_settings.bullets_allowed = 3
        the_settings.alien_speed_factor = 1
        the_settings.fleet_drop_speed = 10
    elif event.key == pygame.K_h:
        # Difficulty = Hard
        the_settings.bullet_width = 3
        the_settings.bullets_allowed = 1
        the_settings.alien_speed_factor = 5
        the_settings.fleet_drop_speed = 30
    elif event.key == pygame.K_UP:
        the_settings.ship_limit += 1
    elif event.key == pygame.K_DOWN and the_settings.ship_limit > 0:
        the_settings.ship_limit -= 1
    elif event.key == pygame.K_m:
        the_settings.options_active = False
        the_settings.menu_active = True
    if the_settings.options_active:
        display_options(the_settings, screen)


def check_game_keydown_events(event, the_settings, screen, ship, bullets):
    if event.key == pygame.K_q:
        sys.exit()
    elif event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullets(the_settings, screen, ship, bullets)


def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_over_keydown_events(event, the_settings):
    if event.key == pygame.K_q:
        sys.exit()
    elif event.key == pygame.K_n:
        the_settings.game_over_active = False
        the_settings.game_active = True
        the_settings.new_game = True
    elif event.key == pygame.K_m:
        the_settings.game_over_active = False
        the_settings.menu_active = True


# Display Methods
def display_menu(screen):
    screen.fill((0, 0, 0))
    display_text('Alien INVASION!!', screen, 100, 100, 50, (0, 255, 64))
    display_text('Press:', screen, 100, 200)
    display_text('[N]ew Game', screen, 100, 300)
    display_text('[O]ptions', screen, 100, 400)
    display_text('[Q]uit', screen, 100, 500)
    pygame.display.flip()


def display_options(the_settings, screen):
    screen.fill((0, 0, 0))
    display_text('Press:', screen, 100, 100)
    display_text('Difficulty: [E]asy, [N]ormal, [H]ard? {0}'.format(get_difficulty(the_settings)), screen, 100, 200)
    display_text('Lives: {0} [up] or [down]'.format((the_settings.ship_limit + 1)), screen, 100, 300)
    display_text('Enable Super [B]ullet? {0}'.format(the_settings.super_bullet), screen, 100, 400)
    display_text('[M]ain Menu', screen, 100, 500)
    display_text('[Q]uit Game', screen, 100, 600)
    pygame.display.flip()


def get_difficulty(the_settings):
    if the_settings.bullets_allowed == 100:
        return 'Easy'
    elif the_settings.alien_speed_factor == 1:
        return 'Normal'
    else:
        return 'Hard'


def display_score(the_settings, stats, screen):
    if the_settings.game_active:
        display_text('Score: {0}'.format(stats.score), screen, 10, 10)


def display_game_over(stats, screen):
    screen.fill((0, 0, 0))
    display_text('The aliens won!', screen, 100, 100, 50, (0, 255, 64))
    display_text('Nice work! You scored {0} points!'.format(stats.score), screen, 100, 200)
    display_text('Press:', screen, 100, 300)
    display_text('[N]ew Game', screen, 100, 400)
    display_text('[M]ain Menu', screen, 100, 500)
    pygame.display.flip()


def display_text(text, screen, x, y, size=30, color=(255, 255, 255), font='fonts/OpenSans-Regular.ttf'):
    try:
        text = str(text)
        font = pygame.font.Font(font, size)
        text = font.render(text, True, color)
        screen.blit(text, (x, y))
    except Exception as e:
        print('Exception details: {}'.format(e))
        raise e


# Game Methods
def update_screen(the_settings, stats, screen, ship, aliens, bullets):
    """Update images on the screen and render a new screen"""
    if the_settings.game_active:
        screen.fill(the_settings.bg_color)  # Set the background color
        # Redraw bullets before ship and aliens
        for bullet in bullets.sprites():
            bullet.draw_bullet()
        ship.blitme()  # Add the ship
        aliens.draw(screen)  # Add the aliens
        display_score(the_settings, stats, screen)
    elif the_settings.game_over_active:
        display_game_over(stats, screen)
    pygame.display.flip()  # Show the most recently drawn screen


def create_fleet(the_settings, screen, ship, aliens):
    """Create a full fleet of aliens"""
    # Create one alien and use the size to determine number of aliens
    alien = Alien(the_settings, screen)
    number_aliens_x = get_number_aliens_x(the_settings, alien.rect.width)
    number_rows = get_number_rows(the_settings, alien.rect.height, ship.rect.height)

    # Create fleet of aliens
    for row_number in range(number_rows):
        # Create a row of aliens
        for alien_number in range(number_aliens_x):
            create_alien(the_settings, screen, aliens, alien_number, row_number)


def get_number_aliens_x(the_settings, alien_width):
    available_space_x = the_settings.screen_width - alien_width
    return int(available_space_x / (1.5 * alien_width))


def get_number_rows(the_settings, alien_height, ship_height):
    available_space_y = the_settings.screen_height - 3 * alien_height - ship_height
    return int(available_space_y / (2 * alien_height))


def create_alien(the_settings, screen, aliens, alien_number, row_number):
    alien = Alien(the_settings, screen)
    alien_width = alien.rect.width
    alien.x = (0.5 * alien_width) + 1.5 * alien_width * alien_number
    alien.rect.x = int(alien.x)
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def update_bullets(the_settings, stats, screen, ship, bullets, aliens):
    """Update the location of the bullets and remove any that are no longer visible"""
    bullets.update()
    check_collisions(the_settings, stats, screen, ship, bullets, aliens)
    # Remove bullets that have left the screen
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)


def check_collisions(the_settings, stats, screen, ship, bullets, aliens):
    # Check for bullets that hit aliens, then remove alien and, optionally, bullet
    collisions = pygame.sprite.groupcollide(bullets, aliens, not (the_settings.super_bullet), True)
    if len(collisions):
        stats.score += 100
    if len(aliens) == 0:
        # Destroy bullets and create a new fleet
        bullets.empty()
        create_fleet(the_settings, screen, ship, aliens)


def fire_bullets(the_settings, screen, ship, bullets):
    """Fire a bullet if the limit is not yet reached"""
    if len(bullets) < the_settings.bullets_allowed:
        bullets.add(Bullet(the_settings, screen, ship))


def update_aliens(the_settings, stats, screen, ship, aliens, bullets):
    """Check if a member of the fleet is at the edge of the screen"""
    check_fleet_edges(the_settings, aliens)
    """Update the positions of all aliens in the fleet"""
    aliens.update()
    # Check for alien-ship collisions
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(the_settings, stats, screen, ship, aliens, bullets)
    check_aliens_bottom(the_settings, stats, screen, ship, aliens, bullets)


def check_fleet_edges(the_settings, aliens):
    """Respond appropriately if aliens have reached the edge of the screen"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(the_settings, aliens)
            break


def change_fleet_direction(the_settings, aliens):
    """Drop the fleet down and change direction"""
    for alien in aliens.sprites():
        alien.rect.y += the_settings.fleet_drop_speed
    the_settings.fleet_direction *= -1


def ship_hit(the_settings, stats, screen, ship, aliens, bullets):
    """Respond to ship being hit by an alien"""
    if stats.ships_left > 0:
        stats.ships_left -= 1  # Decrement number of ships left
        aliens.empty()  # Remove all aliens
        bullets.empty()  # Remove all bullets

        create_fleet(the_settings, screen, ship, aliens)  # Create a new fleet
        ship.center_ship()  # Center the ship at the bottom of the screen

        sleep(0.5)  # Pause
    else:
        the_settings.game_active = False
        the_settings.game_over_active = True
        screen.fill((0, 0, 0))


def check_aliens_bottom(the_settings, stats, screen, ship, aliens, bullets):
    """Check to see if any aliens have reached the bottom of the screen"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(the_settings, stats, screen, ship, aliens, bullets)
            break
