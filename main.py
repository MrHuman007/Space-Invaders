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
        if self.x > 450:
            self.speed=0
        self.speed=5
    def MovePlayerLeft (self):
        self.x+=self.speed
        if self.x < 0:
            self.speed=0
        self.speed=-5

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
    
while True:
  screen.fill(black)
  if timer > 1000:
    timer=0
    SuperAliensList.append(SuperAlien(50,50,pygame.image.load("superalien1.jpg"),75,50,3,True,3))
  if len(AliensList)==-1:
    screen.fill(white)
    show_text("Game Over",250,500,red,20)
    pygame.display.update()
    break
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
        player.MovePlayerRight()
      if event.key == pygame.K_a:
        player.MovePlayerLeft()
      if event.key == pygame.K_SPACE:
        if len(BulletList) <= 0:
          BulletList.append(Bullet(player.x+23,800,pygame.image.load("bullet.png"),5,25,20,True))
          a.Draw()