import pygame
from pygame.sprite import Sprite


class Ship:
    def __init__(self, the_settings, screen):
        """Initialize the ship and set starting position"""
        self.screen = screen
        self.the_settings = the_settings

        # Load ship image
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Start each new ship at the bottom center
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.center = float(self.rect.centerx)

        # Initialize the movement flags to false
        self.moving_right = False
        self.moving_left = False

    def blitme(self):
        """Draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """Update the ship's position based on movement flag"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.the_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.the_settings.ship_speed_factor
        # Update the rect object using self.center
        self.rect.centerx = self.center

    def center_ship(self):
        """Center the ship on the screen"""
        self.center = self.screen_rect.centerx


class Bullet(Sprite):
    """A class to manage bullets fired from the ship"""

    def __init__(self, the_settings, screen, ship):
        """Create bullet object at ship's current position"""
        super(Bullet, self).__init__()
        self.screen = screen

        # Create a bullet rect at ship's position
        self.rect = pygame.Rect(ship.rect.centerx, ship.rect.top, the_settings.bullet_width, the_settings.bullet_height)
        self.y = float(self.rect.y)
        self.color = the_settings.bullet_color
        self.speed_factor = the_settings.bullet_speed_factor

    def update(self):
        """Move the bullet up the screen"""
        self.y -= self.speed_factor
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet to the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)


class Alien(Sprite):
    """A class to represent a single alien in the fleet"""

    def __init__(self, the_settings, screen):
        """Initialize an alien and set starting position"""
        super(Alien, self).__init__()
        self.screen = screen
        self.the_settings = the_settings

        # Load alien image and set rect
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # Starting position is near top left of screen
        self.rect.x = int(self.rect.width / 2)
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)

    def blitme(self):
        """Draw alien at current location"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """Move the alien to the right or left"""
        self.x += (self.the_settings.alien_speed_factor * self.the_settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        """Return True if alien is at the edge of screen"""
        screen_rect = self.screen.get_rect()
        return self.rect.right >= screen_rect.right or self.rect.left <= 0
