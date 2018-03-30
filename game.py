import sys
import os
sys.path.append(os.path.abspath('..'))

import pygame
from pygame.locals import *
import pyganim
import time
import math
import random

from Frozen import Frozen
from Hein import Hein
from Electro import Electro
from Firen import Firen
from Fireball import Fireball

from GameSettings import*
from GameGUI import*
pygame.init()

# display timer in the middle
def timerDisplay(screen, seconds):
    messageToScreen("Timer: %d" % seconds, textColor, screen, 0, timerDisplaceFromCenter)

# display scores in the middle
def displayScore(player1, player2):
    player1Score = player1.winRounds
    player2Score = player2.winRounds
    messageToScreen("%d : %d" % (player1.winRounds, player2.winRounds), 
                    textColor, screen, 0, scoreDisplaceFromCenter)

# load and blit static images on some position
def loadBlitImage(screen, position, folder, path):
    imageSurf = pygame.image.load(os.path.join(folder, path))
    imageSurf.convert()
    screen.blit(imageSurf, (position[0], position[1]))

# display players portrait
def displayPlayer(player, screen, position):
    folder = 'characterImages'
    if isinstance(player, Frozen):
        loadBlitImage(screen, position, folder, 'frozen/frozen_f.bmp')
    elif isinstance(player, Hein):
        loadBlitImage(screen, position, folder, 'hein/hein_f.bmp')  
    elif isinstance(player, Firen):
        loadBlitImage(screen, position, folder, 'firen/firen_f.bmp') 
    elif isinstance(player, Electro):
        loadBlitImage(screen, position, folder, 'electro/electro_f.bmp')

# display power bar for both players
def displayPowerBar(player, screen, barLeft, barTop):
    if player.power == fullPower: player.max = True
    else: player.max = False
    if player.power > fullPower:
        player.power = fullPower
    powerLeft = barLeft
    powerTop = barTop
    powerWidth = barWidth * player.power / 100
    powerHeight = barHeight
    if player.power == 0:
        pygame.draw.rect(screen, red, (barLeft, barTop, barWidth, barHeight))
        pass
    else:
        pygame.draw.rect(screen, red, (barLeft, barTop, barWidth, barHeight))
        pygame.draw.rect(screen, blue, (powerLeft, powerTop, powerWidth, powerHeight))

# display health bar both players
def displayHealthBar(player, screen, barLeft, barTop):
    if player.health <= fullHealth:
        damage = fullHealth - player.health
    else: damage = 0
    damageLeft = barLeft
    damageTop = barTop
    damageWidth = barWidth * damage / 100
    damageHeight = barHeight
    if damage == 0:
        pygame.draw.rect(screen, healthGreen, (barLeft, barTop, barWidth, barHeight))
        pass
    else:
        pygame.draw.rect(screen, healthGreen, (barLeft, barTop, barWidth, barHeight))
        pygame.draw.rect(screen, red, (damageLeft, damageTop, damageWidth, damageHeight))

# collision detection for players and enemies 
def rectanglesOverlap(x1, y1, w1, h1, x2, y2, w2, h2): 
    return not(y2 + h2 < y1 or\
               y2 > y1 + h1 or\
               x2 + w2 < x1 or\
               x2 > x1 + w1)

# used to detect collision with another player
def counterPlayer(player1, player2):
    x1, y1 = player1.x, player1.y
    x2, y2 = player2.x, player2.y
    return rectanglesOverlap(x1, y1, 45, 45, x2, y2, 45, 45)

# control player walking motion
def walkPlayer(player, currDirection):
    walkingDx, walkingDy = player.walkingDx, player.walkingDy
    if currDirection == 'up':
        if player.y - walkingDy < screenHeight / 2 - topMargin:
            player.y = screenHeight / 2 - topMargin
        else:
            player.y -= walkingDy
    elif currDirection == 'down':
        if player.y + walkingDy > screenHeight - bottomMargin:
            player.y = screenHeight - bottomMargin
        else:
            player.y += walkingDy
    elif currDirection == 'left':
        if player.x - walkingDx < leftMargin:
            player.x = leftMargin
        else:
            player.x -= walkingDx
    elif currDirection == 'right':
        if player.x + walkingDx > screenWidth - rightMargin:
            print("HhHh")
            player.x = screenWidth - rightMargin
        else:
            player.x += walkingDx

# control player running motion
def runPlayer(player, currDirection):
    runningDx, runningDy = player.runningDx, player.runningDy
    if currDirection == 'up':
        if player.y - runningDy < screenHeight / 2 - topMargin:
            player.y = screenHeight / 2 - topMargin
        else:
            player.y -= runningDy
    elif currDirection == 'down':
        if player.y + runningDy > screenHeight - bottomMargin:
            player.y = screenHeight - bottomMargin
        else:
            player.y += runningDy
    elif currDirection == 'left':
        if player.x - runningDx < leftMargin:
            player.x = leftMargin
        else:
            player.x -= runningDx
    elif currDirection == 'right':
        if player.x + runningDx > screenWidth - rightMargin:
            player.x = screenWidth - rightMargin
        else:
            player.x += runningDx

# in the battle mode, player1 battle with the other player
def counterToFreezeP1Move(player1, player2, player1CurrDirection):
    isCounter = False
    if counterPlayer(player1, player2):
    # counter -> block way effect
    # player1 to right, player2 on the right -> player1 unable to move forward
    # player1 to left, player2 on the left -> player1 unable to move forward
        if player1CurrDirection == 'right':
            if player2.x > player1.x and abs(player1.y - player2.y) < distanceToFreezeP1:
                isCounter = True
        elif player1CurrDirection == 'left':
            if player2.x < player1.x and abs(player1.y - player2.y) < distanceToFreezeP1:
                isCounter = True
    return isCounter

# in the battle mode, player2 battle with the other player
def counterToFreezeP2Move(player1, player2, player2CurrDirection):
    isCounter = False
    if counterPlayer(player1, player2):
    # counter -> block way effect
    # player2 to right, player1 on the right -> player2 unable to move forward
    # player2 to left, player1 on the left -> player2 unable to move forward
        if player2CurrDirection == 'right':
            if player1.x > player2.x and abs(player1.y - player2.y) < distanceToFreezeP2:
                isCounter = True
        elif player2CurrDirection == 'left':
            if player1.x < player2.x and abs(player1.y - player2.y) < distanceToFreezeP2:
                isCounter = True
    return isCounter

# play get hit animation when certain player get hit
def playGetHitAnim(player1, player2, screen):
    getHitAnim0 = player1.getHit()
    lgetHitAnim0 = player1.lgetHit()
    getHitAnim1 = player2.getHit()
    lgetHitAnim1 = player2.lgetHit()
    if player1.isGetHit: # player1 get hit
        if player1.isGetHit and faceRight(player1, player2):
            getHitAnim0.play()
            getHitAnim0.blit(screen, (player1.x, player1.y))
        else:
            lgetHitAnim0.play()
            lgetHitAnim0.blit(screen, (player1.x, player1.y))
    if player2.isGetHit: # player2 get hit
        if player2.isGetHit and not faceRight(player1, player2):
            getHitAnim1.play()
            getHitAnim1.blit(screen, (player2.x, player2.y))
        else:
            lgetHitAnim1.play()
            lgetHitAnim1.blit(screen, (player2.x, player2.y))

# make players react to battle motion
# player1 battle with player2
def battleWithPlayer(player1, player2, screen, currStatus1, currStatus2):
    player1.timerDelay += 1
    if currStatus1 == 'punch' or currStatus1 == 'kick':
        pygame.mixer.Sound.play(FaceHitSound)
        if currStatus2 == 'defense':
            pass
        elif currStatus2 == 'punch' or currStatus2 == 'kick':
            player2.isGetHit = True
            playGetHitAnim(player1, player2, screen)
            if player1.timerDelay % 20 == 0:
                player1.power += powerIncre
                player2.health -= player1.punchDamage
        elif currStatus2 == 'specialAttack':
            player1.isGetHit = True
            playGetHitAnim(player1, player2, screen)
            if player1.timerDelay % 20 == 0:
                player1.health -= player2.specialDamage
        else:
            player2.isGetHit = True
            playGetHitAnim(player1, player2, screen)
            if player1.timerDelay % 20 == 0:
                player1.power += powerIncre
                player2.health -= player1.punchDamage
    elif currStatus1 == 'defense':
        pass
    elif currStatus1 == "specialAttack":
        pygame.mixer.Sound.play(boxingPunch)
        if currStatus2 == 'defense':
            pass
        elif currStatus2 == 'punch' or currStatus2 == 'kick':
            player2.isGetHit = True
            playGetHitAnim(player1, player2, screen)
            if player1.timerDelay % 20 == 0:
                player2.health -= player1.specialDamage
        elif currStatus2 == 'specialAttack':
            player2.isGetHit = True
            playGetHitAnim(player1, player2, screen)
            if player1.timerDelay % 20 == 0:
                player2.health -= player1.specialDamage
        else:
            player2.isGetHit = True
            playGetHitAnim(player1, player2, screen)
            if player1.timerDelay % 20 == 0:
                player2.health -= player1.specialDamage
    if currStatus2 == 'punch' or currStatus2 == 'kick':
        pygame.mixer.Sound.play(FaceHitSound)
        if currStatus1 == 'defense':
            pass
        elif currStatus1 == 'punch' or currStatus1 == 'kick':
            player1.isGetHit = True
            playGetHitAnim(player1, player2, screen)
            if player1.timerDelay % 20 == 0:
                player2.power += powerIncre
                player1.health -= player2.punchDamage
        elif currStatus1 == 'specialAttack':
            player2.isGetHit = True
            playGetHitAnim(player1, player2, screen)
            if player1.timerDelay % 20 == 0:
                player2.health -= player1.specialDamage
        else:
            player1.isGetHit = True
            playGetHitAnim(player1, player2, screen)
            if player1.timerDelay % 20 == 0:
                player2.power += powerIncre
                player1.health -= player2.punchDamage
    elif currStatus2 == 'defense':
        pass
    elif currStatus2 == 'specialAttack':
        pygame.mixer.Sound.play(boxingPunch)
        if currStatus1 == 'defense':
            pass
        elif currStatus1 == 'punch' or currStatus1 == 'kick':
            player1.isGetHit = True
            playGetHitAnim(player1, player2, screen)
            if player1.timerDelay % 20 == 0:
                player1.health -= player2.specialDamage
        elif currStatus1 == 'specialAttack':
            player1.isGetHit = True
            playGetHitAnim(player1, player2, screen)
            if player1.timerDelay % 20 == 0:
                player1.health -= player2.specialDamage
        else:
            player1.isGetHit = True
            playGetHitAnim(player1, player2, screen)
            if player1.timerDelay % 20 == 0:
                player1.health -= player2.specialDamage

# make two players automatically face each other
def faceRight(player1, player2):
    x1, y1 = player1.x, player1.y
    x2, y2 = player2.x, player2.y
    if x2 > x1: return True
    return False

# main function
def main():
    global clock, screen, basicFont

    # pygame initialization and basic set up of global variables
    pygame.init()
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((screenWidth, screenHeight))
    pygame.display.set_caption("Little Fighter")
    basicFont = pygame.font.Font('freesansbold.ttf', 26)
    # background music
    pygame.mixer.init()
    pygame.mixer.music.load('sound/Cover of ryu.mp3')
    pygame.mixer.music.play(-1)

    gameMode = startScreen() # show the title screen and choose game mode 1p or 2p

    players = characterSelectionScreen(gameMode) # show the character selection panel and choose character
    player1, player2 = players[0], players[1] # initialize two players

    mapId = mapMenu() # show the map choices and choose the battle background

    # initialize the count of game rounds
    roundNum  = 1
    while running:
        # run the mode to actually start the game
        # 2Player mode
        if gameMode == "2P":
            while roundNum <= 3 and player1:
                results = battleMode2P(player1, player2, mapId, roundNum)
                winner, roundNum = results[0], results[1]
                # one round ends
                # reset the health before start a new round
                player1. health, player2.health = 100, 100
                if player1.winRounds == 2 or player2.winRounds == 2: break
        # 1Player mode
        elif gameMode == "1P":
            while roundNum <= 3:
                results = battleMode1P(player1, player2, mapId, roundNum)
                winner, roundNum = results[0], results[1]
                # one round ends
                # reset the health before start a new round
                player1. health, player2.health = 100, 100
                if player1.winRounds == 2 or player2.winRounds == 2: break
        gameOver(player1, player2)

# game over page
def gameOver(player1, player2):
    startImage = pygame.image.load('startScreen.bmp')
    startImage.convert()

    if player1.winRounds == 2:
        messageToScreen("Player 1 Win!", red, startImage, 0, 0, "large")
        messageToScreen("Click Main Button to Restart", red, startImage, 0, 100, "large")
    elif player2.winRounds == 2:
        messageToScreen("Player 2 Win!", red, startImage, 0, 0, "large")
        messageToScreen("Click Main Button to Restart", red, startImage, 0, 100, "large")

    # make buttons on the startscreen
    restartButton = (700, 350, 95, 20)
    gameMode = None
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                if event.key == K_1:
                    return "1P"
                elif event.key == K_2:
                    return "2P"
                # user has pressed a key, so return 

        # Draw the title image to the window:
        screen.blit(startImage, (0,0))
        button("MAIN", restartButton, blue, lightBlue, startImage, "MAIN")

        # display the screen contents to the local screen
        pygame.display.update()
        clock.tick(fps)

# let users to choose game map
def mapMenu():
    screen.fill(darkBlue)
    selectionData = 'selectionImages'
    backgrounds = [['1.png', '2.png'], ['3.png', '4.png']]
    left, top = 100, 50
    xDisplace, yDisplace = 400, 200

    toContinue = False
    # make buttons on the startscreen
    button1 = (95, 45, 210, 110)
    button2 = (495, 45, 210, 110)
    button3 = (95, 245, 210, 110)
    button4 = (495, 245, 210, 110)

    map_1, map_2, map_3, map_4 = None, None, None, None

    while running:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and toContinue:
                # select map by input map id
                if event.key == K_1:
                    return 1
                elif event.key == K_2:
                    return 2
                elif event.key == K_3:
                    return 3
                elif event.key == K_4:
                    return 4
        messageToScreen("Select the Map!", yellow, screen, 0, 0, "large")
        # or select map by click on map button
        # map 1 button
        map_1 = button("", button1, blue, yellow, screen, "map1")
        # map 2 button
        map_2 = button("", button2, blue, yellow, screen, "map2")
        # map 3 button
        map_3 = button("", button3, blue, yellow, screen, "map3")
        # map 4 button
        map_4 = button("", button4, blue, yellow, screen, "map4")
        # if map button clicked, return the selected map
        if map_1 != None:
            return map_1
        elif map_2 != None:
            return map_2
        elif map_3 != None:
            return map_3
        elif map_4 != None:
            return map_4

        map1 = pygame.image.load(os.path.join(selectionData, backgrounds[0][0]))
        map1.convert()
        screen.blit(map1, (left, top))

        map2 = pygame.image.load(os.path.join(selectionData, backgrounds[0][1]))
        map2.convert()
        screen.blit(map2, (left + xDisplace, top))

        map3 = pygame.image.load(os.path.join(selectionData, backgrounds[1][0]))
        map3.convert()
        screen.blit(map3, (left, top + yDisplace))

        map4 = pygame.image.load(os.path.join(selectionData, backgrounds[1][1]))
        map4.convert()
        screen.blit(map4, (left + xDisplace, top + yDisplace))

        pygame.display.update()
        clock.tick(fps)

# display "Fight" on the screen
def displayStartFight(screen):
    roundColor = orange
    roundSurf = blazedfont.render("Fight", True, roundColor)
    roundRect = roundSurf.get_rect()
    roundRect.topleft = (295, 150)
    screen.blit(roundSurf, roundRect)

# display "Round number" on the screen
def displayRoundNumber(screen, roundNum):
    roundColor = orange # ff8000
    roundSurf = blazedfont.render("Round %d" % roundNum, True, roundColor)
    roundRect = roundSurf.get_rect()
    roundRect.topleft = (255, 150)
    screen.blit(roundSurf, roundRect)

# fireball hit the player
def hitPlayer(player, fireball):
    return counterPlayer(player, fireball)

# keep fireball moving
def moveFireball(player1, player2, fireball, owner):
    dx = fireball.movingSpeed
    direction = fireball.movingDirection
    if owner == "1":
        if direction == "right":
            if fireball.x < screenWidth + rightMargin:
                fireball.x += dx
            if hitPlayer(player2, fireball):
                upperCut.play()
                player2.health -= 30
                player1.super, player2.isGetHit = False, True
            elif fireball.x > screenWidth + rightMargin: player1.super = False
        elif direction == "left":
            if fireball.x > -leftMargin:
                fireball.x -= dx
            if hitPlayer(player2, fireball):
                upperCut.play()
                player2.health -= 30
                player1.super, player2.isGetHit = False, True
            elif fireball.x > screenWidth + rightMargin: player1.super = False              
    elif owner == "2":
        if direction == "right":
            if fireball.x < screenWidth + rightMargin:
                fireball.x += dx
            if hitPlayer(player1, fireball):
                upperCut.play()
                player1.health -= 30
                player2.super, player1.isGetHit = False, True
            elif fireball.x > screenWidth + rightMargin: player2.super = False
        elif direction == "left":
            if fireball.x > -leftMargin:
                fireball.x -= dx
            if hitPlayer(player1, fireball):
                upperCut.play()
                player1.health -= 30
                player2.super, player1.isGetHit = False, True
            elif fireball.x > screenWidth + rightMargin: player2.super = False

def battleMode2P(player1, player2, mapId, roundNum):
    # if fight False freeze all moves
    fight = False
    if roundNum == 1:
        pygame.mixer.Sound.play(oneSound)
    elif roundNum == 2:
        pygame.mixer.Sound.play(twoSound)
    elif roundNum == 3:
        pygame.mixer.Sound.play(threeSound)
    # timer count down
    milliseconds = 0
    seconds = 30
    # battlemode background music
    pygame.mixer.music.load('sound/Little Fighter 2 theme song.mp3')
    pygame.mixer.music.play(-1)
    # initialize the battle background
    background = pygame.image.load('backgroundImages/%d.png'%mapId)
    # initialize 1st player
    # 1st players' controller
    walkingDx0, walkingDy0 = player1.walkingDx, player1.walkingDy
    runningDx0, runningDy0 = player1.runningDx, player1.runningDy
    # player1 face right animation
    standAnim0 = player1.stand()
    walkAnim0 = player1.walk()
    runAnim0 = player1.run()
    punchAnim0 = player1.punch()
    kickAnim0 = player1.kick()
    specialAttackAnim0 = player1.specialAttack()
    defenseAnim0 = player1.defense()
    # player1 face left animation
    lstandAnim0 = player1.lstand()
    lwalkAnim0 = player1.lwalk()
    lrunAnim0 = player1.lrun()
    lpunchAnim0 = player1.lpunch()
    lkickAnim0 = player1.lkick()
    lspecialAttackAnim0 = player1.lspecialAttack()
    ldefenseAnim0 = player1.ldefense()
    # player1 current status and direction
    currStatus0 = player1.currStatus
    super0 = player1.super
    currDirection0 = player1.currDirection

    # initialize 2nd player
    # 2nd players' controller
    walkingDx1, walkingDy1 = player2.walkingDx, player2.walkingDy
    runningDx1, runningDy1 = player2.runningDx, player2.runningDy
    # player2 face right animation
    standAnim1 = player2.stand()
    walkAnim1 = player2.walk()
    runAnim1 = player2.run()
    punchAnim1 = player2.punch()
    kickAnim1 = player2.kick()
    specialAttackAnim1 = player2.specialAttack()
    defenseAnim1 = player2.defense()
    # player2 face left aniamtion
    lstandAnim1 = player2.lstand()
    lwalkAnim1 = player2.lwalk()
    lrunAnim1 = player2.lrun()
    lpunchAnim1 = player2.lpunch()
    lkickAnim1 = player2.lkick()
    lspecialAttackAnim1 = player2.lspecialAttack()
    ldefenseAnim1 = player2.ldefense()
    # player2 current status and direction
    currStatus1 = player2.currStatus
    currDirection1 = player2.currDirection
    # constrain the time round fight display
    roundFightCount = 0
    isPause = False
    # player1 Anim ready
    standAnim0.play()
    lstandAnim0.play()
    walkAnim0.play()
    lwalkAnim0.play()
    runAnim0.play()
    lrunAnim0.play()
    punchAnim0.play()
    lpunchAnim0.play()
    kickAnim0.play()
    lkickAnim0.play()
    defenseAnim0.play()
    ldefenseAnim0.play()
    # player2 Anim ready
    standAnim1.play()
    lstandAnim1.play()
    walkAnim1.play()
    lwalkAnim1.play()
    runAnim1.play()
    lrunAnim1.play()
    punchAnim1.play()
    lpunchAnim1.play()
    kickAnim1.play()
    lkickAnim1.play()
    defenseAnim1.play()
    ldefenseAnim1.play()
    while True:
        screen.blit(background, (0, 0))
        # display round number at the start
        # update the count
        roundFightCount += 1
        if roundFightCount < roundNumStay:
            displayRoundNumber(screen, roundNum)
        # display fight at after round number
        elif roundFightCount < fightStay:
            displayStartFight(screen)
            fight = True
        x0, y0 = player1.x, player1.y
        x1, y1 = player2.x, player2.y
        # timer count down
        if milliseconds > oneSecond and fight and not isPause:
            seconds -= 1
            milliseconds = 0
        milliseconds += clock.tick_busy_loop(fps)

        # if counter with another player, battle can start
        if counterPlayer(player1, player2):
            battleWithPlayer(player1, player2, screen, currStatus0, currStatus1)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    main()
                elif event.key == K_p:
                    isPause = not isPause
            #print(isPause)

            if event.type == KEYDOWN and fight == True and not isPause:
                # player1 motion control
                if event.key == K_w:
                    currDirection0 = 'up'
                    currStatus0 = 'walk'

                if event.key == K_s:
                    currDirection0 = 'down'
                    currStatus0 = 'walk'

                if event.key == K_d:
                    currDirection0 = 'right'
                    currStatus0 = 'walk'

                if event.key == K_a:
                    currDirection0 = 'left'
                    currStatus0 = 'walk'

                if event.key == K_LSHIFT:
                    currStatus0 = 'run'
                        
                if event.key == K_f:
                    currStatus0 = 'punch'
                        
                if event.key == K_z:
                    currStatus0 = 'kick'
                        
                if event.key == K_e:
                    currStatus0 = 'defense'

                if event.key == K_x and player1.power > 20:
                    currStatus0 = 'specialAttack'
                    player1.power -= specialPowerDecre
                    if isinstance(player1, Hein):
                        pygame.mixer.Sound.play(fluteSound)
                        if player1.health < fullHealth: player1.health += 10
                    if faceRight(player1, player2) and not player1.isGetHit:
                        specialAttackAnim0.play()
                    elif not player1.isGetHit:
                        lspecialAttackAnim0.play()

                if event.key == K_LCTRL and player1.max:
                    player1.super = True
                    player1.power -= superPowerDecre
                    fireball = Fireball(x0, y0)
                    rfireballAnim = fireball.ball()
                    lfireballAnim = fireball.lball()
                    if faceRight(player1, player2) and not player1.isGetHit:
                        fireball.movingDirection = "right"
                        rfireballAnim.play()
                    elif not player1.isGetHit:
                        fireball.movingDirection = "left"
                        lfireballAnim.play()
                        
                # player2 motion control    
                if event.key == K_UP:
                    currDirection1 = 'up'
                    currStatus1 = 'walk'

                if event.key == K_DOWN:
                    currDirection1 = 'down'
                    currStatus1 = 'walk'

                if event.key == K_RIGHT:
                    currDirection1 = 'right'
                    currStatus1 = 'walk'

                if event.key == K_LEFT:
                    currDirection1 = 'left'
                    currStatus1 = 'walk'

                if event.key == K_RSHIFT:
                    currStatus1 = 'run'

                if event.key == K_RETURN:
                    currStatus1 = 'punch'

                if event.key == K_k:
                    currStatus1 = 'kick'

                if event.key == K_l:
                    currStatus1 = 'defense'

                if event.key == K_j and player2.power > 20:
                    currStatus1 = 'specialAttack'
                    player2.power -= specialPowerDecre
                    if isinstance(player2, Hein):
                        pygame.mixer.Sound.play(fluteSound)
                        if player2.health < fullHealth: player2.health += 10
                    if faceRight(player2, player1) and not player2.isGetHit:
                        specialAttackAnim1.play()
                    elif not player2.isGetHit:
                        lspecialAttackAnim1.play()

                if event.key == K_SPACE and player2.max:
                    player2.super = True
                    player2.power -= superPowerDecre 
                    fireball = Fireball(x1, y1)
                    rfireballAnim = fireball.ball()
                    lfireballAnim = fireball.lball()
                    if faceRight(player2, player1) and not player2.isGetHit:
                        fireball.movingDirection = "right"
                        rfireballAnim.play()
                    elif not player1.isGetHit:
                        fireball.movingDirection = "left"
                        lfireballAnim.play()

            # key up, reset the status to 'stand'
            if event.type == KEYUP:
        # ist player keyup motion control
                if currStatus0 != 'stand' and currStatus0 != 'super':
                    currStatus0 = 'stand'
        # 2nd player keyup motion control
                if currStatus1 != 'stand' and currStatus1 != 'super':
                    currStatus1 = 'stand'

        # 1st player motion display
        if currStatus0 == 'stand':
            if faceRight(player1, player2) and not player1.isGetHit:     
                standAnim0.blit(screen, (x0, y0))
            elif not player1.isGetHit:
                lstandAnim0.blit(screen, (x0, y0))
        elif currStatus0 == 'walk':
            if not counterToFreezeP1Move(player1, player2, currDirection0):
                walkPlayer(player1, currDirection0)
            if faceRight(player1, player2):
                walkAnim0.blit(screen, (x0, y0))
            else: lwalkAnim0.blit(screen, (x0, y0))
        elif currStatus0 == 'run':
            if not counterToFreezeP1Move(player1, player2, currDirection0):
                runPlayer(player1, currDirection0)
            if faceRight(player1, player2):
                runAnim0.blit(screen, (x0, y0))
            else: lrunAnim0.blit(screen, (x0, y0))
        elif currStatus0 == 'punch':
            if faceRight(player1, player2):
                punchAnim0.blit(screen, (x0, y0))
            else: lpunchAnim0.blit(screen, (x0, y0))
        elif currStatus0 == 'kick':
            if faceRight(player1, player2):
                kickAnim0.blit(screen, (x0, y0))
            else: lkickAnim0.blit(screen, (x0, y0))
        elif currStatus0 == 'defense':
            if faceRight(player1, player2):
                defenseAnim0.blit(screen, (x0, y0))
            else: ldefenseAnim0.blit(screen, (x0, y0))
        elif currStatus0 == 'specialAttack':
            if faceRight(player1, player2):
                specialAttackAnim0.blit(screen, (x0, y0))
            else: lspecialAttackAnim0.blit(screen, (x0, y0))
        if player1.super:
            moveFireball(player1,player2, fireball, "1")
            if faceRight(player1, player2):
                rfireballAnim.blit(screen, (fireball.x, fireball.y))
            else: lfireballAnim.blit(screen, (fireball.x, fireball.y))    

        # 2nd player motion display
        if  currStatus1 == 'stand':
            if faceRight(player2, player1) and not player2.isGetHit:
                standAnim1.blit(screen, (x1, y1))
            elif not player2.isGetHit:
                lstandAnim1.blit(screen, (x1, y1))
        elif currStatus1 == 'walk':
            if not counterToFreezeP2Move(player1, player2, currDirection1):
                walkPlayer(player2, currDirection1)
            if faceRight(player2, player1):
                walkAnim1.blit(screen, (x1, y1))
            else: lwalkAnim1.blit(screen, (x1, y1))
        elif currStatus1 == 'run':
            if not counterToFreezeP2Move(player1, player2, currDirection1):
                runPlayer(player2, currDirection1)
            if faceRight(player2, player1):
                runAnim1.blit(screen, (x1, y1))
            else: lrunAnim1.blit(screen, (x1, y1))
        elif currStatus1 == 'punch':
            if faceRight(player2, player1):
                punchAnim1.blit(screen, (x1, y1))
            else: lpunchAnim1.blit(screen, (x1, y1))
        elif currStatus1 == 'kick':
            if faceRight(player2, player1):
                kickAnim1.blit(screen, (x1, y1))
            else: lkickAnim1.blit(screen, (x1, y1))
        elif currStatus1 == 'defense':
            if faceRight(player2, player1):
                defenseAnim1.blit(screen, (x1, y1))
            else: ldefenseAnim1.blit(screen, (x1, y1))
        elif currStatus1 == 'specialAttack':
            if faceRight(player2, player1):
                specialAttackAnim1.blit(screen, (x1, y1))
            else: lspecialAttackAnim1.blit(screen, (x1, y1))
        if player2.super:
            moveFireball(player1, player2,fireball, "2")
            if faceRight(player2, player1):
                rfireballAnim.blit(screen, (fireball.x, fireball.y))
            else: lfireballAnim.blit(screen, (fireball.x, fireball.y))

        if player1.isGetHit: player1.isGetHit = False
        if player2.isGetHit: player2.isGetHit = False

        # ist player healthBar display
        displayHealthBar(player1, screen, leftHealthLeft, leftHealthTop)
        displayPowerBar(player1, screen, leftBarLeft, leftBarTop)
        # 2nd player healthBar display
        displayHealthBar(player2, screen, rightHealthLeft, rightHealthTop)
        displayPowerBar(player2, screen, rightBarLeft, rightBarTop)
        # left player portait dispalay
        displayPlayer(player1, screen, (LpPortrait[0], LpPortrait[1]))
        # right player portrait display
        displayPlayer(player2, screen, (RpPortrait[0], RpPortrait[1]))
        # timer count down display
        timerDisplay(screen, seconds)
        # display score
        displayScore(player1, player2)
        # display if pause
        if isPause:
            messageToScreen("Pause", yellow, screen, 0, -25, "large")
            messageToScreen("Press P to Resume", yellow, screen, 0, 25, "large")

        # time runs out, compare the two players' left health
        if seconds <= 0:
            roundNum += 1
            if player1.health < player2.health:
                player2.winRounds += 1
                return ("Player1 Win", roundNum)
            else:
                player1.winRounds += 1
                return ("Player2 Win", roundNum)
        elif player2.health <= 0 and player1.health > 0:
            roundNum += 1
            player1.winRounds += 1
            return ("Player1 win", roundNum)
        elif player2.health > 0 and player1.health <= 0:
            roundNum += 1
            player2.winRounds += 1
            return ("Player2 win", roundNum)

        pygame.display.update()
        clock.tick(fps)

# player2 ai in 1p mode
# based on, return player2 status and motions(result in changing positions)
def player2AI(player1, player2, getMovingLR = False, getMovingUD = False, toPunch = True):
    # random direction
    directionflag = random.randint(1, 200)
    if directionflag in range(1, 51):
        getMovingLR = True
    elif directionflag in range(51, 100):
        getMovingUD = True
    # random status
    statusflag = random.randint(0, 10000)
    if statusflag in range(0, 1000):
        player2.currStatus = "walk"
    elif statusflag in range(1000, 1200):
        player2.currStatus = "run"
    elif statusflag in range(1200, 2200): player2.currStatus = "punch"
    elif statusflag in range(2200, 3200): player2.currStatus = "defense"

    x0, y0, currStatus0 = player1.x, player1.y, player1.currStatus
    # player2 positions
    x1, y1 = player2.x, player2.y
    if x0 < x1:
        if getMovingLR == True:
            player2.currDirection = "left"
    elif x0 > x1:
        if getMovingLR == True:
            player2.currDirection = "right"
    if y0 < y1:
        if getMovingUD == True:
            player2.currDirection = "up"
    elif y0 > y1:
        if getMovingUD == True:
            player2.currDirection = "down"
    return (player2.currStatus, player2.currDirection)

def battleMode1P(player1, player2, mapId, roundNum):
    # if fight False freeze all moves
    fight = False
    if roundNum == 1:
        pygame.mixer.Sound.play(oneSound)
    elif roundNum == 2:
        pygame.mixer.Sound.play(twoSound)
    elif roundNum == 3:
        pygame.mixer.Sound.play(threeSound)
    # timer count down
    milliseconds = 0
    seconds = 30
    # battlemode background music
    pygame.mixer.init()
    pygame.mixer.music.load('sound/Little Fighter 2 theme song.mp3')
    pygame.mixer.music.play(-1)
    # initialize the battle background
    background = pygame.image.load('backgroundImages/%d.png'%mapId)
    # initialize 1st player
    # 1st players' controller
    walkingDx0, walkingDy0 = player1.walkingDx, player1.walkingDy
    runningDx0, runningDy0 = player1.runningDx, player1.runningDy
    # player1 face right animation
    standAnim0 = player1.stand()
    walkAnim0 = player1.walk()
    runAnim0 = player1.run()
    punchAnim0 = player1.punch()
    kickAnim0 = player1.kick()
    defenseAnim0 = player1.defense()
    specialAttackAnim0 = player1.specialAttack()
    # player1 face left animation
    lstandAnim0 = player1.lstand()
    lwalkAnim0 = player1.lwalk()
    lrunAnim0 = player1.lrun()
    lpunchAnim0 = player1.lpunch()
    lkickAnim0 = player1.lkick()
    ldefenseAnim0 = player1.ldefense()
    lspecialAttackAnim0 = player1.lspecialAttack()
    # player1 current status and direction
    currStatus0 = player1.currStatus
    currDirection0 = player1.currDirection
    # initialize 2nd player
    # 2nd players' controller
    walkingDx1, walkingDy1 = player2.walkingDx, player2.walkingDy
    runningDx1, runningDy1 = player2.runningDx, player2.runningDy
    # player2 face right animation
    standAnim1 = player2.stand()
    walkAnim1 = player2.walk()
    runAnim1 = player2.run()
    punchAnim1 = player2.punch()
    kickAnim1 = player2.kick()
    defenseAnim1 = player2.defense()
    specialAttackAnim1 = player2.specialAttack()
    # player2 face left aniamtion
    lstandAnim1 = player2.lstand()
    lwalkAnim1 = player2.lwalk()
    lrunAnim1 = player2.lrun()
    lpunchAnim1 = player2.lpunch()
    lkickAnim1 = player2.lkick()
    ldefenseAnim1 = player2.ldefense()
    lspecialAttackAnim1 = player2.specialAttack()
    # player2 current status and direction
    currStatus1 = player2.currStatus
    currDirection1 = player2.currDirection
    # count the round number
    roundFightCount = 0
    isPause = False
    # player1 Anim ready
    standAnim0.play()
    lstandAnim0.play()
    walkAnim0.play()
    lwalkAnim0.play()
    runAnim0.play()
    lrunAnim0.play()
    punchAnim0.play()
    lpunchAnim0.play()
    kickAnim0.play()
    lkickAnim0.play()
    defenseAnim0.play()
    ldefenseAnim0.play()
    # player2 Anim ready
    standAnim1.play()
    lstandAnim1.play()
    walkAnim1.play()
    lwalkAnim1.play()
    runAnim1.play()
    lrunAnim1.play()
    punchAnim1.play()
    lpunchAnim1.play()
    kickAnim1.play()
    lkickAnim1.play()
    defenseAnim1.play()
    ldefenseAnim1.play()
    while True:
        screen.blit(background, (0, 0))
        # display round number at the start
        # update the count
        roundFightCount += 1
        if roundFightCount < roundNumStay:
            displayRoundNumber(screen, roundNum)
        # display fight at after round number
        elif roundFightCount < fightStay:
            displayStartFight(screen)
            fight = True
        x0, y0 = player1.x, player1.y
        x1, y1 = player2.x, player2.y
        # timer count down
        if milliseconds > oneSecond and fight and not isPause:
            seconds -= 1
            milliseconds = 0
        milliseconds += clock.tick_busy_loop(fps)

        # if counter with another player, battle can start
        if counterPlayer(player1, player2):
            battleWithPlayer(player1, player2, screen, currStatus0, currStatus1)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    main()
                elif event.key == K_p:
                    isPause = not isPause
            #print(isPause)
            if event.type == KEYDOWN and fight and not isPause:
                if event.key == K_w:
                    currDirection0 = 'up'
                    currStatus0 = 'walk'

                if event.key == K_s:
                    currDirection0 = 'down'
                    currStatus0 = 'walk'

                if event.key == K_d:
                    currDirection0 = 'right'
                    currStatus0 = 'walk'
   
                if event.key == K_a:
                    currDirection0 = 'left'
                    currStatus0 = 'walk'

                if event.key == K_LSHIFT:
                    currStatus0 = 'run'

                if event.key == K_f:
                    currStatus0 = 'punch'

                if event.key == K_z:
                    currStatus0 = 'kick'

                if event.key == K_e:
                    currStatus0 = 'defense'

                if event.key == K_x and player1.power > 20:
                    currStatus0 = 'specialAttack'
                    player1.power -= specialPowerDecre
                    if isinstance(player1, Hein):
                        pygame.mixer.Sound.play(fluteSound)
                        if player1.health < fullHealth: player1.health += 10
                    if faceRight(player1, player2) and not player1.isGetHit:
                        specialAttackAnim0.play()
                    elif not player1.isGetHit:
                        lspecialAttackAnim0.play()

                if event.key == K_LCTRL and player1.max:
                    player1.super = True
                    player1.power -= superPowerDecre
                    fireball = Fireball(x0, y0)
                    rfireballAnim = fireball.ball()
                    lfireballAnim = fireball.lball()
                    if faceRight(player1, player2) and not player1.isGetHit:
                        fireball.movingDirection = "right"
                        rfireballAnim.play()
                    elif not player1.isGetHit:
                        fireball.movingDirection = "left"
                        lfireballAnim.play()

            # key up, reset the status to 'stand'
            if event.type == KEYUP:
            # ist player keyup motion control
                if currStatus0 != 'stand':
                    currStatus0 = 'stand'

        # 1st player motion display
        if currStatus0 == 'stand':
            if faceRight(player1, player2) and not player1.isGetHit:
                standAnim0.blit(screen, (x0, y0))
            elif not player1.isGetHit:
                lstandAnim0.blit(screen, (x0, y0))
        elif currStatus0 == 'walk':
            if not counterToFreezeP1Move(player1, player2, currDirection0):
                walkPlayer(player1, currDirection0)
            if faceRight(player1, player2):
                walkAnim0.blit(screen, (x0, y0))
            else: lwalkAnim0.blit(screen, (x0, y0))
        elif currStatus0 == 'run':
            if not counterToFreezeP1Move(player1, player2, currDirection0):
                runPlayer(player1, currDirection0)
            if faceRight(player1, player2):
                runAnim0.blit(screen, (x0, y0))
            else: lrunAnim0.blit(screen, (x0, y0))
        elif currStatus0 == 'punch':
            if faceRight(player1, player2):
                punchAnim0.blit(screen, (x0, y0))
            else: lpunchAnim0.blit(screen, (x0, y0))
        elif currStatus0 == 'kick':
            if faceRight(player1, player2):
                kickAnim0.blit(screen, (x0, y0))
            else: lkickAnim0.blit(screen, (x0, y0))
        elif currStatus0 == 'defense':
            if faceRight(player1, player2):
                defenseAnim0.blit(screen, (x0, y0))
            else: ldefenseAnim0.blit(screen, (x0, y0))
        elif currStatus0 == 'specialAttack':
            if faceRight(player1, player2):
                specialAttackAnim0.blit(screen, (x0, y0))
            else: lspecialAttackAnim0.blit(screen, (x0, y0))
        if player1.super:
            moveFireball(player1,player2, fireball, "1")
            if faceRight(player1, player2):
                rfireballAnim.blit(screen, (fireball.x, fireball.y))
            else: lfireballAnim.blit(screen, (fireball.x, fireball.y))  

        # get 2nd player currStatus and currDirection
        # pass player1, player2 into player2AI
        if fight and not isPause:
            currStatus1, currDirection1 = player2AI(player1, player2)

        # 2nd player motion display
        if  currStatus1 == 'stand':
            if faceRight(player2, player1) and not player2.isGetHit:
                standAnim1.play()
                standAnim1.blit(screen, (x1, y1))
            elif not player2.isGetHit:
                lstandAnim1.play()
                lstandAnim1.blit(screen, (x1, y1))
        elif currStatus1 == 'walk':
            if not counterToFreezeP2Move(player1, player2, currDirection1):
                walkPlayer(player2, currDirection1)
            if faceRight(player2, player1):
                walkAnim1.blit(screen, (x1, y1))
            else:
                lwalkAnim1.blit(screen, (x1, y1))
        elif currStatus1 == 'run':
            if not counterToFreezeP2Move(player1, player2, currDirection1):
                runPlayer(player2, currDirection1)
            if faceRight(player2, player1):
                runAnim1.blit(screen, (x1, y1))
            else: lrunAnim1.blit(screen, (x1, y1))
        elif currStatus1 == 'punch':
            if faceRight(player2, player1):
                punchAnim1.blit(screen, (x1, y1))
            else:
                lpunchAnim1.blit(screen, (x1, y1))
        elif currStatus1 == 'defense':
            if faceRight(player2, player1):
                defenseAnim1.blit(screen, (x1, y1))
            else: ldefenseAnim1.blit(screen, (x1, y1))
        elif currStatus1 == 'specialAttack':
            pass

        if player1.isGetHit: player1.isGetHit = False
        if player2.isGetHit: player2.isGetHit = False

        # left player healthBar display
        displayHealthBar(player1, screen, leftHealthLeft, leftHealthTop)
        displayPowerBar(player1, screen, leftBarLeft, leftBarTop)
        # right player healthBar display
        displayHealthBar(player2, screen, rightHealthLeft, rightHealthTop)
        displayPowerBar(player2, screen, rightBarLeft, rightBarTop)
        # left player portait dispalay
        displayPlayer(player1, screen, (LpPortrait[0], LpPortrait[1]))
        # right player portrait display
        displayPlayer(player2, screen, (RpPortrait[0], RpPortrait[1]))
        # timer count down display
        timerDisplay(screen, seconds)
        # display score
        displayScore(player1, player2)
        # display if pause
        if isPause:
            messageToScreen("Pause", yellow, screen, 0, -25, "large")
            messageToScreen("Press P to Resume", yellow, screen, 0, 25, "large")

        # time runs out, compare the two players' left health
        if seconds <= 0:
            roundNum += 1
            if player1.health < player2.health:
                player2.winRounds += 1
                return ("Player1 Win", roundNum)
            else:
                player1.winRounds += 1
                return ("Player2 Win", roundNum)
        elif player2.health <= 0 and player1.health > 0:
            roundNum += 1
            player1.winRounds += 1
            return ("Player1 win", roundNum)
        elif player2.health > 0 and player1.health <= 0:
            roundNum += 1
            player2.winRounds += 1
            return ("Player2 win", roundNum)

        pygame.display.update()
        clock.tick(fps)

# Display the start screen (game title and instructions)
# unitl the user press a key
def startScreen():
    startImage = pygame.image.load('startScreen.bmp')
    startImage.convert()

    # make buttons on the startscreen
    button1 = (150, 250, 100, 50)
    button2 = (350, 250, 100, 50)
    button3 = (550, 250, 100, 50)
    button4 = (350, 320, 100, 50)
    gameMode = None
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                if event.key == K_1:
                    return "1P"
                elif event.key == K_2:
                    return "2P"
                # user has pressed a key, so return 

        # Draw the title image to the window:
        screen.blit(startImage, (0,0))
        # GUI
        # 1 player button
        gameMode = button("1 Player", button1, green, lightGreen, startImage, "1P")
        if gameMode == "1P": return "1P"
        # 2 player button
        gameMode = button("2 Player", button2, red, lightRed, startImage, "2P")
        if gameMode == "2P": return "2P"
        # help button
        button("Help", button3, blue, lightBlue, startImage, "HELP")
        # exir button
        button("Quit", button4, yellow, lightYellow, startImage, "QUIT")

        # display the screen contents to the local screen
        pygame.display.update()
        clock.tick(fps)

# control instructions
def helpScreen():
    # make buttons on the startscreen
    button1 = (650, 350, 90, 30)

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
        # Draw the title image to the window:
        screen.fill(textColor)
        # display P1 motion control
        messageToScreen("Player1 Motion Control", yellow, screen, -200, -150)
        messageToScreen("Up: W", yellow, screen, -200, -120)
        messageToScreen("Down: S", yellow, screen, -200, -90)
        messageToScreen("Left: A", yellow, screen, -200, -60)
        messageToScreen("Right: D", yellow, screen, -200, -30)
        messageToScreen("Punch Attack: F", yellow, screen, -200, 0)
        messageToScreen("Kick Attack: Z", yellow, screen, -200, 30)
        messageToScreen("Defense: E", yellow, screen, -200, 60)
        messageToScreen("Special Attack: X", yellow, screen, -200, 90)
        messageToScreen("Super Attack: Ctrl", yellow, screen, -200, 120)
        # diaplay P2 motion control
        messageToScreen("Player2 Motion Control", yellow, screen, 200, -150)
        messageToScreen("Up: UP", yellow, screen, 200, -120)
        messageToScreen("Down: DOWN", yellow, screen, 200, -90)
        messageToScreen("Left: LEFT", yellow, screen, 200, -60)
        messageToScreen("Right: RIGHT", yellow, screen, 200, -30)
        messageToScreen("Punch Attack: RETURN", yellow, screen, 200, 0)
        messageToScreen("Kick Attack: K", yellow, screen, 200, 30)
        messageToScreen("Defense: L", yellow, screen, 200, 60)
        messageToScreen("Special Attack: J", yellow, screen, 200, 90)
        messageToScreen("Super Attack: Space", yellow, screen, 200, 120)
        # help button GUI
        button("Main", button1, blue, lightBlue, screen, "MAIN")

        # display the screen contents to the local screen
        pygame.display.update()
        clock.tick(fps)

# display the selected character on the screen
def displaySelectedPlayer(player, playerNumber, onSurface):
    standAnim, lstandAnim = player.stand(), player.lstand()
    if playerNumber == 1:
        standAnim.play()
        standAnim.blit(onSurface, (100, 300))
        messageToScreen("Player1 Ready", green, onSurface, -250, 100)
    elif playerNumber == 2:
        lstandAnim.play()
        lstandAnim.blit(onSurface, (600, 300))
        messageToScreen("Player2 Ready", green, onSurface, 250, 100)

def characterSelectionScreen(gameMode):
    heroData = 'characterImages'
    selectionData = 'selectionImages'
    heroes = [ 'frozen/frozen_s.bmp',   'hein/hein_s.bmp',
              'electro/electro_s.bmp', 'firen/firen_s.bmp',]             
    playerNumber = 0 # up to two players

    mainMenuImage = pygame.image.load(os.path.join(selectionData, 'selectionPanel.png'))
    mainMenuImage.convert()
    # make hero images on the screen
    left, top = 120, 100

    # make buttons on the startscreen
    button0 = (700, 350, 95, 20)
    button1 = (115, 95, 110, 110)
    button2 = (265, 95, 110, 110)
    button3 = (415, 95, 110, 110)
    button4 = (565, 95, 110, 110)
    pointCount = 0
    pointLeft, pointTop = (225, 200)
    xDisplace = 150
    toContinue = False

    while running:
        if playerNumber == 2 and toContinue:
            return (player1, player2)
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                # choose the first player
                if playerNumber == 0:
                    if event.key == K_1:
                        player1 = Frozen(screenWidth/2 - playerDistance - playerWidth, screenHeight/2)
                        playerNumber += 1
                        displaySelectedPlayer(player1, playerNumber, mainMenuImage)

                    elif event.key == K_2:
                        player1 = Hein(screenWidth/2 - playerDistance - playerWidth, screenHeight/2)
                        playerNumber += 1
                        displaySelectedPlayer(player1, playerNumber, mainMenuImage)

                    elif event.key == K_3:
                        player1 = Electro(screenWidth/2 - playerDistance - playerWidth, screenHeight/2)
                        playerNumber += 1
                        displaySelectedPlayer(player1, playerNumber, mainMenuImage)

                    elif event.key == K_4:
                        player1 = Firen(screenWidth/2 - playerDistance - playerWidth, screenHeight/2)
                        playerNumber += 1
                        displaySelectedPlayer(player1, playerNumber, mainMenuImage)
                # choose the second player
                elif playerNumber == 1:
                    if gameMode == "2P":
                        if event.key == K_1:
                            player2 = Frozen(screenWidth/2 + playerDistance, screenHeight/2)
                            playerNumber += 1
                            displaySelectedPlayer(player2, playerNumber, mainMenuImage)

                        elif event.key == K_2:
                            player2 = Hein(screenWidth/2 + playerDistance, screenHeight/2)
                            playerNumber += 1
                            displaySelectedPlayer(player2, playerNumber, mainMenuImage)

                        elif event.key == K_3:
                            player2 = Electro(screenWidth/2 + playerDistance, screenHeight/2)
                            playerNumber += 1
                            displaySelectedPlayer(player2, playerNumber, mainMenuImage)

                        elif event.key == K_4:
                            player2 = Firen(screenWidth/2 + playerDistance, screenHeight/2)
                            playerNumber += 1
                            displaySelectedPlayer(player2, playerNumber, mainMenuImage)
                    elif gameMode == "1P":
                        player2List = [Frozen(screenWidth/2 + playerDistance, screenHeight/2),
                                       Hein(screenWidth/2 + playerDistance, screenHeight/2),
                                       Electro(screenWidth/2 + playerDistance, screenHeight/2),
                                       Firen(screenWidth/2 + playerDistance, screenHeight/2)]
                        playerId = random.randint(0, 3)
                        player2 = player2List[playerId]
                        playerNumber += 1
                        displaySelectedPlayer(player2, playerNumber, mainMenuImage)

        screen.blit(mainMenuImage, (0, 0))
        # GUI
        # continue button
        toContinue = button("continue", button0, blue, yellow, mainMenuImage, "CONTINUE")
        # num 1
        button("", button1, blue, yellow, mainMenuImage, "1")
        # num 2
        button("", button2, blue, yellow, mainMenuImage, "2")
        # num 3
        button("", button3, blue, yellow, mainMenuImage, "3")
        # num 4
        button("", button4, blue, yellow, mainMenuImage, "4")

        heroFigure1 = pygame.image.load(os.path.join(heroData, heroes[0]))
        heroFigure1.convert()
        screen.blit(heroFigure1, (left, top))

        heroFigure2 = pygame.image.load(os.path.join(heroData, heroes[1]))
        heroFigure2.convert()
        screen.blit(heroFigure2, (left + xDisplace, top))

        heroFigure3 = pygame.image.load(os.path.join(heroData, heroes[2]))
        heroFigure3.convert()
        screen.blit(heroFigure3, (left + xDisplace * 2, top))

        heroFigure4 = pygame.image.load(os.path.join(heroData, heroes[3]))
        heroFigure4.convert()
        screen.blit(heroFigure4, (left + xDisplace * 3, top))

        pygame.display.update()
        clock.tick(fps)

# CITATION: textToButton from https://www.youtube.com/watch?v=D69T-pfI6LY&index=46&list=PL6gx4Cwl9DGAjkwJocj7vlc_mFU-4wXJq
# make text to the button center
def textToButton(msg, color, button, surface):
    textSurf, textRect = textObjects(msg, color, font = "medium")
    buttonx, buttony, width, height = button[0], button[1], button[2], button[3]
    textRect.center = (buttonx + width / 2, buttony + height / 2)
    surface.blit(textSurf, textRect)

# CITATION: button from https://www.youtube.com/watch?v=D69T-pfI6LY&index=46&list=PL6gx4Cwl9DGAjkwJocj7vlc_mFU-4wXJq
# to make buttons that react to mouse hover
def button(text, buttonNum, activeColor, inactiveColor, onSurface, action = None):
    curr = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    # mouse current position
    mouseX, mouseY = curr[0], curr[1]
    x, y, width, height = buttonNum[0], buttonNum[1], buttonNum[2], buttonNum[3]
    if x + width > mouseX > x and y + height > mouseY > y:
        if action == "1":
            messageToScreen("Press Key 1 to Confirm", red, screen, 0, 100)
        elif action == "2":
            messageToScreen("Press Key 2 to Confirm", red, screen, 0, 100)
        elif action == "3":
            messageToScreen("Press Key 3 to Confirm", red, screen, 0, 100)
        elif action == "4":
            messageToScreen("Press Key 4 to Confirm", red, screen, 0, 100)
        pygame.draw.rect(onSurface, inactiveColor, (x, y, width, height))
        if click[0] == 1 and action != None:
            if action == "1P": return "1P"
            elif action == "2P": return "2P"
            elif action == "HELP": helpScreen()
            elif action == "QUIT": terminate()
            elif action == "MAIN": main()
            elif action == "CONTINUE": return True
            elif action == "map1": return 1
            elif action == "map2": return 2
            elif action == "map3": return 3
            elif action == "map4": return 4
    else:
        pygame.draw.rect(onSurface, activeColor, (x, y, width, height))

    textToButton(text, textColor, (x, y, width, height), onSurface)

def terminate():
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
