

import pygame
import sys

#Import configs and object calling functions 
from Config import *
from Object import *

from button import Button

###Global variables #Cant import these variables from Config for some reason
FPS = 60 
PLAYER_VEL = 5 
WIDTH, HEIGHT = 1080, 720
block_size = 96
offset_x = 0
offset_y = 0 
Y_scroll_area_width = 200
X_scroll_area_width = 300

#Import main game functions 
from CoA_Run import *

#File manipulation
from os.path import isfile,join

FPS = 60 



#Set a base screen
SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

#Load base BG 
BG = pygame.image.load("assets\Menu\Menu_backgrounds-statescreens\Menu_background.png")

#Pulls a font (DOUBLED IN CoA_Run!!)
def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets\Menu\Text\Text_font.ttf", size)
        


#First we make a class for the game to test the Game state manager in to keep it organised

class Game:
    def __init__(self):
        self.FPS = FPS
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.gameStateManager = GameStateManager('Main_menu')
        
            #Game states
        self.Startscreen = Startscreen(self.screen,self.gameStateManager)
        self.level = Level(self.screen,self.gameStateManager)
        self.play_game = Play_game(self.screen,self.gameStateManager)
        #self.pause = Pause(self.screen,self.gameStateManager)
        self.Main_menu = Main_menu(self.screen,self.gameStateManager)
        #self.end = End(self.screen,self.gameStateManager)
        self.options = Options(self.screen,self.gameStateManager)
            #Dictionary to keep track of game states
        self.states = {'Startscreen': self.Startscreen,
                       'level': self.level, 
                       #'Pause': self.pause,
                       'Play_game':self.play_game,
                       'Main_menu':self.Main_menu,
                       'Options':self.options
                       
                       }


    #Run method of game class, allows player to quit
        #Each game state will need a run method

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
            self.clock.tick(self.FPS)

                #Get the current state THIS IS WHY YOU NEED A run() METHOD IN EACH GAME STATE
            self.states[self.gameStateManager.get_state()].run()
            
                #Update the display and tick the clock
            pygame.display.update()
            self.clock.tick(self.FPS)


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
class Startscreen(Object): #NOT IN USE YET
    def __init__(self,display,gameStateManager,x=0,y=0,size=10):
        super().__init__(x, y, size, size)
        self.display = display
        self.gameStateManager = gameStateManager
            # initialise text object using Text daughter class in Object.py. X and Y determine where on the screen it is
            # and size determines the size of the object
            #ISSUE: TEXT OBJECT IS 8x10 bit sections on a spritesheet... not equal sides and wrapper doesnt account for


            #SIZE HERE IS ESSENTIALLY TEXTBOX SIZE
        #self.letters = Text(0, 0, size= 140)

        #Run method so that we can dynamically change the game state
    def run(self):
        #self.display.fill('red')
        # draw text object using method draw of parent class: Object
        self.display.fill('white')
        #print("This is self.image",self.image)
        #Startscreen.draw(self.letters,self.display,0) # offset_x

        #allow to change game states with user input

        #gets keys pressed
        keys = pygame.key.get_pressed()
        #check key inputs to change game state
        if keys[pygame.K_p]:
            self.gameStateManager.set_state('Play_game')

        if keys[pygame.K_ESCAPE]:
            self.gameStateManager.set_state('Pause')


#Write new pause class including button class from Object.py
#class Pause(Object):
    #Need to:  
        #Initialize a screen 
        #Initialize 3 buttons 
    #def __init__(self,display,gameStateManager,x=0,y=0,size=10):
    #    super().__init__(x, y, size, size)
    #    self.display = display
    #    self.gameStateManager = gameStateManager
            # initialise text object using Text daughter class in Object.py. X and Y determine where on the screen it is
            # and size determines the size of the object
            #ISSUE: TEXT OBJECT IS 8x10 bit sections on a spritesheet... not equal sides and wrapper doesnt account for


            #SIZE HERE IS ESSENTIALLY TEXTBOX SIZE


class Play_game(Button):
    def __init__(self,display,gameStateManager):
        #Standard variables 
        self.display = display
        self.gameStateManager = gameStateManager

        #Init button class
        
          

    
    def run(self):
            #EXECUTE CoA_run in this function!
        from CoA_Run import main_CoA
        main_CoA(SCREEN) #Run main game

      
class Main_menu(Button):
    def __init__(self,display,gameStateManager):
        #Standard variables 
        self.display = display
        self.gameStateManager = gameStateManager

        #Init button class
        #super().__init__() 
        
    #Main loop of main menu 
    def run(self):
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        #Text and rect
        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        #Buttons
        PLAY_BUTTON = Button(image=pygame.image.load("assets/Menu/Buttons/Play Rect.png"), pos=(640, 250), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Menu/Buttons/Options Rect.png"), pos=(640, 400), 
                            text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Menu/Buttons/Quit Rect.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        #Update buttons colour 
        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        #Event for loop 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

                #Changes gamestates here
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    self.gameStateManager.set_state('Play_game')
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    self.gameStateManager.set_state('Options')
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()



class Options(Button):
        def __init__(self,display,gameStateManager):
        #Standard variables 
            self.display = display
            self.gameStateManager = gameStateManager

            #Init button class
            super().__init__(image=None, pos=(640, 460), 
                                text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")


        def run(self):
            OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

            SCREEN.fill("white")

            OPTIONS_TEXT = get_font(45).render("This is the OPTIONS screen.", True, "Black")
            OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
            SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

            OPTIONS_BACK = Button(image=None, pos=(640, 460), 
                                text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

            OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
            OPTIONS_BACK.update(SCREEN)
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                        GameStateManager.set_state(state="Main_menu") ##MISSING STATE HERE?

            pygame.display.update()


#IF WE WANT TO ONLY RUN IF WE CALL THIS FILE
#if __name__ == "__main__":
#    game = Game()
#    game.run()

game = Game()
game.run()
