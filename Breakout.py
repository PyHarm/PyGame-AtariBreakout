import pygame as pg
from pygame.locals import *
from random import randint

pg.init()
pg.font.init()
font = pg.font.Font('PressStart2P-Regular.ttf', 30)

highscoreFile = open('highscore', 'r')

score = 0
highscore = highscoreFile.read().strip()

scoreCap = 'Score: ' + str(score) 
highscoreCap = 'Highscore: ' + highscore

highscoreFile.close()

titleCap = font.render('Breakout', False, (150,150,150))
scoreSu = font.render(scoreCap, False, (150,150,150))
highscoreSu = font.render(highscoreCap, False, (150,150,150))

playerSound = pg.mixer.Sound('s5.wav')
brickSound = pg.mixer.Sound('s6.wav')
 
pg.display.set_caption('BreakOut')
clock = pg.time.Clock()

width = 1300
heigth = 700

screen = pg.display.set_mode((width, heigth))

on = True

class Brick:
    def __init__(self, lvl, col):
        self.level = lvl
        self.h = 30
        self.w = 100
        self.x = self.w * col
        self.y = self.h * lvl + 75
        self.pad = 0
        self.colors = ((66, 134, 244), (223, 66, 244), (244, 65, 65), (242, 136, 65), (225, 232, 46), (43, 224, 40))  
        self.des = False

    def draw(self):
        p = self.pad
        pg.draw.rect(screen, self.colors[self.level], (self.x+p, self.y+p, self.w-p*2, self.h-p*2))

class Player:
    def __init__(self):
        self.h = 30
        self.w = 200
        self.x = int(width/2)-self.w/2
        self.y = heigth-2*self.h
        self.color = (255,255,255)
        self.speed = 0

    def draw(self):
        pg.draw.rect(screen, self.color, (self.x, self.y, self.w, self.h))
        if not((pg.mouse.get_pos()[0]<=self.w/2 - 50) or (pg.mouse.get_pos()[0]>=width-self.w/2 + 50)):
            self.x = pg.mouse.get_pos()[0]-self.w/2

class Ball:
    def __init__(self):
        self.x = randint(200, 400)
        self.y = 300
        self.r = 9
        self.sx = 6
        self.sy = 6
        self.bx = self.x
        self.by = self.y
        self.topLvl = 5
        self.gameOver = False

    def draw(self):
        self.x += self.sx
        self.y += self.sy
        self.bouncePlayer()
        self.bounceWall()
        self.bounceBrick()
        pg.draw.circle(screen, (255,255,255), (self.x, self.y), self.r)
        self.bx = self.x
        self.by = self.y

    def bouncePlayer(self):
        if player.x <= self.x <= player.x+player.w and player.y <= self.y <= player.y+player.h:
            if self.by <= player.y:
                pg.mixer.Sound.play(playerSound)
                self.sy *= -1
                self.y = player.y-1

    def bounceWall(self):
        if self.x < 0:
            self.sx *= -1
            self.x = 0
        elif self.x > width:
            self.sx *= -1
            self.x = width
        elif self.y < 0:
            self.sy *= -1
            self.y = 0
        elif self.y > heigth:
            self.gameOver = True

    def bounceBrick(self):
        global score, scoreSu, scoreCap
        for brick in wall:
            if brick.x <= self.x <= brick.x+brick.w and brick.y <= self.y <= brick.y+brick.h:
                brick.des = True
                if not (brick.x <= self.bx <= brick.x+brick.w):
                    self.sx *= -1
                elif not (brick.y <= self.by <= brick.y+brick.h):
                    self.sy *= -1
                else:
                    self.sx *= -1
                    self.sy *= -1

                if brick.level < self.topLvl:
                    self.topLvl = brick.level
                    player.w = int(player.w * 0.9)

                pg.mixer.Sound.play(brickSound)
                wall.remove(brick)
                score += 2**(5 - brick.level)
                scoreCap = 'Score: ' + str(score)
                scoreSu = font.render(scoreCap, False, (150,150,150))
                break

wall = []
for i in range(6):
    for j in range(13):
        wall.append(Brick(i, j))

player = Player()
ball = Ball()

while(on):
    pg.draw.rect(screen, (0,0,0), (0,0,width,heigth))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            quit()
            on = False

    if ball.gameOver:
        if score > int(highscore):
            highscoreFile = open('highscore', 'w')
            highscoreFile.write(str(score))
            highscoreFile.close()
        quit()

    screen.blit(titleCap, (0,25))
    screen.blit(scoreSu, (350,25))
    screen.blit(highscoreSu, (750,25))
    player.draw()
    ball.draw()

    if len(wall) == 0 and ball.y > 300:
        for i in range(6):
            for j in range(13):
                wall.append(Brick(i, j))
        ball.sx += 2
        ball.sy += 2

    for brick in wall:
        brick.draw()

    pg.display.flip()
    clock.tick(60)
