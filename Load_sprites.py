#CONFIGS
#from Config import *
from Config import WIDTH, HEIGHT

#Other important modules
import os
import random
import math
import pygame

from os import listdir

from os.path import isfile,join




pygame.init()
#Set Caption (working title: Children of Anor), and key parameters
pygame.display.set_caption("Children of Anor")

#Drawing window
window = pygame.display.set_mode((WIDTH,HEIGHT))

#window = pygame.display.set_mode((1340, 720))



###FUNCTIONS FOR DRAWING GAME###

def draw (window,background,bg_image,player,objects,offset_x):

    #drawing background:
    for tile in background:
        #Passing position that we want to draw at (tile) and also passing the image that we want to draw
        #Can loop because we made tile a tuple in Background.py
        window.blit(bg_image, tile)

    #Draw objects
    for obj in objects:
        obj.draw(window,offset_x)

    player.draw(window,offset_x)
    #Update each frame, clears screen each frame
    pygame.display.update()


def get_background(name):
    #gets image path
    image = pygame.image.load(join("assets", "Background", name))

    #get width and height of image
    _, _, width, height = image.get_rect()
    #Make list for tiles
    tiles = []

    #now looping through to see how many tiles we need in x and y direction
    for i in range (WIDTH // width +1):
        for j in range (HEIGHT // height +1):
            pos = (i * width, j * height)
            tiles.append(pos)

            #denoting the new position of the image that im currently adding
            #Made tuple here to make draw function easier in Draw.py

    #Return the image paths and their tile positions
    return tiles, image


###Functions for handling movement of player/sprites in game ###


def flip(sprites):
    #Flips the sprite sheet to get the left side of the sprite sheet
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]




def load_sprite_sheets(dir1,dir2,width,height,direction=False):
    path = join("assets", dir1, dir2)

    #List comprehension: For loop in a list, very handy!
    #Grabs all files in a specific directory (within a directory) that I pass into the function
    images = [f for f in listdir(path) if isfile(join(path,f))]

    #parse them into a dictionary

    all_sprites = {}

    #Parse the images into right and left facing sprites
    for image in images:
        #Load the sprite sheet, convert alpha to make them transparent background images

        sprite_sheet = pygame.image.load(join(path,image)).convert_alpha()

        sprites = []
        #Get width and height of sprite sheets
        for i in range(sprite_sheet.get_width()//width):

            # load the sprite, passing pygame.SRCALPHA to make the image transparent
            surface = pygame.Surface((width,height), pygame.SRCALPHA,32)

            #Blit the sprite sheet onto the surface, export surface

            #Taking specifc section of spritesheet
            rect = pygame.Rect(i*width,0,width,height)

            #Blit the wanted sprite sheet onto the 0,0 co-ordinate of the NEW surface
            surface.blit(sprite_sheet,(0,0),rect)
            sprites.append(pygame.transform.scale2x(surface))

            if direction:
                #since we got all the right sides of the sprite sheet, I´ll flip them to get the left side
                #Then we are feeding the left(flipped) and right sprites into the dictionary
                all_sprites[image.replace(".png","") + "_right"] = sprites
                all_sprites[image.replace(".png","") + "_left"] = flip(sprites)

            else:
                #Cuts out png before adding to the dictionary
                all_sprites[image.replace(".png","")] = sprites
            #Now there is a sprite sheet with all the sprites in it, next:
                # pulling individual sprites from sprite sheet dictionary:
    return all_sprites
