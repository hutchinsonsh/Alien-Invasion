import pygame
from pygame.sprite import Sprite

class Ship(Sprite):

    def __init__(self, ai_settings, screen):
        super(Ship, self).__init__()

        self.screen = screen
        self.ai_settings = ai_settings

        # gets image of the spaceship/fits screen
        self.image = pygame.image.load('pic/spaceship2.bmp.png')
        self.image = pygame.transform.scale(self.image, (70, 125))
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # sets starting position for the spaceship
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # for making border
        self.center = float(self.rect.centerx)
        self.center2 = float(self.rect.bottom)

        # sets these as false so spaceship only moves when button is pressed
        self.movingRight = False
        self.movingLeft = False
        self.movingUp = False
        self.movingDown = False

    # after the ship hits an alien, it re-centers the ship
    def centerShip(self):
        self.center = self.screen_rect.centerx
        self.center2 = self.screen_rect.bottom

    # updates ship if user moves it
    def update(self):
        # makes the spaceship move up/down, left/right
        if self.movingRight and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.shipSpeed
        elif self.movingLeft and self.rect.left > 0:
            self.center -= self.ai_settings.shipSpeed
        elif self.movingUp and self.rect.top > self.screen_rect.top:
            self.center2 -= self.ai_settings.shipSpeed
        elif self.movingDown and self.rect.bottom < self.screen_rect.bottom:
            self.center2 += self.ai_settings.shipSpeed

        # sets image to the right position
        self.rect.centerx = self.center
        self.rect.bottom = self.center2

    # draws ship after update
    def blitme(self):
        # reflects image on screen after the changes are made
        self.screen.blit(self.image, self.rect)
        
