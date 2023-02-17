import pygame
import time
import random
import string
import sys
from pygame.locals import QUIT
pygame.init()
screen=pygame.display.set_mode((500,1000))
pygame.display.set_caption('Space Invaders')
white=(255,255,255)
red=(255,0,0)
orange=(255, 127, 0)
yellow=(238,230,0) 
green=(124,252,0)
blue=(75, 139, 190)
purple= (230,230,250)
black=(0,0,0)
clock = pygame.time.Clock()
Alien1 = pygame.image.load("alien1.png")
Alien1 = pygame.transform.scale(Alien1,(50,50))
timer = 0
saCount = 0
gameLoop = True
mr=False
ml=False

def SpawnSuperAlien(x,y):
  SuperAliensList.append(SuperAlien(x,y,pygame.image.load("superalien1.jpg"),75,50,3,True,3))

def show_text(msg,x,y,color,size):
    fontobj= pygame.font.SysFont('freesans', size)
    msgobj = fontobj.render(msg,False,color)
    screen.blit(msgobj,(x, y))
    
class Character:
    def __init__(self, x, y, image, length, width):
        self.x=x
        self.y=y
        self.image=image
        self.length=length
        self.width=width
    def Draw (self):
        self.image = pygame.transform.scale(self.image,(self.length,self.width))
        screen.blit(self.image,(self.x,self.y))
        
class Alien(Character):
    def __init__(self, x, y, image, length, width, speed, alive):
        Character.__init__(self, x, y, image, length, width)
        self.alive=alive
        self.speed=speed
    def Draw (self):
        self.image = pygame.transform.scale(self.image,(self.length,self.width))
        if self.alive==False:
            self.image = pygame.transform.scale(self.image,(0,0))
        screen.blit(self.image,(self.x,self.y))
    def MoveAlien(self):
        self.x += self.speed
    def Check(self):
        if self.x > 450:
            for x in AliensList:
                x.CollisionRight()
        if self.x < 0:
            for x in AliensList:
                x.CollisionLeft()
    def CollisionRight(self):
        self.speed=-2
        self.y+=2
    def CollisionLeft(self):
        self.speed=2
        self.y+=2

class Player(Alien):
    def __init__(self, x, y, image, length, width, speed, alive):
        Alien.__init__(self, x, y, image, length, width, speed, alive)
    def Draw (self):
        self.image = pygame.transform.scale(self.image,(self.length,self.width))
        screen.blit(self.image,(self.x,self.y))
    def MovePlayerRight (self):
        self.x+=self.speed
        self.speed=7
        if self.x >= 450:
            self.speed=0
        
    def MovePlayerLeft (self):
        self.x+=self.speed
        self.speed=-7
        if self.x <= 0:
            self.speed=0
        

class Bullet(Alien):
    def __init__(self, x, y, image, length, width, speed, alive):
        Alien.__init__(self, x, y, image, length, width, speed, alive)
    def Draw (self):
        self.image = pygame.transform.scale(self.image,(self.length,self.width))
        screen.blit(self.image,(self.x,self.y))
    def Move (self):
        if self.y > 0:
            self.y-=20
            self.Draw()
        if self.y <= 0:
          BulletList.clear()
    def Check(self,xalien,yalien,alien):
      if self.x in range(xalien,xalien+25) and self.y in range(yalien,yalien+25):
        BulletList.pop(0)
        AliensList.remove(alien)

class SuperAlien(Alien):
    def __init__(self, x, y, image, length, width, speed, alive, health):
        Alien.__init__(self, x, y, image, length, width, speed, alive)
        self.health = health
    def Draw (self):
        self.image = pygame.transform.scale(self.image,(self.length,self.width))
        if self.alive==False:
            self.image = pygame.transform.scale(self.image,(0,0))
        screen.blit(self.image,(self.x,self.y))
    def MoveAlien(self):
        self.x += self.speed
    def CheckCol(self):
        if self.x > 450:
            self.speed=-3
            self.y+=5
        if self.x < 0:
            self.speed=3
            self.y+=5
    def Check(self,xbullet,ybullet):
        if xbullet in range(self.x,self.x+75) and ybullet in range(self.y,self.y+50):
            BulletList.clear()
            self.health-=1
        if self.health <= 0:
            SuperAliensList.remove(self)
    
            
player=Player(225,800,pygame.image.load("ship.png"),50,50,0,True)
AliensList=[]
BulletList=[]
SuperAliensList=[]

for y in range (1,6,1):
  for x in range (1,9,1):
    pic=pygame.image.load("alien1.png")
    alien=Alien(x*50,y*50,pic,25,25,2,True)
    AliensList.append(alien)
    
while gameLoop == True:
  screen.fill(black)
  if mr == True:
    player.MovePlayerRight()
    ml=False
  if ml == True:
    player.MovePlayerLeft()
    mr=False
  if timer > 1000 and saCount <= 3:
    timer=0
    saCount+=1
    SpawnSuperAlien(50,50)
  for a in BulletList: 
    a.Move()
  for a in AliensList:
    for b in BulletList:
      b.Check(a.x,a.y,a)
  for a in BulletList:
    for b in SuperAliensList:
      b.Check(a.x,a.y)
  for a in AliensList:
    a.MoveAlien()
    a.Draw()
  for a in SuperAliensList:
    a.MoveAlien()
    a.Draw()
  for a in AliensList:
    a.Check()
  for a in SuperAliensList:
    a.CheckCol()
  player.Draw()
  for a in AliensList:
    if a.y >= 775:
      screen.fill(white)
      show_text("Game Over",190,500,red,20)
      pygame.display.update()
      gameLoop=False
      break
  clock.tick(50)
  timer+=1
##=============== EVENTS ============================
  pygame.display.update()
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit()
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_d:
        mr=True
      if event.key == pygame.K_a:
        ml=True
      if event.key == pygame.K_SPACE:
        if len(BulletList) <= 1:
          BulletList.append(Bullet(player.x+23,800,pygame.image.load("bullet.png"),5,25,20,True))
          a.Draw()
    if event.type == pygame.KEYUP:
      if event.key == pygame.K_d:
        mr=False
      if event.key == pygame.K_a:
        ml=False