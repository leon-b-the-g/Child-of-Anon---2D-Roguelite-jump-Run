

import pygame
import sys

from Config import *
from Object import *



from CoA_Run import load_sprite_sheets

from os.path import isfile,join

# from os import listdir



#First we make a class for the game to test the Game state manager in to keep it organised

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.gameStateManager = GameStateManager('Startscreen')
        
            #Game states
        self.Startscreen = Startscreen(self.screen,self.gameStateManager)
        self.level = Level(self.screen,self.gameStateManager)
        #self.end = End(self.screen,self.gameStateManager)
        
            #Dictionary to keep track of game states
        self.states = {'Startscreen': self.Startscreen, 'level': self.level, 'Pause': Pause(self.screen,self.gameStateManager)}




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
class Level:
    def __init__(self,display,gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager

        
        # Run method so that we can dynamically change the game state
    def run(self):
        self.display.fill('red')


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


#Write new pause class including button class from Object.py
class Pause():


if __name__ == "__main__":
    game = Game()
    game.run()



