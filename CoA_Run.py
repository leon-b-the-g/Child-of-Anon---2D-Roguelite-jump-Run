#Importng from my scripts


from Background import *
from Player import *
from Object import *

#Other important modules
import os
import random
import math
import pygame

from os import listdir

from os.path import isfile,join

###CONFIGS###

#BG_Colour = (255,255,255)
FPS = 60
PLAYER_VEL = 5


###INITIALISING GAME WINDOW###
#Display window
WIDTH, HEIGHT = 1000, 800



pygame.init()
#Set Caption (working title: Children of Anor), and key parameters
pygame.display.set_caption("Children of Anor")

#Drawing window
window = pygame.display.set_mode((WIDTH,HEIGHT))





###FUNCTIONS FOR DRAWING GAME###

def draw (window,background,bg_image,player,objects):

    #drawing background:
    for tile in background:
        #Passing position that we want to draw at (tile) and also passing the image that we want to draw
        #Can loop because we made tile a tuple in Background.py
        window.blit(bg_image, tile)

    #Draw objects
    for obj in objects:
        obj.draw(window)

    player.draw(window)
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


#Function for loading sprite sheets

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



####CLASS FOR PLAYER OBJECT HANDLING###

#Class for generating player object
#Inherits from the Sprite class to help handle collisions
class Player(pygame.sprite.Sprite):
    # Class var - might move gravity to Config later
    COLOR = (255,0,0)
    GRAVITY = 1 # 9.81,but setting this to 1 for now
    ANIMATION_DELAY = 3 #Keeps track of delay between changing sprites


    #Loads sprite, with directories ref. and sprite size and then whether we are having directions
    SPRITES = load_sprite_sheets("MainCharacters","MaskDude",32,32,True)


    def __init__(self, x, y, width, height):

        #Putting variables in a Rect (tuple with 4 variables)
        super().__init__()
        self.rect = pygame.Rect (x,y,width,height)
        self.x_vel = 0
        self.y_vel = 0
        #Mask for collisions
        self.mask = None

        #Default direction to help keep track of player direction
        self.direction = "left"
        #Default animation count to help keep track of player animation
        self.animation_count = 0
        #How long have we been falling
        self.fall_count = 0
        #Jump count to keep track of how many times we have jumped
        self.jump_count = 0
        ###, cleaner __init__function statement
        self.sprite = pygame.Surface((width, height), pygame.SRCALPHA)

    def jump(self):
        # negative gravity to make the player jump up
        self.y_vel = -self.GRAVITY * 8
        #reset animation count
        self.animation_count = 0
        #increment jump count
        self.jump_count += 1
        #RESET fall count if it's the first jump
        if self.jump_count == 1:
            self.fall_count = 0



    def move(self, dx, dy):
        #Changing the position of the player by dx and dy
        self.rect.x += dx
        self.rect.y += dy

    def move_right(self,vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0 #Resetting animation count

        #Note , negative x velocity since negative x co ordinate is left
    def move_left(self,vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0 #Resetting animation count


    #Not using these yet, but up down in theory too
    def move_up(self,vel):
        self.y_vel = -vel

    def move_down(self,vel):
        self.y_vel = vel

    ###PLAYER LOOP###
    def loop (self,FPS):

        #If player is falling, increment fall count by 1 OR by time falling/FPS multiplied by GRAVITY
        #CAN CHANGE MIN VAL HERE TO CHANGE FEEL OF GRAVITY
        ###GRAVITY TURNED: OFF###
        self.y_vel += min(1, (self.fall_count/FPS) * self.GRAVITY)

        #Moving player each frame/update each frame

        self.move(self.x_vel,self.y_vel)

        self.fall_count += 1
        #Calling update sprite method each frame (loop iteration), to update sprite
        ### constantly updating object with gravity, so jump "wears off"
        self.update_sprite()

    def landed(self):
        #reset fall count
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0


    def hit_head(self):
        self.count = 0
        #This is to stop the player from moving up if they hit their head, and bounce them down
        self.y_vel *= -1

    def update_sprite(self):
        #Default
        sprite_sheet = "idle"

        #If y velocity, we are jumping or falling
        if self.y_vel < 0:
            #jump count 1 means jump sprite sheet is needed
            if self.jump_count == 1:
                sprite_sheet = "jump"
            #jump count 2 means double jump sprite sheet is needed
            elif self.jump_count == 2:
                sprite_sheet = "double_jump"
        #If y velocity is positive, we are falling - but glitches unless we
        elif self.y_vel > self.GRAVITY * 2:
            sprite_sheet = "fall"
        #If x velocity, run
        elif self.x_vel != 0:
            sprite_sheet = "run"


        #Get the name of the exact sprite sheet we need
        sprite_sheet_name = sprite_sheet + "_" + self.direction
        #Get the sprites from the dictionary
        sprites = self.SPRITES[sprite_sheet_name]

        #animation count divided by animation delay, modulo the length of the sprites (every 10 frames, change to second sprite etc.)
        #Is dynamic and works for any sprite sheet

        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        #Update mask for collision
        self.update()

    def update(self):
        #Updating the rectangle of the character (adjusted based on sprite used)
        self.rect = self.sprite.get_rect(topleft=(self.rect.x,self.rect.y))
        #Getting mask for collisions (mask is a mapping of pixels in the sprite)
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self,win):
        #loading sprite from dictionary: sprites using update method
        #blitting on window
        win.blit(self.sprite,(self.rect.x,self.rect.y))


###FUNCTIONS FOR COLLISION DETECTION###
def handle_vertical_collision(player, objects, dy):
    #Make a list for collided objects
    collided_objects = []
    #Check passed objects for collision
    for obj in objects:
        #THIS LINE LETS US USE MASKS FOR COLLISION DETECTION
        if pygame.sprite.collide_mask(player,obj):
            #If dy is positive, we are moving down, so we need to set the bottom of the player to the top of the object
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            #if dy is negative, we are moving up, so we need to set the top of the player to the bottom of the object
            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()

        #Append object to collided objects list
        collided_objects.append(obj)
    return collided_objects # return list of collided objects




def handle_move(player,objects):
    #Gets pressed keys
    keys = pygame.key.get_pressed()

    #First we set player velocity to 0, because the player methods set a new velocity and
    # will continue in one direction until reset
    player.x_vel = 0
    if keys[pygame.K_LEFT]:
        player.move_left(PLAYER_VEL)

    if keys[pygame.K_RIGHT]:
        player.move_right(PLAYER_VEL)

    handle_vertical_collision(player,objects, player.y_vel)


###FUNCTION FOR MAIN GAME LOOP ####

#Main game loop
def main(window):
    #Keep track of loop iterations
    clock = pygame.time.Clock()
    #Get background image, could load different backgrounds for levels here in future
    background, bg_image = get_background("Green.png")

    #
    block_size = 96

    #Create player object
    player = Player(100,100,50,50)

    #Create a floor, creating blocks to left and right of screen

    floor = [Block(i* block_size, HEIGHT - block_size,block_size)
             for i in range(-WIDTH//block_size, WIDTH * 2 // block_size)]


    run = True
    while run:
        clock.tick(FPS)

        #If we close the window, the game will end
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            #HANDLING JUMP here, could do it in handle_move, but this is cleaner because
                ##Handle move version would break if any keys are held down
            if event.type == pygame.KEYDOWN:
                #And statement allows for double jump!
                if event.key == pygame.K_SPACE and player.jump_count < 2:
                    player.jump()


        #Run the player loop, handle movement, draw update (each frame)
        player.loop(FPS)
        handle_move(player,floor)
        draw(window, background, bg_image, player,floor)


    pygame.quit()
    quit()

#Runs game only if we are running this script directly
if __name__ == "__main__":
    main(window)
