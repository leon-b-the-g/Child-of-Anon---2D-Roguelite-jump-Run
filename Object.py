#from Background import *
#from Draw import *
import pygame

from Config import *

import os
#Display window
WIDTH, HEIGHT = 1280, 720

from os import listdir

from os.path import isfile,join


pygame.init()





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
    def draw(self,win,offset_x,offset_y): #offset_y
        #Minusing offset_x to make the player move left and right on the screen
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y - offset_y))


#Class for generating blocks
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

#Class for generating text
class Text(Object):
    def __init__(self,x,y,size):
        #need to pass 4 arguments to the super init constructor, duplicating size as it's the same
        # for width and height for now
        super().__init__(x,y,size,size)

        #Load image with get_text function
        self.letters = get_text(size)

        ###WORKS!!!! Put draw function here maybe to draw specific text? BUT IT WORKS!!!
        #Blit image onto surface
        self.image.blit(self.letters['H'][0], (0,0))
        self.image.blit(self.letters['E'][0], (14,0))
        self.image.blit(self.letters['H'][0], (28, 0))
        self.image.blit(self.letters['E'][0], (42, 0))

        #self.image.blit(self.image, (0,0))
        self.mask = pygame.mask.from_surface(self.image)

#Class for generating platforms
class Platform(Object):
    def __init__(self,x,y,width,height):
        super().__init__(x,y,width,height)
        #function for loading platform (using get platform function) then blitting it 
            #CAN DECLARE SIZE HERE, good if we dont have equal width and height of obj

        #from Load_sprites import load_sprite_sheets
        #self.platform = load_sprite_sheets("Terrain","",width,height)
        #print("This is self.platform:",self.platform)
        #self.image = self.platform["Terrain"][6] # takes the only iteration of images we want from the dict laod_sprite_sheets creates

        # Updating the rectangle of the character (adjusted based on sprite used)
        #self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))

        # Update mask for collision check (mask is a mapping of pixels in the sprite)
        #self.mask = pygame.mask.from_surface(self.image)



#load USING load_sprite_sheets, kinda works, but restricted to one "line" 
        #path = join("assets","Terrain","Terrain.png")
        #get image (load via path)
        #self.image = pygame.image.load(path).convert_alpha()

        #self.surface = pygame.Surface((width,height), pygame.SRCALPHA, 32)
        #load a rect from x = 96 pixel, y = 0 pixel (position on Terrain.png that I want to load the image from)
        #rect = pygame.Rect(192, 64,width,height)
            ###x:96 y:128 is PINK BLOCK
            ###x:96, y:0 is GREEN NORMAL BLOCK
        #Blit the image onto the surface (but only the part of the image that I want)
        #self.surface.blit(self.image, (0,0), rect)


        self.width = width
        self.height = height

        #returning the surface on which the image of the block is blit'ed, but then scaled up by 2
        
        #Load image
        platform = get_platform(self.width,self.height)
        #Blit image onto surface
        self.image.blit(platform, (0,0))

        #Grab mask for collision detection
        self.mask = pygame.mask.from_surface(self.image)

#Class for generating fire
class Fire(Object):
    #Animation delay class variable to make its animation independent of the frame rate
    ANIMATION_DELAY = 3

    def __init__(self,x,y,width,height):
        super().__init__(x,y,width,height,"fire") #NOTE passing optional name here, helps determine what object
        #is being collided with in CoA_Run.py
        from Load_sprites import load_sprite_sheets
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




#Function for loading block images
def get_block(size):
    path = join("assets","Terrain","Terrain.png")
    #get image (load via path)
    image = pygame.image.load(path).convert_alpha()

    #load , size= width, height of our surface
    surface = pygame.Surface((size,size), pygame.SRCALPHA, 32)
    #load a rect from x = 96 pixel, y = 0 pixel (position on Terrain.png that I want to load the image from)
    rect = pygame.Rect(96,0,size,size)
        ###x:96 y:128 is PINK BLOCK
        ###x:96, y:0 is GREEN NORMAL BLOCK
    #Blit the image onto the surface (but only the part of the image that I want)
    surface.blit(image, (0,0), rect)


    #returning the surface on which the image of the block is blit'ed, but then scaled up by 2
    return pygame.transform.scale2x(surface)

def clip_block(surface, x, y, x_size, y_size): #Get a part of the image
        # x, y = position of image on original surface
        # x_size,y_size = new size of image 
    handle_surface = surface.copy() #Sprite that will get process later
    clipRect = pygame.Rect(x,y,x_size,y_size) #Part of the image
    handle_surface.set_clip(clipRect) #Clip or you can call cropped
    image = surface.subsurface(handle_surface.get_clip()) #Get subsurface
    return image.copy() #Return



#Function for loading block images
def get_platform(width,height):
    path = join("assets","Terrain","Terrain.png")
    #get image (load via path)
    image = pygame.image.load(path).convert_alpha()
        #Orange platform
            #location: 192, 128
            #Dimensions 16, 72

        ###x:96 y:128 is PINK BLOCK 
        ###x:96, y:0 is GREEN NORMAL BLOCK
    #load a surface
    #Create a new surface

    surface = pygame.Surface((width, height), pygame.SRCALPHA, 32) #image size

    #X and Y are horizontal and vertical dimensions in px respectively.
    rect = pygame.Rect(192,64, width,height)
    #Blit the image on the surface
   
    surface.blit(image, (0,0), rect)
    #surface.blit(image, (192, 64), (0, 0, 16, 48) )
    #surface.blit(image, (x, y), (cut_x, cut_y, x_size, y_size) )
    #x and y are the distance from the top left corner. This places the image on the surface x px down and y px left.

    #cut_x and cut_y are the cropped part of the image from the top left corner. cut_x px down, cut_y px left.

    #x_size,y_size and F define the image size.
    #load a rect from x = 192 pixel, y = 64, because of grey platform dimensions
                            #platform_rect = clip_block(surface, x=192,y=60, x_size=16,y_size=48) # call clip_block to get new image we want
        ###x:96 y:128 is PINK BLOCK
        ###x:96, y:0 is GREEN NORMAL BLOCK

    

    #returning the surface on which the image of the block is blit'ed, but then scaled up by 2
    return pygame.transform.scale2x(surface)
  



# Function for loading text sprite sheet
def get_text(size):
    #MIGHT NOT WORK BECAUSE TEXT.PNG IS ONE DIRECTORY DEEPER
    path = join("assets", "Menu", "Text(White)(8x10).png")

    
    #loading text sprite sheet in the dimensions 8x10 (which is what we want)
    from Load_sprites import load_sprite_sheets
    all_text = load_sprite_sheets("Menu","Text",8,10)
    print(all_text)
        #Parsing letters into dictionary, loaded:
            #Key: Text(Black)(8x10).png , Text(Black)(8x10).png
            #Value: List of Surfaces

     # load a rect

    ABC_dict = {'A': [], 'B': [], 'C': [], 'D': [], 'E': [], 'F': [], 'G': [], 'H': [], 'I': [], 'J': [],
                'K': [], 'L': [], 'M': [], 'N': [], 'O': [], 'P': [], 'Q': [], 'R': [], 'S': [], 'T': [],
                'U': [], 'V': [], 'W': [], 'X': [], 'Y': [], 'Z': []}

    #Make me a list for the ABC
    ABC_list = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    letter_count = 0

    ###I BUILT THIS I AM A GENIUS
    #For loop - goes through all the letters in the dictionary, then assigns a surface from a value in the dictionary
    #containing the surfaces of the letters accordingly
    #Stops at 26 letters
    for k,v in all_text.items():
        for surface in all_text.values():
            for letter in surface:
                ABC_dict[ABC_list[letter_count]].append(letter)
                letter_count += 1
                if letter_count == 26:
                    break
        print(ABC_dict)

        #Returns a perfect dictionary, with keys of letters, and values with according surfaces
        return ABC_dict


