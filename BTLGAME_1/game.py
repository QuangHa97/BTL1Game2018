import pygame
import random
import math
pygame.init()


def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))

win = pygame.display.set_mode((900, 600))
myfont = pygame.font.SysFont("monospace", 15)
pygame.mixer.music.load('backgroundMusic.mp3')
pygame.mixer.music.play(-1)
fireSound = pygame.mixer.Sound('fire.wav')
hitSound = pygame.mixer.Sound('hit.wav')

pygame.display.set_caption("First Game")
bg = pygame.image.load('background.jpg')
accuracy = pygame.image.load('accuracy.png')
walkRight = [pygame.image.load('crouch1.png'), pygame.image.load('crouch2.png'), pygame.image.load('crouch3.png'),
             pygame.image.load('crouch4.png'), pygame.image.load('crouch5.png'), pygame.image.load('crouch6.png'),
             pygame.image.load('crouch7.png'), pygame.image.load('crouch8.png'), pygame.image.load('crouch9.png')]
walkLeft = [pygame.image.load('crouch1.png'), pygame.image.load('crouch2.png'), pygame.image.load('crouch3.png'),
             pygame.image.load('crouch4.png'), pygame.image.load('crouch5.png'), pygame.image.load('crouch6.png'),
             pygame.image.load('crouch7.png'), pygame.image.load('crouch8.png'), pygame.image.load('crouch9.png')]
doorOpen = [pygame.image.load('DoorLocked.png'), pygame.image.load('DoorUnlocked.png'), pygame.image.load('DoorOpen.png')]
die = [pygame.image.load('die1.png'), pygame.image.load('die2.png'), pygame.image.load('die3.png'), pygame.image.load('die4.png'),pygame.image.load('die5.png')]
char = pygame.image.load('idle.png')
gunarm = pygame.image.load('gun.png')
aimimage = pygame.image.load('aim.png')
aim = pygame.image.load('aim.png')
aimshot = pygame.image.load('aimshot.png')
shotdelay = -1
clock = pygame.time.Clock()

miss = 0
hit = 0
class door(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.frameCount = 0

    def draw(self, win):
        if self.frameCount +1 >= 3*27:
            self.frameCount = 0
        if self.frameCount <= 1*27:
            man.invisible()
            win.blit(doorOpen[0], (self.x, self.y))
        elif self.frameCount <= 2*27:
            win.blit(doorOpen[1], (self.x, self.y))
        else:
            if self.frameCount == 2*27+1 :
                man.changePosition()

            win.blit(doorOpen[2], (self.x, self.y))

        self.frameCount += 1

class enemy(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.left = False
        self.right = False
        self.walkCount = 0
        self.jumpCount = 10
        self.isDead = False
        self.deadCount = 0
    def changePosition(self):
        index = random.randint(0, 4)
        self.x = enemyPosition[index][0]
        self.y = enemyPosition[index][1]

    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0
        if self.deadCount + 1 >= 40:
            self.deadCount = 0
            self.isDead = False
            self.invisible()
        if not self.isDead:
            win.blit(char, (self.x, self.y))
            self.walkCount += 1
        else:
            win.blit(die[self.deadCount//8], (self.x,  self.y))
            self.deadCount += 1
    def kill(self):
        self.isDead = True

    def invisible(self):
        if not self.isDead:
            self.x = 1000
            self.y = 1000

def redrawGameWindow():
    win.blit(bg, (0, 0))

    door1.draw(win)
    door2.draw(win)
    door3.draw(win)
    door4.draw(win)
    door5.draw(win)
    man.draw(win)
    win.blit(accuracy, (50, 530))
    # calcylate gunarm angle

    win.blit(gunarm, ( min(pygame.mouse.get_pos()[0],900-175), 500))
    text = ''
    if hit == 0 and miss == 0:
        text = text + str(100.0) + '%'
    else:
        text = text + str("{0:.2f}".format((hit*100.0/(hit + miss)))) + '%'
    label = myfont.render(text, 1, (255, 255, 0))
    win.blit(label, (120, 550))
    win.blit(aimimage, (pygame.mouse.get_pos()[0]-32,pygame.mouse.get_pos()[1]-32))
    pygame.display.update()


# mainloop
enemyPosition = [[376+13-23, 18+90-64], [0+13-23, 348 + 90-64], [495+13-23, 352+90-64], [694+13-23, 268+90-64], [841+13-23, 20+90-64]]
man = enemy(200, 410, 64, 64)
door1 = door(376, 18, 90, 150)
door2 = door(0, 348, 90, 150)
door3 = door(495, 352, 90, 150)
door4 = door(694, 268, 90, 150)
door5 = door(841, 20, 90, 150)
run = True
while run:
    clock.tick(27)
    if shotdelay >= 0:
        shotdelay -= 1
    if shotdelay == 0:
        aimimage = aim
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            fireSound.play()
            aimimage = aimshot
            shotdelay = 3
            pos = pygame.mouse.get_pos()
            if not man.isDead:
                if (pos[0] - man.x - 32) * (pos[0] - man.x - 32) + (pos[1] - man.y - 32) * (pos[1] - man.y - 32) <= 64 * 64:
                    man.kill()
                    hitSound.play()
                    hit += 1
                else:
                    miss += 1
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False

    redrawGameWindow()

pygame.quit()


