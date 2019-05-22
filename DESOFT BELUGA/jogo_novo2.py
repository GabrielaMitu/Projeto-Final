# -*- coding: utf-8 -*-
###jogo numa função (game_screen)

# Importando as bibliotecas necessárias.
import pygame
import random
from os import path
import math
from pygame.locals import *
import time
import pygameMenu


# Estabelece a pasta que contem as figuras e sons.
img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')
fnt_dir = path.join(path.dirname(__file__), 'font')

# Dados gerais do jogo.
WIDTH = 800 # Largura da tela
HEIGHT = 600 # Altura da tela
FPS = 60 # Frames por segundo

# Define algumas variáveis com as cores básicas
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0    , 255)
YELLOW = (255, 255, 0)
 
# Tamanho dos blocos
block_width = 23
block_height = 15


# Estados para controle do fluxo da aplicação
INIT = 0
GAME = 1
QUIT = 2
GAME_OVER = 3
INTRODUCAO = 4


level = 1

def draw_text_middle(text, size, color, surface):
    label = score_font.render(text, 1, color)

    surface.blit(label, (WIDTH/2 - (label.get_width() / 2), HEIGHT/2 - label.get_height()/2))

def introducao(screen):
    # Variável para o ajuste de velocidade
    clock = pygame.time.Clock()

    # Carrega o fundo da tela inicial
    background = pygame.image.load(path.join(img_dir, 'intro-02.png')).convert()
    background_rect = background.get_rect()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

   
    running = True
    i=3

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
                    background = pygame.image.load(path.join(img_dir, 'intro-0{}.png'.format(i))).convert()
                    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
                    i+=1
                    if i >= 6:
                        
                        state = GAME
                        running = False
                                
        # A cada loop, redesenha o fundo e os sprites
        screen.fill(BLACK)
        screen.blit(background, background_rect)

        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()

    return state
                


   
def fundo_nivel(imagem):
        background = pygame.image.load(path.join(img_dir, imagem)).convert()
        background.get_rect()
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))    
        return background
        


# 
def create_blocks(numero_blocos,inimigo, tiros, blocks, all_sprites):
        top = 80 
        imagem_inimigo= pygame.image.load(path.join(img_dir, inimigo)).convert()
        blockcount=14
        for row in range(7):
                for column in range(0, blockcount):
                    block=Block(column*(block_width+20)+1,top, (imagem_inimigo,tiros)) 
                    blocks.add(block)
                    all_sprites.add(block)
                top += block_height + 2

def init_screen(screen):
    # Variável para o ajuste de velocidade
    clock = pygame.time.Clock()

    # Carrega o fundo da tela inicial
    background = pygame.image.load(path.join(img_dir, 'intro-01.png')).convert()
    background_rect = background.get_rect()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    
    running = True
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
                state = INTRODUCAO
                running = False
                    
        # A cada loop, redesenha o fundo e os sprites
        screen.fill(BLACK)
        screen.blit(background, background_rect)

        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()

    return state
                
def game_over_screen(screen):
    
    clock = pygame.time.Clock()

    background = pygame.image.load(path.join(img_dir, 'game_over.png')).convert()
    background_rect = background.get_rect()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))


    running = True
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
                if event.key == pygame.K_n:
                    state = GAME
                    running = False

        # A cada loop, redesenha o fundo e os sprites
        screen.fill(BLACK)
        screen.blit(background, background_rect)

        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()
        
        return state
                        
# Classe Jogador que representa a beluga
class Player(pygame.sprite.Sprite):
    
    # Construtor da classe.
    def __init__(self, player_img):
        
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)
        
        # Carregando a imagem de fundo.
        self.image = player_img
        
        # Diminuindo o tamanho da imagem.

        self.image = pygame.transform.scale(player_img, (70, 70))
        
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
    
    # Metodo que atualiza a posição da beluga
    def update(self):
        self.rect.x += self.speedx
        
        # Mantem dentro da tela
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
                    

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, submarine_img, tiros):

        self.tiros=tiros

        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        # Create the image of the block of appropriate size
        # The width and height are sent as a list for the first parameter.
        self.image = pygame.transform.scale(submarine_img, (45, 30))

        self.image.set_colorkey(BLACK)


        # Fetch the rectangle object that has the dimensions of the image
        self.rect = self.image.get_rect()

        # Move the top left of the rectangle to x,y.
        # This is where our block will appear..
        self.rect.x = x
        self.rect.y = y

    def update(self):

            # Have a random 1 in 200 change of shooting each frame
        if random.randrange(20000) == 0:
            tiro=Tiro(self.rect.centerx, self.rect.bottom, assets["tiros_img"])
            self.tiros.add(tiro)
    
        
class Tiro(pygame.sprite.Sprite):
    def __init__(self, x, y, tiro_img):

        pygame.sprite.Sprite.__init__(self)

        # Diminuindo o tamanho da imagem.
        #random.randrange(200) == 0:
        self.image = pygame.transform.scale(tiro_img, (10, 10))
        self.image.set_colorkey(BLACK)
        self.rect= self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = y
        velocidade=random.randint(1,7)
        self.speed_y=velocidade

    def update(self):
        self.rect.y+=self.speed_y

    
        
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
        self.image.fill(WHITE)

        # Get a rectangle object that shows where our image is
        self.rect = self.image.get_rect()

        self.xspeed = math.sqrt(50)
        self.yspeed = math.sqrt(50)

        # Get attributes for the height/width of the screen
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()

    # This function will bounce the ball off a horizontal surface (not a vertical one)
    def bounce(self,lado):
        # self.direction = (180-self.direction)%360
        # self.direction -= diff
        if lado:
            self.xspeed = -self.xspeed
        else:
            self.yspeed = -self.yspeed

    # Update the position of the ball
    def update(self):
        # Change the position (x and y) according to the speed and direction
        self.x += self.xspeed
        self.y -= self.yspeed

        # Move the image to where our x and y are
        self.rect.x = self.x
        self.rect.y = self.y

        # Do we bounce off the top of the screen?
        if self.y <= 0:
            self.bounce(False)

        # Do we bounce off the left of the screen?
        if self.x <= 0:
            self.bounce(True)

        # Do we bounce of the right side of the screen?
        if self.x > self.screenwidth-self.width:
            self.bounce(True)

        # Did we fall off the bottom edge of the screen?
        if self.y > 600:
            return True
        else:
            return False

        
        
        
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
 
 

# Carrega todos os assets uma vez só.
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




def game_screen(screen,level, assets):
    
    
    # Nome do jogo
    pygame.display.set_caption("BELUGA")
    

    
    # Variável para o ajuste de velocidade
    clock = pygame.time.Clock()
    
    # Carrega os sons do jogo
    boom_sound = assets["boom_sound"]
    
    
    # Cria uma nave. O construtor será chamado automaticamente.
    player = Player(assets["player_img"])
    
    # Carrega a fonte para desenhar o score.
    score_font = assets["score_font"]
    
    # Cria um grupo de todos os sprites e adiciona a nave.
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    blocks = pygame.sprite.Group()
    tiros=pygame.sprite.Group()
    balls = pygame.sprite.Group()
    
    # Loop principal.
    score = 0
    lives = 3

    #Estados do jogo
    PLAYING = 0
    EXPLODING = 1
    DONE = 2
    PAUSED = 3
   
    
    if level == 1:
        background = fundo_nivel('norway.png')
        FPS = 50
        #create_blocks(4,'submarine-prata.png', tiros, blocks, all_sprites)
         # The top of the block (y position)
        top = 80
         
        # Number of blocks to create
        blockcount = 32
         
    #    
        font = pygame.font.Font(None, 36)
        
    #    
        # --- Create blocks
         
        # Five rows of blocks
        for row in range(8):
            # 32 columns of blocks
            for column in range(0, 19):
                # Create a block (color,x,y)
                block=Block(column*(block_width+20)+1,top, (assets["submarine_img"]),tiros)
                blocks.add(block)
                all_sprites.add(block)
            # Move the top of the next row down
            top += block_height + 2
            
            
            
            
    elif level == 2:
        fundo_nivel('underwater2.png')
        create_blocks(5,'submarine.png', tiros)
        FPS=75
    elif level == 3:
        fundo_nivel('atlantis2.png')
        FPS=100
        create_blocks(6,'submarine.png', tiros)
    elif level == 4:
        fundo_nivel('area_51_2.1.png')
        create_blocks(7,'submarine-azul.png')
        FPS=125
    elif level == 5:
        fundo_nivel('atlantis2.png')
        FPS=150
        create_blocks(8,'submarine-verde.png')


         
        
    state = PLAYING
    level=1
    while state != DONE:
        
        # Ajusta a velocidade do jogo.
        clock.tick(FPS)
        
        if state == PLAYING:
            hits = pygame.sprite.groupcollide(blocks, balls, True, False)
            for hit in hits: # Pode haver mais de um
                score+=100
                ball.bounce(False)
                
            # Processa os eventos (mouse, teclado, botão, etc).
            for event in pygame.event.get():
                
                # Verifica se foi fechado.
                if event.type == pygame.QUIT:
                    state = DONE
                    
                
                # Verifica se apertou alguma tecla.
                if event.type == pygame.KEYDOWN:
                    # Dependendo da tecla, altera a velocidade.
                    if event.key == pygame.K_LEFT:
                        player.speedx = -8
                    if event.key == pygame.K_RIGHT:
                        player.speedx = 8
                    if event.key == pygame.K_SPACE:
                        ball = Ball(player.rect.x)

                        all_sprites.add(ball)
                        balls.add(ball)
                        
                       # pew_sound.play()
                    if event.key ==pygame.K_ESCAPE:
                        state = PAUSED
            

                        
                # Verifica se soltou alguma tecla.
                if event.type == pygame.KEYUP:
                    # Dependendo da tecla, altera a velocidade.
                    if event.key == pygame.K_LEFT:
                        player.speedx = 0
                    if event.key == pygame.K_RIGHT:
                        player.speedx = 0
                        
                
            # See if the ball hits the player paddle
            for ball in pygame.sprite.spritecollide(player, balls, False):
                ball.bounce(False)

         
            # Check for collisions between the ball and the blocks
            for ball in balls:
                if ball.y > HEIGHT:
                    lives -= 1
                    ball.kill()
                                                    
            if len(blocks) == 0:
                    if level<=5:
                        level+=1
                    else:
                        state=DONE

                                
    
     #-------------------               
#                Verifica se houve colisão entre nave e meteoro
            hits = pygame.sprite.spritecollide(player, tiros, False, pygame.sprite.collide_circle)
            if hits:
                # Toca o som da colisão
                boom_sound.play()
                player.kill()
                lives -= 1
                for ball in balls:
                    ball.kill()
                explosao = Explosion(player.rect.center, assets["explosion_anim"])
                all_sprites.add(explosao)
                state = EXPLODING
                explosion_tick = pygame.time.get_ticks()
                explosion_duration = explosao.frame_ticks * len(explosao.explosion_anim) + 400
#            
        if state == EXPLODING:
            now = pygame.time.get_ticks()
            if now - explosion_tick > explosion_duration:
                if lives == 0:
                    state = DONE
                else:
                    state = PLAYING
                    player = Player(assets["player_img"])
                    all_sprites.add(player)
                    

                
     #----------------------
        
     
        # Depois de processar os eventos.
        # Atualiza a acao de cada sprite.
        all_sprites.update()
        tiros.update()
        
                    
        # A cada loop, redesenha o fundo e os sprites
        background_rect=background.get_rect()
        screen.fill(BLACK)
        screen.blit(background, background_rect)
        all_sprites.draw(screen)
        tiros.draw(screen)

        # Desenha o score
        text_surface = score_font.render("{:08d}".format(score), True, YELLOW)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (WIDTH / 2,  10)
        screen.blit(text_surface, text_rect)

        # Desenha as vidas
        text_surface = score_font.render(chr(9829) * lives, True, RED)
        text_rect = text_surface.get_rect()
        text_rect.bottomleft = (10, HEIGHT - 10)
        screen.blit(text_surface, text_rect)
        
        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()
            
            
    return QUIT 


# Inicialização do Pygame.
pygame.init()
pygame.mixer.init()

# Tamanho da tela.
screen = pygame.display.set_mode((WIDTH, HEIGHT))


# Nome do jogo
pygame.display.set_caption("FBI")
# Carrega todos os assets uma vez só e guarda em um dicionário
assets = load_assets(img_dir, snd_dir, fnt_dir)

# Comando para evitar travamentos.
try:
    state = INIT
    while state != QUIT:
        if state == INIT:
            state = init_screen(screen)
        if state == INTRODUCAO:
            state=introducao(screen)
        elif state == GAME:
            state = game_screen(screen,level, assets)
        elif state == GAME_OVER:
            state= game_over_screen(screen)
        else:
            state = QUIT
finally:
    pygame.quit()

  




