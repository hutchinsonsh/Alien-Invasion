import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    def __init__(self, ai_settings, screen, ship, direction):
        super(Bullet, self).__init__()
        # basics for the bullets
        self.screen = screen
        self.direction = direction
        self.color = ai_settings.bulletColor
        self.speed = ai_settings.bulletSpeed

        # sets the bullets to appear next to the spaceship
        self.rect = pygame.Rect(0, 0, ai_settings.bulletWidth, ai_settings.bulletHeight)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        self.y = float(self.rect.y)
        self.x = float(self.rect.x)

    # updates bullet every iteration in the direction it was fired
    def update(self, direction):
        # moves the bullet in the direction it was fired from
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

