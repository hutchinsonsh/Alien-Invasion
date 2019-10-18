import pygame
from pygame.sprite import Sprite


class QueenBeeBullet(Sprite):
    def __init__(self, ai_settings, screen, queenBee, direction):
        super(QueenBeeBullet, self).__init__()

        # basics for the bullets
        self.screen = screen
        self.direction = direction
        self.color = ai_settings.beeBulletColor
        self.speed = ai_settings.beeBulletSpeed

        # sets the bullets to appear next to the spaceship
        self.rect = pygame.Rect(0, 0, ai_settings.bulletWidth, ai_settings.bulletHeight)

        for x in queenBee:
            self.rect.centerx = x.rect.centerx
            self.rect.top = x.rect.bottom

        self.y = float(self.rect.y)
        self.x = float(self.rect.x)


    # updates bullet every iteration in the direction it was fired
    def update(self):
        if self.direction == 'up':
            self.y -= self.speed
            self.rect.y = self.y
        if self.direction == 'down':
            self.y += self.speed
            self.rect.y = self.y
        if self.direction == 'left':
            self.x -= self.speed
            self.rect.x = self.x
        if self.direction == 'right':
            self.x += self.speed
            self.rect.x = self.x


    # shows update from bullet update
    def drawBullet(self):
        # shows the bullet on the gaming screen
        pygame.draw.rect(self.screen, self.color, self.rect)


