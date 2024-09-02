

#Importing necessary libraries




#from Background import *
#from Draw import *
import pygame
from Config import *

import os
#Display window
WIDTH, HEIGHT = 1000, 800

from os import listdir

from os.path import isfile,join


pygame.init()
#Set Caption (working title: Children of Anor), and key parameters
pygame.display.set_caption("Children of Anor")

#Drawing window
window = pygame.display.set_mode((WIDTH,HEIGHT))


###Functions for handling movement of player/sprites in game ###



