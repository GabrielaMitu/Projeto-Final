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

#estados
JOGANDO=0
DONE=7
QUIT=2
EXPLODING=6
INTRO=9

def introducao_nivel_extra(screen):
    # Variável para o ajuste de velocidade
    clock = pygame.time.Clock()

    # Carrega o fundo da tela inicial
    background = pygame.image.load(path.join(img_dir, 'nivel_extra-01.png')).convert()
    background_rect = background.get_rect()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    pygame.mixer.music.load(path.join(snd_dir, 'MissionImpossibleTheme.mp3'))
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(loops=-1)

   
    running = True
    i=2

    while running:      
        # Ajusta a velocidade do jogo.
        clock.tick(FPS)  
        # Processa os eventos (mouse, teclado, botão, etc).
        for event in pygame.event.get():
            # Verifica se foi fechado.
            if event.type == pygame.QUIT:
                state = QUIT
                running = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    background = pygame.image.load(path.join(img_dir, 'nivel_extra-0{}.png'.format(i))).convert()
                    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
                    i+=1
                    if i >4:
                        
                        state = JOGANDO
                        running = False
                                
        # A cada loop, redesenha o fundo e os sprites
        screen.fill(BLACK)
        screen.blit(background, background_rect)

        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()

    return state
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
    def __init__(self, player_img):
        
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)
        
        # Carregando a imagem de fundo.
        self.image = pygame.image.load(path.join(img_dir, "player.png")).convert()
        
        # Diminuindo o tamanho da imagem.

        self.image = pygame.transform.scale(self.image, (70, 70))
        
        # Deixando transparente.
        self.image.set_colorkey(BLACK)
        
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()
        
        # Centraliza embaixo da tela.
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        
        # Velocidade da nave
        self.speedx = 0
        
        # Melhora a colisão estabelecendo um raio de um circulo
        self.radius = 70
    
    
        self.n_balls = 0

    def move(self):
        self.rect.x += self.speedx
        
        # Mantem dentro da tela
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
            
            
#    def shoot(self):
#        key = pygame.key.get_pressed()
#        if key[pygame.K_SPACE] and self.n_balls < 1:
#            self.n_balls += 1
#            ball = Ball(img="player.png", vel=10, angle=45, startPosition=self.rect.center)
#            return ball
#        return None
    def update(self):
        self.move()

            
            
class Submarine(pygame.sprite.Sprite):
    # Construtor da classe.
    def __init__(self, img, startPosition, xspeed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(path.join(img_dir, 'airplane.png')).convert()
        self.image = pygame.transform.scale(self.image, (45, 30))
        self.rect = self.image.get_rect()
        self.rect.centerx = startPosition[0]
        self.rect.bottom = startPosition[1]
        self.xspeed = xspeed
        self.image.set_colorkey(BLACK)

    def shoot(self):
        chance = random.randint(0,1500)
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
    # Constructor. Pass in the color of the block, and its x and y position
    def __init__(self, x):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        # Speed in pixels per cycle
        self.speed = 10.0

        # Floating point representation of where the ball is
        self.x = x
        self.y = 500

        # Direction of ball (in degrees)
        # self.direction = 45

        self.width=10
        self.height=10

        # Create the image of the ball
        self.image = pygame.Surface([self.width, self.height])

        # Color the ball
        self.image.fill(RED)

        # Get a rectangle object that shows where our image is
        self.rect = self.image.get_rect()

        self.xspeed = math.sqrt(50)
        self.yspeed = math.sqrt(50)

        # Get attributes for the height/width of the screen
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()

    # This function will bounce the ball off a horizontal surface (not a vertical one)
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
        self.image.set_colorkey(BLACK)


    def move(self):
        self.rect.y += self.yspeed
        
class Explosion(pygame.sprite.Sprite):

    # Construtor da classe.
    def __init__(self, center, explosion_anim):
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)

        # Carrega a animação de explosão
        self.explosion_anim = explosion_anim

        # Inicia o processo de animação colocando a primeira imagem na tela.
        self.frame = 0
        self.image = self.explosion_anim[self.frame]
        self.rect = self.image.get_rect()
        self.rect.center = center

        # Guarda o tick da primeira imagem
        self.last_update = pygame.time.get_ticks()

        # Controle de ticks de animação: troca de imagem a cada self.frame_ticks milissegundos.
        self.frame_ticks = 50

    def update(self):
        # Verifica o tick atual.
        now = pygame.time.get_ticks()

        # Verifica quantos ticks se passaram desde a ultima mudança de frame.
        elapsed_ticks = now - self.last_update

        # Se já está na hora de mudar de imagem...
        if elapsed_ticks > self.frame_ticks:

            # Marca o tick da nova imagem.
            self.last_update = now

            # Avança um quadro.
            self.frame += 1

            # Verifica se já chegou no final da animação.
            if self.frame == len(self.explosion_anim):
                # Se sim, tchau explosão!
                self.kill()
            else:
                # Se ainda não chegou ao fim da explosão, troca de imagem.
                center = self.rect.center
                self.image = self.explosion_anim[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
 
def nivel_extra(screen,state):
        pygame.init()
        screen = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption("Jogo Beluga")
        
        assets = load_assets(img_dir, snd_dir, fnt_dir)
        
        
        clock = pygame.time.Clock()
        
        background = pygame.image.load(path.join(img_dir, 'ilha.png')).convert()
        background_rect = background.get_rect()
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    
        
        #game sets
        #width_screen = display_specs.current_w
        #height_screen = display_specs.current_h + 23
        
        FPS = 100
        
        lifes = 3
        
        player = Player('player.png')
        player_group = pygame.sprite.Group()
        player_group.add(player)
        
        subs_group = pygame.sprite.Group()
        
        for a in range(5):
            for y in range(10):
                x = random.randint(50, WIDTH-50)
                sub = Submarine("airplane.png", [x,y*30+40], 3)
                subs_group.add(sub)
        
        balls_group = pygame.sprite.Group()
        shoot_group = pygame.sprite.Group()
        explosion_group=pygame.sprite.Group()
        
        state = JOGANDO
        while state != QUIT:
            if state == JOGANDO:
                FPS=60
                clock.tick(FPS)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT :
                        lifes = 0
            
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            lifes = 0
                            
                    if event.type == pygame.KEYDOWN:
                                # Dependendo da tecla, altera a velocidade.
                                if event.key == pygame.K_LEFT:
                                    player.speedx = -8
                                if event.key == pygame.K_RIGHT:
                                    player.speedx = 8
                                if event.key == pygame.K_SPACE:
                                    print()
                                    ball = Ball(player.rect.centerx)
            
                                    balls_group.add(ball)
                                   # balls.add(ball)
                                    
                                   
                            
                    # Verifica se soltou alguma tecla.
                    if event.type == pygame.KEYUP:
                        # Dependendo da tecla, altera a velocidade.
                        if event.key == pygame.K_LEFT:
                            player.speedx = 0
                        if event.key == pygame.K_RIGHT:
                            player.speedx = 0
            balls_group.update()
            shoot_group.update()
            explosion_group.update()
            if state == JOGANDO:
    
                for sub in subs_group:
                    if sub.rect.right >= WIDTH or sub.rect.left <= 0:
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
                    # Toca o som da colisão
                    # boom_sound.play()
                    player.kill()
                    for ball in balls_group:
                        ball.kill()
                    explosao = Explosion(player.rect.center, assets["explosion_anim"])
                    explosion_group.add(explosao)
                    state = EXPLODING
                    explosion_tick = pygame.time.get_ticks()
                    explosion_duration = explosao.frame_ticks * len(explosao.explosion_anim) + 400
                
                
      
                        
            
                for ball in balls_group:
                    colisions = pygame.sprite.spritecollide(ball, player_group, False)
                    for colision in colisions:
                        ball.rect.bottom = player.rect.top - 5
                        ball.vertical_bounce()
            
                    colisions = pygame.sprite.spritecollide(ball, subs_group, True)
                    for colision in colisions:
                        ball.vertical_bounce()
            
            #    ball = Ball
            #    if ball != None:
            #        balls_group.add(ball)
            
                for ball in balls_group:
                    ball.update()
                    if ball.rect.right >= WIDTH or ball.rect.left <= 0:
                        ball.lateral_bounce()
                    if ball.rect.top <= 0:
                        ball.vertical_bounce()
                    if ball.rect.top > HEIGHT + 30:
                        lifes -= 1
                        player.n_balls -= 1
                        ball.kill()
                        
                        
                if lifes <= 0:
                    state = DONE
                    
                    
            elif state == EXPLODING:
                now = pygame.time.get_ticks()
                if now - explosion_tick > explosion_duration:
                    if lifes == 0:
                        state = DONE
                    else:
                        state = JOGANDO
                        player = Player(assets["player_img"])
                        player_group.add(player)   
            
        
            player.update()
            background_rect=background.get_rect()
            screen.fill(BLACK)
            screen.blit(background, background_rect)    
            subs_group.draw(screen)
            shoot_group.draw(screen)
            player_group.draw(screen)
            balls_group.draw(screen)
            balls_group.draw(screen)
            pygame.display.update()
        
        return QUIT
    
    
    
# Inicialização do Pygame.
pygame.init()
pygame.mixer.init()

# Tamanho da tela.
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Carrega todos os assets uma vez só e guarda em um dicionário
assets = load_assets(img_dir, snd_dir, fnt_dir)

# Comando para evitar travamentos.
state = INTRO
while state != QUIT:
    if state == INTRO:
        state = introducao_nivel_extra(screen)
    elif state == JOGANDO:
        state=nivel_extra(screen,state)
    else:
        state = QUIT

pygame.quit()

  




