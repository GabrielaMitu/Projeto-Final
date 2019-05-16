import pygame

# Define algumas variáveis com as cores básicas
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0    , 255)
YELLOW = (255, 255, 0)

# Dados gerais do jogo.
WIDTH = 800 # Largura da tela
HEIGHT = 600 # Altura da tela

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
        self.radius = 70

    # Metodo que atualiza a posição da beluga
    def update(self):
        self.rect.x += self.speedx

        # Mantem dentro da tela
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
