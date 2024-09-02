#Importng from my scripts
from Config import *
from Background import *
from Player import *

#Other important modules
import os
import random
import math
import pygame

from os import listdir

from os.path import isfile,join

pygame.init()


def draw (window,background,bg_image,player):
    """

    :rtype: object
    """
    #drawing background:
    for tile in background:
        #Passing position that we want to draw at (tile) and also passing the image that we want to draw
        #Can loop because we made tile a tuple in Background.py
        window.blit(bg_image, tile)
    player.draw(window)
    #Update each frame, clears screen each frame
    pygame.display.update()

