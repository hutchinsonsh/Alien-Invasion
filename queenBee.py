import pygame
from pygame.sprite import Sprite

class QueenBee(Sprite):
    def __init__(self, ai_settings, screen):
        super(QueenBee, self).__init__()
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings

        # loads pic of queenBee
        self.image = pygame.image.load('pic/queenBee.png.bmp.png')
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()

        self.rect.centerx = self.screen_rect.centerx
        self.rect.top = self.screen_rect.top + 60


        self.x = float(self.rect.x)
        self.y = float(self.rect.y)


    def update(self, move1, move2, stats):
        screen_rect1 = self.screen.get_rect()
        # moves the queen bee in a random direction
        if self.rect.right >= screen_rect1.right:
            stats.framesPassed = 25
            self.x += 1 * move1 * -1
        elif self.rect.left <= 0:
            stats.framesPassed = 25
            self.x += 1 * move1 * -1
        else:
            self.x += 1 * move1
        self.rect.x = self.x

        if self.rect.top < self.screen_rect.top:
            stats.framesPassed = 25
            self.y += move2 * -1
        elif self.rect.bottom > self.screen_rect.bottom:
            stats.framesPassed = 25
            self.y += move2 * -1
        else:
            self.y += move2
        self.rect.y = self.y

    # shows image of the ufo
    def blitme(self):
        self.screen.blit(self.image, self.rect)
        
        
