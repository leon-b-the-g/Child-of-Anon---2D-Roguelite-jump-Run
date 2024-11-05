

#BG_Colour = (255,255,255)

#Display window
WIDTH, HEIGHT = 1280, 720

###CONFIGS###

#BG COLOUR ON FOR GAMESTATEMANAGER TEST
BG_Colour = (255,255,255)


PLAYER_VEL = 5
FPS = 60 
CHUNK_SIZE = 4 ##CHANGE according ratio of screen, 4x 96 (tile size) 384 pixel in 1 chunk
                ### N chunks in axis = N of pixels in axis / N of pixels in chunk
                
# 

###Global variables #Cant import these variables from Config for some reason
FPS = 60 
PLAYER_VEL = 5 
WIDTH, HEIGHT = 1080, 720
block_size = 96
offset_x = 0
offset_y = 0 
Y_scroll_area_width = 200
X_scroll_area_width = 300

from os import listdir

from os.path import isfile,join



from Background import *    

from Object import *       #Object classes: Block, Text, Fire , 
#from Object import Block   #Have to specifically import Block class for some reason

from Load_sprites import * #load_sprite_sheets
from button import *       #Button classes: button , Methods: CheckForInput, changeColor,update
#from GameStateManager import *

#Other important modules
from os import listdir
from os.path import isfile,join
import random
import math


#THINGS TO ADD#