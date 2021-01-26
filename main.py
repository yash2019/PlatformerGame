import pygame

# import random
# import time
# from pygame.locals import *

pygame.init()
scrx, scry = 1200, 680
screen = pygame.display.set_mode((scrx, scry))
pygame.display.set_caption("Tower battle")
screen.fill((255, 255, 255))
pygame.display.update()


class images:
    Icon = pygame.image.load('RedStillL.png')
    Red = [pygame.image.load('RedStillL.png'),
           pygame.image.load('RedStillR.png')]
    Blue = [pygame.image.load('BlueStillL.png'),
            pygame.image.load('BlueStillR.png')]
    wall = pygame.image.load('wall.png')
    cwall = pygame.image.load('CreateWall.png')


pygame.display.set_icon(images.Icon)
pygame.display.update()

Game = 1


class Player:
    def __init__(self, Sprites, x, y):
        self.x, self.y = x, y

        self.Sprites = Sprites
        self.currSprite = self.Sprites[0]

        self.isJump = False
        self.JumpC = 15

        self.Gravity = False
        self.Fall = 0
        self.Gint = 6

        self.run = True
        self.Speed = 4

        self.bpress = False

    def left(self):
        for coord in wallright:
            if coord[0] >= self.x - 40 >= coord[0] - self.Speed and coord[1] < self.y < coord[2]:
                self.x = coord[0] + 40
                self.currSprite = self.Sprites[0]
                self.run = False
                break
        if self.run:
            self.currSprite = self.Sprites[0]
            self.x -= self.Speed

        self.run = True

    def right(self):
        for coord in wallleft:
            if coord[0] <= self.x + 38 <= coord[0] + self.Speed and coord[1] < self.y < coord[2]:
                self.x = coord[0] - 38
                self.currSprite = self.Sprites[1]
                self.run = False
                break
        if self.run:
            self.currSprite = self.Sprites[1]
            self.x += self.Speed
        self.run = True

    def jump(self, KEY):
        if not self.Gravity and not self.isJump:
            if keyD[KEY]:
                self.isJump = True

        elif self.isJump:
            if self.JumpC >= 0:
                self.y -= (self.JumpC ** 2) / self.Gint
                self.JumpC -= 1

            for coord in wallbottom:
                if coord[0] >= self.y - 40 >= (coord[0] - ((self.JumpC + 1) ** 2) / self.Gint) and coord[1] <= self.x <= \
                        coord[2]:
                    self.JumpC = 0
                    self.y = coord[0] + 40
                    self.isJump = False

    def gravity(self):

        self.Gravity = True
        self.y += self.Fall
        for coor in walltop:
            if coor[0] <= self.y + 36 <= coor[0] + self.Fall and coor[1] <= self.x <= coor[2]:
                self.y = coor[0] - 36
                self.Gravity = False
                if self.JumpC == -1:
                    self.JumpC = 15
                    self.isJump = False
                self.Fall = 0
                break

        if self.Gravity:
            self.Fall += 0.55

    def block(self):
        global doneW
        if self.bpress:
            return
        # print(doneW)
        if [40 * round(self.x / 40), 40 * round((self.y + 40) / 40)] not in doneW:
            # doneW.append([40 * round(self.x / 40), 40 * round((self.y + 40) / 40)])
            wL.append(Wall(40 * round(self.x / 40), 40 * round((self.y + 40) / 40)))
            print(len(wL))
            self.bpress = True

    def update(self):
        screen.blit(self.currSprite, (self.x, self.y))


walltop = [[scry, 0 - 15, scrx]]
wallleft = [[scrx, 0, scry]]
wallright = [[-40, 0, scry]]
wallbottom = [[0, 0, scrx]]
doneW = []


class Wall:
    def __init__(self, x, y):
        self.x, self.y = 40 * round(x / 40), 40 * round(y / 40)

        walltop.append([self.y, self.x - 36, self.x + 36])
        wallbottom.append([self.y, self.x - 36, self.x + 36])
        wallleft.append([self.x, self.y - 35, self.y + 35])
        wallright.append([self.x, self.y - 35, self.y + 35])

        doneW.append([self.x, self.y])

    def update(self):
        screen.blit(images.wall, (self.x, self.y))


p1 = Player(
    images.Red,
    350,
    500)
p2 = Player(
    images.Blue,
    400,
    500)

wL = [Wall(scrx - 610, scry - 40)]
'''
      Wall(scrx - 600, scry - 80),
      Wall(scrx - 600, scry - 120),
      Wall(scrx - 600, scry - 160),
      # Wall(scrx - 600, scry - 200),
      # dWall(scrx - 600, scry - 240),

      Wall(scrx - 560, scry - 120),
      Wall(scrx - 520, scry - 80),

      Wall(scrx - 900, scry - 40),
      Wall(scrx - 860, scry - 40)'''

while Game:
    pygame.time.delay(20)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Game = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_s:
                p1.bpress = False
            if event.key == pygame.K_DOWN:
                p2.bpress = False
    keyD = pygame.key.get_pressed()

    if keyD[pygame.K_a]:
        p1.left()
    if keyD[pygame.K_d]:
        p1.right()
    p1.jump(pygame.K_w)
    p1.gravity()
    if keyD[pygame.K_s]:
        p1.block()

    if keyD[pygame.K_LEFT]:
        p2.left()
    if keyD[pygame.K_RIGHT]:
        p2.right()
    p2.jump(pygame.K_UP)
    p2.gravity()
    if keyD[pygame.K_DOWN]:
        p2.block()

    screen.fill((255, 255, 255))
    if len(wL) > 0:
        for WL in wL:
            WL.update()
    p1.update()
    p2.update()
    pygame.display.update()
