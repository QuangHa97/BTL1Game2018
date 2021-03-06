
import pygame
import random
import math
pygame.init()

win = pygame.display.set_mode((845, 410))
myfont = pygame.font.SysFont("monospace", 15)
bg = pygame.image.load('background.jpg')
pygame.mixer.music.load('backgroundMusic.mp3')
pygame.mixer.music.play(-1)
#fireSound = pygame.mixer.Sound('fire.wav')
#hitSound = pygame.mixer.Sound('hit.wav')

pygame.display.set_caption("First Game")
clock = pygame.time.Clock()

leftScore = 0
rightScore = 0
# 1-1
# 3-3
gameMode = 3
isDebug = False
isGoal = False
class hitBox(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        return

class recHitBox(hitBox):
    def __init__(self, x, y, width, height):
        hitBox.__init__(self, x, y)
        self.width = width
        self.height = height

    def draw(self):
        if isDebug:
            pygame.draw.rect(win,  pygame.color.THECOLORS["red"], (self.x, self.y, self.width, self.height), 2);
class cirHitBox(hitBox):
    def __init__(self, x, y, rad):
        hitBox.__init__(self, x, y)
        self.rad = rad
    def draw(self):
        if isDebug:
            pygame.draw.circle(win, pygame.color.THECOLORS["red"],(self.x, self.y), self.rad,2)
class ball(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 2
        self.color = pygame.color.THECOLORS["white"]
        self.velocity = [0,0]
        self.isMoving = False
        self.slowCount = 25
        self.hitBox = cirHitBox(x, y, 13)
        self.rad = 11
        self.isShot = False
        self.maximumVelocity = 1000


    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), 11, 0);
        if isDebug:
            pygame.draw.circle(win, pygame.color.THECOLORS["red"], (self.x, self.y), self.hitBox.rad, 2)
        self.hitBox.draw()

    def update(self):

        xdecrease = 0
        ydecrease = 0

        if not self.velocity[0] == 0 or not self.velocity[1] == 0:
            xdecrease = 1/5.0 * (float(abs(self.velocity[0])) / math.sqrt(
                float((self.velocity[0]) * (self.velocity[0])) + float((self.velocity[1]) * (self.velocity[1]))))
            ydecrease = 1/5.0 * (float(abs(self.velocity[1])) / math.sqrt(
                float((self.velocity[0]) * (self.velocity[0])) + float((self.velocity[1]) * (self.velocity[1]))))
        ######### fix ball move

        if not self.isMoving :

            if self.velocity[0] > 0:
                self.velocity[0] -= xdecrease
                if self.velocity[0] < 0:
                    self.velocity[0] = 0
            if self.velocity[0] < 0:
                self.velocity[0] += xdecrease
                if self.velocity[0] > 0:
                    self.velocity[0] = 0
            if self.velocity[1] > 0:
                self.velocity[1] -= ydecrease
                if self.velocity[1] < 0:
                    self.velocity[1] = 0
            if self.velocity[1] < 0:
                self.velocity[1] += ydecrease
                if self.velocity[1] > 0:
                    self.velocity[1] = 0



        if not self.checkIntersectWithBound(ballBound):
           # if not self.checkIntersectWithPlayer(p1):
                self.x += int(self.velocity[0])
                self.y += int(self.velocity[1])


        self.hitBox.x = self.x
        self.hitBox.y = self.y
        self.checkIntersectWithB()
        if self.checkIntersectWithGoalLeft() or self.checkIntersectWithGoalRight():
            self.x = 451
            self.y = 234
            self.velocity = [0,0]

        if (self.isShot):
            if ((self.velocity[0] <= self.maximumVelocity[0] / 2.2) and
                    (self.velocity[1] <= self.maximumVelocity[1] / 2.2)):
                print('Pass')
                changeChar()
                changeCharTwo()
                self.isShot = False


    def checkIntersectWithPlayer(self, temp):
        if (temp.x - self.x) * (temp.x - self.x) + (temp.y - self.y) * (
                temp.y - self.y) < (self.rad + temp.rad + temp.offset) * (self.rad + temp.rad + temp.offset):
            return True
        else:
            return False
    def checkIntersectWithGoalLeft(self):
        global rightScore
        global isGoal
        if self.hitBox.x - self.hitBox.rad + self.velocity[0] <= goalLeftBound.x + goalLeftBound.width and self.y +self.rad > goalLeftBound.y and self.y - self.rad < goalLeftBound.y +goalLeftBound.height:
            rightScore += 1
            isGoal = True
            return True
        else:
            return False
    def checkIntersectWithGoalRight(self):
        global leftScore
        global isGoal
        if self.hitBox.x + self.hitBox.rad + self.velocity[0] >= goalRightBound.x + goalRightBound.width  and self.y + self.rad > goalRightBound.y and self.y - self.rad < goalRightBound.y + goalRightBound.height:
            leftScore += 1
            isGoal = True
            return True
        else:
            return False

    def checkIntersectWithB(self):
        global  b
        for _b in b:
            if (_b.x -  self.x) * (_b.x - self.x) + (_b.y - self.y) * (
                    _b.y - self.y) < (self.rad + _b.rad + 2) * (self.rad + _b.rad + 2):
                self.velocity[0] = -self.velocity[0]
                self.velocity[1] = -self.velocity[1]

    ## check intersect and adjust velocity
    def checkIntersectWithBound(self, temp):
        #with rec
        if self.hitBox.x + self.hitBox.rad + self.velocity[0] >= temp.x + temp.width:
            self.velocity = [-self.velocity[0], self.velocity[1]]
            return True
        elif self.hitBox.x - self.hitBox.rad + self.velocity[0] <= temp.x:
            self.velocity = [-self.velocity[0], self.velocity[1]]
            return True
        elif self.hitBox.y + self.hitBox.rad + self.velocity[1] >= temp.y +temp.height:
            self.velocity = [self.velocity[0], -self.velocity[1]]
            return True
        elif self.hitBox.y - self.hitBox.rad + self.velocity[1] <= temp.y:
            self.velocity = [self.velocity[0], -self.velocity[1]]
            return True
        else:
            return False



class player(object):
    def __init__(self, x, y, color, _group):
        self.x = x
        self.y = y
        self._originalX = x
        self._originalY = y
        self.speed = 4
        self.isSelected = False
        self.color = pygame.color.THECOLORS[color]
        self.velocity = [0,0]
        self.moveState = [0,0,0,0] #Up, down, left, right
        self.isMoving = False
        self.slowCount = 25
        self.hitBox = cirHitBox(x, y, 25)
        self.shotRadius = 40
        self.shotForce = 10
        self.offset = 2
        self.rad = 16
        self.group = _group
        self.randomMove = 0
    def draw(self, win):
        global isGoal
        if (isGoal):
            self.x = self._originalX
            self.y = self._originalY
        pygame.draw.circle(win, self.color, (self.x, self.y), self.rad, 0);
        if self.isSelected:
            pygame.draw.circle(win, pygame.color.THECOLORS["gray"], (self.x, self.y), self.hitBox.rad, 1)
        self.hitBox.draw()
    def setIsMovingUp(self, set):
        self.moveState[0] = 1 if set else 0
    def setIsMovingDown(self, set):
        self.moveState[1] = 1 if set else 0
    def setIsMovingLeft(self, set):
        self.moveState[2] = 1 if set else 0
    def setIsMovingRight(self, set):
        self.moveState[3] = 1 if set else 0

    def move(self):
        if (self.moveState[2] + self.moveState[3] is not 0):
            self.velocity[0] = (-self.moveState[2] + self.moveState[3]) * self.speed // (self.moveState[2] + self.moveState[3])
        else:
            self.velocity[0] = 0
        if (self.moveState[0] + self.moveState[1] is not 0):
            self.velocity[1] = (-self.moveState[0] + self.moveState[1]) * self.speed // (self.moveState[0] + self.moveState[1])
        else:
            self.velocity[1] =0
        #if self.isSelected:
            #print('x velocity ' + str(self.velocity[0]))
            #print('y velocity ' + str(self.velocity[1]))

    def checkIsMoving(self):
        if (sum(self.moveState) == 4):
            self.isMoving = False
        else:
            if ((sum(self.moveState) % 2) == 1):
                self.isMoving = True
            else:
                if (self.moveState[0] == self.moveState[1] or self.moveState[2] == self.moveState[3]):
                    self.isMoving = False
                else:
                    self.isMoving = True

    def checkShotRadius(self,temp):
        if (temp.x - self.x)*(temp.x - self.x) + (temp.y - self.y)*(temp.y - self.y) < self.shotRadius*self.shotRadius:
            return True
        else:
            return False

    def checkIntersectWithBall(self,temp):
        if (temp.x - self.x) * (temp.x - self.x) + (temp.y - self.y) * (
                temp.y - self.y) < (self.rad+ temp.rad+self.offset)*(self.rad +temp.rad +self.offset):
            return True
        else:
            return False
    def shot(self,temp,force):
        if self.checkShotRadius(temp):
            total = (temp.x - self.x) * (temp.x - self.x) + (temp.y - self.y) * (temp.y - self.y)
            shotDirection = [(temp.x - self.x) / math.sqrt(total), (temp.y - self.y) / math.sqrt(total)]
            temp.velocity = [int(shotDirection[0] * force),int(shotDirection[1] * force)]
            temp.maximumVelocity = temp.velocity
            temp.isShot = True
            return True
        else:
            return False

    def update(self):
        self.randomMove += 1

        if not self.isSelected:
            if self.randomMove > 10:
                index = random.randint(0,3)
                if index == 0:
                    self.setIsMovingLeft(not random.getrandbits(1))
                if index == 1:
                    self.setIsMovingRight(not random.getrandbits(1))
                if index == 2:
                    self.setIsMovingUp(not random.getrandbits(1))
                if index == 3:
                    self.setIsMovingDown(not random.getrandbits(1))
                self.move()
                self.randomMove = 0

        # moved by player
        if self.checkIntersectWithBall(_ball):
            if self.velocity[0]>0:
                xdir = 1
            elif self.velocity[0] == 0:
                xdir = 0
            else:
                xdir = -1
            if self.velocity[1]>0:
                ydir = 1
            elif self.velocity[1] == 0:
                ydir = 0
            else:
                ydir = -1
            _ball.velocity = [self.velocity[0]+self.offset*xdir,self.velocity[1]+self.offset*ydir]
            _ball.isMoving = True
        else:
            _ball.isMoving = False

        xdecrease = 0
        ydecrease = 0

        if not self.velocity[0] == 0 or not self.velocity[1] == 0:
            xdecrease = 1 / 5.0 * (float(abs(self.velocity[0])) / math.sqrt(
                float((self.velocity[0]) * (self.velocity[0])) + float((self.velocity[1]) * (self.velocity[1]))))
            ydecrease = 1 / 5.0 * (float(abs(self.velocity[1])) / math.sqrt(
                float((self.velocity[0]) * (self.velocity[0])) + float((self.velocity[1]) * (self.velocity[1]))))
        ######### fix ball move

        if not self.isMoving:

            if self.velocity[0] > 0:
                self.velocity[0] -= xdecrease
                if self.velocity[0] < 0:
                    self.velocity[0] = 0
            if self.velocity[0] < 0:
                self.velocity[0] += xdecrease
                if self.velocity[0] > 0:
                    self.velocity[0] = 0
            if self.velocity[1] > 0:
                self.velocity[1] -= ydecrease
                if self.velocity[1] < 0:
                    self.velocity[1] = 0
            if self.velocity[1] < 0:
                self.velocity[1] += ydecrease
                if self.velocity[1] > 0:
                    self.velocity[1] = 0

        if not self.checkIntersect(bgHitBox):
            if not self.checkIntersectWithBall(_ball):
                if not self.checkIntersectWithOtherPlayer():
                    self.x += int(self.velocity[0])
                    self.y += int(self.velocity[1])


        self.hitBox.x = self.x
        self.hitBox.y = self.y



    def checkIntersectWithOtherPlayer(self):
        global  p
        global pTwo

        for _p in pTwo:
            if (not _p == self) and ((_p.group == self.group and not _p.isSelected) or (not _p.group == self.group )) and (_p.x - self.x - self.velocity[0]) * (_p.x - self.x- self.velocity[0]) + (_p.y - self.y- self.velocity[1]) * (_p.y - self.y  - self.velocity[1]) < (self.rad + _p.rad + self.offset) * (self.rad + _p.rad + self.offset) :
                return True

        for _p in p:
            if (not _p == self) and ((_p.group == self.group and not _p.isSelected) or (not _p.group == self.group )) and (_p.x - self.x - self.velocity[0]) * (_p.x - self.x- self.velocity[0]) + (_p.y - self.y- self.velocity[1]) * (_p.y - self.y  - self.velocity[1]) < (self.rad + _p.rad + self.offset) * (self.rad + _p.rad + self.offset) :
                return True
        return False

    def checkIntersect(self, temp):
        #with rec
        if self.hitBox.x + self.hitBox.rad + self.velocity[0] >= temp.x + temp.width:
            return True
        elif self.hitBox.x - self.hitBox.rad + self.velocity[0] <= temp.x:
            return True
        elif self.hitBox.y + self.hitBox.rad + self.velocity[1] >= temp.y +temp.height:
            return True
        elif self.hitBox.y - self.hitBox.rad + self.velocity[1] <= temp.y:
            return True
        else:
            return False

def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))

b1L = cirHitBox(42+28+15,148+27, 10)
b2L = cirHitBox(42+28+15, 148+27+116,10)
b1R = cirHitBox(785+28 ,148+27,10)
b2R = cirHitBox(785 +28 , 148+27+116, 10)
b = [b1L,b2L,b1R,b2R]
goalLeftBound = recHitBox(42+28,148+27,11,116)
goalRightBound = recHitBox(785+28,148+27,11,116)
bgHitBox = recHitBox(0, 0, 900, 465)
ballBound = recHitBox(50+28, 34+27, 743, 343)


p =  [player(150+28,120+27,"black",1),player(219+28,287+27,"black",1),player(312+28,200+27,"black",1)]
pTwo =  [player(510+28,188+27,"red",2),player(619+28,102+27,"red",2),player(683+28,287+27,"red",2)]
p1 = p[0]
p2 = pTwo[0]
p1.isSelected = True
p2.isSelected = False
_ball = ball(451,234)
leftOfset = 0
rightOfset = 0


def changeCharTwo():
    if gameMode == 1:
        return
    global p2
    global rightOfset
    dis0 = (pTwo[0].x - _ball.x)*(pTwo[0].x - _ball.x) +(pTwo[0].y - _ball.y)*(pTwo[0].y - _ball.y)
    dis1 = (pTwo[1].x - _ball.x) * (pTwo[1].x - _ball.x) + (pTwo[1].y - _ball.y) * (pTwo[1].y - _ball.y)
    dis2 = (pTwo[2].x - _ball.x) * (pTwo[2].x - _ball.x) + (pTwo[2].y - _ball.y) * (pTwo[2].y - _ball.y)

    minDis = 100000*100000
    index = -1
    if dis0 <minDis and not pTwo[0].isSelected :
        minDis = dis0
        index = 0
    if dis1 <minDis and not pTwo[1].isSelected :
        minDis = dis1
        index = 1
    if dis2 <minDis and not pTwo[2].isSelected :
        minDis = dis2
        index = 2
    p2.isSelected = False
    p2 = pTwo[index]
    p2.isSelected = True
    rightOfset = 1
def changeChar():
    if gameMode == 1:
        return
    global p1
    global  leftOfset

    dis0 = (p[0].x - _ball.x)*(p[0].x - _ball.x) +(p[0].y - _ball.y)*(p[0].y - _ball.y)
    dis1 = (p[1].x - _ball.x) * (p[1].x - _ball.x) + (p[1].y - _ball.y) * (p[1].y - _ball.y)
    dis2 = (p[2].x - _ball.x) * (p[2].x - _ball.x) + (p[2].y - _ball.y) * (p[2].y - _ball.y)

    minDis = 100000*100000
    index = -1
    if dis0 <minDis and not p[0].isSelected :
        minDis = dis0
        index = 0
    if dis1 <minDis and not p[1].isSelected :
        minDis = dis1
        index = 1
    if dis2 <minDis and not p[2].isSelected :
        minDis = dis2
        index = 2
    p1.isSelected = False
    p1 = p[index]
    p1.isSelected = True
    leftOfset =1
def redrawGameWindow():
    global isGoal
    win.blit(bg, (0, 0))
    for p1 in p:
        p1.draw(win)

    for p2 in pTwo:
        p2.draw(win)
    ballBound.draw()
    goalRightBound.draw()
    goalLeftBound.draw()
    bgHitBox.draw()
    b1L.draw()
    b2L.draw()
    b2R.draw()
    b1R.draw()
    _ball.draw(win)
    text = ''
    text = text + str(leftScore) + ' - ' + str(rightScore)
    label = myfont.render(text, 1, (255, 255, 0))
    win.blit(label, (726, 15))
    pygame.display.update()
    if (isGoal):
        isGoal = False


# mainloop
run = True
while run:
    clock.tick(27)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()


    if rightOfset > 0:
        rightOfset += 1
    if rightOfset > 27:
        rightOfset = 0

    if leftOfset > 0:
        leftOfset += 1
    if leftOfset > 27:
        leftOfset = 0
    ##1 player
    if keys[pygame.K_1]:
        p2.isSelected = False
    if keys[pygame.K_2]:
        p2.isSelected = True
    #1 vs 1
    if keys[pygame.K_3]:
        gameMode = 1
        p =  [player(150,120,"black",1)]
        p1 = p[0]
        p[0].isSelected = True
        pTwo = [player(510, 188, "red", 2)]
        p2 = pTwo[0]
        pTwo[0].isSelected = True
    if keys[pygame.K_4]:
        isDebug = not isDebug
    #p1 input
    p1.isMoving = False

    if keys[pygame.K_a]:
        p1.setIsMovingLeft(True)
    else:
        p1.setIsMovingLeft(False)

    if keys[pygame.K_d]:
        p1.setIsMovingRight(True)
    else:
        p1.setIsMovingRight(False)

    if keys[pygame.K_w]:
        p1.setIsMovingUp(True)
    else:
        p1.setIsMovingUp(False)

    if keys[pygame.K_s]:
        p1.setIsMovingDown(True)
    else:
        p1.setIsMovingDown(False)

    p1.checkIsMoving()
    if p1.isMoving:
        p1.move()

    if leftOfset == 0:
        if keys[pygame.K_v]:
            p1.shot(_ball,15)
            p1.isMoving = False

        if keys[pygame.K_b]:
            p1.shot(_ball,20)
            p1.isMoving = False

        if keys[pygame.K_q]:
            p1.isMoving = False
            changeChar()

    #p2 input

    p2.isMoving = False

    if keys[pygame.K_LEFT]:
        p2.setIsMovingLeft(True)
    else:
        p2.setIsMovingLeft(False)

    if keys[pygame.K_RIGHT]:
        p2.setIsMovingRight(True)
    else:
        p2.setIsMovingRight(False)

    if keys[pygame.K_UP]:
        p2.setIsMovingUp(True)
    else:
        p2.setIsMovingUp(False)

    if keys[pygame.K_DOWN]:
        p2.setIsMovingDown(True)
    else:
        p2.setIsMovingDown(False)

    p2.checkIsMoving()
    if p2.isMoving:
        p2.move()

    if rightOfset == 0:
        if keys[pygame.K_KP1]:
            p2.shot(_ball, 15)
            p2.isMoving = False

        if keys[pygame.K_KP2]:
            p2.shot(_ball, 20)
            p2.isMoving = False

        if keys[pygame.K_KP3]:
            p2.isMoving = False
            changeCharTwo()

    #update

    for _p in p:
        _p.update()
    for _p in pTwo:
        _p.update()
    _ball.update()
    redrawGameWindow()

pygame.quit()

