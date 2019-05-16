# -*- coding: utf-8 -*-

# Importando as bibliotecas necessárias.
import pygame
import random
import time
from os import path
import math

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
 
# Size of break-out blocks
block_width = 23
block_height = 15


# Classe Jogador que representa a nave
class Player(pygame.sprite.Sprite):
    
    # Construtor da classe.
    def __init__(self, player_img):
        
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)
        
        # Carregando a imagem de fundo.
        self.image = player_img
        
        # Diminuindo o tamanho da imagem.
        self.image = pygame.transform.scale(player_img, (50, 38))
        
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
        self.radius = 25
    
    # Metodo que atualiza a posição da navinha
    def update(self):
        self.rect.x += self.speedx
        
        # Mantem dentro da tela
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
                    

class Block(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
       
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
 
        # Create the image of the block of appropriate size
        # The width and height are sent as a list for the first parameter.
        self.image = pygame.Surface([block_width, block_height])
 
        # Fill the image with the appropriate color
        self.image.fill(color)
 
        # Fetch the rectangle object that has the dimensions of the image
        self.rect = self.image.get_rect()
 
        # Move the top left of the rectangle to x,y.
        # This is where our block will appear..
        self.rect.x = x
        self.rect.y = y
        
        
        
class Ball(pygame.sprite.Sprite):
   
    # Speed in pixels per cycle
    speed = 10.0
 
    # Floating point representation of where the ball is
    x = 0.0
    y = 180.0
 
    # Direction of ball (in degrees)
    direction = 200
 
    width = 10
    height = 10
 
        # Constructor. Pass in the color of the block, and its x and y position
    def __init__(self):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
 
        # Create the image of the ball
        self.image = pygame.Surface([self.width, self.height])
 
        # Color the ball
        self.image.fill(WHITE)
 
        # Get a rectangle object that shows where our image is
        self.rect = self.image.get_rect()
 
        # Get attributes for the height/width of the screen
        self.height = pygame.display.get_surface().get_HEIGHT()
        self.width = pygame.display.get_surface().get_WIDTH()
 
    def bounce(self, diff):
       
        self.direction = (180 - self.direction) % 360
        self.direction -= diff
 
    def update(self):
        # Sine and Cosine work in degrees, so we have to convert them
        direction_radians = math.radians(self.direction)
 
        # Change the position (x and y) according to the speed and direction
        self.x += self.speed * math.sin(direction_radians)
        self.y -= self.speed * math.cos(direction_radians)
 
        # Move the image to where our x and y are
        self.rect.x = self.x
        self.rect.y = self.y
 
        # Do we bounce off the top of the screen?
        if self.y <= 0:
            self.bounce(0)
            self.y = 1
 
        # Do we bounce off the left of the screen?
        if self.x <= 0:
            self.direction = (360 - self.direction) % 360
            self.x = 1
 
        # Do we bounce of the right side of the screen?
        if self.x > self.WIDTH - self.width:
            self.direction = (360 - self.direction) % 360
            self.x = self.WIDTH - self.width - 1
 
        # Did we fall off the bottom edge of the screen?
        if self.y > 600:
            return True
        else:
            return False
 
 

# Carrega todos os assets uma vez só.
def load_assets(img_dir, snd_dir, fnt_dir):
    assets = {}
    assets["player_img"] = pygame.image.load(path.join(img_dir, "player_img.png")).convert()
    assets["background_img"] = pygame.image.load(path.join(img_dir, 'background_img.png')).convert()
    assets["score_font"] = pygame.font.Font(path.join(fnt_dir, "PressStart2P.ttf"), 28)
    return assets

# Inicialização do Pygame.
pygame.init()
pygame.mixer.init()

# Tamanho da tela.
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Nome do jogo
pygame.display.set_caption("BELUGA")

# Carrega todos os assets uma vez só e guarda em um dicionário
assets = load_assets(img_dir, snd_dir, fnt_dir)

# Variável para o ajuste de velocidade
clock = pygame.time.Clock()

# Carrega o fundo do jogo
background = assets["background"]
background_rect = background.get_rect()

# Carrega os sons do jogo
pygame.mixer.music.load(path.join(snd_dir, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
pygame.mixer.music.set_volume(0.4)

# Cria uma nave. O construtor será chamado automaticamente.
player = Player(assets["player_img"])

# Carrega a fonte para desenhar o score.
score_font = assets["score_font"]

# Cria um grupo de todos os sprites e adiciona a nave.
all_sprites = pygame.sprite.Group()
all_sprites.add(player)


blocks = pygame.sprite.Group()
balls = pygame.sprite.Group()
 

# Create the ball
ball = Ball()
all_sprites.add(ball)
balls.add(ball)
 
# The top of the block (y position)
top = 80
 
# Number of blocks to create
blockcount = 32
 

font = pygame.font.Font(None, 36)


# --- Create blocks
 
# Five rows of blocks
for row in range(5):
    # 32 columns of blocks
    for column in range(0, blockcount):
        # Create a block (color,x,y)
        block = Block(WHITE, column * (block_width + 2) + 1, top)
        blocks.add(block)
        all_sprites.add(block)
    # Move the top of the next row down
    top += block_height + 2


# Comando para evitar travamentos.
try:
    
    # Loop principal.
    pygame.mixer.music.play(loops=-1)

    score = 0

    lives = 3

    PLAYING = 0
    DONE = 2

    state = PLAYING
    while state != DONE:
        
        # Ajusta a velocidade do jogo.
        clock.tick(FPS)
        
        if state == PLAYING:
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
                        
                # Verifica se soltou alguma tecla.
                if event.type == pygame.KEYUP:
                    # Dependendo da tecla, altera a velocidade.
                    if event.key == pygame.K_LEFT:
                        player.speedx = 0
                    if event.key == pygame.K_RIGHT:
                        player.speedx = 0
                        
             
                # See if the ball hits the player paddle
                if pygame.sprite.spritecollide(player, balls, False):
                    # The 'diff' lets you try to bounce the ball left or right
                    # depending where on the paddle you hit it
                    diff = (player.rect.x + player.width/2) - (ball.rect.x+ball.width/2)
             
                    # Set the ball's y position in case
                    # we hit the ball on the edge of the paddle
                    ball.rect.y = screen.get_height() - player.rect.height - ball.rect.height - 1
                    ball.bounce(diff)
             
                # Check for collisions between the ball and the blocks
                deadblocks = pygame.sprite.spritecollide(ball, blocks, True)
             
                # If we actually hit a block, bounce the ball
                if len(deadblocks) > 0:
                    ball.bounce(0)
             
                    # Game ends if all the blocks are gone
                    if len(blocks) == 0:
                        state = DONE
 
    
        # Depois de processar os eventos.
        # Atualiza a acao de cada sprite.
        all_sprites.update()
        
        
        
        if state == PLAYING:
           
            
                # Ganhou pontos!
                score += 100
            
        # A cada loop, redesenha o fundo e os sprites
        screen.fill(BLACK)
        screen.blit(background, background_rect)
        all_sprites.draw(screen)

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
        
finally:
    
    pygame.quit()











