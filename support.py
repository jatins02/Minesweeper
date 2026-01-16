import pygame
import random
import math
pygame.font.init()


#COLORS:
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LAVENDERBLUSH = (255, 240, 245)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)

# WINDOW SPECIFICATIONS:
WIDTH, HEIGHT = 440, 440
FPS = 4

#WINDOW INITIALISATION:
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper")

#MISC. DECLARATION:
grid_array = []
diagonal_dist = math.sqrt(2)
adjacent_dist = 1
surrounding_tile_dist = [diagonal_dist, adjacent_dist]
flip_state = {}

#MAIN GAME FUNCTION DEFINITIONS:
def main():
    running = True
    timer = pygame.time.Clock()
    setting_up = True
    easy_rect = mid_rect = hard_rect = None

    while running:
        timer.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:   
                running = False

            if setting_up:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    setting_up, difficulty = handle_setup_click(event, easy_rect, mid_rect, hard_rect)
                    bomb_indices, num_rows = initGame(difficulty)
                    grid_array = draw_game_grid(num_rows)
                    
            elif not setting_up:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    running = handle_main_click(event, grid_dict, grid_array)
                

        if setting_up:
            easy_rect, mid_rect, hard_rect = set_up()
        else:
            
            grid_dict = fill_grid(num_rows, bomb_indices)
            #init_grid(grid_dict)

        pygame.display.update()


def set_up():
    top_margin = 22
    label_height = 69
    setting_label_height = 44
    top_padding = 18

    WINDOW.fill(LAVENDERBLUSH)

    label = pygame.Rect(0, 22, WIDTH, label_height)
    font = pygame.font.SysFont("monospace", 55, True)
    text = font.render("MINESWEEPER", 1, BLACK)
    WINDOW.blit(text, (WIDTH//2 - text.get_width()//2, label.y))

    setting_font = pygame.font.SysFont("helvetica", 36)

    easy_rect = pygame.Rect(0, top_margin + label_height + top_padding, WIDTH, setting_label_height)
    easy_surface = setting_font.render("EASY", 1, ORANGE)
    WINDOW.blit(easy_surface, (WIDTH//2 - easy_surface.get_width()//2, easy_rect.y))

    mid_rect = pygame.Rect(0, easy_rect.y + setting_label_height + top_padding, WIDTH, setting_label_height)
    mid_surface = setting_font.render("MID", 1, ORANGE)
    WINDOW.blit(mid_surface, (WIDTH//2 - mid_surface.get_width()//2, mid_rect.y))

    hard_rect = pygame.Rect(0, mid_rect.y + setting_label_height + top_padding, WIDTH, setting_label_height)
    hard_surface = setting_font.render("HARD", 1, ORANGE)
    WINDOW.blit(hard_surface, (WIDTH//2 - hard_surface.get_width()//2, hard_rect.y))

    return [easy_rect, mid_rect, hard_rect]


def handle_setup_click(event, easy_rect, mid_rect, hard_rect):
    if easy_rect.collidepoint(event.pos):
        return [False, "easy"]
    elif mid_rect.collidepoint(event.pos):
        return [False, "mid"]
    elif hard_rect.collidepoint(event.pos):
        return [False, "hard"]
    else:
        print("don't initialise game")
        return [True, None]


def initGame(difficulty):
    num_rows = {"easy": 8, "mid": 10, "hard": 12}

    total_tiles = num_rows[difficulty] ** 2
    num_of_bombs = {64: 7, 100: 10, 144: 15}        # keys is the number of tiles in the grid, value is the number of bombs in the grid
    bomb_indices = []

    while len(bomb_indices) < num_of_bombs[total_tiles]:
        bomb_index = random.randrange(0, total_tiles)
        if bomb_index not in bomb_indices:
            bomb_indices.append(bomb_index)
        else:
            pass
        
    return [bomb_indices, num_rows[difficulty]]


def draw_game_grid(num_rows):
    WINDOW.fill(LAVENDERBLUSH)

    tile_side = {8: 44, 10: 35, 12: 30}         # key is the number of rows in the grid, value is the length of one side of the tile
    padding = {8: 10, 10: 7, 12: 5}             # key is the number of rows in the grid, value is the padding around each tile.

    for row in range(num_rows):
        row_array = []
        for column in range(num_rows):
            left = (column * tile_side[num_rows]) + padding[num_rows] * (column + 1)
            top = (row * tile_side[num_rows]) + padding[num_rows] * (row + 1)
            tile = pygame.Rect(left, top, tile_side[num_rows], tile_side[num_rows])
            row_array.append(tile)
            pygame.draw.rect(WINDOW, RED, tile)
        grid_array.append(row_array)

    return grid_array


def fill_grid(num_rows, bomb_indices):
    grid_dict = {}      # will store the coordinate of each tile along with its associated value (bomb/number).
    counter = 0
    
    for row in range(num_rows):
        row_text = []
        for tile in range(num_rows):
            flip_state[(row, tile)] = "hidden"
            if counter in bomb_indices:
                row_text.append("O")
                grid_dict[(row, tile)] = "O"
            else:
                row_text.append(0)
                grid_dict[(row, tile)] = 0
            counter += 1
        
    bomb_coordinates = []       # list storing the coordinates of bomb locations
    bomb_surrounding = {}       # dict storing the bomb coordinate along with the coordinate of its surrounding boxes
    bomb_surr_tile_list = []    # temporary list, storing the coordinate of a bomb and its surrounding tiles

    for tile_coord, tile_content in grid_dict.items():
        if type(tile_content) != str:   #tile is numeric
            pass

        elif type(tile_content) == str:     #tile is bomb
            bomb_coordinates.append(tile_coord)
            for coord in grid_dict.keys():
                if get_dist(coord, tile_coord) in surrounding_tile_dist:
                    bomb_surr_tile_list.append(coord)    
            bomb_surrounding[tile_coord] = bomb_surr_tile_list

        bomb_surr_tile_list = []


    for bomb in bomb_surrounding.keys():
        for tile in bomb_surrounding[bomb]:
            if type(grid_dict[tile]) != str:    #checking for surrounding tiles that are not bombs
                grid_dict[tile] += 1
            else:
                pass
    #init_grid(grid_dict)
    return grid_dict


def init_grid(grid_dict):
    bombFont = pygame.font.SysFont("monospace", 20, True)
    bombFont_surface = bombFont.render("X", 1, BLACK)

    numFont = pygame.font.SysFont("monospace", 22, True)

    for tile in grid_dict.keys():
        current_tile = grid_array[tile[0]][tile[1]]
        if type(grid_dict[tile]) == str:    #tile contains a bomb
            WINDOW.blit(bombFont_surface, (current_tile.x, current_tile.y))

        else:   # tile does not contain a bomb, it corresponds to a number
            numFont_surface = numFont.render(f"{grid_dict[tile]}", 1, True)
            WINDOW.blit(numFont_surface, (current_tile.x, current_tile.y))
            

def handle_main_click(event, grid_dict, grid_array):
    
    row_count = 0
    for row in grid_array:
        column_count = 0
        for tile in row:
            if tile.collidepoint(event.pos):
                clicked_tile_coord = (row_count, column_count)
                surrounding_tiles = get_surrounding_tiles(clicked_tile_coord, grid_dict)

                if grid_dict[clicked_tile_coord] != 0: #meaning it is a bomb, or a number
                    if grid_dict[clicked_tile_coord] == "O": #tile is a bomb
                        #end_game()     # call function to finish the game, player loses
                        print("game lost")
                        flip_tile(grid_dict, clicked_tile_coord, tile)
                        flip_state[clicked_tile_coord] = "revealed"
                        print("bomb tile was clicked")
                        return False
                    else:
                        print("number tile was clicked")
                        flip_tile(grid_dict, clicked_tile_coord, tile)      # tile is a number, simply flip it and nothing else
                        flip_state[clicked_tile_coord] = "revealed"
                        return True
                else:
                    print("zero tile is clicked")
                    surrounding_tiles = get_surrounding_tiles(clicked_tile_coord, grid_dict)
                    zero_clicked(clicked_tile_coord, surrounding_tiles, grid_dict, flip_state)
                    flip_state[clicked_tile_coord] = "revealed"
                    return True
        #check for the surrounding tiles, and recursively flip each tile that is a zero.


                #check if the tile you clicked on is a number or bomb, or a zero.

                #define a flip function (or you could do with the already defined init_grid function),
                #now loop through all the neighbouring tiles in the surrounding tiles list,
                #ONLY IF THE TILE ON WHICH PLAYER HAS CLICKED IS A ZERO, will you check for the surrounding tiles
                #if the tile on which player has clicked is a number or a bomb, then the only open that tile, and NOT THE SURROUNDING TILES

                # if the tile on which player clicked is 0 tile, then get the surrounding tiles list, and check if the list contains any zero or not
                # if it does then get the coordinates of that zero tile and get its surrounding tiles and on and on.

            column_count += 1
        row_count += 1


def zero_clicked(clicked_tile_coord, surrounding_tiles, grid_dict, flip_state):
    if flip_state[clicked_tile_coord] == "revealed":
        return 
    
    current_rect = grid_array[clicked_tile_coord[0]][clicked_tile_coord[1]]
    flip_tile(grid_dict, clicked_tile_coord, current_rect)
    flip_state[clicked_tile_coord] = "revealed"

    if grid_dict[clicked_tile_coord] == 0:
        for tile in surrounding_tiles:
            new_surrounding = get_surrounding_tiles(tile, grid_dict)
            zero_clicked(tile, new_surrounding, grid_dict, flip_state)

    
def flip_tile(grid_dict, coord, tile):
    bombFont = pygame.font.SysFont("monospace", 20, True)
    bombFont_surface = bombFont.render("X", 1, BLACK)

    numFont = pygame.font.SysFont("monospace", 22, True)
    
    if flip_state[coord] != "revealed":
        if type(grid_dict[coord]) == int:
            text = numFont.render(f"{grid_dict[coord]}", 1, BLACK)
            WINDOW.blit(text, (tile.x, tile.y))
        else:
            WINDOW.blit(bombFont_surface, (tile.x, tile.y))


def get_surrounding_tiles(clicked_tile_coord, grid_dict):
    surrounding_tiles = []
    for tile in grid_dict.keys():
        if get_dist(tile, clicked_tile_coord) in surrounding_tile_dist:
            surrounding_tiles.append(tile)
        
    return surrounding_tiles


# UTILITY FUNCTIONS:
def get_dist(tup1, tup2):
    x_dist = (tup1[0] - tup2[0]) ** 2
    y_dist = (tup1[1] - tup2[1]) ** 2

    dist = math.sqrt(x_dist + y_dist)
    return dist





if __name__ == "__main__":
    main()

