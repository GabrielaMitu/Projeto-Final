# -*- coding: utf-8 -*-
###jogo numa função (game_screen)

# Importando as bibliotecas necessárias.
import pygame
import random
from os import path
import math
from pygame.locals import *
import time
import ptext



# Estabelece a pasta que contem as figuras e sons.
img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')
fnt_dir = path.join(path.dirname(__file__), 'font')

# Dados gerais do jogo.
WIDTH = 830 # Largura da tela
HEIGHT = 600 # Altura da tela
FPS = 100 # Frames por segundo

# Define algumas variáveis com as cores básicas
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0    , 255)
YELLOW = (255, 255, 0)
 
# Tamanho dos blocos
block_width = 40
block_height = 25


# Estados para controle do fluxo da aplicação
INIT = 0
PLAYING = 1
QUIT = 2
GAME_OVER = 3
INTRODUCAO = 4

#PLAYING = 5
EXPLODING = 6
DONE = 7
MORREU = 8

LEVEL_CONFIG = {
        1:{"fundo":'norway.png','rows':3,'descricao':"Sua aventura começa nos fiordes da Noruega","submarino":"submarine_pink"},
        2:{"fundo":'underwater2.png','rows':4, 'descricao': "Entrando nas profundezas do oceano","submarino":"submarine_purple"},
        3:{"fundo":'atlantis2.png','rows':5, 'descricao': "Olha! Atlantis!","submarino":"submarine_silver"},
        4:{"fundo":'area_51_2.1.png','rows':6, 'descricao':"Invadindo a Área 51!","submarino":"submarine_green"},
        5:{"fundo":'submarine.png','rows':7, 'descricao': "CENTRO DE COMANDO DO SUBMARINO MASTER","submarino":"submarine_img"},
        6:{"fundo":'ilha.png',"rows":5,"descricao":"FASE FINAL!!!","submarino":"submarine_img"}
         }


GAME_SPEED=1


level=1





def Escreve_nivel(text):
#    fonte= pygame.font.Font(path.join(fnt_dir, "Boogaloo.ttf"), 28)
#    label = fonte.render(text, 1, color)

    texto = ptext.draw(text,
    midbottom=(WIDTH/2,HEIGHT/4), width=360, fontname="fonts\Boogaloo.ttf", fontsize=100, underline=True,
    color="#AAFF00", gcolor="#66AA00", owidth=1.5, ocolor="black", alpha=0.8, angle=5)
    #texto = surface.blit(label, (WIDTH/2, HEIGHT/2))
    return texto

def Escreve_descricao(text):
    texto=ptext.draw(text,
    midbottom=(WIDTH/2,3*HEIGHT/4), width=360, fontname="fonts\Boogaloo.ttf", fontsize=40, underline=False,
    color=WHITE, gcolor="#66AA00", owidth=1.5, ocolor="black", alpha=0.8, angle=0)
    return texto



    
def fade(WIDTH, HEIGHT): 
    fade = pygame.Surface((WIDTH, HEIGHT))
    fade.fill((0,0,0))
    for alpha in range(0, 300):
        fade.set_alpha(alpha)
        #redrawWindow()
        screen.blit(fade, (0,0))
        pygame.display.update()
        pygame.time. delay(3)
        
        
def level_up(WIDTH, HEIGHT,level):
    config=LEVEL_CONFIG[level]
    descricao=config["descricao"]
    if level>1:
        pygame.mixer.music.load(path.join(snd_dir, 'level-up.mp3'))
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(loops=-1)
    fade = pygame.Surface((WIDTH, HEIGHT))
    

    fade.fill((0,0,0))
    for alpha in range(0, 250):
        fade.set_alpha(alpha)
        pygame.time.delay(5)
        if level>1:
            Escreve_nivel("LEVEL UP")
        Escreve_descricao(descricao)
        
        #redrawWindow()
        screen.blit(fade, (0,0))
        pygame.display.update()
        
        
        


def introducao(screen):
    # Variável para o ajuste de velocidade
    clock = pygame.time.Clock()

    # Carrega o fundo da tela inicial
    background = pygame.image.load(path.join(img_dir, 'intro-02.png')).convert()
    background_rect = background.get_rect()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    pygame.mixer.music.load(path.join(snd_dir, 'MissionImpossibleTheme.mp3'))
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(loops=-1)

   
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
                        fade(WIDTH,HEIGHT)
                        state = PLAYING
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
        


## 
#def create_blocks(numero_blocos,inimigo, tiros, blocks, all_sprites):
#        top = 80 
#        imagem_inimigo= pygame.image.load(path.join(img_dir, inimigo)).convert()
#        blockcount=10
#        for row in range(5):
#                for column in range(0, blockcount):
#                    block=Block(column*(block_width+20)+1,top, (imagem_inimigo,tiros)) 
#                    blocks.add(block)
#                    all_sprites.add(block)
#                top += block_height + 2

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
                
def game_over_screen(screen,ret):
    
    level=ret['level']
    clock = pygame.time.Clock()

    background = pygame.image.load(path.join(img_dir, 'GameOver-01.png')).convert()
    background_rect = background.get_rect()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    
    pygame.mixer.music.load(path.join(snd_dir, 'MissionImpossibleTheme.ogg'))
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
                if i == 5:
                    background = pygame.image.load(path.join(img_dir, 'GameOver-0{}.png'.format(i))).convert()
                    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
                    if event.key == pygame.K_n:
                                    state = INIT
                                    level=1
                                    
                                    running=False

                else:
                    background = pygame.image.load(path.join(img_dir, 'GameOver-0{}.png'.format(i))).convert()
                    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
                    i+=1
                
                       
                            
        # A cada loop, redesenha o fundo e os sprites
        screen.fill(BLACK)
        screen.blit(background, background_rect)
    
        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()
        
    return state,level

def morreu(screen, level):
    clock = pygame.time.Clock()
    background = pygame.image.load(path.join(img_dir, 'GameOver-05.png')).convert()
    background_rect = background.get_rect()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = QUIT
                running=False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    state = INIT
                    level=1
        # A cada loop, redesenha o fundo e os sprites
        screen.fill(BLACK)
        screen.blit(background, background_rect)

        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()
    return state


def timer():
    dt = 0
    timer = 100
    t=True
    while t==True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = QUIT
        timer -= dt

        score_font=assets["score_font"]
        time_txt = score_font.render(str(round(timer, 2)), True, BLACK)
        screen.blit(time_txt, (50, 20))
        fps_clock = pygame.time.Clock()
    
        pygame.display.flip()
            # clock.tick(30) limits the game to 30 frames per second.
            # dt = time needed for last frame in ms. /1000 to convert to seconds.
        dt = fps_clock.tick(30) / 1000
        if timer==0:
            state=DONE
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
        self.rect.x += self.speedx*GAME_SPEED
        
        # Mantem dentro da tela
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
                    

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, submarino_img, tiros):

        self.tiros=tiros

        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        # Create the image of the block of appropriate size
        # The width and height are sent as a list for the first parameter.
        self.image = pygame.transform.scale(submarino_img, (45, 30))

        self.image.set_colorkey(BLACK)


        # Fetch the rectangle object that has the dimensions of the image
        self.rect = self.image.get_rect()

        # Move the top left of the rectangle to x,y.
        # This is where our block will appear..
        self.rect.x = x
        self.rect.y = y

    def update(self):

            # Have a random 1 in 200 change of shooting each frame
        if random.randrange(15000) == 0:
            tiro=Tiro([self.rect.centerx, self.rect.bottom], assets["tiros_img"])
            self.tiros.add(tiro)
    


class airplane(pygame.sprite.Sprite):
    # Construtor da classe.
    def __init__(self, img, startPosition, xspeed, tiros):
        self.tiros=tiros

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(path.join(img_dir, 'airplane.png')).convert()
        self.image = pygame.transform.scale(self.image, (45, 30))
        self.rect = self.image.get_rect()
        self.rect.centerx = startPosition[0]
        self.rect.bottom = startPosition[1]
        self.xspeed = xspeed
        self.image.set_colorkey(BLACK)

    def shoot(self):
        if random.randrange(9500) == 0:
            tiro=Tiro([self.rect.centerx, self.rect.bottom], assets["tiros_img"])
            self.tiros.add(tiro)
            
#        chance = random.randint(0,20000)
#        if chance <= 1:
#            shoot = Tiro([self.rect.centerx,self.rect.bottom], assets["tiros_img"])
#            return shoot
#        return None

    def move(self):
        self.rect.x += self.xspeed

    def flip(self):
        self.xspeed = -self.xspeed
        self.image = pygame.transform.flip(self.image, True, False)
        
    #################
#class Shoot(pygame.sprite.Sprite):
#    # Construtor da classe.
#    def __init__(self, img, startPosition, yspeed):
#        pygame.sprite.Sprite.__init__(self)
#        self.image = pygame.image.load(path.join(img_dir, 'airplane_missile.png')).convert()
#        self.image = pygame.transform.scale(self.image, (10, 10))
#        self.rect = self.image.get_rect()
#        self.rect.center = startPosition
#        self.yspeed = yspeed
#        self.image.set_colorkey(BLACK)


#    def move(self):
#        self.rect.y += self.yspeed    
        
class Tiro(pygame.sprite.Sprite):
    def __init__(self, startPosition, tiro_img):

        pygame.sprite.Sprite.__init__(self)

        # Diminuindo o tamanho da imagem.
        #random.randrange(200) == 0:
        self.image = pygame.transform.scale(tiro_img, (10, 10))
        self.image.set_colorkey(BLACK)
        self.rect= self.image.get_rect()
        self.rect.centerx = startPosition[0]
        self.rect.y = startPosition[1]
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
        self.speed = 10.0*GAME_SPEED

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
    assets["submarine_img"] = pygame.image.load(path.join(img_dir, "submarine.png")).convert()
    assets["submarine_pink"] = pygame.image.load(path.join(img_dir, "submarine-rosa.png")).convert()
    assets["submarine_purple"] = pygame.image.load(path.join(img_dir, "submarine-roxo.png")).convert()
    assets["submarine_green"] = pygame.image.load(path.join(img_dir, "submarine-verde.png")).convert()
    assets["submarine_silver"] = pygame.image.load(path.join(img_dir, "submarine-prata.png")).convert()
    assets["airplane_img"] = pygame.image.load(path.join(img_dir, "airplane.png")).convert()
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




def game_screen(screen, assets,level,score,submarino_img) :
    global GAME_SPEED
    
    config=LEVEL_CONFIG[level]
    # Nome do jogo
    pygame.display.set_caption("BELUGA")
    

    
    # Variável para o ajuste de velocidade
    clock = pygame.time.Clock()
    
    # Carrega os sons do jogo
    boom_sound = assets["boom_sound"]
    
    
    # Cria o player. O construtor será chamado automaticamente.
    player = Player(assets["player_img"])
    
    # Carrega a fonte para desenhar o score.
    score_font = assets["score_font"]
    
    submarino=config["submarino"]
    submarino_img = assets[submarino]
    
    
    
    # Cria um grupo de todos os sprites e adiciona o player.
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    blocks = pygame.sprite.Group()
    tiros=pygame.sprite.Group()
    balls = pygame.sprite.Group()
    shoot_group = pygame.sprite.Group()
    subs_group = pygame.sprite.Group()


    
    
    # Loop principal.
    lives = 10

    
    background = fundo_nivel(config['fundo'])
    FPS = 60
    #create_blocks(4,'submarine-prata.png', tiros, blocks, all_sprites)
     # The top of the block (y position)
    top = 80

    font = pygame.font.Font(None, 36)
    
    if level<=len(LEVEL_CONFIG)-1:
        for row in range(config['rows']):
            # 32 columns of blocks
            for column in range(0, 14):
                # Create a block (color,x,y)
                block=Block(column*(block_width+20)+1,top, submarino_img,tiros)
                blocks.add(block)
                all_sprites.add(block)
            # Move the top of the next row down
            top += block_height + 2
    else:
        print(config)
        for a in range(config['rows']):
            
            for y in range(10):
                x = random.randint(50, WIDTH-50)
                vel=random.randint(2,8)
                block = airplane("airplane.png", [x,y*30+40], vel,tiros)
                subs_group.add(block)
                blocks.add(block)
                all_sprites.add(block)
                

        
        

         
    level_done=False    
    state = PLAYING
    while state != QUIT and not level_done:
        
        # Ajusta a velocidade do jogo.
#        clock.tick(FPS)
        
        if state == PLAYING:
            FPS=60
            clock.tick(FPS)



            font = pygame.font.Font(None, 36)
            hits = pygame.sprite.groupcollide(balls, blocks, False, True)
            for hit in hits: # Pode haver mais de um
                score+=100
                hit.bounce(False)
                
                
            if level>len(LEVEL_CONFIG)-1:
                print(blocks)
                for sub in blocks:#subs_group:
                        if sub.rect.right >= WIDTH or sub.rect.left <= 0:
                            sub.flip()
                        sub.move()
                        shoot = sub.shoot()
                        if shoot != None:
                            shoot_group.add(shoot)
                            tiros.add(shoot)
                            all_sprites.add(tiros)

                
                        for shoot in shoot_group:
                            shoot.update()
                

            # Processa os eventos (mouse, teclado, botão, etc).
            for event in pygame.event.get():

                # Verifica se foi fechado.
                if event.type == pygame.QUIT:
                    state = QUIT

                # Verifica se apertou alguma tecla.
                if event.type == pygame.KEYDOWN:
                    # Dependendo da tecla, altera a velocidade.
                    if event.key == pygame.K_LEFT:
                        player.speedx = -10
                    if event.key == pygame.K_RIGHT:
                        player.speedx = 10
                    if event.key == pygame.K_SPACE:
                        ball = Ball(player.rect.x)

                        all_sprites.add(ball)
                        balls.add(ball)

#                       # pew_sound.play()
#                    if event.key ==pygame.K_ESCAPE:
#                        state = PAUSED

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
                if level<len(LEVEL_CONFIG):
                    level+=1
                    GAME_SPEED+=0.25
                    lives+=3
                else:
                    state = DONE
                level_done=True
                        
   

            for ball in balls:
                if ball.y > HEIGHT:
                    lives -= 1
                    ball.kill()

            if lives <= 0:
                state = DONE
                level_done=True
                
                
            
            
               # Verifica se houve colisão entre nave e meteoro
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

        if state == EXPLODING:
            now = pygame.time.get_ticks()
            if now - explosion_tick > explosion_duration:
                if lives == 0:
                    state = DONE
                else:
                    state = PLAYING
                    player = Player(assets["player_img"])
                    all_sprites.add(player)
                    
     

        background_rect=background.get_rect()
        screen.fill(BLACK)
        screen.blit(background, background_rect)
        # Depois de processar os eventos.
        # Atualiza a acao de cada sprite.
        all_sprites.update()
        tiros.update()
        player.update()
        subs_group.draw(screen)
        shoot_group.draw(screen)
        shoot_group.update()

        #pygame.display.update()
        
          
                    
        # A cada loop, redesenha o fundo e os sprites
        
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
    ret ={'state':state,'level':level,'score':score,'FPS':FPS}
    print(ret)        
    return ret 


# Inicialização do Pygame.
pygame.init()
pygame.mixer.init()

# Tamanho da tela.
screen = pygame.display.set_mode((WIDTH, HEIGHT))



# Nome do jogo
pygame.display.set_caption("FBI")
# Carrega todos os assets uma vez só e guarda em um dicionário
assets = load_assets(img_dir, snd_dir, fnt_dir)

score=0
level=1
# Comando para evitar travamentos.
#try:
state = INIT
while state != QUIT:
    if state == INIT:
        state = init_screen(screen)
    if state == INTRODUCAO:
        fade(WIDTH,HEIGHT)
        state=introducao(screen)
    elif state == PLAYING:
        level_up(WIDTH,HEIGHT,level)
        pygame.mixer.music.load(path.join(snd_dir, 'HawaiiFive-O-ThemeSongFullVersion.mp3'))
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(loops=-1)
        ret = game_screen(screen, assets,level,score,FPS)
        score=ret['score']
        level=ret['level']
        state=ret['state']
    elif state == DONE:
        if level==len(LEVEL_CONFIG):
            state,level = game_over_screen(screen,ret)
        else:
            state,level = morreu(screen, level)
    else:
        state = QUIT
#finally:
pygame.quit()

  




