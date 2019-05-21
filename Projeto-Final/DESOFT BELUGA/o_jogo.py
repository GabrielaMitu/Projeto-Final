# -*- coding: utf-8 -*-

# Importando as bibliotecas necessárias.
import pygame
import random
from os import path, environ
import math
from pygame.locals import *
import time
import pygameMenu
from ClassBall import *
from ClassPlayer import *


# Estabelece a pasta que contem as figuras e sons.
img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')
fnt_dir = path.join(path.dirname(__file__), 'font')

environ['SDL_VIDEO_CENTERED'] = '1'


# Dados gerais do jogo.
WIDTH = 830 # Largura da tela
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
block_width = 40    #23
block_height = 25   #15


def draw_text_middle(text, size, color, surface):
    label = score_font.render(text, 1, color)

    surface.blit(label, (WIDTH/2 - (label.get_width() / 2), HEIGHT/2 - label.get_height()/2))



def main_menu():

    tela = pygame.display.set_mode((WIDTH, HEIGHT))
    run = True
    state = MENU
    while run:
        tela.fill((0,0,0))
        draw_text_middle('Press any key to begin.', 60, WHITE, tela)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state=DONE
                run = False

            if event.type == pygame.KEYDOWN:
                # print('l')
                state = PLAYING
                run = False


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
    assets["background_img"] = pygame.image.load(path.join(img_dir, 'NORWAY.png')).convert()
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
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Carrega os sons do jogo
# pygame.mixer.music.load(path.join(snd_dir, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
# pygame.mixer.music.set_volume(0.4)
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

# The top of the block (y position)
top = 80

# Number of blocks to create
blockcount = 14

font = pygame.font.Font(None, 36)

# --- Create blocks

# Five rows of blocks
for row in range(5):
    # 32 columns of blocks
    for column in range(0, blockcount):
        # Create a block (color,x,y)
        block=Block(column*(block_width+20)+1,top, (assets["submarine_img"]),tiros)
        blocks.add(block)
        all_sprites.add(block)
    # Move the top of the next row down
    top += block_height + 2

# Comando para evitar travamentos.
try:
    # Loop principal.
    # pygame.mixer.music.play(loops=-1)
    score = 0
    lives = 99

    #Estados do jogo
    BOLA_NA_BELUGA = 0
    PLAYING = 1
    EXPLODING = 2
    DONE = 3
    PASSOU_NIVEL_1 = 3
    PASSOU_NIVEL_2= 5
    PAUSED = 5
    MENU=6

#    state= MENU
#    surface= 200,300#pygame.Surface(800,600)
#    #pygame.surface.fill(BLUE)
#    window_width=WIDTH
#    window_height=HEIGHT
#    title="MENU PRINCIPAL"
#    text_surface = score_font.render("Aperte uma tecla para começar", True, YELLOW)
#    text_rect = text_surface.get_rect()
#    text_rect.midtop = (WIDTH / 2,  10)
#    screen.blit(text_surface, text_rect)
#    pygameMenu.Menu(surface, window_width, window_height, score_font, title) # -> Menu object
#    for event in pygame.event.get():
#                    # Verifica se foi fechado.
#                    if event.type == pygame.QUIT:
#                        state = DONE
#                    # Verifica se apertou alguma tecla.
#                    if event.type == pygame.KEYDOWN:
#                        state=PLAYING

    main_menu()
    state = PLAYING
    while state != DONE:

        # Ajusta a velocidade do jogo.
        clock.tick(FPS)

        if state == PLAYING:
            hits = pygame.sprite.groupcollide(balls, blocks, False, True)
            for hit in hits: # Pode haver mais de um
                score+=100
                hit.bounce(False)

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
                        print()
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

                # Game ends if all the blocks are gone
            if len(blocks) == 0:
                    state = PASSOU_NIVEL_1

            for ball in balls:
                if ball.y > HEIGHT:
                    lives -= 1
                    ball.kill()

            if lives <= 0:
                state = DONE

               # Verifica se houve colisão entre nave e meteoro
            hits = pygame.sprite.spritecollide(player, tiros, False, pygame.sprite.collide_circle)
            if hits:
                # Toca o som da colisão
                # boom_sound.play()
                player.kill()
                lives -= 1
                for ball in balls:
                    ball.kill()
                explosao = Explosion(player.rect.center, assets["explosion_anim"])
                all_sprites.add(explosao)
                state = EXPLODING
                explosion_tick = pygame.time.get_ticks()
                explosion_duration = explosao.frame_ticks * len(explosao.explosion_anim) + 400

        if state == EXPLODING:
            now = pygame.time.get_ticks()
            if now - explosion_tick > explosion_duration:
                if lives == 0:
                    state = DONE
                else:
                    state = PLAYING
                    player = Player(assets["player_img"])
                    all_sprites.add(player)
#---------------------------------            
        if state==PASSOU_NIVEL_1:
            blockcount=14
            top=80
            velocidade=random.randint(5,8)
            state=PLAYING
            for row in range(7):
    # 32 columns of blocks
                for column in range(0, blockcount):
                    # Create a block (color,x,y)
                    block=Block(column*(block_width+20)+1,top, (assets["submarine_img"]),tiros)
                    blocks.add(block)
                    all_sprites.add(block)
                # Move the top of the next row down
                top += block_height + 2
            
            assets["background_img"] = pygame.image.load(path.join(img_dir, 'area_51_2.png')).convert()
            background = assets["background_img"]
            background_rect = background.get_rect()
            background = pygame.transform.scale(background, (WIDTH, HEIGHT))
            hits = pygame.sprite.groupcollide(balls, blocks, False, True)
            for hit in hits: # Pode haver mais de um
                score+=100
                hit.bounce(False)

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
                        print()
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

                # Game ends if all the blocks are gone
            if len(blocks) == 0:
                    state = PASSOU_NIVEL_2

            for ball in balls:
                if ball.y > HEIGHT:
                    lives -= 1
                    ball.kill()

            if lives <= 0:
                state = DONE

               # Verifica se houve colisão entre nave e meteoro
            hits = pygame.sprite.spritecollide(player, tiros, False, pygame.sprite.collide_circle)
            if hits:
                # Toca o som da colisão
                # boom_sound.play()
                player.kill()
                lives -= 1
                for ball in balls:
                    ball.kill()
                explosao = Explosion(player.rect.center, assets["explosion_anim"])
                all_sprites.add(explosao)
                state = EXPLODING
                explosion_tick = pygame.time.get_ticks()
                explosion_duration = explosao.frame_ticks * len(explosao.explosion_anim) + 400
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
                    if random.randrange(10000) == 0:
                        tiro=Tiro(self.rect.centerx, self.rect.bottom, assets["tiros_img"])
                        self.tiros.add(tiro)
            
            
            
        if state==PASSOU_NIVEL_2:
            blockcount=14
            top=80
            for row in range(5):
    # 32 columns of blocks
                for column in range(0, blockcount):
                    # Create a block (color,x,y)
                    block=Block(column*(block_width+20)+1,top, (assets["submarine_img"]),tiros)
                    blocks.add(block)
                    all_sprites.add(block)
                # Move the top of the next row down
                top += block_height + 2
            state=PLAYING
            assets["background_img"] = pygame.image.load(path.join(img_dir, 'white_house2.png')).convert()
            background = assets["background_img"]
            background_rect = background.get_rect()
            background = pygame.transform.scale(background, (WIDTH, HEIGHT))
            
            hits = pygame.sprite.groupcollide(balls, blocks, False, True)
            for hit in hits: # Pode haver mais de um
                score+=100
                hit.bounce(False)
            for event in pygame.event.get():
                # Verifica se foi fechado.
                if event.type == pygame.QUIT:
                    state = DONE
                if event.type == pygame.KEYDOWN:
                    # Dependendo da tecla, altera a velocidade.
                    if event.key == pygame.K_LEFT:
                        player.speedx = -8
                    if event.key == pygame.K_RIGHT:
                        player.speedx = 8
                    if event.key == pygame.K_SPACE:
                        print()
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
                for ball in pygame.sprite.spritecollide(player, balls, False):
                    ball.bounce(False)

                    # Game ends if all the blocks are gone
                if len(blocks) == 0:
                        state = DONE
        
                for ball in balls:
                    if ball.y > HEIGHT:
                        lives -= 1
                        ball.kill()
        
                if lives <= 0:
                    state = DONE
        
                   # Verifica se houve colisão entre nave e meteoro
                hits = pygame.sprite.spritecollide(player, tiros, False, pygame.sprite.collide_circle)
                if hits:
                    # Toca o som da colisão
                    # boom_sound.play()
                    player.kill()
                    lives -= 1
                    for ball in balls:
                        ball.kill()
                    explosao = Explosion(player.rect.center, assets["explosion_anim"])
                    all_sprites.add(explosao)
                    state = EXPLODING
                    explosion_tick = pygame.time.get_ticks()
                    explosion_duration = explosao.frame_ticks * len(explosao.explosion_anim) + 400

            
#-------------------------
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
