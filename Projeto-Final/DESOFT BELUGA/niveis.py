# -*- coding: utf-8 -*-
"""
Created on Sat May 11 22:46:44 2019

@author: gabic
"""


def level(velocidade, imagem, musica, numero_blocos, imagem_submarino):
         
        FPS = velocidade
        background = imagem
        background_rect = background.get_rect()

        pygame.mixer.music.load(path.join(snd_dir, musica))
        pygame.mixer.music.set_volume(0.4)

        top = 80 
 
# Number of blocks to create
        blockcount = numero_blocos


#font = pygame.font.Font(None, 36)
# --- Create blocks
 
# Five rows of blocks
for row in range(5):
    # 32 columns of blocks
    for column in range(0, blockcount):
        # Create a block (color,x,y)
        block=Block(column*(block_width+20)+1,top, (imagem_submarino,tiros))
        blocks.add(block)
        all_sprites.add(block)
    # Move the top of the next row down
    top += block_height + 2


