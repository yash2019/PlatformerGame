import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame

# import random
# import time
# from pygame.locals import *

pygame.init()
scrx, scry = 1170, 780
screen = pygame.display.set_mode((scrx, scry))
mainSurf = pygame.Surface((scrx, scrx))
scry -= 117
pygame.display.set_caption("Tower battle")
mainSurf.fill((255, 255, 255))
pygame.display.update()

isLava = 0


class images:
    Icon = pygame.image.load('C:/Users/ayash/PycharmProjects/TowerBattles/RedStillR.png')
    Red = [pygame.image.load('C:/Users/ayash/PycharmProjects/TowerBattles/RedStillL.png'),
           pygame.image.load('C:/Users/ayash/PycharmProjects/TowerBattles/RedStillR.png')]
    RedWalkR = [pygame.image.load('C:/Users/ayash/PycharmProjects/TowerBattles/RedWalkR1.png'),
                pygame.image.load('C:/Users/ayash/PycharmProjects/TowerBattles/RedWalkR2.png')]
    RedWalkL = [pygame.image.load('C:/Users/ayash/PycharmProjects/TowerBattles/RedWalkL1.png'),
                pygame.image.load('C:/Users/ayash/PycharmProjects/TowerBattles/RedWalkL2.png')]

    Blue = [pygame.image.load('C:/Users/ayash/PycharmProjects/TowerBattles/BlueStillL.png'),
            pygame.image.load('C:/Users/ayash/PycharmProjects/TowerBattles/BlueStillR.png')]
    BlueWalkR = [pygame.image.load('C:/Users/ayash/PycharmProjects/TowerBattles/BlueWalkR1.png'),
                 pygame.image.load('C:/Users/ayash/PycharmProjects/TowerBattles/BlueWalkR2.png')]
    BlueWalkL = [pygame.image.load('C:/Users/ayash/PycharmProjects/TowerBattles/BlueWalkL1.png'),
                 pygame.image.load('C:/Users/ayash/PycharmProjects/TowerBattles/BlueWalkL2.png')]

    wall = pygame.image.load('C:/Users/ayash/PycharmProjects/TowerBattles/Wall.png')
    cwall = pygame.image.load('C:/Users/ayash/PycharmProjects/TowerBattles/CreateWall.png')

    Mystery = [pygame.image.load('C:/Users/ayash/PycharmProjects/TowerBattles/Mystery1.png')]
    iLava = [pygame.image.load('C:/Users/ayash/PycharmProjects/TowerBattles/Lava1.png')]

    iBullet = [pygame.image.load('C:/Users/ayash/PycharmProjects/TowerBattles/Bullet.png')]
    iCoin = [pygame.image.load('C:/Users/ayash/PycharmProjects/TowerBattles/coin.png')]


pygame.display.set_icon(images.Icon)
pygame.display.update()

Game = 1
wall_r = 39
bSpeed = 10


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

        self.bDown = False

    def left(self):

        if self.x < 0 + self.Speed:
            self.x = 0
            self.run = False

        for wall in wL:
            if wall.y < self.y and pygame.Rect(self.x, self.y, wall_r, wall_r).colliderect(
                    pygame.Rect(wall.x + 2, wall.y, wall_r, wall_r)):
                self.x = wall.x + wall_r
                self.currSprite = self.Walk_Sprites[1]
                self.run = False
                break

        if self.run:
            self.currSprite = self.Walk_Sprites[0]
            self.x -= self.Speed
            self.walkC += 1
        self.run = True
        self.dir = "left"

    def right(self):

        if self.x > scrx - 37 - self.Speed:
            self.x = scrx - 37
            self.run = False

        for wall in wL:
            if wall.y < self.y and pygame.Rect(self.x + 10, self.y, wall_r, wall_r).colliderect(
                    pygame.Rect(wall.x, wall.y, 39, 39)):
                self.x = wall.x - wall_r + 1
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

            if self.y <= 0:
                self.y = 0
                self.isJump = False
                self.JumpC = 0

            for wall in wL:
                if wall.y < self.y and pygame.Rect(self.x - 2, self.y, wall_r, wall_r).colliderect(
                        pygame.Rect(wall.x, wall.y, 39 - 2, 39)):
                    self.JumpC = 0
                    self.y = wall.y + wall_r
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
            if wall.y > self.y and pygame.Rect(self.x, self.y, wall_r, wall_r).colliderect(
                    pygame.Rect(wall.x + 1, wall.y, 39 - 1, 39)):
                self.y = wall.y - wall_r + 2
                self.Gravity = False
                if self.JumpC == -1:
                    self.JumpC = 15
                    self.isJump = False
                self.Fall = 0
                break

        if self.Gravity:
            self.Fall += self.fall_by

    def shoot(self):
        # print("Shoot")
        self.bDown = True
        bullets.append(Bullet(self.dir, self.x, self.y))
        print(len(bullets))

    def block(self):
        global wall_r
        if self.bpress:
            return

        for wall in wL:
            if wall.x == wall_r * round(self.x / wall_r) and wall.y == wall_r * round((self.y + 37) / wall_r):
                return

        wL.append(Wall(wall_r * round(self.x / wall_r), wall_r * round(self.y / wall_r), create=True))

        self.bpress = True

    def update(self):
        if self.walkC > 12:
            self.walkC = 0
        if self.dir == "right":
            self.currSprite = self.WalkR[round(self.walkC / 12)]
        if self.dir == "left":
            self.currSprite = self.WalkL[round(self.walkC / 12)]

        mainSurf.blit(self.currSprite, (self.x, self.y))


class Bullet:
    def __init__(self, direction, x, y):
        self.x = x
        self.y = y
        if direction == "left":
            self.bSpeed = -bSpeed
            pass
        else:
            self.bSpeed = bSpeed
            pass

    def move(self):
        self.x += self.bSpeed
        mainSurf.blit(images.iCoin[0], (self.x, self.y))

        if self.x > scrx or self.x < 0:
            bullets.remove(self)

        for wall in wL:
            if pygame.Rect(self.x, self.y, 15, 15).colliderect(pygame.Rect(wall.x, wall.y, wall_r, wall_r)):
                bullets.remove(self)
                break


bullets = []


class Wall:
    def __init__(self, x, y, create=False):
        self.create = create
        self.wall_r = wall_r
        self.sprite = images.wall
        if create:
            self.sprite = images.cwall
        self.x, self.y = wall_r * round(x / wall_r), wall_r * round((y + 37) / wall_r)

    def update(self):
        mainSurf.blit(self.sprite, (self.x, self.y))


wL = [Wall(scrx - 610, scry - 40),
      Wall(scrx - 600, scry - 80),
      Wall(scrx - 600, scry - 120),
      Wall(scrx - 600, scry - 160),
      # Wall(scrx - 600, scry - 200),
      # Wall(scrx - 600, scry - 240),s

      Wall(scrx - 560, scry - 120),
      Wall(scrx - 520, scry - 80),

      Wall(scrx - 900, scry - 40),
      Wall(scrx - 860, scry - 40)]


def lava():
    global wL, wall_r
    for wall in wL:
        wall.y += wall_r
    wL = [Wall(wallLoop.x, wallLoop.y - wall_r, wallLoop.create) for wallLoop in wL if wallLoop.y < scry]
    # aRwall = random.randint(0, round(scrx / wall_r))
    # print(len(wL))
    # print(Rwall)


p1 = Player(
    images.RedWalkR,
    images.RedWalkL,
    images.Red,
    350,
    500)
p2 = Player(
    images.BlueWalkR,
    images.BlueWalkL,
    images.Blue,
    400,
    500)

for WL in range(0, scrx, wall_r):
    wL.append(Wall(WL, scry - wall_r * 2))

LAVA = pygame.USEREVENT + 1
pygame.time.set_timer(LAVA, 3000)
Lavain = False
while Game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Game = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_s:
                p1.bpress = False
            if event.key == pygame.K_DOWN:
                p2.bpress = False
            if event.key == pygame.K_LSHIFT:
                p1.bDown = False
            if event.key == pygame.K_RSHIFT:
                p2.bDown = False
        if event.type == LAVA and isLava:
            Lavain = True
            lava()

    keyD = pygame.key.get_pressed()

    if keyD[pygame.K_a]: p1.left()
    if keyD[pygame.K_d]: p1.right()
    if keyD[pygame.K_s]: p1.block()
    if keyD[pygame.K_LSHIFT] and not p1.bDown: p1.shoot()

    p1.jump(pygame.K_w)
    p1.gravity()

    if keyD[pygame.K_LEFT]: p2.left()
    if keyD[pygame.K_RIGHT]: p2.right()
    if keyD[pygame.K_DOWN]: p2.block()
    if keyD[pygame.K_RSHIFT] and not p2.bDown: p2.shoot()

    p2.jump(pygame.K_UP)
    p2.gravity()

    mainSurf.fill((255, 255, 255))

    pygame.time.delay(10)
    if len(wL) > 0:
        for WL in wL:
            WL.update()
    if Lavain:
        for lImage in range(0, scrx, 40):
            mainSurf.blit(images.iLava[0], (lImage, scry - 40))
    mainSurf.blit(images.Mystery[0], (40, 79))
    for bullet in bullets:
        bullet.move()

    p1.update()
    p2.update()
    screen.blit(mainSurf, (0, 0))
    pygame.display.update()
