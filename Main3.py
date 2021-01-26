import pygame

# import random
# import time
# from pygame.locals import *

pygame.init()
scrx, scry = 1170, 780
screen = pygame.display.set_mode((scrx, scry))
pygame.display.set_caption("Tower battle")
screen.fill((255, 255, 255))
pygame.display.update()


class images:
    Icon = pygame.image.load('C:/Users/ayash/PycharmProjects/TowerBattles/RedStillL.png')
    Red = [pygame.image.load('C:/Users/ayash/PycharmProjects/TowerBattles/RedStillL.png'),
           pygame.image.load('C:/Users/ayash/PycharmProjects/TowerBattles/RedStillR.png')]
    RedWalkR = [pygame.image.load('C:/Users/ayash/PycharmProjects/TowerBattles/RedWalkR1.png'),
                pygame.image.load('C:/Users/ayash/PycharmProjects/TowerBattles/RedWalkR2.png')]
    RedWalkL = [pygame.image.load('C:/Users/ayash/PycharmProjects/TowerBattles/RedWalkL1.png'),
                pygame.image.load('C:/Users/ayash/PycharmProjects/TowerBattles/RedWalkL2.png')]
    Blue = [pygame.image.load('C:/Users/ayash/PycharmProjects/TowerBattles/BlueStillL.png'),
            pygame.image.load('C:/Users/ayash/PycharmProjects/TowerBattles/BlueStillR.png')]
    wall = pygame.image.load('C:/Users/ayash/PycharmProjects/TowerBattles/Wall.png')
    cwall = pygame.image.load('C:/Users/ayash/PycharmProjects/TowerBattles/CreateWall.png')


pygame.display.set_icon(images.Icon)
pygame.display.update()

Game = 1
wall_r = 39


class Player:
    def __init__(self, WalkR, WalkL, Sprites, x, y):
        self.x, self.y = x, y

        self.Walk_Sprites = Sprites
        self.currSprite = self.Walk_Sprites[0]

        self.isJump = False
        self.JumpC = 15

        self.Gravity = False
        self.Fall = 0
        self.fall_by = .60
        self.Gint = 6

        self.run = True
        self.Speed = 4
        self.dir = "right"
        self.walkC = 0
        self.WalkR = WalkR
        self.WalkL = WalkL
        self.bpress = False

    def left(self):

        for coord in wallright:
            if coord[0] >= self.x - 38 >= coord[0] - self.Speed and coord[1] < self.y < coord[2]:
                self.x = coord[0] + 38
                self.currSprite = self.Walk_Sprites[0]
                self.run = False
                break
        if self.run:
            self.currSprite = self.Walk_Sprites[0]
            self.x -= self.Speed
            self.walkC += 1
        self.run = True
        self.dir = "left"

    def right(self):
        for coord in wallleft:
            if coord[0] <= self.x + 38 <= coord[0] + self.Speed and coord[1] < self.y < coord[2]:
                self.x = coord[0] - 38
                self.currSprite = self.Walk_Sprites[1]
                self.run = False
                break
        if self.run:
            self.currSprite = self.Walk_Sprites[1]
            self.x += self.Speed
            self.walkC += 1
        self.run = True
        self.dir = "right"

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
        # print(scry, self.y+39, scry + self.Fall)
        if scry <= self.y + 36 <= scry + self.Fall:
            self.y = scry - 37
            self.Gravity = False
            if self.JumpC == -1:
                self.JumpC = 15
                self.isJump = False
            self.Fall = 0
            return
        for wall in wL:
            if pygame.Rect(self.x + 3, self.y+3, 30, 37).colliderect(pygame.Rect(wall.x, wall.y, 39, 39)) or self.y == scry - 39:
                self.y = wall.y - 37
                self.Gravity = False
                if self.JumpC == -1:
                    self.JumpC = 15
                    self.isJump = False
                self.Fall = 0
                break

        if self.Gravity:
            self.Fall += self.fall_by

    def block(self):
        global doneW, wall_r
        if self.bpress:
            return
        # print(doneW)
        if [wall_r * round(self.x / wall_r), wall_r * round((self.y + wall_r) / wall_r)] not in doneW:
            # doneW.append([40 * round(self.x / 40), 40 * round((self.y + 40) / 40)])
            wL.append(Wall(self.x, self.y + 40, create=True))
            print(len(wL))
            self.bpress = True

        # if

    def update(self):
        if self.walkC > 12:
            self.walkC = 0
        if self.dir == "right":
            self.currSprite = self.WalkR[round(self.walkC / 12)]
        if self.dir == "left":
            self.currSprite = self.WalkL[round(self.walkC / 12)]

        screen.blit(self.currSprite, (self.x, self.y))


walltop = [[scry, 0 - 30, scrx]]
wallleft = [[scrx, 0, scry]]
wallright = [[-40, 0, scry]]
wallbottom = [[0, 0 - 30, scrx]]
doneW = []


class Wall:
    def __init__(self, x, y, create=False):
        self.wall_r = wall_r
        self.sprite = images.wall
        if create:
            self.sprite = images.cwall
        self.x, self.y = self.wall_r * round(x / self.wall_r), self.wall_r * round(y / self.wall_r)

        walltop.append([self.y, self.x - 36, self.x + 36])
        wallbottom.append([self.y, self.x - 36, self.x + 36])
        wallleft.append([self.x, self.y - 35, self.y + 35])
        wallright.append([self.x, self.y - 35, self.y + 35])

        doneW.append([self.x, self.y])

    def update(self):
        screen.blit(self.sprite, (self.x, self.y))


def lava():
    global wall_r
    for wall in wL:
        wall.y += wall_r


p1 = Player(
    images.RedWalkR,
    images.RedWalkL,
    images.Red,
    350,
    500)
p2 = Player(
    images.RedWalkR,
    images.RedWalkL,
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
LAVA = pygame.USEREVENT + 1
pygame.time.set_timer(LAVA, 3000)

while Game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Game = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_s:
                p1.bpress = False
            if event.key == pygame.K_DOWN:
                p2.bpress = False
        if event.type == LAVA:
            print("LAVA")
            lava()
    keyD = pygame.key.get_pressed()

    if keyD[pygame.K_a]:
        p1.left()
    if keyD[pygame.K_d]:
        p1.right()
    if keyD[pygame.K_s]:
        p1.block()
    p1.jump(pygame.K_w)
    p1.gravity()

    if keyD[pygame.K_LEFT]:
        p2.left()
    if keyD[pygame.K_RIGHT]:
        p2.right()
    if keyD[pygame.K_DOWN]:
        p2.block()
    p2.jump(pygame.K_UP)
    p2.gravity()

    screen.fill((255, 255, 255))

    pygame.time.delay(20)
    if len(wL) > 0:
        for WL in wL:
            WL.update()
    p1.update()
    p2.update()
    pygame.display.update()
