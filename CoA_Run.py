#See Config.py for list of module initializations 
from Config import *
FPS = 60 #Cant import these variables from Config for some reason
PLAYER_VEL = 5 
WIDTH, HEIGHT = 1280, 720
import pygame

pygame.init()
#Set Caption (working title: Children of Anor), and key parameters
pygame.display.set_caption("Children of Anor")

#Drawing window
#WIDTH AND HEIGHT ARE BEING WIERD
window = pygame.display.set_mode((1280, 720))


#Pulls a font ###FIND A BETTER PLACE FOR THIS
def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets\Menu\Text\Text_font.ttf", size)

###Clickables ###
    ###BUTTONS###
    #pause button
def PB_init():
    unscaled_pause = pygame.image.load("assets\Menu\Buttons\Restart.png") # 21 x 22 pxl 
    new_size = (unscaled_pause.get_width() * 3, unscaled_pause.get_height() * 3) #pulls exact dimensions and scales 
    pause_image = pygame.transform.scale(unscaled_pause, new_size) # scale up
    
        #pause button #Made here because needed in draw
    pause_button = Button(image=(pause_image), pos=(1100, 50 ), 
                        text_input=None, font=get_font(75), base_color="White", hovering_color="Green")
    Button_text = get_font(100).render(None, True, "#b68f40") #Renders font, dont need this but important for drawing
    Button_rect = Button_text.get_rect(center=(0,0)) # need this for making text buttons
    button_surf = pygame.Surface((255, 100), pygame.SRCALPHA)  # need this for making text buttons

    PLAY_MOUSE_POS = pygame.mouse.get_pos() #get player mouse position 
    pause_button.changeColor(PLAY_MOUSE_POS) #Handle pause button interaction
    pause_button.update(window) #Handle pause button interaction
    return pause_button

###FUNCTIONS FOR DRAWING GAME###

def draw (window,background,bg_image,player,objects,offset_x,offset_y):

    #drawing background:
    for tile in background:
        #Passing position that we want to draw at (tile) and also passing the image that we want to draw
        #Can loop because we made tile a tuple in Background.py
        window.blit(bg_image, tile)
        
    #Draw objects
    for obj in objects:
        obj.draw(window,offset_x,offset_y)
    
    #Update window with pause button THIS ALREADY DRAWS THE BUTTON
    #call button_init to make the button
    Pause_onscreen = PB_init()
    PLAY_MOUSE_POS = pygame.mouse.get_pos() #get player mouse position 
    Pause_onscreen.changeColor(PLAY_MOUSE_POS) #Handle pause button interaction
    Pause_onscreen.update(window) #Handle pause button interaction

    player.draw(window,offset_x,offset_y)

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


#Function for loading sprite sheets. ALso in Load_sprites

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



####CLASS FOR PLAYER OBJECT HANDLING####

#Class for generating player object
#Inherits from the Sprite class to help handle collisions
class Player(pygame.sprite.Sprite):
    # Class var - might move gravity to Config later
    COLOR = (255,0,0)
    GRAVITY = 1 # 9.81,but setting this to 1 for now
    ANIMATION_DELAY = 3 #Keeps track of delay between changing sprites


    #Loads sprite, with directories ref. and sprite size and then whether we are having directions
    SPRITES = load_sprite_sheets("MainCharacters","VirtualGuy",32,32,True)
   

    def __init__(self, x, y, width, height):
        super().__init__()

        #Putting variables in a Rect (tuple with 4 variables)
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
        #Hit or not
        self.hit = False
        #Hit count for I frames
        self.hit_count = 0

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
        ###GRAVITY TURNED: ON### Set to 0.8 to make the game feel a little floaty
        self.y_vel += min(0.8, (self.fall_count/FPS) * self.GRAVITY)

        #Moving player each frame/update each frame

        self.move(self.x_vel,self.y_vel)

    #If statement that checks how long player has been in I frame
        if self.hit:
            self.hit_count += 1

        #If player has been hit for more than 2 seconds, set hit to false and reset hit count
        if self.hit_count > FPS * 2:
            self.hit = False
            self.hit_count = 0

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

    def make_hit(self):
        self.hit = True
        self.hit_count = 0


    #Updating sprite sheet based on player movement
    def update_sprite(self):
        #Default
        sprite_sheet = "idle"
        #If hit, we are flashing
        if self.hit:
            sprite_sheet = "hit"
        #If y velocity, we are jumping or falling
        if self.y_vel < 0:
            #jump_count 1 means jump sprite sheet is needed
            if self.jump_count == 1:
                sprite_sheet = "jump"
            #jump_count 2 means double jump sprite sheet is needed
            elif self.jump_count == 2:
                sprite_sheet = "double_jump"

        #If y velocity is positive, we are falling - but glitches unless we have a minimum value
        elif self.y_vel > self.GRAVITY * 2:
            sprite_sheet = "fall"
        #If x velocity, run
        elif self.x_vel != 0:
            sprite_sheet = "run"

        #Get the name of the exact sprite sheet we need
        sprite_sheet_name = sprite_sheet + "_" + self.direction

        #Get the sprites from the dictionary
        sprites = self.SPRITES[sprite_sheet_name]

        #animation count divided by animation delay, modulo the length of the sprites (roughly every 10 frames, change to second sprite etc.)
        #Is dynamic and works for any sprite sheet

        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1

        #Update mask for collision check (mask is a mapping of pixels in the sprite)
        self.update()

    #Updating the rectangle of the character (adjusted based on sprite used)
    def update(self):
        #Updating the rectangle of the character (adjusted based on sprite used)
        self.rect = self.sprite.get_rect(topleft=(self.rect.x,self.rect.y))
        #Getting mask for collisions (mask is a mapping of pixels in the sprite)
        self.mask = pygame.mask.from_surface(self.sprite)

    #Draw method for player
    def draw(self,win,offset_x,offset_y):
        #loading sprite from dictionary: sprites using update method
        #blitting on window
        win.blit(self.sprite,(self.rect.x - offset_x,self.rect.y -offset_y))


###FUNCTIONS FOR COLLISION DETECTION###
#CHECK VERT collision FIRST, then horizontal
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

def collide(player,objects,dx):
    #Displaces player preemptively in x direction by dx and 0 in vertical (y) direction
    player.move(dx,0)
    #Need to update mask before collision check
    player.update()
    #Making a list for collided objects
    collided_objects = None

    #Now check if player would collide if moved
    for obj in objects:
        if pygame.sprite.collide_mask(player,obj):
            #Feeding collided object into collided_objects list
            collided_objects = obj
            break

    #Moving player back to OG spot and then decide if they would collide
    player.move(-dx,0)
    #Updating mask to reverse the move we made
    player.update()
    #Returning all object that the player collided with

    return collided_objects



#Function for handling Movement of player in relation to objects
def handle_move(player,objects):
    #Gets pressed keys
    keys = pygame.key.get_pressed()

    #First we set player velocity to 0, because the player methods set a new velocity and otherwise
    # will continue in one direction until reset
    player.x_vel = 0

    #Checking for collision in x direction
    collide_left = collide(player,objects,-PLAYER_VEL*2) #Note neg X velocity because left is NEG x co ordinate
    collide_right = collide(player,objects,PLAYER_VEL*2) #Note *2 to make sure we are checking far enough ahead for collision
    #Note if we make this value 1.5 its almost like the player is "sticky" to the wall...

    #If keys are pressed, move player

    if keys[pygame.K_LEFT] and not collide_left:
        player.move_left(PLAYER_VEL)

    if keys[pygame.K_RIGHT] and not collide_right:
        player.move_right(PLAYER_VEL)

    #Check vertical collision last
    vertical_collide = handle_vertical_collision(player,objects, player.y_vel)
    to_check = [collide_left,collide_right,*vertical_collide]

    #If we collide with an object, we need to check if we are hitting a trap
    for obj in to_check:
        if obj and obj.name == "fire":
            player.make_hit()


###FUNCTION FOR MAIN GAME LOOP ####


def main_CoA(window):
    #Keep track of loop iterations
    clock = pygame.time.Clock()
    #Get background image, could load different backgrounds for levels here in future
    background, bg_image = get_background("Green.png")
        #Blue.png
        #Brown.png
        #Gray.png
        #Green.png
        #Pink.png
        #Purple.png
        #Yellow.png

    #Block size for floor
    block_size = 96
    #platform_size = 64
    platform_x = 96
    platform_y = 96

    #Create player object
    player = Player(100,100,50,50)

    ###Clickables
    #pause button
    #Loaded image at the start of script
    #pause_image = pygame.image.load("assets\Menu\Buttons\Settings.png") # 21 x 22 pxl
    #Init button
    #pause_button = Button(image=pause_image, pos=(980, 40), 
    #                    text_input=None, font=get_font(75), base_color="White", hovering_color="Green")
   
    ###Enviornment###
    
    #Creating a floor by creating blocks to left and right of a point at the bottom of the screen
    floor = [Block(i* block_size, HEIGHT - block_size,block_size)
             for i in range(-WIDTH//block_size, WIDTH * 2 // block_size)
             ]

    ###PLATFORMS###
    ###floating platforms at 8* height-block_size
    air_blocks=[Block(block_size * i, HEIGHT-block_size *8,block_size)
    for i in range(0,block_size-48,4)] 

    #First few blocks
    blocks = [#Block(block_size*3,HEIGHT-block_size*4,block_size),
              Block(block_size*5,HEIGHT-block_size*4,block_size),
              Block(block_size*7,HEIGHT-block_size*4,block_size),
              Block(block_size*10,HEIGHT-block_size*6,block_size)
              ]
    
    #Winning platform 

        
        #init platformblock 
    first_platform = Platform(block_size*3,HEIGHT-block_size*4,block_size,platform_x,platform_y)
    #first_platform = [Platform(i* platform_size, HEIGHT//2,platform_size)
    #         for i in range(-WIDTH//platform_size, WIDTH * 2 // platform_size)]
    #all_platforms = [Platform(i* block_size, HEIGHT//2,block_size)
    #            for i in range(-WIDTH//block_size, WIDTH * 2 // block_size)]
    #Can build for loops here to make more easily
    #                     for i in range(-WIDTH//platform_width, WIDTH *2 //block_size))

    ###TRAPS###

    fire = Fire(100,HEIGHT-block_size -64, 16, 32)  #Dimensions: 16x32
    fire.on()
    

    ###BUTTONS###
    Pause_onscreen = PB_init()

    #SCREEN.fill("black") WRITE FUNCTION FOR DRAWING BACKGROUND maybe?

    pygame.display.update() # Update (COULD BE SOURCE OF GETTING GAME STUCK)

    #Making a list of objects being drawn, passing floor into this list too
    #This list is used to draw objects in the game loop
    objects = [*floor, *blocks, *air_blocks,first_platform, Block(0,HEIGHT-block_size*2,block_size),
               #This block is roughly in the middle of the screen
               Block(block_size*3,HEIGHT-block_size*4,block_size),
               fire]


    #Creating scrolling backgrounds
    #By offsetting how we draw the background, we can make it look like we scroll through the background
    offset_x = 0
    offset_y = 0 ### IMPLEMENT Y SCROLLING HERE
    Y_scroll_area_width = 200
    X_scroll_area_width = 300

    #### Main game loop###
    run = True
    while run:
        clock.tick(FPS)

        #If we close the window, the game will end
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            #HANDLING JUMP here, could do it in handle_move, but this is cleaner because
                ##if we handle the jump in the Handle move method it would break if any keys are held down
            if event.type == pygame.KEYDOWN:
                #statement allows for double jump! Can add extra jumps or dashes here
                if event.key == pygame.K_SPACE and player.jump_count < 2:
                    player.jump()

            
          
            if event.type == pygame.QUIT:
                pygame.quit()
                os.sys.exit()

            #If we click button, exec main_menu
            PLAY_MOUSE_POS = pygame.mouse.get_pos() #get player mouse position 
            Pause_onscreen.changeColor(PLAY_MOUSE_POS) #Handle pause button interaction DOESNT WORKING TRYING IN IF LOOP
            Pause_onscreen.update(window)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if Pause_onscreen.checkForInput(PLAY_MOUSE_POS):
                   
                    from GameStateManager import Game
                    Pause_onscreen.changeColor("Green")
                    game = Game() #Run Game class from GameStateManager
                    game.run()

        #Run the animation loops, handle movement, draw each frame with the list of objects
        player.loop(FPS)  #runs player
        fire.loop()       #runs fire 
        handle_move(player,objects) #handle movement via input
        draw(window, background, bg_image, player,objects,offset_x,offset_y)
        #window.blit(Button_text, Button_rect)   #draw pause button (after game frame) ###NOT WORKING AS INTENDED ###
        PLAY_MOUSE_POS = pygame.mouse.get_pos() #get player mouse position 
        Pause_onscreen.changeColor(PLAY_MOUSE_POS) #Handle pause button interaction
        Pause_onscreen.update(window) #Handle pause button interaction

        #Handling horizontal scrolling background
            #if im going right im checking if im near the boundary then offsetting x accordingly
            #If im going left, I am checking the other boundary and adjusting x accordingly
        if ((player.rect.right - offset_x >= WIDTH - X_scroll_area_width) and player.x_vel > 0) or (
                (player.rect.left - offset_x <= X_scroll_area_width) and player.x_vel < 0):
            ###JUMP CUT to next screen###
            #offset_x= min(player.rect.right - WIDTH + scroll_area_width, WIDTH * 2 - WIDTH)
            #SCROLLING###
            offset_x += player.x_vel

        #Handles vertical scrolling 
        if ((player.rect.top - offset_y >= HEIGHT - Y_scroll_area_width) and player.y_vel > 0)or (
                (player.rect.bottom - offset_y <= Y_scroll_area_width) and player.y_vel < 0):
                #CAN ADD OR STATEMENT TO ADD DOWNWARD SCROLLING
            ###JUMP CUT to next screen###
            #offset_x= min(player.rect.right - WIDTH + scroll_area_width, WIDTH * 2 - WIDTH)
            #SCROLLING###
            offset_y += player.y_vel
    pygame.quit()
    quit()

#Runs game only if we are running this script directly
if __name__ == "__main__":
    main_CoA(window)
