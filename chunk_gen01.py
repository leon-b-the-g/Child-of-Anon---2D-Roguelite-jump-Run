import pygame, sys, os, random, noise

CHUNK_SIZE = 8

true_scroll = [0,0]

#Generates chunks, each chunk consists of data: x,y of starting position of drawing of chunk and the tile in it
def generate_chunk(x,y):
    chunk_data = []
    for y_pos in range(CHUNK_SIZE):
        for x_pos in range(CHUNK_SIZE):
            target_x = x * CHUNK_SIZE + x_pos
            target_y = y * CHUNK_SIZE + y_pos
            tile_type = 0 # nothing

            #Uses noise library here to randomize the height of landscape.
                #Could use noise function to semi randomize platform positions
            height = int(noise.pnoise1(target_x * 0.1, repeat=9999999) * 5)
            if target_y > 8 - height:
                tile_type = 2 # dirt
            elif target_y == 8 - height:
                tile_type = 1 # grass
            elif target_y == 8 - height - 1:
                if random.randint(1,5) == 1:
                    tile_type = 3 # plant
            if tile_type != 0:
                chunk_data.append([[target_x,target_y],tile_type])
    return chunk_data




#Uses a dict to organise chunks
    #each chunk is a list of tiles 
game_map = {}

#Loads images needed in chunks 
grass_img = pygame.image.load('grass.png')
dirt_img = pygame.image.load('dirt.png')
plant_img = pygame.image.load('plant.png').convert()
plant_img.set_colorkey((255,255,255))

#Makes an index for all elements in a chunk
tile_index = {1:grass_img,
              2:dirt_img,
              3:plant_img
              }

#handles scrolling
true_scroll[0] += (player_rect.x-true_scroll[0]-152)/20
true_scroll[1] += (player_rect.y-true_scroll[1]-106)/20
scroll = true_scroll.copy()
scroll[0] = int(scroll[0])
scroll[1] = int(scroll[1])


tile_rects = []
for y in range(3):
    for x in range(4):
        target_x = x - 1 + int(round(scroll[0]/(CHUNK_SIZE*16)))
        target_y = y - 1 + int(round(scroll[1]/(CHUNK_SIZE*16)))
        target_chunk = str(target_x) + ';' + str(target_y)
        if target_chunk not in game_map:
            game_map[target_chunk] = generate_chunk(target_x,target_y)
        for tile in game_map[target_chunk]:
            display.blit(tile_index[tile[1]],(tile[0][0]*16-scroll[0],tile[0][1]*16-scroll[1]))
            if tile[1] in [1,2]:
                tile_rects.append(pygame.Rect(tile[0][0]*16,tile[0][1]*16,16,16))  