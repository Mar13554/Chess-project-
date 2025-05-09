import pygame
import os
from standards import color_list, font_list, button_info, spacing,\
    button_id_checker, square_screen_cords, coloured_squares, text_numbers_rows, text_letters_files
from Chess_Main import Board
from Chess_modules import convert_to_algebraic, convert_to_cord

pygame.init()
#Global variables
screen_state = "Start_Screen"
piece_selected = None #Square ID
#Game info
Outcome = 0
is_white_turn = True
is_white = True
promote_piece = "Q"
is_singleplayer = False
game_ongoing = False
Main_board = Board()

#Planned dimensions: (800, 600), (1024, 728)
pieces_folder = os.path.join(os.path.dirname(__file__), "chess_pieces_images")
piece_image_names = {"P": "white_pawn.png", "p": "black_pawn.png", "N": "white_knight.png", "n":"black_knight.png",
                     "B":"white_bishop.png", "b":"black_bishop.png","R": "white_rook.png", "r": "black_rook.png",
                     "Q": "white_queen.png", "q": "black_queen.png" ,"K": "white_king.png","k": "black_king.png", "_":None}

screen_width, screen_height = None, None
screen = None; fonts = None
space = None; button_sizes = None
def set(width, height):
    screen_width, screen_height = width, height
    screen = pygame.display.set_mode((width, height))
    fonts = font_list(screen_width)
    space = spacing(screen_width)
    button_sizes = button_info(screen_width, screen_height)

def run():
    global screen_state, is_piece_selected, piece_selected,is_singleplayer, is_white, game_ongoing, Main_board, is_white_turn, promote_piece, Outcome
    global screen_width, screen_height, screen, fonts, space, button_sizes
    #Set
    Info = pygame.display.Info()
    native_width = Info.current_w; native_height = Info.current_h
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Chessn't V.1a")
    clock = pygame.time.Clock()
    #Initialize custom objects
    colours = color_list()
    fonts = font_list(screen_width)
    space = spacing(screen_width)
    button_sizes = button_info(screen_width, screen_height)

    #Functions (sub)
    def create_button(id, screen, position, size, text, colour, thickness):
        #Rectangle and text
        pygame.draw.rect(screen, colour, (position[0], position[1], size[0], size[1]))
        pygame.draw.rect(screen, colours.black, (position[0], position[1], size[0], size[1]), width=thickness)
        text = fonts.text.render(text, True, colours.black)
        screen.blit(text, ((size[0]-text.get_width())/2+position[0], (size[1]-text.get_height())/2+position[1]))
        return [id, [position[0], position[0] + size[0]], [position[1], position[1] + size[1]]]  # [[id], [x-range], [y-range]

    def invisible_button(id, position, size):
        return [id, [position[0], position[0] + size[0]], [position[1], position[1] + size[1]]]

    #Functions (screens)
    def start_screen():
        screen.fill(colours.light_green)
        text_surface = fonts.H1.render("Welcome!", True, colours.black)
        screen.blit(text_surface, ((screen_width-text_surface.get_width())/2, 25))
        y_position = text_surface.get_height()+50 #For moving down
        total_split = (screen_height-y_position)/3-button_sizes.button_main[1]
        #Button creation
        buttons_start_screen = []
        buttons_start_screen.append(create_button(0, screen, (space.margin, y_position), button_sizes.button_main, "Play", colours.light_purple, 2))
        y_position += button_sizes.button_main[1] + total_split
        buttons_start_screen.append(create_button(1, screen, (space.margin, y_position), button_sizes.button_main, "Settings", colours.light_purple, 2))
        y_position += button_sizes.button_main[1] + total_split
        buttons_start_screen.append(create_button(2, screen, (space.margin, y_position), button_sizes.button_main, "Info", colours.light_purple, 2))
        return buttons_start_screen

    def side_bar(space_position, space_size, square_size):
        buttons_sidebar = []
        if game_ongoing:
            if Outcome == 0: text_surface = fonts.H1.render("White's turn", True, colours.black) if is_white_turn else fonts.H1.render("Black's turn", True, colours.black)
            else: text_surface = fonts.H1.render("White Wins!", True, colours.black) if Outcome == 1 else fonts.H1.render("Black Wins!", True, colours.black)
            y_level = space_position[1] + space.margin / 3
            screen.blit(text_surface, (space_size[0]/2-3*square_size[0]/2+space_position[0], y_level))
            y_level += space.margin
            text_surface = fonts.H2.render("Promote into?", True, colours.black)
            screen.blit(text_surface, (space_size[0] / 2 - 3 * square_size[0] / 2 + space_position[0], y_level))
            #First Layer Selection
            y_level += space.margin
            square_position_1 = (space_position[0] + (space_size[0] / 2) - 17 * square_size[0] / 16, y_level)
            square_position_2 = (space_position[0] + (space_size[0] / 2) + square_size[0] / 16, y_level)
            pygame.draw.rect(screen, colours.white,(square_position_1[0], square_position_1[1], square_size[0], square_size[1]))
            pygame.draw.rect(screen, colours.white,(square_position_2[0], square_position_2[1], square_size[0], square_size[1]))
            loaded_image = pygame.transform.scale(pygame.image.load(os.path.join(pieces_folder, "white_queen.png" if is_white_turn else "black_queen.png")), (square_size[0]/1.5, square_size[1]/ 1.5))
            screen.blit(loaded_image,(square_position_1[0] + square_size[0] / 6, square_position_1[1] + square_size[1] / 6))
            loaded_image = pygame.transform.scale(pygame.image.load(os.path.join(pieces_folder, "white_rook.png" if is_white_turn else "black_rook.png")),(square_size[0] / 1.5, square_size[1] / 1.5))
            screen.blit(loaded_image,(square_position_2[0] + square_size[0] / 6, square_position_2[1] + square_size[1] / 6))
            buttons_sidebar.append(invisible_button(75, square_position_1, square_size))
            buttons_sidebar.append(invisible_button(76, square_position_2, square_size))
            #Second Layer selection
            y_level += 9*square_size[0]/8
            square_position_3 = (space_position[0] + (space_size[0] / 2) - 17 * square_size[0] / 16, y_level)
            square_position_4 = (space_position[0] + (space_size[0] / 2) + square_size[0] / 16, y_level)
            pygame.draw.rect(screen, colours.white,(square_position_3[0], square_position_3[1], square_size[0], square_size[1]))
            pygame.draw.rect(screen, colours.white,(square_position_4[0], square_position_4[1], square_size[0], square_size[1]))
            loaded_image = pygame.transform.scale(pygame.image.load( os.path.join(pieces_folder, "white_bishop.png" if is_white_turn else "black_bishop.png")),(square_size[0] / 1.5, square_size[1] / 1.5))
            screen.blit(loaded_image,(square_position_3[0] + square_size[0] / 6, square_position_3[1] + square_size[1] / 6))
            loaded_image = pygame.transform.scale(pygame.image.load(os.path.join(pieces_folder, "white_knight.png" if is_white_turn else "black_knight.png")),(square_size[0] / 1.5, square_size[1] / 1.5))
            screen.blit(loaded_image,(square_position_4[0] + square_size[0] / 6, square_position_4[1] + square_size[1] / 6))
            buttons_sidebar.append(invisible_button(77, square_position_3, square_size))
            buttons_sidebar.append(invisible_button(78, square_position_4, square_size))
            #Highlight selected
            pygame.draw.rect(screen, colours.light_blue, (square_position_1[0] if (promote_piece == "Q" or promote_piece == "B") else square_position_2[0], square_position_1[1] if (promote_piece == "Q" or promote_piece == "R") else square_position_3[1], square_size[0], square_size[1]), width=3)
            #Reset
            buttons_sidebar.append(create_button(79, screen, (space_position[0] + space.margin, space_position[1] + space_size[1] - space.margin),(space_size[0] - 2 * space.margin, space.margin), text="Reset", colour=colours.white, thickness=2))
        else:
            #Two kings (colour) selection
            y_level = space_position[1]+space.margin/2
            square_position_1 = (space_size[0]/2-5*square_size[0]/4+space_position[0], y_level)
            square_position_2 = (space_size[0]/2+square_size[0]/4+space_position[0], y_level)
            pygame.draw.rect(screen, colours.white, (square_position_1[0], square_position_1[1], square_size[0], square_size[1]))
            pygame.draw.rect(screen, colours.black, (square_position_2[0], square_position_2[1], square_size[0], square_size[1]))
            pygame.draw.rect(screen, colours.light_blue, (square_position_1[0] if is_white else square_position_2[0], square_position_1[1], square_size[0], square_size[1]), width=3)
            loaded_image = pygame.transform.scale(pygame.image.load(os.path.join(pieces_folder, "white_king.png")), (square_size[0]/1.5, square_size[1]/ 1.5))
            screen.blit(loaded_image, (square_position_1[0]+square_size[0]/6, square_position_1[1]+square_size[1]/6))
            loaded_image = pygame.transform.scale(pygame.image.load(os.path.join(pieces_folder, "black_king.png")),(square_size[0] / 1.5, square_size[1] / 1.5))
            screen.blit(loaded_image,(square_position_2[0] + square_size[0] / 6, square_position_2[1] + square_size[1] / 6))
            buttons_sidebar.append(invisible_button(64, square_position_1, square_size))
            buttons_sidebar.append(invisible_button(65, square_position_2, square_size))
            y_level +=  square_size[1]+space.margin/2
            #Single or multiplayer selection
            buttons_sidebar.append(create_button(66, screen, (space_position[0], y_level),(space_size[0], space.margin), text="Singleplayer",colour=colours.white, thickness=2))
            buttons_sidebar.append(create_button(67, screen, (space_position[0], y_level+space.margin), (space_size[0], space.margin),text="Multiplayer", colour=colours.white, thickness=2))
            pygame.draw.rect(screen, colours.light_blue, (space_position[0], y_level if is_singleplayer else y_level+space.margin, space_size[0], space.margin), width=3)
            #Bot selections (add later should be 6)
            pass
            #Start button
            buttons_sidebar.append(create_button(74, screen, (space_position[0]+space.margin, space_position[1]+space_size[1]-space.margin), (space_size[0]-2*space.margin, space.margin), text="Start", colour=colours.white, thickness=2))
        return buttons_sidebar

    def game_screen():
        screen.fill(colours.gray)
        board_length = screen_height-2*space.margin
        square_length = board_length/8
        #Board
        pygame.draw.rect(screen, colours.white, (space.margin, space.margin, board_length, board_length))
        position_squares = square_screen_cords((space.margin, space.margin), square_length)
        dark_squares = coloured_squares(position_squares)
        for pos in dark_squares:
            pygame.draw.rect(screen, colours.green, (pos[0], pos[1], square_length, square_length))
            #Highlight selected square
            if piece_selected is not None:
                temp_num = piece_selected
                for row in range(0, 8):
                    if temp_num >= 8:
                        temp_num -= 8
                    else:
                        pygame.draw.rect(screen, colours.light_red,(position_squares[row][temp_num][0], position_squares[row][temp_num][1], square_length, square_length))
                        break
            #Outline
            pygame.draw.rect(screen, colours.black, (space.margin, space.margin, board_length, board_length), width=2)
        #Buttons id, 0-63
        buttons = []; id = 0
        for row in position_squares:
            for cords in row:
                buttons.append(invisible_button(id, cords, (square_length, square_length)))
                id+=1
        #Fill board
        Displayed_board = Main_board.return_board(flipped=(not is_white))
        for row in range(0, 8):
            for file in range(0, 8):
                piece = Displayed_board[row][file]
                path_piece = piece_image_names.get(piece) if piece != "_" else None
                if path_piece is not None:
                    path_piece = os.path.join(pieces_folder, path_piece)
                    loaded_image = pygame.image.load(path_piece)
                    loaded_image = pygame.transform.scale(loaded_image, (square_length/1.5, square_length/1.5))
                    screen.blit(loaded_image, (position_squares[row][file][0]+square_length/6, position_squares[row][file][1]+square_length/6))
        #Fill letters and numbers around board
        y_level = space.margin+square_length*(12/32)
        for i in range(0, 8):
            text = fonts.text.render(text_numbers_rows[1][i] if is_white else text_numbers_rows[0][i], True, colours.black)
            screen.blit(text, (space.margin/2, y_level))
            text = fonts.text.render(text_letters_files[0][i] if is_white else text_letters_files[1][i], True, colours.black)
            screen.blit(text, (y_level, space.margin+board_length))
            y_level += square_length
        #Create sidebar
        sidebar_position, sidebar_size = (space.margin + board_length, space.margin), (screen_width-board_length-2*space.margin, board_length)
        pygame.draw.rect(screen, colours.dark_gray, (sidebar_position[0], sidebar_position[1], sidebar_size[0], sidebar_size[1]))
        pygame.draw.rect(screen, colours.black, (sidebar_position[0], sidebar_position[1], sidebar_size[0], sidebar_size[1]), width=2)
        buttons += side_bar(sidebar_position, sidebar_size, square_size=(square_length, square_length))
        return buttons

    def settings_screen():
        screen.fill(colours.gray)
        text_surface = fonts.H1.render("Settings", True, colours.black)
        screen.blit(text_surface, ((screen_width - text_surface.get_width()) / 2, 25))
        y_position = text_surface.get_height() + 50  # For moving down
        # Button creation
        buttons_settings_screen = []
        buttons_settings_screen.append(create_button(0, screen, (space.margin, y_position), button_sizes.button_sub, "768x1028", colours.light_purple,2))
        buttons_settings_screen.append(create_button(1, screen, (3*space.margin/2+button_sizes.button_sub[0], y_position), button_sizes.button_sub, "800x600", colours.light_purple, 2))
        y_position += button_sizes.button_sub[1] + space.margin/2
        buttons_settings_screen.append(create_button(2, screen, (space.margin, y_position), button_sizes.button_sub, "1280x720", colours.light_purple,2))
        buttons_settings_screen.append(create_button(3, screen, (3*space.margin/2+button_sizes.button_sub[0], y_position), button_sizes.button_sub, "Auto", colours.light_purple,2))
        #Exit
        buttons_settings_screen.append(create_button(-1, screen, ((screen_width-button_sizes.button_sub[0])/2, screen_height-button_sizes.button_sub[1]), button_sizes.button_sub, "Exit", colours.light_purple, 2))
        return buttons_settings_screen

    #Running logic
    loaded_buttons = []
    running = True
    while running:
        #Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                result_id = button_id_checker(loaded_buttons, mouse_pos)
                print(result_id)
                if screen_state == "Start_Screen": #0: Game, 1: Settings, 2: Info
                    if result_id == 0:
                        screen_state = "Game_Screen"
                    if result_id == 1:
                        screen_state = "Settings_Screen"
                elif screen_state == "Game_Screen": #0-63: Board, 64-65: Colour selection, 66-67: Single player, 68-73: Bots (WIP), 74: Start
                    match result_id:
                        case 64:
                            if not is_white: is_white = True
                        case 65:
                            if is_white: is_white = False
                        case  66:
                            if not is_singleplayer: is_singleplayer = True
                        case 67:
                            if is_singleplayer: is_singleplayer = False
                        case 74: game_ongoing = True
                        case 75: promote_piece = "Q"
                        case 76: promote_piece = "R"
                        case 77: promote_piece = "B"
                        case 78: promote_piece = "N"
                        case 79:
                            game_ongoing = False
                            is_white_turn = True
                            Main_board = Board()
                            Outcome = 0
                        case _: #0-63 Reserved for board
                            if result_id != -1:
                                coordinate = convert_to_cord(result_id, is_white)
                                print(convert_to_algebraic(coordinate))
                                if Main_board.turn_is_white is is_white_turn or piece_selected:
                                    if piece_selected is None: #Select
                                        piece_selected = result_id
                                    else: #Move
                                        game_ongoing = True
                                        previous_cord = convert_to_cord(piece_selected, is_white)
                                        piece_selected = None
                                        if Main_board.make_move(previous_cord, coordinate, promote_piece) == 0:
                                            is_white_turn = False if is_white_turn else True
                                        else: print("Failed to move")
                                        if Outcome == 0: Outcome = Main_board.check_king_alive()
                            else:
                                piece_selected = None
                elif screen_state == "Settings_Screen": #Dimension Selections, 0: , 1:, 2:, 3:
                    match result_id:
                        case 0:
                            set(768, 1028)
                        case 1:
                            set(800, 600)
                        case 2:
                            set(1280, 720)
                        case 3:
                            set(native_width, native_height)
                        case -1:
                            screen_state = "Start_Screen"
        #Screen draw
        if screen_state == "Start_Screen":
            loaded_buttons = start_screen()
        elif screen_state == "Game_Screen":
            loaded_buttons = game_screen()
        elif screen_state == "Settings_Screen":
            loaded_buttons = settings_screen()
        #Display
        pygame.display.flip()
        clock.tick(10)
    pygame.quit()

if __name__ == "__main__":
    run()