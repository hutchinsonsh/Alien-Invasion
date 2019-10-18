class Settings():
    def __init__(self):
        # basics
        self.screenWidth = 1200
        self.screenHeight = 750
        self.bgColor = (240, 100, 100)
        self.bg1Color = (255, 171, 153)

        # for the ship
        self.shipLimit = 3

        # for the bullet
        self.bulletWidth = 3
        self.bulletHeight = 15
        self.bulletColor = 60, 109, 127
        self.bulletNums = 5

        # for the aliens
        self.dropDown = 20

        # for the queenBeeBullet
        self.beeBulletColor = 28, 175, 161
        self.beeBulletSpeed = 9

        # for the game
        self.speedScale = 1.1
        self.scoreScale = 1.5
        self.initDynamicSettings()

    # initializes variables that change
    def initDynamicSettings(self):
        self.shipSpeed = 4
        self.bulletSpeed = 4
        self.alienSpeed = 3
        self.alienPoints = 50
        self.fleetDirection = 1
        self.num1 = 1

    # increases speed each level
    def increaseSpeed(self):
        self.shipSpeed *= self.speedScale
        self.bulletSpeed *= self.speedScale
        self.alienSpeed *= self.speedScale
        self.alienPoints = int(self.alienPoints * self.scoreScale)
        
