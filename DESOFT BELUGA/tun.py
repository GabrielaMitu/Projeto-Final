#!/usr/bin/python2.7
# Encoding: utf-8

# System:
import pygame
import sys
import math
import random
from pygame.locals import *

# Gra:
import GameModule
from GameModule.Models import *
from GameModule.Constants import *

class Game:
  def playSound( self, fileName ):
    sound = pygame.mixer.Sound(fileName)
    sound.play()
    
  def __init__(self):
    pygame.init()
    pygame.mixer.init(11025)

    # Bardzo ważne pole klasy, definiujące nam aktualny stan gry - od tego zależy jak będą przetwarzane zdarzenia itp.
    self.actualState = states["START"]

    self.display = pygame.display.set_mode( gfx["screen"] )
    pygame.display.set_caption( "Arkanoid v" + version )
    # Mamy 4 podstawowe obiekty, które tworzą nam grę
    ## Painter - rysujący na ekran aktualną klatkę gry.
    ## Mapper - odpowiadający za ładowanie mapy.
    ## Status - przechowujący stan aktualny gry - punkty, życia, aktualnie działające efekty itp.
    ## Objects - przechowujący aktualne obiekty w grze - kulki, bloczki, paletkę itp.

    self.objects = GameModule.Objects() 
    self.mapper =  GameModule.Mapper( self.objects )
    self.status =  Status()
    self.painter = GameModule.Painter( self.display, self.objects, self.status )
    self.lastState = None 
    self.fps = pygame.time.Clock()
    self.newLevel()

  def loop(self):
    # W pętli gry jak to w pętli gry - przetwarzamy zdarzenia, sprawdzamy stan gry i rysujemy nową klatkę.
    self.fps.tick( gfx["framerate"] )
    for event in pygame.event.get():
      self.handleGlobalEvents( event )
      self.handleEvents( event )
    self.handleKeyboard()
    self.updateState()
    if self.actualState != states["GAMEOVER"]:
      self.painter.draw()
    else:
      self.display.fill( (0,0,0) )
      bigFont = pygame.font.SysFont( "sans-serif", 32 )
      gameOver = bigFont.render( "GAME OVER!", True, (255,255,255) )
      smallFont = pygame.font.SysFont( "sans-serif", 18 )
      points = smallFont.render( "Punktow: " + str(self.status.points), True, (255,255,255) )
      self.display.blit( gameOver, (gfx["screen"][0]/2 - gameOver.get_size()[0]/2, gfx["screen"][1]/2 - gameOver.get_size()[1]/2) )
      self.display.blit( points, (gfx["screen"][0]/2 - points.get_size()[0]/2, gfx["screen"][1]/2 - gameOver.get_size()[1]/2 - 40) )
    pygame.display.update()

  def handleEvents( self, event ):
    if self.actualState != states["PAUSE"]:
      if event.type == KEYDOWN:
        if event.key == K_p:
          self.lastState = self.actualState
          self.actualState = states["PAUSE"]
          self.painter.paused = True
    else:
      if event.type == KEYDOWN:
        if event.key == K_p:
          self.actualState = self.lastState
          self.painter.paused = False

    if self.actualState == states["START"]:
      if event.type == KEYDOWN:
        if event.key == K_SPACE:
          self.actualState = states["PROGRESS"]
          (self.objects.balls())[0].speedChange( int( math.copysign( 5., float(self.objects.pad().lastMove) ) ), -5 )

  def handleGlobalEvents( self, event ):
    if event.type == QUIT:
      sys.exit()

  def handleKeyboard(self):
    pressed = pygame.key.get_pressed()

    if self.actualState == states["PROGRESS"] or self.actualState == states["START"]:
      if pressed[K_LEFT]:
        if self.objects.pad().move(-10) and self.actualState == states["START"]:
          (self.objects.balls())[0].move(-10,0)
      if pressed[K_RIGHT]:
        if self.objects.pad().move(10) and self.actualState == states["START"]:
          (self.objects.balls())[0].move(10,0) 
      
        
  def updateState(self):
    if self.actualState == states["PAUSE"]:
      return
    if self.actualState == states["PROGRESS"]:
      self.objects.updatePowerups()
      for ball in self.objects.balls():
        speed = ball.speed()
        ball.move( speed[0], speed[1] )
        if ball.collideWithWall():
          pos = ball.pos()
          if pos[0] == 0 or pos[0] >= gfx["screen"][0] - ball.image.get_size()[0] - 1:
            ball.xInvert()
          if pos[1] == 0:
            ball.yInvert()
          if pos[1] >= gfx["screen"][1] - ball.image.get_size()[1] - 1:
            self.status.lives -= 1
            self.actualState = states["START"]
            self.playSound( "Resources/snd/chord.wav" )
            while len(self.objects.balls()) != 1:
              self.objects.removeBall((self.objects.balls())[0])
            for powerup in self.objects.powerups():
              self.objects.deletePowerup(powerup)

            self.objects.balls()[0].reset()
            self.objects.pad().reset()

        for obj in self.objects.grid():
          if ball.collision(obj):
            self.status.points += 100
            if obj.realx <= ball.position[0] and obj.realx + gfx["grid"][0] >= ball.position[0]:
              ball.yInvert()
            if obj.realy <= ball.position[1] and obj.realy + gfx["grid"][1] >= ball.position[1]:
              ball.xInvert()
            self.handleBrickCollision(obj)

        if ball.collision(self.objects.pad()):
          ball.yInvert()
          if self.objects.pad().position[1] <= ball.position[1] and self.objects.pad().position[1] + gfx["grid"][1] >= ball.position[1]:
            ball.xInvert()

      for powerup in self.objects.powerups():
        pad = self.objects.pad()
        if powerup.collision(pad):
          self.objects.deletePowerup(powerup)
          self.generatePowerup()
        if powerup.y == gfx["screen"][1] - 1 - powerup.image.get_size()[1]:
          self.objects.deletePowerup(powerup)

    if self.status.lives == 0:
      self.actualState = states["GAMEOVER"]
    if self.objects.grid() == []:
      self.status.level += 1
      if len(levels) == self.status.level:
        self.actualStatus = states["GAMEOVER"]
      else:
        self.newLevel()

    for modifier in self.status.modifiers:
      modifier[1] -= 1
      if modifier[1] == 0:
        if modifier[0] == "big_pad":
          self.objects.pad().setWidth(3)
          del modifier

  def generatePowerup(self):
    r = random.randint(1,3)
    # Mamy do wygenerowania 3 powerupy:
    # 1 - +1 żyć
    # 2 - na 30 sekund pad jest zwiększony do 5 "kratek"
    # 3 - dodatkowa kulka
    if r == 1:
      self.status.lives += 1
    elif r == 2:
      self.status.modifiers.append( [ "big_pad", gfx["framerate"] * 30 ] )
      self.objects.pad().setWidth(5)
    elif r == 3:
      ball = Ball()
      ball.position[0] = self.objects.pad().position[0] + (gfx["grid"][0]*self.objects.pad().gridWidth/2)
      ball.speedChange( int( math.copysign( 5., float(self.objects.pad().lastMove) ) ), -5 )
      self.objects.addBall(ball)

  def handleBrickCollision(self,obj):
    brickType = obj.getType()
    if brickType == "simple":
      self.objects.setGrid( obj.x, obj.y, None )
      rand = random.randint( 0, 9 )
      if rand == 9: # 1/10 szansy na powerupa
        self.objects.spawnPowerup( obj.x, obj.y )

    elif brickType == "solid":
      self.objects.setGrid( obj.x, obj.y, SimpleBrick(obj.x,obj.y) )
    elif brickType == "ghost":
      newType = random.randint( 0, 1 )
      if newType == 0:
        self.objects.setGrid( obj.x, obj.y, SimpleBrick(obj.x,obj.y) )
      elif newType == 1:
        self.objects.setGrid( obj.x, obj.y, SolidBrick(obj.x,obj.y) )

    self.playSound( "Resources/snd/ding.wav" )

  def newLevel(self):
    self.playSound( "Resources/snd/tada.wav" )
    self.mapper.load( self.status.level ) 
    self.objects.pad().reset() 
    while len(self.objects.balls()) != 1:
      self.objects.removeBall((self.objects.balls())[0])
    self.objects.balls()[0].reset()
    self.actualState = states["START"]

class Status:
  def __init__(self):
    self.level = 0
    self.points = 0
    self.lives = startState["lives"]
    self.modifiers = []

game = Game()

while True:
  game.loop()
