#from Background import *
#from Draw import *
import pygame

from CoA_Run import load_sprite_sheets
from Config import *
import os
#Display window
WIDTH, HEIGHT = 1000, 800

from os import listdir

from os.path import isfile,join


pygame.init()

#Function for loading block images
def get_block(size):
    path = join("assets","Terrain","Terrain.png")
    #get image (load via path)
    image = pygame.image.load(path).convert_alpha()

    #load a surface
    surface = pygame.Surface((size,size), pygame.SRCALPHA, 32)
    #load a rect from x = 96 pixel, y = 0 pixel (position on Terrain.png that I want to load the image from)
    rect = pygame.Rect(96,128,size,size)
        ###x:96 y:128 is PINK BLOCK
        ###x:96, y:0 is GREEN NORMAL BLOCK
    #Blit the image onto the surface (but only the part of the image that I want)
    surface.blit(image, (0,0), rect)


    #returning the surface on which the image of the block is blit'ed, but then scaled up by 2
    return pygame.transform.scale2x(surface)


#Make a super class for all objects in the game to inherit from
class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()

        #Rect for object
        self.rect = pygame.Rect(x, y, width, height)

        #Load the sprite sheet, convert alpha to make them transparent background images
        self.image = pygame.Surface((width,height), pygame.SRCALPHA)

        #Image properties
        self.width = width
        self.height = height
        self.name = name

    #Draw method for Object parent class
    def draw(self,win,offset_x): #offset_y
        #Minusing offset_x to make the player move left and right on the screen
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))


#Class for generating blocks
class Block(Object):
    def __init__(self,x,y,size):
        #need to pass 4 arguments to the super init constructor, duplicating size as it's the same
        # for width and height for now
        super().__init__(x,y,size,size)

        #Load image
        block = get_block(size)
        #Blit image onto surface
        self.image.blit(block, (0,0))

        #Grab mask for collision detection
        self.mask = pygame.mask.from_surface(self.image)



#Class for generating fire
class Fire(Object):
    #Animation delay class variable to make its animation independent of the frame rate
    ANIMATION_DELAY = 3

    def __init__(self,x,y,width,height):
        super().__init__(x,y,width,height,"fire") #NOTE passing optional name here, helps determine what object
        #is being collided with in CoA_Run.py
        self.fire = load_sprite_sheets("Traps","Fire",width,height)

        #Load image
        self.image = self.fire["off"][0]
        self.mask = pygame.mask.from_surface(self.image)
        #Animation count, just like with player animation
        self.animation_count = 0
        #Default animation state. Have to make a function for each state
        self.animation_name = "off"

    def on(self):
        self.animation_name= "on"

    def off(self):
        self.animation_name = "off"

    #Loop animation of fire, based on what I did with the player sprites
    def loop(self):
        # Get the sprites of the fire from the dictionary
        sprites = self.fire[self.animation_name]

        # animation count divided by animation delay, modulo the length of the sprites (roughly every 10 frames, change to second sprite etc.)
        # Is dynamic and works for any sprite sheet

        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1   #Incrementing animation count each loop

        # Updating the rectangle of the character (adjusted based on sprite used)
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        # Update mask for collision check (mask is a mapping of pixels in the sprite)
        self.mask = pygame.mask.from_surface(self.image)

        #CHECK if animation count isnt getting too high for statically animated sprites bec otherwise it will crash the game
        if self.animation_count // self.ANIMATION_DELAY > len(sprites): #Not doing this with player bec it kills double jump
            self.animation_count = 0
