import pygame
from pygame import mixer
import random
import math


pygame.init()
screen = pygame.display.set_mode((800,600))
running = True

scoreval = 0
font = pygame.font.Font("freesansbold.ttf",32)
scoreX = 10
scoreY = 10
def dis_score(x,y):
    score = font.render("Score: " + str(scoreval),True , (126, 128, 127))
    screen.blit(score,(x,y))

def gover():
    gfont = pygame.font.Font("freesansbold.ttf",64)
    over = gfont.render("Game Over",True, (46, 46, 46))
    screen.blit(over,(200,250))

icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("Space Shooter")
background = pygame.image.load("background.png")
mixer.music.load("background.wav")
mixer.music.play(-1)

playerImg = pygame.image.load("player.png")
playerX = 370
playerY = 480
pchangeX = 0

enemyImg = []
enemyX = []
enemyY = []
echangeX = []
echangeY = []
for i in range(4):
    enemyImg.append(pygame.image.load("enemy1.png"))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    echangeX.append(3)
    echangeY.append(40)

bulletImg = pygame.image.load("bullet.png")
bulletX =  0
bulletY = 480
bchangeX = 0
bchangeY = 7
bstate =  False #False for ready and True for fire


def player(x,y):
    screen.blit(playerImg,(x,y))

def enemy(x,y,h):
    screen.blit(enemyImg[h],(x,y))

def collisonDetector(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt((enemyX - bulletX)**2 + (enemyY-bulletY)**2) #D = root over ((x2 - x1)^2 + (y2-y1)^2)
    if distance < 27:
        return True
    return False

def bfire(x,y):
    global bstate
    bstate =  True
    screen.blit(bulletImg,(x+16,y+10))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                pchangeX = 5
            if event.key == pygame.K_LEFT:
                pchangeX = -5
            if event.key == pygame.K_SPACE:
                if not bstate:
                    bulletX = playerX
                    bfire(bulletX,bulletY)
                    bsound = mixer.Sound("bullet.wav")
                    bsound.play()
        if event.type == pygame.KEYUP and (event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT):
            pchangeX = 0

        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736


    print(enemyX)
    screen.fill((0,0,0))
    screen.blit(background,(0,0))
    player(playerX,playerY)

    playerX += pchangeX


    if bulletY < -2:
        bstate = False
        bulletY = 480

    if bstate:
        bfire(bulletX, bulletY)
        bulletY -= bchangeY


    for h in range(4):
        if enemyY[h] > 440:
            for k in range(4):
                enemyY[k] = 2000
            gover()
            break
        if enemyX[h] <= 0:
            echangeX[h] = 3
            enemyY[h] += echangeY[h]
        elif enemyX[h] >= 736:
            echangeX[h] = -3
            enemyY[h] += echangeY[h]

        if collisonDetector(enemyX[h],enemyY[h],bulletX,bulletY):
            bstate = False # False for ready True for false
            bulletY = 480
            enemyX[h] = random.randint(0,735)
            enemyY[h] = random.randint(50,150)
            scoreval += 1
            esound = mixer.Sound("explosion.wav")
            esound.play()
        enemyX[h] += echangeX[h]
        enemy(enemyX[h],enemyY[h],h)
    dis_score(scoreX,scoreY)
    pygame.display.update()
