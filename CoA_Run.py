#See Config.py for list of module initializations 
from Config import *


import pygame

###Global variables #Cant import these variables from Config for some reason
FPS = 60 
PLAYER_VEL = 5 
WIDTH, HEIGHT = 1340, 720
block_size = 96
offset_x = 0
offset_y = 0 
Y_scroll_area_width = 200 
X_scroll_area_width = 300 #at what distance from the sides of screen we start scrolling 

player_world_x = 0  #track x pos of player in world 
player_world_y = 0  #track y pos of player in world 

# Chunk storage
generated_chunks = {}
CHUNK_OFFSET = 128  # How much we generate offscreen to allow for smooth scrolling
# Screen settings
SCREEN_WIDTH = 1340
SCREEN_HEIGHT = 720

#Chunk settings 
CHUNK_WIDTH = 1340  # Width of each chunk
CHUNK_HEIGHT = 96  # Height of each chunk 
TILE_SIZE = 48
PLATFORM_WIDTH = 96  # Size of each tile
PLATFORM_HEIGHT = 32

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

#
RUNGAME = True


pygame.init()
#Set Caption (working title: Children of Anor), and key parameters
pygame.display.set_caption("Children of Anor")

#Drawing window
#WIDTH AND HEIGHT ARE BEING WIERD
window = pygame.display.set_mode((1340, 720))


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



###FUNCTION FOR DRAWING GAME###

def draw (window,background,bg_image,player
        ,objects,offset_x,offset_y): 

    #drawing background:
    for tile in background:
        #Passing position that we want to draw at (tile) and also passing the image that we want to draw
        #Can loop because we made tile a tuple in Background.py
        window.blit(bg_image, tile)

    ###Failed idea for drawing the game_map here, the arguement must be a rect style object when passed into draw function
    #For each key value pair in dictionary, we need to grab the xy co ordinate (key; an array) and the value (block object)
    #for keys,values in game_map.items():
    #    coordinates = keys.split(";")
    #    #make an object using the coordinates 
    #    make_a_block = Platform(coordinates[0],coordinates[1],96,32)
    #    print("THis is make_a_block;",type(make_a_block))
    #    objects.append(make_a_block)

    #Draw objects
    for obj in objects:
        obj.draw(window,offset_x,offset_y)
    
    #Update window with pause button THIS ALREADY DRAWS THE BUTTON
    #call button_init to make the button
    Pause_onscreen = PB_init()
    #PLAY_MOUSE_POS = pygame.mouse.get_pos() #get player mouse position 
    #Pause_onscreen.changeColor(PLAY_MOUSE_POS) #Handle pause button interaction
    Pause_onscreen.update(window) #Handle pause button interaction

    
    #draw health bar
    #player.healthbar_init()
    #player.update_healthbar()

    #health_bar.draw(window) # Refactored into player class
    #Update each frame, clears screen each frame
    player.draw(window, offset_x,offset_y)
    player.draw_health_bar(window)
    pygame.display.update()

###Drawing background tiles
def get_background(name):
    """draws background tiles using Background image in assets folder"""
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

###renders game world chunks 

def generate_chunk(chunk_x,chunk_y):
    """Function to generate a chunk"""
    chunk_data = []
    
    # Let's generate platforms at random y positions within this chunk
    for _ in range(random.randint(10, 15)):  # Random number of platforms 
        
        platform_x = random.randrange((chunk_x * CHUNK_WIDTH), ((chunk_x + 1) * CHUNK_WIDTH - TILE_SIZE ), 192)
        platform_y = random.randrange((chunk_y * CHUNK_HEIGHT), ((chunk_y + 1) * CHUNK_HEIGHT - TILE_SIZE), 128) ###implimented chunk_y, now adjust code accordingly 
        tile_type = 0
        #if _ in range(random.randint(5,25)):
        #    tile_type = 1 # can integrate tile_type here for tile index, different platforms in future 

        chunk_data.append((platform_x, platform_y)) #,tile_type

    #Impliment other biome here 
    #if chunk_y < -5000:
         
    #    platform_x = random.randrange((chunk_x * CHUNK_WIDTH), ((chunk_x + 1) * CHUNK_WIDTH - TILE_SIZE ), 192)
    #    platform_y = random.randrange((chunk_y * CHUNK_HEIGHT), ((chunk_y + 1) * CHUNK_HEIGHT - TILE_SIZE + 128), 128) ###implimented chunk_y, now adjust code accordingly 
        tile_type = 0
        #if _ in range(random.randint(5,25)):
        #    tile_type = 1 # can integrate tile_type here for tile index, different platforms in future 

    #    chunk_data.append((platform_x, platform_y)) #,tile_type

    return chunk_data

    # chunks are stored in this data format 

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


###Healthbars
class Old_HealthBar(): # refactored this to fit into the player class in future to init several healthbars 
    def Healthbar__init__(self, x, y, w, h, max_hp):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.hp = 100
        self.max_hp = max_hp


    def draw_healthbar(self, surface):
        #calculate health ratio
        ratio = self.hp / self.max_hp
        pygame.draw.rect(surface, "red", (self.x, self.y, self.w, self.h))
        pygame.draw.rect(surface, "green", (self.x, self.y, self.w * ratio, self.h))

    #def update_healthbar(self,new_hp):
    #    self.hp = new_hp

        #Can check if player.rect.bottom touches the bottom of the screen
        #player.rect.bottom
     #   if self.hp == 0:
      #      print("self.hp is 0.")
        #if the hp = 0, then we change gamestate to end game

####CLASS FOR PLAYER OBJECT HANDLING####

#Class for generating player object
#Inherits from the Sprite class to help handle collisions
class Player(pygame.sprite.Sprite):
    # Class var - might move gravity to Config later
    COLOR = (255,0,0)
    GRAVITY = 1 # 9.81,but setting this to 1 for now
    ANIMATION_DELAY = 3 #Keeps track of delay between changing sprites


   
    SPRITES = load_sprite_sheets("MainCharacters","VirtualGuy",32,32,True)

    def __init__(self, player_x, player_y, width, height,healthb_x,healthb_y,healthb_w,healthb_h,health,max_health):
        super().__init__()

        #Putting variables in a Rect (tuple with 4 variables)
        self.rect = pygame.Rect (player_x,player_y,width,height)
     
        #Player vel
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
        
        #self.SPRITES = load_sprite_sheets("MainCharacters","VirtualGuy",32,32,True)
        self.mask = pygame.mask.from_surface(self.sprite)
        #rects 
        #self.hbrect1 = pygame.Rect (healthb_x,healthb_y,healthb_w,healthb_h)
        #self.hbrect2 = pygame.Rect (self.healthb_x, self.healthb_y, self.healthb_w * self.ratio, self.healthb_h)

        ##Healthbar properties
        self.healthb_x = healthb_x
        self.healthb_y = healthb_y
        self.healthb_w = healthb_w
        self.healthb_h = healthb_h
        self.health = 100 - self.hit_count
        self.max_health = max_health
        
        self.ratio = self.health / self.max_health

        


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
        if self.hit == True:
            sprite_sheet = "hit"
            self.health -= 1 
        #End game if hp = 0
        if self.health == 0:
            print("You are dead!")
            from GameStateManager import GameStateManager, Game
            run_pause = GameStateManager.set_state(state='Main_menu')
            self.health == 100 
            Game.run()
            #pygame.quit()
            
        
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
        #mask for player sprites
        self.animation_count += 1
        
        #Update mask for collision check (mask is a mapping of pixels in the sprite)
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
        if self.hit_count > FPS / 2:
            self.hit = False
            
        

        self.fall_count += 1
        #Calling update sprite method each frame (loop iteration), to update sprite
        ### constantly updating object with gravity, so jump "wears off"
        
        self.update_sprite()
        
        self.update()
        self.draw(window,offset_x,offset_y)
    
    #Updating the rectangle of the character (adjusted based on sprite used)
    def update(self):
        #Updating the rectangle of the character (adjusted based on sprite used)
        self.rect = self.sprite.get_rect(topleft=(self.rect.x,self.rect.y)) ###MIGHT NOT BE player_x , but just x and y

        #Getting mask for collisions (mask is a mapping of pixels in the sprite)
        self.mask =  pygame.mask.from_surface(self.sprite)
        #if self.health == 0:
        #    print("self.hp is 0!")

        if self.health != None or self.health != 0 and death_note == None: #if health 0, then:
            from Object import Text
            death_note = Text(self.healthb_x,self.healthb_y,TILE_SIZE)
            
            death_note.draw_youredead()
    #        print("You are dead!")
          
    #        pygame.draw.rect(win, "red", (self.healthb_x, self.healthb_y, self.healthb_w, self.healthb_h))
    #        pygame.draw.rect(win, "green", (self.healthb_x, self.healthb_y, self.healthb_w * self.ratio, self.healthb_h))
    #    
    #    else:
            #Blit "Dead" onto surface
            
    #Draw method for player
    def draw(self,win,offset_x,offset_y):
        #loading sprite from dictionary: sprites using update method
        #blitting on window
        win.blit(self.sprite,(self.rect.x - offset_x,self.rect.y -offset_y))
        
  
    #def update_healthbar(self,win):
    #    if self.healthb_w != None or self.healthb_w != 0:
    #        pygame.draw.rect(win, "red", (self.healthb_x, self.healthb_y, self.healthb_w, self.healthb_h))
    #        pygame.draw.rect(win, "green", (self.healthb_x, self.healthb_y, self.healthb_w * self.ratio, self.healthb_h))
    #    
    ##    self.hp = new_hp


    def draw_health_bar(self, win):
        bar_width = 100
        bar_height = 10
        fill_width = int(bar_width * (self.health / self.max_health))
        outline_rect = pygame.Rect(10, 10, bar_width, bar_height)
        fill_rect = pygame.Rect(10, 10, fill_width, bar_height)

        pygame.draw.rect(win, (255, 0, 0), fill_rect)      # Red bar for health
        pygame.draw.rect(win, (255, 255, 255), outline_rect, 2)  # White border for the health ba

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
    #global player_world_y # prevent unbound error 
    keys = pygame.key.get_pressed()

    #First we set player velocity to 0, because the player methods set a new velocity and otherwise
    # will continue in one direction until reset
    player.x_vel = 0
    
    #To stop player from going out of bounds, could make an object alongside border of screen and collide player with it

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
    platform_size = 64
    
    #Creating scrolling backgrounds
    #By offsetting how we draw the background, we can make it look like we scroll through the background
    #Creating scrolling backgrounds
    #By offsetting how we draw the background, we can make it look like we scroll through the background
    offset_x = 1
    offset_y = 0
    Y_scroll_area_width = 200
    #X_scroll_area_width = 300
    global player_world_x,player_world_y # declare local var to prevent unbound error 

    
    player_1 = Player(100,100,50,50,healthb_x=950,healthb_y=85,healthb_w=300,healthb_h=40,health=40, max_health = 100) #Create player object

    ###BUTTONS###
    Pause_onscreen = PB_init()
    
    #SCREEN.fill("black") WRITE FUNCTION FOR DRAWING BACKGROUND maybe?

    pygame.display.update() # Update (COULD BE SOURCE OF GETTING GAME STUCK)

   

    ###PLATFORMS HARD CODE###
    ###floating platforms at 8* height-block_size
    #air_blocks=[Block(block_size * i, HEIGHT-block_size *8,block_size)
    #for i in range(0,block_size-48,4)] 

    #First few blocks
    #blocks = [#Block(block_size*3,HEIGHT-block_size*4,block_size),
              #Block(block_size*5,HEIGHT-block_size*4,block_size),
    #          Block(block_size*7,HEIGHT-block_size*4,block_size),
    #          Block(block_size*10,HEIGHT-block_size*6,block_size)
    #          ]
    
        #platform init requirements
        #self,x,y,width,height
            #x,y positions on screen
            #x_size, y_size dimensions of image
     
    #first_platform = Platform((WIDTH - block_size*4),(HEIGHT-block_size*2),96,32) 
    #[Block(block_size * i, HEIGHT-block_size *8,block_size)
    #for i in range(0,block_size-48,4)]

    #platforms = [Platform(WIDTH-block_size*8, block_size* i,96,32)
    #             for i in range(0,block_size-48,4)]
    #first_platform = [Platform(i* platform_size, HEIGHT//2,platform_size)
    #         for i in range(-WIDTH//platform_size, WIDTH * 2 // platform_size)]
    #all_platforms = [Platform(i* block_size, HEIGHT//2,block_size)
    #            for i in range(-WIDTH//block_size, WIDTH * 2 // block_size)]
    #Can build for loops here to make more easily
    #                     for i in range(-WIDTH//platform_width, WIDTH *2 //block_size))

    ####HARD CODE WORLD ENV
       ###Enviornment###
    objects = [] #resetting objects each frame 
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
              #Block(block_size*5,HEIGHT-block_size*4,block_size),
              Block(block_size*7,HEIGHT-block_size*4,block_size),
              Block(block_size*10,HEIGHT-block_size*6,block_size)
              ]
    
    #First platform 
    
    #platform_x = 96
    #platform_y = 32
        #Platform takes: self,x,y,width,height
            #x,y positions on screen
            #width: x_size, height: y_size dimensions of image
     
    #first_platform = Platform((WIDTH - block_size*4),(HEIGHT-block_size*2),96,32) 
    #[Block(block_size * i, HEIGHT-block_size *8,block_size)
    #for i in range(0,block_size-48,4)]

    platforms = [Platform(WIDTH-block_size*8, block_size* i,96,32)
                 for i in range(0,block_size-48,4)]
    #first_platform = [Platform(i* platform_size, HEIGHT//2,platform_size)
    #         for i in range(-WIDTH//platform_size, WIDTH * 2 // platform_size)]
    #all_platforms = [Platform(i* block_size, HEIGHT//2,block_size)
    #            for i in range(-WIDTH//block_size, WIDTH * 2 // block_size)]
    #Can build for loops here to make more easily
    #                     for i in range(-WIDTH//platform_width, WIDTH *2 //block_size))

    ###TRAPS###
        #x,y = position, width height are dimensions
    fire = Fire(100,HEIGHT-block_size -64, 16, 32)  #Dimensions: 16x32
    fire.on()
    #healthbar = player.update_healthbar(window)

    #Making a list of objects being drawn, passing floor into this list too
    #This list is used to draw objects in the game loop
    objects = [*floor, *blocks, *air_blocks, Block(0,HEIGHT-block_size*2,block_size),
               #This block is roughly in the middle of the screen
               Block(block_size*3,HEIGHT-block_size*4,block_size),
               fire, *platforms]

    

    #### Main game loop###
    run = True
    while run:
        
        clock.tick(FPS)

        #Event handling 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            #HANDLING JUMP here, could do it in handle_move, but this is cleaner because
                ##if we handle the jump in the Handle move method it would break if any keys are held down
            if event.type == pygame.KEYDOWN:
                #statement allows for double jump! Can add extra jumps or dashes here
                if event.key == pygame.K_SPACE and player_1.jump_count < 2:
                    player_1.jump()

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


        ###GENERATING ENVIORNMENT ###
        #tile_index = {1:Block,
        #                2:Platform #-> takes different parameters so we have to blit differently 
        #                }
        
        
        ###Handle world gen and drawing:
        current_chunk_x = math.floor(player_1.rect.right / CHUNK_WIDTH)
        current_chunk_y = math.floor(player_1.rect.top / CHUNK_HEIGHT) #math.floor correctly rounds negative numbers 
        
        #print("This is current_chunk_x:",current_chunk_x)
        #print("This is current_chunk_y:",current_chunk_y)
        
        gend_a_chunk = False 
        #for chunk_x in range(int(current_chunk_x ) -1, int(current_chunk_x) + 1) :  # Symmetric chunk generation
            ### ISSUE HERE: if the above values that - or + the range parameters it ONLY draws either the left or the right of the middle of the screen

        for chunk_y in range(int(current_chunk_y) - 1, int(current_chunk_y) + 1) : #Generate chunks above and below
            if (current_chunk_x,chunk_y) not in generated_chunks:
                gend_a_chunk = True 
                generated_chunks[(current_chunk_x, chunk_y)] = generate_chunk(current_chunk_x, chunk_y)
                #print("This is chunk_x: ",chunk_x)
                #print("This is generated_chunks: ",generated_chunks)
                #print("This is generated chunks keys: ",generated_chunks.keys())
   
        #print(f"Generating chunk: {chunk_x}, {chunk_y}")
        kill_these_chunks = []
        index_objpos = {}
        if gend_a_chunk == True:
        #if we generate a chunk, clear the dictionary of any chunks that arent in the screen range 
            current_keys = generated_chunks.keys()
        
            for badkeys in current_keys:
                #badkeys[0] not in range(round(current_chunk_x - 2), round(current_chunk_x + 1))
                if badkeys[1] not in range(round(current_chunk_y - 1), round(current_chunk_y + 3)): # check the y value of chunk is out of range 
                    
                    #print("This is the range of allowed y values: ", range(round(current_chunk_y - 1), round(current_chunk_y + 3)))
                    
                    kill_these_chunks.append(badkeys)

       
        # Add platforms from generated chunks to objects list if we made a new chunk
            for indexpos in generated_chunks:
                chunk_data = generated_chunks[current_chunk_x,chunk_y]
                #print(chunk_x)
                # Function to draw the chunk
                list_obj_indexes = []
                for platform in chunk_data: 
                    #can init and draw platforms here 
                    #make a dictionary corresponding to the chunk x that contains the generated objects, so we can iterate through it and manage it
                   
                    platform_x = (platform[0] ) #removed offset_x since there isnt any side scrolling in this version
                    platform_y = (platform[1] + offset_y)
                    
                    if chunk_y > -2000: #first biome 
                        platform = Platform(platform_x,platform_y,96,32)
                        #platform = Platform(platform_x,platform_y,96,32)
                        objects.append(platform)
                        obj_index = objects.index(platform)
                        list_obj_indexes.append(obj_index)

                    #IMPLIMENT BIOME HERE
                    elif chunk_y <= -2000:
                        platform = Block(platform_x,platform_size,block_size)
                        objects.append(platform)
                        obj_index = objects.index(platform)
                        list_obj_indexes.append(obj_index)
                
                index_objpos[indexpos] = list_obj_indexes #makes a dictionary to relate the position of the objects in the objects list to the chunks they are drawn in 
            #print("This is generated chunks: ",generated_chunks)
        #remove chunks from generated_chunks dict if they are out of our range of vision

        for chunk in kill_these_chunks:
            #print("This is chunk in kill these chunks section:", chunk)
            if chunk in generated_chunks.keys():
                #print("killed this chunk: ",generated_chunks[chunk])
                #generated_chunks.pop(items)
                del generated_chunks[chunk]


                ###This takes care of most of the memory issues! 
                #Now iterate through objects list and kick out index members related to the chunk 
                #ONLY if we are removing chunks 
                #print("This is index_objpos dict: ",index_objpos)
                #for obj_indexes in index_objpos[chunk]:
                #    if obj_indexes in index_objpos[chunk] and chunk in generated_chunks.keys():
                #        #print("Removing this from obj_indexes:",obj_indexes)
                #        print("This is length of objects list:",len(objects))
                #        del objects[obj_indexes]
                #        print("This is the new length of objects: ",len(objects))
                #    else:
                #        pass
                    #index_objpos = {} #reset index dictionary??
            else:
                pass
                #print(f"The {str(items)} key was not in {generated_chunks.keys()}")


        # Clear screen before drawing next frame
        window.fill(WHITE)
        #Run the animation loops, handle movement, draw each frame with the list of objects

        player_1.loop(FPS)  #runs player loop, CHECK if healthbar refactor worked
        #player.draw(window,offset_x,offset_y)
       
        fire.loop()       #runs fire 
       
        draw(window,background,bg_image, player_1,
             objects,offset_x,offset_y)
          
        #handle movement via input
        handle_move(player_1,objects)
      
        #run a update health bar method here after handling move/collision
        
        
        PLAY_MOUSE_POS = pygame.mouse.get_pos() #get player mouse position 
        Pause_onscreen.changeColor(PLAY_MOUSE_POS) #Handle pause button interaction
        Pause_onscreen.update(window) #Handle pause button interaction
        
        
        #if ((player.rect.right - offset_x >= WIDTH - X_scroll_area_width) and player.x_vel > 0) or (
        #    (player.rect.left - offset_x <= X_scroll_area_width) and player.x_vel < 0):
        #    offset_x += player.x_vel
        #    player_world_x += player.x_vel
        #Handling horizontal scrolling background
            #if im going right im checking if im near the boundary then offsetting x accordingly
            #If im going left, I am checking the other boundary and adjusting x accordingly
        #if ((player.rect.right - offset_x >= WIDTH - X_scroll_area_width) and player.x_vel > 0) or (
        #        (player.rect.left - offset_x <= X_scroll_area_width) and player.x_vel < 0):
            ###JUMP CUT to next screen###
            #offset_x= min(player.rect.right - WIDTH + scroll_area_width, WIDTH * 2 - WIDTH)
            #SCROLLING###
        #    offset_x += player.x_vel

        #Handles vertical scrolling 
        if ((player_1.rect.bottom - offset_y <= Y_scroll_area_width) and player_1.y_vel < 0):
            #add this for downward scrolling or 
            #    
        #:((player.rect.top - offset_y >= HEIGHT - Y_scroll_area_width) and player.y_vel > 0)
                #CAN ADD OR STATEMENT TO ADD DOWNWARD SCROLLING
            
            ###JUMP CUT to next screen###
            #offset_x= min(player.rect.right - WIDTH + scroll_area_width, WIDTH * 2 - WIDTH)
            #SCROLLING###
            offset_y += player_1.y_vel
            player_world_y += player_1.y_vel
           
        #print("This is the length of objects: ", len(objects))
        


    pygame.quit()
    quit()

#Runs game only if we are running this script directly

if __name__ == "__main__" and RUNGAME == True:
    main_CoA(window)
