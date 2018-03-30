import pygame
pygame.mixer.init()
pygame.font.init()

# one second count
oneSecond = 490
roundNumStay = 50
fightStay = 100
# pause
isPause = False
# player width, height
playerWidth = 80
playerHeight = 80
# screen size 
screenWidth = 800
screenHeight = 400
halfScreenWidth = screenWidth // 2
halfScreenHeight = screenHeight // 2

# the total wiath and height of each tile on pixels
tileWidth = 50
tielHeight = 85
tileFloorHeight = 40
# player portrait position on the screen
# in battle 
LpPortrait = (95, 25)
RpPortrait = (655, 25)
# timer y diplace distance from center
timerDisplaceFromCenter = -160
# score y displace distance from center
scoreDisplaceFromCenter = -135
# full Health
fullHealth = 100
# full Power
fullPower = 100
# power increase by each hit
powerIncre = 20
superPowerDecre = 50
specialPowerDecre = 20
# left player power bar position
leftBarLeft = 150
leftBarTop = 55
# right player power bar position
rightBarLeft = 450
rightBarTop = 55
# left player health bar position
leftHealthLeft = 150
leftHealthTop = 25
# right player health bar position
rightHealthLeft = 450
rightHealthTop = 25
# bar width and height for health and power display
barWidth = screenWidth / 4
barHeight = screenHeight / 20
# distance between two players to freeze move
distanceToFreezeP1 = 40
distanceToFreezeP2 = 20
# colors
textColor = (0, 0, 0) # black
white = (255, 255, 255)
orange = (255, 128, 0)
red = (255, 0, 0)
lightRed = (255, 153, 153)
green = (0, 255, 0)
healthGreen = (0, 204, 0)
lightGreen = (153, 255, 153)
blue = (0, 0, 255)
lightBlue = (204, 209, 255)
darkBlue = (0, 51, 102)
yellow = (200, 200, 0)
lightYellow = (255, 255, 0)
# regular game display setup
running = True
fps = 60
# contrain player's activity scope
topMargin = 80
bottomMargin = 115
leftMargin = 5
rightMargin = 80
# basic font used in the game
# small to large in ironSans font
smallfont = pygame.font.Font('ironSans.ttf', 15)
medfont = pygame.font.Font('ironSans.ttf', 25)
largefont = pygame.font.Font('ironSans.ttf', 35)
blazedfont = pygame.font.Font('Blazed.ttf', 50)
# in battle mode, define two players' distance
playerDistance = 200
# True if two players counter each other
isCounter = False
# sound effects
bombSound = pygame.mixer.Sound("sound/BombSound_SoundBible.com.wav")
upperCut = pygame.mixer.Sound("sound/UpperCutSoundBible.com.wav")
FaceHitSound = pygame.mixer.Sound("sound/StrongPunch.wav")
fluteSound = pygame.mixer.Sound("sound/heinFlute.wav")
boxingPunch = pygame.mixer.Sound("sound/BoxingPunch.wav")
fightSound = pygame.mixer.Sound("sound/Street_Fighter_Fight_Sound_Effect.wav")
oneSound = pygame.mixer.Sound("sound/mkt-round1.wav")
twoSound = pygame.mixer.Sound("sound/mkt-round2.wav")
threeSound = pygame.mixer.Sound("sound/mkt-round3.wav")