import pygame.font
from pygame.sprite import Group
from ship import Ship

class Scoreboard():
    def __init__(self, ai_settings, screen, stats):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        self.prepScore()
        self.prepHighScore()
        self.prepLevel()
        self.prepShips()

    # sets score
    def prepScore(self):
        roundedScore = int(round(self.stats.score, -1))
        strScore = "{:,}".format(roundedScore)
        if self.stats.normalLevel:
            self.score_image = self.font.render(strScore, True, self.text_color, self.ai_settings.bgColor)
        else:
            self.score_image = self.font.render(strScore, True, self.text_color, self.ai_settings.bg1Color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    # sets high score
    def prepHighScore(self):
        highScore = int(round(self.stats.highScore, -1))
        strHighScore = "{:,}".format(highScore)
        if self.stats.normalLevel:
            self.highScore_image = self.font.render(strHighScore, True, self.text_color, self.ai_settings.bgColor)
        else:
            self.highScore_image = self.font.render(strHighScore, True, self.text_color, self.ai_settings.bg1Color)

        self.highScore_rect = self.highScore_image.get_rect()
        self.highScore_rect.centerx = self.screen_rect.centerx
        self.highScore_rect.top = self.score_rect.top

    # sets level
    def prepLevel(self):
        if self.stats.normalLevel:
            self.level_image = self.font.render(str(self.stats.level), True, self.text_color, self.ai_settings.bgColor)
        else:
            self.level_image = self.font.render(str(self.stats.level), True, self.text_color, self.ai_settings.bg1Color)

        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    # sets lives left (ship images)
    def prepShips(self):
        self.ships = Group()
        for x in range(self.stats.ships_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = 10 + x * ship.rect.width
            ship.rect.y = 0
            self.ships.add(ship)

    # score, high score, lives left
    def showScore(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.highScore_image, self.highScore_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)
        
