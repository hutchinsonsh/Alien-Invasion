import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    def __init__(self, ai_settings, screen):
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # loads pic of ufo
        self.image = pygame.image.load('pic/ufo.png.bmp.png')       //pic: seperate file for all pictures
        self.image = pygame.transform.scale(self.image, (75, 60))
        self.rect = self.image.get_rect()

        # start alien at top left
        self.rect.centerx = self.rect.centerx
        self.rect.bottom = self.rect.bottom + 10

        self.x = float(self.rect.x)

    # checks if the fleet reaches the left/right edge of the screen
    def checkEdge(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    # moves the alien fleet either 1 to the right or left
    def update(self):
        self.x += self.ai_settings.alienSpeed * self.ai_settings.fleetDirection
        self.rect.x = self.x

    # shows image of the ufo
    def blitme(self):
        self.screen.blit(self.image, self.rect)
