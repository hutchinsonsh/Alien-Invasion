import sys
import pygame
import gameFunction as gf
from pygame.sprite import Group
from settings import Settings
from ship import Ship
from button import Button
from gameStats import GameStats
from scoreboard import Scoreboard
from queenBee import QueenBee
from alien import Alien


def runGame():
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screenWidth, ai_settings.screenHeight))
    pygame.display.set_caption("Alien Invasion")
    ship = Ship(ai_settings, screen)
    aliens = Group()
    bullets = Group()
    queenBees = Group()
    queenBullets = Group()
    stats = GameStats(ai_settings)

    sb = Scoreboard(ai_settings, screen, stats)
    gf.createFleet(ai_settings, screen, stats, sb, ship, aliens)

    playButton = Button(ai_settings, screen, "Play", 200, 50, 0)
    resumeButton = Button(ai_settings, screen, "Resume Game", 250, 50, 0)

    pygame.mixer.music.load('audioFiles/were going on a trip.wav')
    pygame.mixer.music.play(-1)

    # updates game every run through
    while True:
        gf.checkEvents(ai_settings, screen, stats, sb, playButton, ship, aliens, bullets, queenBees, queenBullets)
        if stats.gameActive:
            ship.update()
            gf.updateAliens(ai_settings, screen, stats, sb, ship, aliens, bullets, queenBees, queenBullets)
            gf.updateBullets(ai_settings, screen, stats, sb, ship, aliens, bullets, queenBees, playButton, queenBullets)
            gf.updateQueenBeeBullets(ai_settings, screen, stats, sb, ship, aliens, bullets, queenBees, playButton, queenBullets)

        gf.updateScreen(ai_settings, screen, stats, sb, ship, bullets, aliens, queenBees, queenBullets, playButton, resumeButton)

runGame()
