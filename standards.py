import pygame
#Classes holding info
class color_list:
    def __init__(self):
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.gray = (150, 150, 150)
        self.dark_gray = (130, 130, 130)
        self.light_purple = (130, 16, 243)
        self.light_green = (0, 204, 102)
        self.green = (64, 174, 56)
        self.light_red = (255, 36, 36)
        self.light_blue = (120, 223, 255)

class font_list:
    def __init__(self, screen_width):
        pygame.font.init()
        self.H1 = pygame.font.Font(None, int(screen_width/17.3913043478)) #46 (800)
        self.H2 = pygame.font.Font(None, int(screen_width / 20))  # 40 (800)
        self.text = pygame.font.Font(None, int(screen_width/24)) #33.333... (800)

class spacing:
    def __init__(self, screen_width):
        self.margin = int(screen_width/16)

class button_info:
    def __init__(self, screen_width, screen_height):
        self.button_main = (screen_width/4, screen_height/6) #(200, 100)
        self.button_sub = (screen_width/6, screen_height/9)

#List on the side of the board
text_numbers_rows = (["1", "2", "3", "4", "5", "6", "7", "8"], ["8", "7", "6", "5", "4", "3", "2", "1"])
text_letters_files = (["A", "B", "C", "D", "E", "F", "G", "H"], ["H", "G", "F", "E", "D", "C", "B", "A"])

#Functions for screen
def button_id_checker(buttons, position):
    for idx in range(0, len(buttons)):
        x_range = buttons[idx][1]
        y_range = buttons[idx][2]
        if x_range[0] <= position[0] and position[0] <= x_range[1]:
            if y_range[0] <= position[1] and position[1] <= y_range[1]:
                return buttons[idx][0]
    return -1

def square_screen_cords(position, length):
    x = position[0]; y = position[1]
    coordinates = []
    for row in range(0, 8):
        row_list = []
        for column in range(0, 8):
            row_list.append((x+length*column, y+length*row))
        coordinates.append(row_list)
    return coordinates

def coloured_squares(coordinates):
    squares_selected = []
    changed = False
    for row in range(0, 8):
        changed = True if changed is False else False
        for column in range(0, 8):
            if changed is True:
                changed = False
            else:
                squares_selected.append(coordinates[row][column])
                changed = True
    return squares_selected