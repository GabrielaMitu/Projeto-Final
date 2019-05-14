# -*- coding: utf-8 -*-
"""
Created on Sun May 12 08:52:12 2019

@author: gabic
"""

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
 
# Size of break-out blocksnit()
pygame.init()
pygame.mixer.init()


block_width = 23
block_height = 15


def load_assets(img_dir, snd_dir, fnt_dir):
    assets = {}
    
    assets["score_font"] = pygame.font.Font(path.join(fnt_dir, "PressStart2P.ttf"), 28)
    
    return assets

assets = load_assets(img_dir, snd_dir, fnt_dir)
score_font = assets["score_font"]


####trocar fonte

###############
def draw_text_middle(text, size, color, surface):
    label = score_font.render(text, 1, color)
 
    surface.blit(label, (WIDTH/2 - (label.get_width() / 2), HEIGHT/2 - label.get_height()/2))



def main_menu():
    
    tela = pygame.display.set_mode((WIDTH, HEIGHT))
    run = True
    while run:
        tela.fill((0,150,175))
        draw_text_middle('Aperte qualquer tecla para começar', 60, WHITE, tela)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
 
            if event.type == pygame.KEYDOWN:
                state = PLAYING 
  #  pygame.quit()
    
main_menu()  



#def Main_Menu(self): 
#        state= MENU
#        surface=pygame.surface.fill(BLUE)
#        window_width=WIDTH
#        window_height=HEIGHT
#        title="MAIN MENU"
#        text_surface = score_font.render("Aperte uma tecla para começar", True, YELLOW)
#        text_rect = text_surface.get_rect()
#        text_rect.midtop = (WIDTH / 2,  10)
#        screen.blit(text_surface, text_rect)
#        pygameMenu.Menu(surface, window_width, window_height, font, title) # -> Menu object
#        for event in pygame.event.get():
#                        # Verifica se foi fechado.
#                        if event.type == pygame.QUIT:
#                            state = DONE
#                        # Verifica se apertou alguma tecla.
#                        if event.type == pygame.KEYDOWN:
#                            state=PLAYING