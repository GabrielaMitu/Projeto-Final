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


# Classe Jogador que representa a beluga
class Player(pygame.sprite.Sprite):
    
    # Construtor da classe.
    def __init__(self, player_img):
        
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)
        
        # Carregando a imagem de fundo.
        self.image = player_img
        
        # Diminuindo o tamanho da imagem.
        self.image = pygame.transform.scale(player_img, (70, 50))

        
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
        self.radius = 140
    
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
        self.image = pygame.transform.scale(submarine_img, (25, 15))
        
        self.image.set_colorkey(BLACK)
 
 
        # Fetch the rectangle object that has the dimensions of the image
        self.rect = self.image.get_rect()
 
        # Move the top left of the rectangle to x,y.
        # This is where our block will appear..
        self.rect.x = x
        self.rect.y = y
        
        self.enemy_list = None
        self.bullet_list = None
        
    def update(self):
        """All the logic to move, and the game logic goes here. """

            # Have a random 1 in 200 change of shooting each frame
        if random.randrange(200) == 0:
            tiro=Tiro(self.rect.centerx, self.rect.bottom, assets["tiros_img"])
            self.tiros.add(tiro)

        
class Tiro(pygame.sprite.Sprite):
    def __init__(self, x, y, tiro_img):
        
        pygame.sprite.Sprite.__init__(self)
        
        # Diminuindo o tamanho da imagem.
        self.image = pygame.transform.scale(tiro_img, (10, 10))
        self.image.set_colorkey(BLACK)
        self.rect= self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = y
        self.speed_y=5
    
    def update(self):
        self.rect.y+=self.speed_y
    
        
class Ball(pygame.sprite.Sprite):
    # Speed in pixels per cycle
    speed = 10.0
    
    # Floating point representation of where the ball is
    x = 0.0
    y = 180.0
    
    # Direction of ball (in degrees)
    direction = 95

    width=10
    height=10
    
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
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()
    
    # This function will bounce the ball off a horizontal surface (not a vertical one)
    def bounce(self,diff):
        self.direction = (180-self.direction)%360
        self.direction -= diff
    
    # Update the position of the ball
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
            self.y=1
            
        # Do we bounce off the left of the screen?
        if self.x <= 0:
            self.direction = (360-self.direction)%360
            self.x=1
            
        # Do we bounce of the right side of the screen?
        if self.x > self.screenwidth-self.width:
            self.direction = (360-self.direction)%360
            self.x=self.screenwidth-self.width-1
        
        # Did we fall off the bottom edge of the screen?
        if self.y > 600:
            return True
        else:
            return False
 
 

# Carrega todos os assets uma vez só.
def load_assets(img_dir, snd_dir, fnt_dir):
    assets = {}
    assets["background_img"] = pygame.image.load(path.join(img_dir, 'background.png')).convert()
    assets["player_img"] = pygame.image.load(path.join(img_dir, "player.png")).convert()
    assets["tiros_img"] = pygame.image.load(path.join(img_dir, 'Red_laser.png')).convert()
    assets["submarine_img"] = pygame.image.load(path.join(img_dir, "submarine.png")).convert()
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
background = assets["background_img"]
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

tiros=pygame.sprite.Group()

balls = pygame.sprite.Group()


 
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
        block=Block(column*(block_width+2)+1,top, (assets["submarine_img"]),tiros)
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

    #Estados do jogo
    BOLA_NA_BELUGA = 0
    PLAYING = 1
    DONE = 3
    PASSOU_NIVEL = 4
    PAUSE = 5

    state = PLAYING
    while state != DONE:
        
        # Ajusta a velocidade do jogo.
        clock.tick(FPS)
        
        if state == PLAYING:
            hits = pygame.sprite.groupcollide(blocks, balls, True, True)
            for hit in hits: # Pode haver mais de um
                block = Block(assets["submarine_img"]) 
                all_sprites.add(block)
                blocks.add(block)
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
                        ball = Ball()

                        all_sprites.add(ball)
                        balls.add(ball)
                        
                       # pew_sound.play()

                        
                # Verifica se soltou alguma tecla.
                if event.type == pygame.KEYUP:
                    # Dependendo da tecla, altera a velocidade.
                    if event.key == pygame.K_LEFT:
                        player.speedx = 0
                    if event.key == pygame.K_RIGHT:
                        player.speedx = 0
                        
             
            # See if the ball hits the player paddle
            for ball in pygame.sprite.spritecollide(player, balls, False):
                # The 'diff' lets you try to bounce the ball left or right
                # depending where on the paddle you hit it
                diff = (player.rect.x) - (ball.rect.x+ball.width/2)
         
                # Set the ball's y position in case
                # we hit the ball on the edge of the paddle
                ball.rect.y = screen.get_height() - player.rect.height - ball.rect.height - 1
                ball.bounce(diff)
         
            # Check for collisions between the ball and the blocks
            for ball in balls:
                deadblocks = pygame.sprite.spritecollide(ball, blocks, True)
         
            # If we actually hit a block, bounce the ball
                if len(deadblocks) > 0:
                    ball.bounce(0)
                    score += 100

         
                # Game ends if all the blocks are gone
                if len(blocks) == 0:
                    state = DONE
            for ball in balls:
                if ball.y > HEIGHT:
                    lives -= 1
                    ball.kill()
                
            
            if lives == 0:
                state = DONE
                    
                    
             
    
        # Depois de processar os eventos.
        # Atualiza a acao de cada sprite.
        all_sprites.update()
        tiros.update()
        
                    
        # A cada loop, redesenha o fundo e os sprites
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
        
        if state == DONE and lives > 0:
            text_surface = score_font.render("{:10d}".format(score), True, BLUE)
            text_rect = text_surface.get_rect()
            text_rect.midtop = (WIDTH / 2,  HEIGHT/2)
            screen.blit(text_surface, text_rect)
            
            
        
finally:
    
    pygame.quit()











