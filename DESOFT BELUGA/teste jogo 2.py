import random
from os import path, environ
import pygame
import math
from pygame.locals import *
import time
import pygameMenu

# Estabelece a pasta que contem as figuras e sons.
img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')
fnt_dir = path.join(path.dirname(__file__), 'font')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0    , 255)
YELLOW = (255, 255, 0)

# Dados gerais do jogo.
WIDTH = 800 # Largura da tela
HEIGHT = 600 # Altura da tela
FPS = 60 # Frames por segundo


def load_assets(img_dir, snd_dir, fnt_dir):
    assets = {}
    assets["background_img"] = pygame.image.load(path.join(img_dir, 'background.png')).convert()
    assets["player_img"] = pygame.image.load(path.join(img_dir, "player.png")).convert()
    assets["tiros_img"] = pygame.image.load(path.join(img_dir, 'Red_laser.png')).convert()
    assets["submarine_img"] = pygame.image.load(path.join(img_dir, "submarine.png")).convert()
    assets["score_font"] = pygame.font.Font(path.join(fnt_dir, "PressStart2P.ttf"), 28)
    assets["boom_sound"] = pygame.mixer.Sound(path.join(snd_dir, 'expl3.wav'))

    explosion_anim = []
    for i in range(9):
        filename = 'regularExplosion0{}.png'.format(i)
        img = pygame.image.load(path.join(img_dir, filename)).convert()
        img = pygame.transform.scale(img, (32, 32))        
        img.set_colorkey(BLACK)
        explosion_anim.append(img)
    assets["explosion_anim"] = explosion_anim
    assets["score_font"] = pygame.font.Font(path.join(fnt_dir, "PressStart2P.ttf"), 28)
    return assets




class Player(pygame.sprite.Sprite):
    # Construtor da classe.
    def __init__(self, player_img, max_vel, screenDimensions):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img#pygame.image.load(path.join(img_dir, 'player.png')).convert()
        self.image = pygame.transform.scale(player_img, (70, 70))
        self.image = pygame.transform.scale(player_img, (70, 70))
        self.rect = self.image.get_rect()
        self.rect.centerx = screenDimensions[0]/2
        self.rect.bottom = screenDimensions[1] -50
        self.max_vel = max_vel
        self.screenX = screenDimensions[0]
        self.n_balls = 0

    def move(self):
        key = pygame.key.get_pressed()
        self.xspeed = 0
        if self.rect.left >= 0:
            if key[pygame.K_d]:
                self.xspeed = self.max_vel
        else:
            self.rect.left = 1
        if self.rect.right <= self.screenX:
            if key[pygame.K_a]:
                self.xspeed = -self.max_vel
        else:
            self.rect.left = self.screenX-28

        self.rect.x += self.xspeed

    def shoot(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_w] and self.n_balls < 1:
            self.n_balls += 1
            ball = Ball(img="player.png", vel=10, angle=45, startPosition=self.rect.center)
            return ball
        return None

    def update(self):
        self.move()

class Submarine(pygame.sprite.Sprite):
    # Construtor da classe.
    def __init__(self, img, startPosition, xspeed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(path.join(img_dir, 'submarine.png')).convert()
        self.image = pygame.transform.scale(self.image, (45, 30))
        self.rect = self.image.get_rect()
        self.rect.centerx = startPosition[0]
        self.rect.bottom = startPosition[1]
        self.xspeed = xspeed

    def shoot(self):
        chance = random.randint(0,1000)
        if chance <= 1:
            shoot = Shoot("Red_laser.png" ,self.rect.center, 5)
            return shoot
        return None

    def move(self):
        self.rect.x += self.xspeed

    def flip(self):
        self.xspeed = -self.xspeed
        self.image = pygame.transform.flip(self.image, True, False)


class Ball(pygame.sprite.Sprite):
    # Construtor da classe.
    def __init__(self, img, vel, angle, startPosition):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = startPosition[0]
        self.rect.bottom = startPosition[1] -20
        self.vel = vel
        self.angle = angle
        self.xspeed = vel*math.cos(angle)
        self.yspeed = vel*math.sin(angle)

    def move(self):
        self.rect.x += self.xspeed
        self.rect.y -= self.yspeed

    def lateral_bounce(self):
        self.xspeed = -self.xspeed

    def vertical_bounce(self):
        self.yspeed = -self.yspeed

    def update(self):
        self.move()


class Shoot(pygame.sprite.Sprite):
    # Construtor da classe.
    def __init__(self, img, startPosition, yspeed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(path.join(img_dir, 'Red_laser.png')).convert()
        self.image = pygame.transform.scale(self.image, (10, 10))
        self.rect = self.image.get_rect()
        self.rect.center = startPosition
        self.yspeed = yspeed

    def move(self):
        self.rect.y += self.yspeed

pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Jogo Beluga")
environ['SDL_VIDEO_CENTERED'] = '1'

clock = pygame.time.Clock()

background = pygame.image.load(path.join(img_dir, 'background.png')).convert()
background_rect = background.get_rect()


red = [255,0,0]
green = [0,255,0]
blue = [0,0,255]
white = [255,255,255]
black = [0,0,0]

#display specs
display_specs = pygame.display.Info()

#game sets
width_screen = display_specs.current_w
height_screen = display_specs.current_h + 23

FPS = 100

lifes = 3

player = Player('player.png', max_vel=15, screenDimensions=(width_screen, height_screen))
player_group = pygame.sprite.Group()
player_group.add(player)

subs_group = pygame.sprite.Group()

for a in range(5):
    for y in range(10):
        x = random.randint(50, width_screen-50)
        sub = Submarine("submarine.png", [x,y*30+40], 3)
        subs_group.add(sub)

balls_group = pygame.sprite.Group()
shoot_group = pygame.sprite.Group()

while lifes > 0:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT :
            lifes = 0

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                lifes = 0

    for sub in subs_group:
        if sub.rect.right >= width_screen or sub.rect.left <= 0:
            sub.flip()
        sub.move()
        shoot = sub.shoot()
        if shoot != None:
            shoot_group.add(shoot)

    for shoot in shoot_group:
        shoot.move()

    colisions = pygame.sprite.spritecollide(player, shoot_group, True)
    for colision in colisions:
        lifes -= 1

    for ball in balls_group:
        colisions = pygame.sprite.spritecollide(ball, player_group, False)
        for colision in colisions:
            ball.rect.bottom = player.rect.top - 5
            ball.vertical_bounce()

        colisions = pygame.sprite.spritecollide(ball, subs_group, True)
        for colision in colisions:
            ball.vertical_bounce()

    ball = player.shoot()
    if ball != None:
        balls_group.add(ball)

    for ball in balls_group:
        ball.update()
        if ball.rect.right >= width_screen or ball.rect.left <= 0:
            ball.lateral_bounce()
        if ball.rect.top <= 0:
            ball.vertical_bounce()
        if ball.rect.top > height_screen + 30:
            lifes -= 1
            player.n_balls -= 1
            ball.kill()

    player.update()
    screen.fill(black)
    subs_group.draw(screen)
    shoot_group.draw(screen)
    player_group.draw(screen)
    balls_group.draw(screen)
    pygame.display.update()
