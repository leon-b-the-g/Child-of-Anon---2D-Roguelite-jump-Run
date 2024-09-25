

import pygame
import sys

from Config import *
from Object import *

######## WHY DOES MY IMAGE IMPORT FUNCTION NOT FIND THE PAUSE SCREENS

#from CoA_Run import load_sprite_sheets

from os.path import isfile,join

# from os import listdir

#Function for grabbing our images needed for displaying the game
def load_menusheets(dir1,dir2,width,height,direction=False):
    path = join("assets", dir1, dir2)

    #List comprehension: For loop in a list, very handy!
    #Grabs all files in a specific directory (within a directory) that I pass into the function
    images = [f for f in listdir(path) if isfile(join(path,f))]
    print("This is images:",images)
    #parse them into a dictionary

    all_menus = {}

    #Parse the images into right and left facing sprites
    for image in images:
        print("this is image:",image)
        #Load the sprite sheet, convert alpha to make them transparent background images
        menu_sheet = pygame.image.load(join(path,image)).convert_alpha()
        sprites = []
        print("This is menu width calc:",menu_sheet.get_width()//width)
        for i in range(menu_sheet.get_width()//width):

            # load the sprite, passing pygame.SRCALPHA to make the image transparent
            surface = pygame.Surface((width,height), pygame.SRCALPHA,32)

            #Blit the sprite sheet onto the surface, export surface

            #Taking specifc section of spritesheet
            rect = pygame.Rect(0,0,width,height)

            #Blit the wanted sprite sheet onto the 0,0 co-ordinate of the NEW surface
            surface.blit(menu_sheet,(0,0),rect)
            sprites.append(pygame.transform.scale2x(surface))


            sprites = all_menus[image.replace(".png","")]
            print("This is sprites:",sprites)
    print("This is all_menus",all_menus)
    return all_menus


#First we make a class for the game to test the Game state manager in to keep it organised

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        
        self.gameStateManager = GameStateManager('Pause')
            #Game states
        self.Startscreen = Startscreen(self.screen,self.gameStateManager)
        self.level = Level_1(self.screen,self.gameStateManager)
        #self.end = End(self.screen,self.gameStateManager)
        self.pause = Pause(self,self.gameStateManager)
        
            #Dictionary to keep track of game states
        self.states = {'Startscreen': self.Startscreen, 'Level_1': self.level, 'Pause': self.pause}
        

    #Run method of game class, allows player to quit
        #Each game state will need a run method

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            #pygame.display.update()
            #self.clock.tick(FPS)

                #Get the current state THIS IS WHY YOU NEED A run() METHOD IN EACH GAME STATE
            self.states[self.gameStateManager.get_state()].run()
            
                #Update the display and tick the clock
            pygame.display.update()
            self.clock.tick(FPS)


    #Making a class for the game state manager+
class GameStateManager:
    def __init__(self, currentState):
        self.currentState = currentState

        #Method to get current state
    def get_state(self):
        return self.currentState

        #Method to update the game state
    def set_state(self, state):
        self.currentState = state


    #Making a class for a level
class Level_1:
    def __init__(self,display,gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager

        
        # Run method so that we can dynamically change the game state
    def run(self):
        self.display.fill('red')
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.gameStateManager.set_state('Pause')

    #Making a class for the Startscreen screen of the game, inheriting from object class, so we can have text on screen
class Startscreen(Object):
    def __init__(self,display,gameStateManager,x=0,y=0,size=10):
        super().__init__(x, y, size, size)
        self.display = display
        self.gameStateManager = gameStateManager
            # initialise text object using Text daughter class in Object.py. X and Y determine where on the screen it is
            # and size determines the size of the object
            #ISSUE: TEXT OBJECT IS 8x10 bit sections on a spritesheet... not equal sides and wrapper doesnt account for


            #SIZE HERE IS ESSENTIALLY TEXTBOX SIZE
        self.letters = Text(0, 0, size= 140)

        #Run method so that we can dynamically change the game state
    def run(self):
        #self.display.fill('red')
        # draw text object using method draw of parent class: Object
        self.display.fill('white')
        #print("This is self.image",self.image)
        Startscreen.draw(self.letters,self.display,0) # offset_x

        #allow to change game states with user input

        #gets keys pressed
        keys = pygame.key.get_pressed()
        #check key inputs to change game state
        if keys[pygame.K_e]:
            self.gameStateManager.set_state('level')

        if keys[pygame.K_ESCAPE]:
            self.gameStateManager.set_state('Pause')


    #Making class for pause screen
class Pause(Object):
    def __init__(self, display, gameStateManager, x=0, y=0, size=10):
        super().__init__(x, y, size, size)
        self.display = display
        self.gameStateManager = gameStateManager

        #loading image from assets into a dictionary
        self.pausescreen = load_menusheets("Menu","Statescreens",175,100)
        print("this is self.pausescreen:",self.pausescreen.keys())

        #Setting default image to be the pause screen
        #self.image = self.pausescreen["Pause-idle"][0]
        self.mask = pygame.mask.from_surface(self.image)
        # Animation count, just like with player animation
        self.animation_count = 0
        # Default animation state. Have to make a function for each state
        self.animation_name = "Pause-idle"

    def new_method(self):
        return 255

    #Method for each state of the pause screen
    #def pause_screen_idle(self):
    #    self.animation_name = "Pause-idle"

    #def pause_screen_resume(self):
    #    self.animation_name = "Pause-resume"

    #def pause_screen_save(self):
    #    self.animation_name = "Pause-save"

    #def pause_screen_quit(self):
     #   self.animation_name = "Pause-quit"


        # Function to get pausescreen, needs size input and dont want to mess up run method with non-self arguements
    #def draw_pausescreen(self,size):
    #    # load a surface

        # load a rect from x = 96 pixel, y = 0 pixel (position on Terrain.png that I want to load the image from)


    #    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    #    rect = pygame.Rect(96, 128, size, size)
    #    # returning the surface on which the image of the block is blit'ed, but then scaled up by 2
    #    surface.blit(self.image, (0, 0), rect)

       #return pygame.transform.scale2x(surface)

        # Run method so that we can dynamically change the game state

    ###CURRENTLY WORKING ON RUN METHOD FOR PAUSE SCREEN
        ###BASED ON FIRE ANIMATION LOOP METHOD
    def run(self):
        #get sprite sheet for specific state
        sprites = self.pausescreen[self.animation_name]
        # get rect for specific sprite
        self.rect = self.pausescreen[self.animation_name].get_rect(topleft=(self.rect.x, self.rect.y))
        self.display.fill('grey')


        #self.draw_pausescreen(self.image)  # offset_x
        Startscreen.run(self.image, self.display, 0)  # offset_x

        # allow to change game states with user input

        # gets keys pressed
        keys = pygame.key.get_pressed()
        # check key inputs to change game state


if __name__ == "__main__":
    game = Game()
    game.run()



