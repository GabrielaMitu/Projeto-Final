import pygame
import math


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0    , 255)
YELLOW = (255, 255, 0)


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
