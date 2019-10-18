import sys
import pygame
import random
from time import sleep
from bullet import Bullet
from alien import Alien
from button import Button
from queenBee import QueenBee
from queenBeeBullet import QueenBeeBullet

# sets direction of the bullet/determines movement
direction1 = ''
direction2 = ''


# updates screen
def updateScreen(ai_settings, screen, stats, sb,  ship, bullets, aliens, queenBee, queenBeeBullets, playButton, resumeButton):
    # for showing the level/game over sign
    if stats.waitPlease:
        stats.levelUp = False
        stats.gameActive = True
        stats.waitPlease = False
        pygame.time.wait(1000)

    # sets the color of the screen
    if stats.normalLevel:
        screen.fill(ai_settings.bgColor)
    else:
        screen.fill(ai_settings.bg1Color)

    # updates the bullets, ship, aliens, and score if playing game
    for bullet in bullets.sprites():
        bullet.drawBullet()
    for bullet in queenBeeBullets.sprites():
        bullet.drawBullet()
    ship.blitme()
    aliens.draw(screen)
    sb.showScore()

    # check for bonus level
    if stats.level % stats.bonusLevel == 0:
        stats.normalLevel = False
        queenBee.draw(screen)
    if stats.level % stats.bonusLevel != 0:
        stats.normalLevel = True

    # updates play button, if not already  playing; shows play, resume, and level up message
    if not stats.gameActive and not stats.alreadyPlaying and not stats.showInstructions and not stats.gameOverBool:
        playButton.drawButton()
    if not stats.gameActive and not stats.alreadyPlaying and not stats.showInstructions and stats.gameOverBool:
        gameOverMsg = "Game Over"
        gameOverMsg = Button(ai_settings, screen, gameOverMsg, 300, 50, 0)
        gameOverMsg.drawButton()
        stats.waitPlease = True
    if not stats.gameActive and stats.alreadyPlaying and not stats.levelUp and not stats.showInstructions:
        resumeButton.drawButton()
    if not stats.gameActive and stats.alreadyPlaying and stats.levelUp and not stats.showInstructions and stats.normalLevel:
        levelMsg = "Level " + str(stats.level)
        levelMsg2 = Button(ai_settings, screen, levelMsg, 300, 50, 0)
        levelMsg2.drawButton()
        stats.waitPlease = True
    if not stats.gameActive and stats.alreadyPlaying and stats.levelUp and not stats.showInstructions and not stats.normalLevel:
        levelMsg = "Bonus Round"
        levelMsg2 = Button(ai_settings, screen, levelMsg, 300, 50, 0)
        levelMsg2.drawButton()
        stats.waitPlease = True

    # for instruction page
    if stats.showInstructions:
        instruction1 = "Q = quit"
        instruction2 = "I = instructions"
        instruction3 = "P = pause"
        doneInst = "Done"
        instMsg1 = Button(ai_settings, screen, instruction1, 550, 50, 3)
        instMsg2 = Button(ai_settings, screen, instruction2, 550, 50, 1)
        instMsg3 = Button(ai_settings, screen, instruction3, 550, 50, 2)
        doneInstMsg = Button(ai_settings, screen, doneInst, 550, 50, 0)
        instMsg1.drawButton()
        instMsg2.drawButton()
        instMsg3.drawButton()
        doneInstMsg.drawButton()

    if stats.levelUp:
        sb.prepLevel()
        sb.prepHighScore()
        sb.prepScore()


    # shows whatever was updated
    pygame.display.flip()


# makes the bullet move in a direction/removes it once it's off screen
def updateBullets(ai_settings, screen, stats, sb, ship, aliens, bullets, queenBee, playButton, queenBeeBullets, direction=direction1):
    bullets.update(direction)
    checkCollision(ai_settings, screen, stats, sb, ship, aliens, bullets, queenBee, queenBeeBullets, playButton)
    # removes the bullet if it is out of range
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
        if bullet.rect.x <= 0:
            bullets.remove(bullet)
        if bullet.rect.bottom >= 750:
            bullets.remove(bullet)
        if bullet.rect.x >= 1200:
            bullets.remove(bullet)


# updates the fired bullets- moves in direction fired
def updateQueenBeeBullets(ai_settings, screen, stats, sb, ship, aliens, bullets, queenBee, playButton, queenBeeBullets):
    queenBeeBullets.update()
    checkBeeBulletShipCollision(ai_settings, screen, stats, sb, ship, aliens, bullets, queenBee, queenBeeBullets)
    if not stats.normalLevel:
        for x in queenBeeBullets.copy():
            if x.rect.bottom <= 0:
                bullets.remove(x)
            if x.rect.x <= 0:
                bullets.remove(x)
            if x.rect.bottom >= 750:
                bullets.remove(x)
            if x.rect.x >= 1200:
                bullets.remove(x)


# checks the direction of the ufo/moves fleet left/right, down; checks if ship hits alien fleet
def updateAliens(ai_settings, screen, stats, sb, ship, aliens, bullets, queenBee, queenBeeBullets):
    checkFleetEdge(ai_settings, aliens)

    # collision between ship and alien/treats it as though the ship had been hit(reusing code)
    if pygame.sprite.spritecollideany(ship, aliens):
        shipHit(ai_settings, screen, stats, sb, ship, aliens, bullets, queenBee, queenBeeBullets)

    alienReachBottom(ai_settings, screen, stats, sb, ship, aliens, bullets, queenBee, queenBeeBullets)
    aliens.update()


# creates bullets for queen bee
def createBeeBullets(ai_settings, screen, queenBee, queenBeeBullets, direction2):
    new_bullet = QueenBeeBullet(ai_settings, screen, queenBee, direction2)
    queenBeeBullets.add(new_bullet)


# creates a new bullet if bullenNum not max and adds it to 'bullets'
def fireBullet(ai_settings, screen, ship, bullets, direction):
    if len(bullets) < ai_settings.bulletNums:
        new_bullet = Bullet(ai_settings, screen, ship, direction)
        bullets.add(new_bullet)


# drops the fleet down/changes the direction the aliens
def changeFleetDirection(ai_settings, aliens):
    for x in aliens.sprites():
        x.rect.y += ai_settings.dropDown
    ai_settings.fleetDirection *= -1


# checks if ship hits ufo, if yes: resets game/takes off one life
# also checks num of ships left/exits game if 0
# ends game if num of ships left is 0
def shipHit(ai_settings, screen, stats, sb, ship, aliens, bullets, queenBee, queenBeeBullets):
    if stats.ships_left > 0 and stats.normalLevel:
        stats.ships_left -= 1
        ship.centerShip()
        bullets.empty()
        sb.prepShips()
        aliens.empty()
        createFleet(ai_settings, screen, stats, sb, ship, aliens)
        num1 = 0
        sleep(.5)
    elif stats.ships_left > 0 and not stats.normalLevel:
        stats.ships_left -= 1
        ship.centerShip()
        queenBeeBullets.empty()
        bullets.empty()
        sb.prepShips()
        queenBee.empty()
        bee = QueenBee(ai_settings, screen)
        queenBee.add(bee)
        stats.beeDefeated()
    else:
        if not stats.gameOverBool:
            stats.gameOverBool = True
        elif stats.gameOverBool:
            stats.gameOverBool = False
        stats.gameActive = False
        stats.alreadyPlaying = False
        pygame.mouse.set_visible(True)


# checks to make sure aliens haven't reached the bottom of the screen/ restarts game if they have
def alienReachBottom(ai_settings, screen, stats, sb, ship, aliens, bullets, queenBee, queenBeeBullets):
    screen_rect = screen.get_rect()
    for x in aliens.sprites():
        if x.rect.bottom >= screen_rect.bottom:
            shipHit(ai_settings, screen, stats, sb, ship, aliens, bullets, queenBee, queenBeeBullets)
            break


# calculates how many rows of ufos there are
def getRowNum(ai_settings, stats, sb, shipHeight, alienHeight):
    if stats.level < 10:
        numRows = stats.level
    else:
        numRows = 10
    return numRows


# calculates how many aliens can fit in a row
def getAlienNum(ai_settings, alienWidth):
    avalSpace = ai_settings.screenWidth - 2 * alienWidth
    numAlienx = int(avalSpace / (2 * alienWidth))
    return numAlienx


# creates a single alien/ adds it to Alien instance
def createAlien(ai_settings, screen, aliens, alienNum, rowNum):
    alien = Alien(ai_settings, screen)
    alienWidth = alien.rect.width
    alien.x = alienWidth + (2 * alienWidth * alienNum)
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height - 2 * alien.rect.height * rowNum
    aliens.add(alien)


# brings gerRowNum and getAlienNum together / creates rows of individual ufos
def createFleet(ai_settings, screen, stats, sb, ship, aliens):
    alien = Alien(ai_settings, screen)
    alienNum = getAlienNum(ai_settings, alien.rect.width)
    rowNum = getRowNum(ai_settings, stats, sb, ship.rect.height, alien.rect.height)
    for y in range(rowNum):
        for x in range(alienNum):
            createAlien(ai_settings, screen, aliens, x, y)


# checks if the fleet has reached the edge of the screen/changes direction if true
def checkFleetEdge(ai_settings, aliens):
    for x in aliens.sprites():
        if x.checkEdge():
            changeFleetDirection(ai_settings, aliens)
            break


# checks collisions between bullets and queen during bonus level; also checks collisions between queenBee and ship
def checkQueenCollisions(ai_settings, screen, stats, sb, ship, aliens, bullets, queenBee, queenBeeBullets):
    move1 = 0
    move2 = 0
    effect = pygame.mixer.Sound('audioFiles/bomb.wav')

    # to slow down the speed of the bee- so that it doesnt change directions every update
    if stats.framesPassed >= 25:
        stats.resetSpeedOfBee()
        stats.setXDirectionOfBee()
        stats.setYDirectionOfBee()
        num1 = random.randint(0, 3)
        if num1 == 0:
            direction2 = 'left'
        elif num1 == 1:
            direction2 = 'right'
        elif num1 == 2:
            direction2 = 'up'
        elif num1 == 3:
            direction2 = 'down'
        createBeeBullets(ai_settings, screen, queenBee, queenBeeBullets, direction2)
    elif stats.framesPassed < 25:
        stats.increaseSpeedOfBee()
    move1 = stats.xDirectionOfBee()
    move2 = stats.yDirectionOfBee()

    # to check how many times the bee has been hit; if hit 5 times- ends bonus round
    queenBee.update(move1, move2, stats)
    collisions2 = pygame.sprite.groupcollide(bullets, queenBee, True, False)
    # level over once queenBee is hit 4 times
    if collisions2 and stats.beeHits == 4:
        effect.play()
        createFleet(ai_settings, screen, stats, sb, ship, aliens)
        stats.level += 1
        ship.centerShip()

        stats.alreadyPlaying = True
        stats.gameActive = False
        stats.levelUp = True
        stats.beeDefeated()
        stats.resetSpeedOfBee()

        bullets.empty()
        queenBeeBullets.empty()
        queenBee.empty()

    # beeHit < 4- checks points/adds for each hit
    if collisions2 and stats.beeHits < 4:
        effect.play()
        stats.updateBeeHits()
        stats.score += 100 * stats.level
        sb.prepScore()
        checkHighScore(stats, sb)

    if pygame.sprite.spritecollideany(ship, queenBee):
        effect.play()
        shipHit(ai_settings, screen, stats, sb, ship, aliens, bullets, queenBee, queenBeeBullets)
        stats.updateBeeHits()


# checks any collisions between the ship and the bee's bullets
def checkBeeBulletShipCollision(ai_settings, screen, stats, sb, ship, aliens, bullets, queenBee, queenBeeBullets):
    collisions = pygame.sprite.spritecollideany(ship, queenBeeBullets)
    effect = pygame.mixer.Sound('audioFiles/bomb.wav')
    if collisions:
        effect.play()
        shipHit(ai_settings, screen, stats, sb, ship, aliens, bullets, queenBee, queenBeeBullets)


# checks collision between ufo and bullets; if all ufo's gone- restarts game, adds collision to score
def checkCollision(ai_settings, screen, stats, sb, ship, aliens, bullets, queenBee, queenBeeBullets, playButton):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    effect = pygame.mixer.Sound('audioFiles/bomb.wav')

    # plays sound effect, sets high score
    if collisions and (stats.level % stats.bonusLevel != 0):
        effect.play()
        for x in collisions.values():
            stats.score += ai_settings.alienPoints * len(x)
            sb.prepScore()
        checkHighScore(stats, sb)

    # all ufos gone- restarts game/level added/increases speed
    if len(aliens) == 0 and ((stats.level + 1) % stats.bonusLevel != 0) and stats.normalLevel:
        bullets.empty()
        ai_settings.increaseSpeed()

        stats.level += 1
        sb.prepLevel()
        sb.prepScore()
        sb.prepHighScore()

        stats.alreadyPlaying = True
        stats.gameActive = False
        stats.levelUp = True

        ship.centerShip()
        createFleet(ai_settings, screen, stats, sb, ship, aliens)

    # for level before bonus level- sets up game
    elif len(aliens) == 0 and ((stats.level + 1) % stats.bonusLevel == 0 or stats.level == 1) and stats.normalLevel:
        bee = QueenBee(ai_settings, screen)
        queenBee.add(bee)
        bullets.empty()
        ai_settings.increaseSpeed()

        stats.alreadyPlaying = True
        stats.gameActive = False
        stats.levelUp = True
        stats.level += 1

        sb.prepLevel()
        sb.prepScore()
        sb.prepHighScore()

        ship.centerShip()

    # for bonus level
    elif len(aliens) == 0 and (stats.level % stats.bonusLevel == 0):
        checkQueenCollisions(ai_settings, screen, stats, sb, ship, aliens, bullets, queenBee, queenBeeBullets)


# replaces high score if beaten
def checkHighScore(stats, sb):
    if stats.score > stats.highScore:
        stats.highScore = stats.score
        sb.prepHighScore()


# for play button, once clicked- makes mouse disappear, resets level to 1/starts game
def checkPlayButton(ai_settings, screen, stats, sb, playButton, ship, aliens, bullets, mouseX, mouseY, queenBee, queenBeeBullets):
    buttonClicked = playButton.rect.collidepoint(mouseX, mouseY)
    # for resetting the game/user presses 'play'
    if buttonClicked and not stats.gameActive and not stats.alreadyPlaying and not stats.showInstructions:
        gameOver(ai_settings, screen, stats, sb, ship, aliens, bullets, queenBee, queenBeeBullets)

    # for if user presses 'resume'
    if buttonClicked and not stats.gameActive and not stats.showInstructions:
        stats.gameActive = True
        pygame.mouse.set_visible(False)

    # for if user presses 'done with instructions'
    if buttonClicked and not stats.gameActive:
        stats.gameActive = True
        stats.showInstructions = False
        pygame.mouse.set_visible(False)


# when a key is pressed down, moves the ship/bullet in that direction
# q = quit, p = pause, makes mouse visable again
def checkKeyDown(event, ai_settings, screen, stats, sb, ship, aliens, bullets, queenBee, queenBeeBullets):
    effect = pygame.mixer.Sound('audioFiles/pew pew.wav')
    if event.key == pygame.K_RIGHT:
        ship.movingRight = True
    elif event.key == pygame.K_LEFT:
        ship.movingLeft = True
    elif event.key == pygame.K_UP:
        ship.movingUp = True
    elif event.key == pygame.K_DOWN:
        ship.movingDown = True

    # checks if bullets can be created/moves them across the screen
    if event.key == pygame.K_w and len(bullets) < ai_settings.bulletNums:
        fireBullet(ai_settings, screen, ship, bullets, 'up')
        direction1 = 'up'
        effect.play()
    elif event.key == pygame.K_a and len(bullets) < ai_settings.bulletNums:
        fireBullet(ai_settings, screen, ship, bullets, 'left')
        direction1 = 'left'
        effect.play()
    elif event.key == pygame.K_d and len(bullets) < ai_settings.bulletNums:
        fireBullet(ai_settings, screen, ship, bullets, 'right')
        direction1 = 'right'
        effect.play()
    elif event.key == pygame.K_s and len(bullets) < ai_settings.bulletNums:
        fireBullet(ai_settings, screen, ship, bullets, 'down')
        direction1 = 'down'
        effect.play()

    # if user presses 'p' and 'p' had already been pressed
    if event.key == pygame.K_p and stats.gameActive == False and not stats.gameOverBool:
        stats.gameActive = True
        stats.alreadyPlaying = True
        pygame.mouse.set_visible(False)
    elif event.key == pygame.K_p and stats.gameActive == False and stats.gameOverBool:
        gameOver(ai_settings, screen, stats, sb, ship, aliens, bullets, queenBee, queenBeeBullets)
    elif event.key == pygame.K_p and stats.gameActive == True:
        stats.alreadyPlaying = True
        stats.gameActive = False
        pygame.mouse.set_visible(True)

    # for instruction page
    if event.key == pygame.K_i and stats.gameActive and not stats.showInstructions:
        stats.gameActive = False
        stats.showInstructions = True
        pygame.mouse.set_visible(True)
    elif event.key == pygame.K_i:
        stats.gameActive = True
        pygame.mouse.set_visible(False)
        stats.showInstructions = False

    # to exit the game
    if event.key == pygame.K_q:
        sys.exit()


# stops movement of the ship
def checkKeyUp(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.movingRight = False
    elif event.key == pygame.K_LEFT:
        ship.movingLeft = False
    elif event.key == pygame.K_UP:
        ship.movingUp = False
    elif event.key == pygame.K_DOWN:
        ship.movingDown = False


# checks user events (key downs /key ups/ mouse clicks/ button presses)
def checkEvents(ai_settings, screen, stats, sb, playButton, ship, aliens, bullets, queenBee, queenBeeBullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            checkKeyDown(event, ai_settings, screen, stats, sb, ship, aliens, bullets, queenBee, queenBeeBullets)
        elif event.type == pygame.KEYUP:
            checkKeyUp(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = pygame.mouse.get_pos()
            checkPlayButton(ai_settings, screen, stats, sb, playButton, ship, aliens, bullets, mouseX, mouseY, queenBee, queenBeeBullets)


# resets all the stats/levels
def gameOver(ai_settings, screen, stats, sb, ship, aliens, bullets, queenBee, queenBeeBullets):
    ai_settings.initDynamicSettings()
    pygame.mouse.set_visible(False)
    stats.resetStats()
    stats.beeDefeated()
    stats.resetSpeedOfBee()
    stats.gameActive = True

    stats.setXDirectionOfBee()
    stats.setYDirectionOfBee()

    stats.gameOverBool = False
    stats.normalLevel = True

    sb.prepScore()
    sb.prepHighScore()
    sb.prepLevel()
    sb.prepShips()

    aliens.empty()
    bullets.empty()

    queenBee.empty()
    queenBeeBullets.empty()

    ship.centerShip()
    createFleet(ai_settings, screen, stats, sb, ship, aliens)


