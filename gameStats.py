import random

class GameStats():
    def __init__(self, ai_settings):
        self.ai_settings = ai_settings
        self.resetStats()
        self.gameActive = False
        self.alreadyPlaying = False
        self.levelUp = False
        self.waitPlease = False
        self.showInstructions = False

        # for the queenBee level
        self.normalLevel = True
        self.isDead = False
        self.bonusLevel = 2

        self.highScore = 0

        self.gameOverBool = False

    # for when user restarts game
    def resetStats(self):
        self.ships_left = self.ai_settings.shipLimit
        self.score = 0
        self.level = 1

    def updateBeeHits(self):
        self.beeHits += 1

    def beeDefeated(self):
        self.beeHits = 0;

    def increaseSpeedOfBee(self):
        self.framesPassed += 1

    def resetSpeedOfBee(self):
        self.framesPassed = 0

    def setSpeedOfBee(self):
        self.framesPassed = random.randint(10, 30)
        print(self.framesPassed)

    def getSpeedOfBee(self):
        return self.framesPassed

    def setXDirectionOfBee(self):
        self.move1 = random.randint(-5, 5)

    def setYDirectionOfBee(self):
        self.move2 = random.randint(-5, 5)

    def xDirectionOfBee(self):
        return self.move1

    def yDirectionOfBee(self):
        return self.move2
