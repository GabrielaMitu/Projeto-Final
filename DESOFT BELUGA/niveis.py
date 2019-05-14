# -*- coding: utf-8 -*-
"""
Created on Sat May 11 22:46:44 2019

@author: gabic
"""


def level01():
        background = 
        self.position = (40, 500)
        tile = image_tile[0].convert()

        ##submarinos

        for w in walls:

            self.walls.add(Wall(w[0], w[1], w[2]))

        for w in walls_side:

            self.walls_side.add(Wall(w[0], w[1], w[2]))


class Level_02(Level):

    

    def __init__(self, player):

        Level.__init__(self, player)

        self.background = image_bg[1].convert()

        self.position = (480, 460)

        tile = image_tile[1].convert()

        

        walls = []

        walls_side = []

        for i in range(0, 561, 40):

            walls_side.append((0, i, tile))

            walls_side.append((960, i, tile))

        for i in range(40, 161, 40):

            walls_side.append((i, 0, tile))

            walls.append((i, 560, tile))            

        for i in range(800, 921, 40):

            walls_side.append((i, 0, tile))

            walls.append((i, 560, tile))

        for i in range(280, 681, 40):

            walls_side.append((i, 0, tile))

            walls.append((i, 560, tile))

            walls.append((i, 520, tile))

        for i in range(120, 801, 40):

            walls.append((i, 400, tile))

        for i in range(320, 641, 40):

            walls.append((i, 280, tile))

            walls.append((i, 120, tile))

        for i in range(200, 241, 40):

            walls.append((i, 200, tile))

        for i in range(720, 761, 40):

            walls.append((i, 200, tile))      

        walls.append((280, 240, tile))

        walls.append((680, 240, tile))

        walls.append((280, 160, tile))

        walls.append((680, 160, tile))

        

        for w in walls:

            self.walls.add(Wall(w[0], w[1], w[2]))

        for w in walls_side:

            self.walls_side.add(Wall(w[0], w[1], w[2]))



        monsters = [ (400, 200), (500, 320), (200, 80), (800, 80) ]

        for m in monsters:

            mm = Monster(m[0], m[1])

            for w in self.walls:

                mm.walls.add(w)

            for w in self.walls_side:

                mm.walls.add(w)

            self.monsters.add(mm)     

        

              

        

        

        

class Level_03(Level):

    

    def __init__(self, player):

        Level.__init__(self, player)

        self.background = image_bg[2].convert()

        self.position = (900, 500)

        tile = image_tile[2].convert()

        

        walls = []

        walls_side = []

        for i in range(0, 561, 40):

            walls_side.append((0, i, tile))

            walls_side.append((960, i, tile))

        for i in range(40, 961, 40):

            walls_side.append((i, 0, tile))

            walls.append((i, 560, tile))            

        walls.append((40, 440, tile))

        walls.append((80, 440, tile))

        walls.append((120, 400, tile))

        walls.append((120, 360, tile))

        walls.append((80, 320, tile))

        walls.append((40, 320, tile))

        walls.append((120, 160, tile))

        walls.append((120, 200, tile))

        walls.append((160, 240, tile))

        walls.append((200, 240, tile))

        walls.append((240, 200, tile))

        walls.append((240, 160, tile))

        for i in range(400, 761, 40):

            walls.append((i, 160, tile)) 

        for i in range(480, 961, 40):

            walls.append((i, 320, tile))     

                   

        for w in walls:

            self.walls.add(Wall(w[0], w[1], w[2]))

        for w in walls_side:

            self.walls_side.add(Wall(w[0], w[1], w[2]))



        monsters = [ (50, 380), (170, 180), (920, 260), (820, 260), (700, 70), (600, 70), (200, 500) ]

        for m in monsters:

            mm = Monster(m[0], m[1])

            for w in self.walls:

                mm.walls.add(w)

            for w in self.walls_side:

                mm.walls.add(w)

            self.monsters.add(mm)     

                

        

        

        

        

        