import pygame
import random
import math
import time
pygame.font.init()

#COLORS:
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LAVENDERBLUSH = (255, 240, 245)
ORANGE = (255, 165, 0)
TILE_COLOR = (175, 207, 147)
FLIPPED_COLOR = (75, 82, 77)
SETUP_BACKGROUND = (71, 83, 89)

# WINDOW SPECIFICATIONS:
WIDTH, HEIGHT = 440, 440
FPS = 44

#WINDOW INITIALISATION:
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper")

#MISC. DECLARATION:
grid_array = []
diagonal_dist = math.sqrt(2)
adjacent_dist = 1
surrounding_tile_dist = [diagonal_dist, adjacent_dist]
flip_state = {}


#Main game functions definitions:
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
                    if difficulty is not None:
                        bomb_indices, num_rows = initGame(difficulty)
                        grid_array = draw_game_grid(num_rows)
                    
            elif not setting_up:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    running = handle_main_click(event, grid_dict, grid_array)

        if setting_up:
            easy_rect, mid_rect, hard_rect = set_up()
        else:            
            grid_dict = fill_grid(num_rows, bomb_indices)

        pygame.display.update()


#GAME SETUP FUNCTIONS
def set_up():       #makes the setting window
    top_margin = 22
    label_height = 69
    setting_label_height = 44
    top_padding = 18

    WINDOW.fill(SETUP_BACKGROUND)

    label = pygame.Rect(0, 69, WIDTH, label_height)
    my_font = pygame.font.Font("F:/FONTS_/PressStart2P-Regular.ttf", 36)
    text = my_font.render("MINESWEEPER", 1, BLACK)
    WINDOW.blit(text, (WIDTH//2 - text.get_width()//2, label.y))

    setting_font = pygame.font.Font("F:/FONTS_/PressStart2P-Regular.ttf", 28)

    easy_rect = pygame.Rect(0, top_margin + label_height + top_padding + 44, WIDTH, setting_label_height)
    easy_surface = setting_font.render("EASY", 1, ORANGE)
    WINDOW.blit(easy_surface, (WIDTH//2 - easy_surface.get_width()//2, easy_rect.y))

    mid_rect = pygame.Rect(0, easy_rect.y + setting_label_height + top_padding, WIDTH, setting_label_height)
    mid_surface = setting_font.render("MID", 1, ORANGE)
    WINDOW.blit(mid_surface, (WIDTH//2 - mid_surface.get_width()//2, mid_rect.y))

    hard_rect = pygame.Rect(0, mid_rect.y + setting_label_height + top_padding, WIDTH, setting_label_height)
    hard_surface = setting_font.render("HARD", 1, ORANGE)
    WINDOW.blit(hard_surface, (WIDTH//2 - hard_surface.get_width()//2, hard_rect.y))

    return [easy_rect, mid_rect, hard_rect]


def initGame(difficulty):                                           #initialises game by setting up important parameters
    num_rows = {"easy": 8, "mid": 10, "hard": 12}

    total_tiles = num_rows[difficulty] ** 2
    num_of_bombs = {64: 7, 100: 10, 144: 15}                        #keys is number of tiles and value is number of bombs in the grid.
    bomb_indices = []

    while len(bomb_indices) < num_of_bombs[total_tiles]:
        bomb_index = random.randrange(0, total_tiles)
        if bomb_index not in bomb_indices:
            bomb_indices.append(bomb_index)
        else:
            pass
        
    return [bomb_indices, num_rows[difficulty]]


def draw_game_grid(num_rows):
    WINDOW.fill((60, 60, 60))

    tile_side = {8: 44, 10: 36, 12: 31}         # key = number of rows in the grid, value = length of one side of the tile
    padding = {8: 10, 10: 7, 12: 5}             # key = number of rows in the grid, value = padding around each tile.

    for row in range(num_rows):
        row_array = []
        for column in range(num_rows):
            left = (column * tile_side[num_rows]) + padding[num_rows] * (column + 1)
            top = (row * tile_side[num_rows]) + padding[num_rows] * (row + 1)
            tile = pygame.Rect(left, top, tile_side[num_rows], tile_side[num_rows])
            row_array.append(tile)
            pygame.draw.rect(WINDOW, TILE_COLOR, tile)
        grid_array.append(row_array)

    return grid_array


def fill_grid(num_rows, bomb_indices):      #fills grid with numbers and bombs
    grid_dict = {}                          # will store the coordinate of each tile along with its associated value (bomb/number).

    counter = 0
    for row in range(num_rows):             #loop to initialise grid_dict 
        for column in range(num_rows):
            flip_state[(row, column)] = "hidden"
            if (row * num_rows) + column in bomb_indices:               #replaced counter with row*num_rows + column
                grid_dict[(row, column)] = "X"
            else:
                grid_dict[(row, column)] = 0
            counter += 1
        
    bomb_surrounding = {}       # dict storing the bomb coordinate along with the coordinates of its surrounding boxes
    bomb_surr_tile_list = []    # temporary list, storing the coordinate of a bomb and its surrounding tiles

    for tile_coord, tile_content in grid_dict.items():
        if type(tile_content) != str:       #tile is numeric
            pass

        elif type(tile_content) == str:     #tile is bomb
            for coord in grid_dict.keys():
                if get_dist(coord, tile_coord) in surrounding_tile_dist:
                    bomb_surr_tile_list.append(coord)    
            bomb_surrounding[tile_coord] = bomb_surr_tile_list

        bomb_surr_tile_list = []

    for bomb in bomb_surrounding.keys():
        for tile in bomb_surrounding[bomb]:
            if type(grid_dict[tile]) != str:        #tile is not a bomb, it is numeric type
                grid_dict[tile] += 1
            else:
                pass

    return grid_dict


#GAME EVENT HANDLING FUNCTIONS
def handle_setup_click(event, easy_rect, mid_rect, hard_rect):      #handles left mouse click during game setup
    if easy_rect.collidepoint(event.pos):
        return [False, "easy"]
    elif mid_rect.collidepoint(event.pos):
        return [False, "mid"]
    elif hard_rect.collidepoint(event.pos):
        return [False, "hard"]
    else:
        print("don't initialise game")
        return [True, None]


def handle_main_click(event, grid_dict, grid_array):        #handles clicks on the grid of tiles
    row_count = 0
    for row in grid_array:
        column_count = 0
        for tile in row:
            if tile.collidepoint(event.pos):
                clicked_tile_coord = (row_count, column_count)
                surrounding_tiles = get_surrounding_tiles(clicked_tile_coord, grid_dict)

                if grid_dict[clicked_tile_coord] != 0:              #meaning it is a bomb, or a number
                    if grid_dict[clicked_tile_coord] == "X":        #tile is a bomb
                        flip_tile(grid_dict, clicked_tile_coord, tile)
                        end_lost()  
                        pygame.display.update()
                        flip_state[clicked_tile_coord] = "revealed"
                        time.sleep(3)                                                             
                        return False
                    else:
                        flip_tile(grid_dict, clicked_tile_coord, tile)      #tile is a number, just simply flip it
                        flip_state[clicked_tile_coord] = "revealed"
                        if check_game_won(grid_dict, flip_state):
                            return False
                        return True
                else:
                    surrounding_tiles = get_surrounding_tiles(clicked_tile_coord, grid_dict)
                    zero_clicked(clicked_tile_coord, surrounding_tiles, grid_dict, flip_state)
                    flip_state[clicked_tile_coord] = "revealed"
                    return True

            column_count += 1
        row_count += 1
    return True


def zero_clicked(clicked_tile_coord, surrounding_tiles, grid_dict, flip_state):     #handles if player clicked on a tile with 0
    if flip_state[clicked_tile_coord] == "revealed":
        return 
    
    current_rect = grid_array[clicked_tile_coord[0]][clicked_tile_coord[1]]
    flip_tile(grid_dict, clicked_tile_coord, current_rect)
    flip_state[clicked_tile_coord] = "revealed"

    if grid_dict[clicked_tile_coord] == 0:
        for tile in surrounding_tiles:
            new_surrounding = get_surrounding_tiles(tile, grid_dict)
            zero_clicked(tile, new_surrounding, grid_dict, flip_state)


# UTILITY FUNCTIONS:
def check_game_won(grid_dict, flip_state):
    for coord, content in grid_dict.items():
        if content != "X" and flip_state[coord] == "hidden":
            return False
            
    end_rect = pygame.Rect(0, HEIGHT//2 - 22, WIDTH, 150)
    end_font = pygame.font.Font("F:/FONTS_/PressStart2P-Regular.ttf", 44)
    text = end_font.render("GAME WON", 1, ORANGE)
    WINDOW.blit(text, (WIDTH//2 - text.get_width()//2, end_rect.y))
    pygame.display.update()
    time.sleep(3)
    return True


def end_lost():
    end_rect = pygame.Rect(0, HEIGHT//2 - 22, WIDTH, 150)
    end_font = pygame.font.Font("F:/FONTS_/PressStart2P-Regular.ttf", 44)
    text = end_font.render("GAME ENDED", 1, ORANGE)
    WINDOW.blit(text, (WIDTH//2 - text.get_width()//2, end_rect.y))


def get_dist(tup1, tup2):
    x_dist = (tup1[0] - tup2[0]) ** 2
    y_dist = (tup1[1] - tup2[1]) ** 2

    dist = math.sqrt(x_dist + y_dist)
    return dist


def flip_tile(grid_dict, coord, rect):
    TILE_FONT_COLOR = (44, 44, 44)
    ZERO_FONT_COLOR = (180, 220, 169)
    bombFont = pygame.font.SysFont("monospace", 20, True)
    bombFont_surface = bombFont.render("X", 1, TILE_FONT_COLOR)

    numFont = pygame.font.SysFont("monospace", 22, True)

    pygame.draw.rect(WINDOW, FLIPPED_COLOR, rect)
    
    if flip_state[coord] != "revealed":
        if type(grid_dict[coord]) == int:
            if grid_dict[coord] == 0:
                text = numFont.render(f"{grid_dict[coord]}", 1, ZERO_FONT_COLOR)
            else:
                text = numFont.render(f"{grid_dict[coord]}", 1, TILE_FONT_COLOR)
            WINDOW.blit(text, (rect.x, rect.y))
        else:
            WINDOW.blit(bombFont_surface, (rect.x, rect.y))


def get_surrounding_tiles(clicked_tile_coord, grid_dict):
    surrounding_tiles = []
    for tile in grid_dict.keys():
        if get_dist(tile, clicked_tile_coord) in surrounding_tile_dist:
            surrounding_tiles.append(tile)
        
    return surrounding_tiles







if __name__ == "__main__":
    main()

