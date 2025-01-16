#Board UI
import copy

from colorama import Fore, Back

Files = ["a", "b", "c", "d", "e", "f", "g", "h"]
#1) Board print function
def split_strings(row):
    print(row[0], end="")
    for i in range(1, 8):
        print(f"  {row[i]}", end="") #Space by 2

def board_print(board):
    for i in range(0, 8):
        print(Back.GREEN, end="") #Background colour
        split_strings(board[i])     #
        print(Back.RESET, end="") #Reset background colour for Row number
        print(f" {8-i}") #Row number
    print(Back.RESET, end="")
    split_strings(Files); print()

#2) Moves
    #Convert notation to usable data
def notation_data(notation: str, white_turn, debug=False):
    # Notation: piece, file[start*], row[start*], (capture), file[end], row[end]; e.g. Qh4xe1
    piece = None
    movement = [None, None, None, None]  # [file[start], row[start], file[end], row[end]
    length_notation = len(notation)
    is_capture = False if notation.find("x") == -1 else True
    # Move info
    if (length_notation >= 2) and (length_notation < 7):
        movement[2] = notation[length_notation - 2]
        movement[3] = notation[length_notation - 1]
        if length_notation >= 3:
            if notation[0] == notation[0].upper(): piece = notation[0] if white_turn else notation[0].lower()
            else: piece = None; movement[0] = notation[0]
            if (length_notation == 5 and is_capture) or (length_notation == 4 and not is_capture):
                try: movement[1] = int(notation[1])
                except ValueError:
                    if notation[1] in Files: movement[0] = notation[1]
                    else: return -1
            elif (length_notation == 6 and is_capture) or (length_notation == 5 and not is_capture):
                if notation[1] in Files: movement[0] = notation[1]
                else: return -1
                try: movement[1] = int(notation[2])
                except ValueError: return -1
    else: return -1 #Out of range
    # Pawn notation
    if piece is None: piece = "P" if white_turn else "p"
    if debug: print([is_capture, piece, movement])
    return [is_capture, piece, movement]

file_to_index = {"a": 0, "b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7}
def notation_to_index(data, debug):
    data[2][0] = file_to_index.get(data[2][0])
    data[2][2] = file_to_index.get(data[2][2])
    try: data[2][1] = 8-int(data[2][1])
    except Exception: pass
    try: data[2][3] = 8 - int(data[2][3])
    except ValueError: return -1  # Row not a number
    if data[2][2] is None: return -1  # File not a valid letter
    if debug: print(data)
    return data
#Index, row (Inverse Y from board)
vector_square = ((0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1))
rook_vector = ((0, -1), (1, 0), (0, 1), (-1, 0))
diagonal_vector = ((1, -1), (1, 1), (-1, 1), (-1, -1))
knight_vector = ((-1, -2), (1, -2), (2, -1), (2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1))
def disambiguate(x, y, x1, y1, i: tuple, j: int):
    #x, y start cords; x1, y1; end cords; j scalar multiplication on vector i
    if (x is not None) and (y is not None):
        if x == x1 + j * i[0] and y == y1 + j * i[1]: return [x, y]
        return 0
    elif x is not None:
        if x == x1 + j * i[0]: return [x, y1 + j * i[1]]
        return 0
    elif y is not None:
        if y == y1 + j * i[1]: return [x1 + j * i[0], y]
        return 0
    else: return [x1 + j * i[0], y1 + j * i[1]]
    #Zero means square cords don't match up

def find_starting_coordinates(piece: str, end_coordinates: list, board: list, is_capture, en_passant, start_cords):
    #Return [File(index), Row(list_index)] or -1
    if piece == "Q" or piece == "q":
        for i in vector_square:
            for j in range(1, 8):
                try:
                    selected_square = board[end_coordinates[1]+j*i[1]][end_coordinates[0]+j*i[0]]
                except Exception: break
                if selected_square == piece:
                    cords = disambiguate(start_cords[0], start_cords[1], end_coordinates[0], end_coordinates[1], i, j)
                    if cords != 0: return cords
                elif selected_square != "_": break
        return -1
    elif piece == "K" or piece == "k":
        for i in vector_square:
            if board[end_coordinates[1]+i[1]][end_coordinates[0]+i[0]] == piece:
                return [end_coordinates[0]+i[0], end_coordinates[1]+i[1]]
        return -1 #No valid king move
    elif piece == "P" or piece == "p":
        match piece:
            case "P":
                if end_coordinates[1] == 7: return -1  # Off the board
                if is_capture:
                    if (board[end_coordinates[1] + 1][end_coordinates[0] + 1] == "P") and (end_coordinates[0] + 1 != 7) and (start_cords[0]==end_coordinates[0]+1 or start_cords[0] is None):
                        return [end_coordinates[0] + 1, end_coordinates[1] + 1]
                    elif board[end_coordinates[1] + 1][end_coordinates[0] - 1] == "P" and end_coordinates[0] - 1 != -1 and (start_cords[0]==end_coordinates[0]-1 or start_cords[0] is None):
                        return [end_coordinates[0] - 1, end_coordinates[1] + 1]
                    elif not (en_passant[0] is None):
                        if en_passant[0] == end_coordinates[0] and en_passant[1] == end_coordinates[1]+1:
                            if board[end_coordinates[1] + 1][end_coordinates[0] + 1] == "P" and end_coordinates[0] + 1 != 7 and (start_cords[0]==end_coordinates[0]+1 or start_cords[0] is None):
                                return [end_coordinates[0] + 1, end_coordinates[1] + 1]
                            elif board[end_coordinates[1] + 1][end_coordinates[0] - 1] == "P" and end_coordinates[0] - 1 != -1 and (start_cords[0]==end_coordinates[0]-1 or start_cords[0] is None):
                                return [end_coordinates[0] - 1, end_coordinates[1] + 1]
                            else: return -1
                        else: return -1
                    else: return -1 #Pawn not found that can capture
                else: #Move up
                    if board[end_coordinates[1]+1][end_coordinates[0]] == "P":
                        return [end_coordinates[0], end_coordinates[1]+1]
                    elif end_coordinates[1] == 4: #If pawn can advance by 2
                        if board[6][end_coordinates[0]] == "P":
                            return [end_coordinates[0], 6, [end_coordinates[0], 4]]
                    else: return -1 #No pawn move
            case "p":
                if end_coordinates[1] == 0: return -1
                if is_capture:
                    if board[end_coordinates[1] - 1][end_coordinates[0] + 1] == "p" and end_coordinates[0] + 1 != 7 and (start_cords[0]==end_coordinates[0]+1 or start_cords[0] is None):
                        return [end_coordinates[0] + 1, end_coordinates[1] - 1]
                    elif board[end_coordinates[1] - 1][end_coordinates[0] - 1] == "p" and end_coordinates[0] - 1 != -1 and (start_cords[0]==end_coordinates[0]-1 or start_cords[0] is None):
                        return [end_coordinates[0] - 1, end_coordinates[1] - 1]
                    elif not (en_passant[0] is None):
                        if en_passant[0] == end_coordinates[0] and en_passant[1] == end_coordinates[1]-1:
                            if board[end_coordinates[1] - 1][end_coordinates[0] + 1] == "p" and end_coordinates[0] + 1 != 7 and (start_cords[0]==end_coordinates[0]+1 or start_cords[0] is None):
                                return [end_coordinates[0] + 1, end_coordinates[1] - 1]
                            elif board[end_coordinates[1] - 1][end_coordinates[0] - 1] == "p" and end_coordinates[0] - 1 != -1 and (start_cords[0]==end_coordinates[0]-1 or start_cords[0] is None):
                                return [end_coordinates[0] - 1, end_coordinates[1] - 1]
                            else: return -1
                        else: return -1
                    else: return -1 #Pawn not found that can capture
                else: #Move up
                    if board[end_coordinates[1]-1][end_coordinates[0]] == "p":
                        return [end_coordinates[0], end_coordinates[1]-1]
                    elif end_coordinates[1] == 3: #If pawn can advance by 2
                        if board[1][end_coordinates[0]] == "p":
                            return [end_coordinates[0], 1, [end_coordinates[0], 3]]
                    else: return -1 #No pawn move
    elif piece == "N" or piece == "n":
        for i in knight_vector:
            try:
                if board[end_coordinates[1]+i[1]][end_coordinates[0]+i[0]] == piece:
                    try: square_selected = board[end_coordinates[1] + i[1]][end_coordinates[0] + i[0]]
                    except Exception: break
                    if square_selected == piece:
                        cords = disambiguate(start_cords[0], start_cords[1], end_coordinates[0], end_coordinates[1], i, 1)
                        if cords != 0: return cords
            except Exception: pass
        return -1
    elif piece == "B" or piece == "b":
        for i in diagonal_vector:
            for j in range(1, 8):
                try: square_selected = board[end_coordinates[1] + j * i[1]][end_coordinates[0] + j * i[0]]
                except Exception: break
                if square_selected == piece:
                    cords = disambiguate(start_cords[0], start_cords[1], end_coordinates[0], end_coordinates[1], i, j)
                    if cords != 0: return cords
                elif square_selected != "_": break
        return -1
    elif piece == "R" or piece == "r":
        for i in rook_vector:
            for j in range(1, 8):
                try: square_selected = board[end_coordinates[1]+j*i[1]][end_coordinates[0]+j*i[0]]
                except Exception: break
                if square_selected == piece:
                    cords = disambiguate(start_cords[0], start_cords[1], end_coordinates[0], end_coordinates[1], i, j)
                    if cords != 0: return cords
                elif square_selected != "_": break
        return -1

def find_king(board, white_turn):
    #Return cord, (index, row)
    king = "K" if white_turn else "k"
    for row in range(0, 8):
        for index in range(0, 8):
            if board[row][index] == king:
                return [index, row]
    return -1

#Given a coordinate, check if the square is attacked, return True of False
def check_square_safety(board: list, cords, white_turn: bool, debug=None):
    #Piece type
    piece_list_check = ["p", "n", "b", "r", "q", "k"] if white_turn else ["P", "N", "B", "R", "Q", "K"]
    #Diagonal
    for i in diagonal_vector:
        for j in range(1, 7):
            if cords[1]+j*i[1] < 0 or cords[0]+j*i[0] < 0: break
            try:
                selected_square = board[cords[1]+j*i[1]][cords[0]+j*i[0]]
            except Exception: break
            if selected_square == piece_list_check[2] or selected_square == piece_list_check[4]:
                if debug: print(f"King attacked by {selected_square}, when j is {j} from vector {i}; cord is {cords}, selected_square is {[cords[1]+j*i[1],cords[0]+j*i[0]]}")
                return False
            elif selected_square != "_": break
    #Vertical and horizontal
    for i in rook_vector:
        for j in range(1, 7):
            if cords[1] + j * i[1] < 0 or cords[0] + j * i[0] < 0: break
            try: selected_square = board[cords[1]+j*i[1]][cords[0]+j*i[0]]
            except Exception: break
            if selected_square == piece_list_check[3] or selected_square == piece_list_check[4]:
                if debug: print("King attacked by rook or queen")
                return False
            elif selected_square != "_": break
    #Knight
    for i in knight_vector:
        if cords[1] + i[1] < 0 and cords[0] + i[0] < 0:
            try:
                selected_square = board[cords[1]+i[1]][cords[0]+i[0]]
                if selected_square == piece_list_check[1]:
                    if debug: print("King attacked by knight")
                    return False
            except Exception: pass
    #King?
    for i in vector_square:
        if cords[1] + i[1] >= 0 and cords[0] + i[0] >= 0:
            try:
                selected_square = board[cords[1]+i[1]][cords[0]+i[0]]
                if selected_square == piece_list_check[5]:
                    if debug: print("King attacked by king?")
                    return False
            except Exception: pass
    #Pawn
    pawn_vector = (diagonal_vector[0], diagonal_vector[3]) if white_turn else (diagonal_vector[1], diagonal_vector[2])
    for i in pawn_vector:
        if cords[1] + i[1] >= 0 and cords[0] + i[0] >= 0:
            try:
                selected_square = board[cords[1]+i[1]][cords[0]+i[0]]
                if selected_square == piece_list_check[0]:
                    if debug: print("King attacked by pawn")
                    return False
            except Exception: pass
    return True

#(((rook index, rook row),squares_in_between), ())
#Before
king_squares = ((4, 7), (4, 0)); rook_squares = ((7, 7), (7, 0), (0, 7), (0, 0))
squares_castle_O2_W = ((5, 7), (6, 7)); squares_castle_O2_B = ((5, 0), (6, 0))
squares_castle_O3_W = ((2, 7), (3, 7)); squares_castle_O3_B = ((2, 0), (3, 0))
#After (King, Rook)
after_castle = (((6, 7), (5, 7)), ((6, 0), (5, 0)))
def castle(notation: str, white_turn: bool, board: list, moved_data: list):
    match notation:
        case "O-O":
            if white_turn:
                king_square = king_squares[0]; rook_square = rook_squares[0]
                check_squares = squares_castle_O2_W; king = "K"; rook = "R"
                rook_index_moved_data = 2; after_castle_cord = after_castle[0]
            else:
                king_square = king_squares[1]; rook_square = rook_squares[1]
                check_squares = squares_castle_O2_B; king = "k"; rook = "r"
                rook_index_moved_data = 3; after_castle_cord = after_castle[1]
        case "O-O-O":
            if white_turn:
                king_square = king_squares[0]; rook_square = rook_squares[2]
                check_squares = squares_castle_O3_W; king = "K"; rook = "R"
                rook_index_moved_data = 4; after_castle_cord = squares_castle_O3_W
            else:
                king_square = king_squares[1]; rook_square = rook_squares[3]
                check_squares = squares_castle_O3_B; king = "k"; rook = "r"
                rook_index_moved_data = 5; after_castle_cord = squares_castle_O3_B
        case _:
            return 0
    #King
    if board[king_square[1]][king_square[0]] != king or moved_data[0] == True: return -1
    #Rook
    if board[rook_square[1]][rook_square[0]] != rook or moved_data[rook_index_moved_data] == True: return -1
    #Check square is safe and empty
    for i in check_squares:
        if not check_square_safety(board, i, white_turn):
            return -1
        if board[i[1]][i[0]] != "_":
            return -1
    return [[False, king, [king_square[0], king_square[1], after_castle_cord[0][0], after_castle_cord[0][1]]], rook_square, [rook, after_castle_cord[1]]]


def update_board(board, data: list, extra, extra1=None):
    #Data: [capture, piece, [index_clear, row_clear, index_move, row_move]]
    #Extra: [index_clear, row_clear], #Extra1: [piece, [index_move, row_move]]
    #extra for en-passant and castling, extra1 for moving rook from castling
    board[data[2][3]][data[2][2]] = data[1]
    board[data[2][1]][data[2][0]] = "_"
    if extra is not None:
        board[extra[1]][extra[0]] = "_"
        if extra1 is not None:
            board[extra1[1][1]][extra1[1][0]] = extra1[0]
    return board

def move(notation: str, board1, white_turn: bool, pawn_advanced: list, moved_pieces: list, debug=False):
    en_passant = [None]
    board = copy.deepcopy(board1)
    #Check if it's castling notation
    castle_info = castle(notation, white_turn, board, moved_pieces)
    if castle_info != 0:
        if castle_info == -1:
            return [-5]
        else:
            board = update_board(board, castle_info[0], castle_info[1], castle_info[2])
            return [board, [white_turn, None], moved_pieces]
            #Not used currently
            #king_cord = find_king(board, white_turn)
            #if check_square_safety(board, king_cord, white_turn, debug):
            #    return [board, [white_turn, None], moved_pieces]
            #return [-6]
    data = notation_data(notation, white_turn, debug)
    if data == -1: return [-1] #Notation error 1
    #Convert coordinate to computer indexes
    data = notation_to_index(data, debug)
    if data == -1: return [-2] #Notation error 2
    #Check if square is closed in case of capture and vise versa
    if (data[0] and board[data[2][3]][data[2][2]]=="_")or(not data[0] and board[data[2][3]][data[2][2]]!="_"):
        if data[1] == "P" or data[1] == "p" and (not pawn_advanced[0] is None): #En passant check
            en_passant = pawn_advanced #only case (has cords of advanced pawn)
        else: return [-3] #Square is either occupied or not which doesn't match with capture

    #Fill out data that notation hasn't provided (row_start, file_start)
    start_cords = find_starting_coordinates(piece=data[1],start_cords=[data[2][0], data[2][1]], end_coordinates=[data[2][2], data[2][3]], board=board, is_capture=data[0], en_passant=en_passant)
    if start_cords == -1: return [-4] #Error with finding start cords
    data[2][0] = start_cords[0]; data[2][1] = start_cords[1]
    #Future info for enpassant
    try:
        pawn_advanced_info = start_cords[2]
        if debug: print("Pawn advanced info set")
    except IndexError: pawn_advanced_info = None
    #Enpassant
    extra = en_passant if not (en_passant[0] is None) else None
    if debug: print(data)
    #Future info for castling (changes moved_pieces)
    if start_cords in king_squares:
        for i in range(0, 2):
            if start_cords == king_squares[i]:
                moved_pieces[i] = True; break
    if start_cords in rook_squares:
        for i in range(0, 4):
            if start_cords == rook_squares[i]:
                moved_pieces[i+2] = True; break
    #Update board
    board = update_board(board, data, extra)
    return [board, [white_turn, pawn_advanced_info], moved_pieces]
    #Not used currently:
    #king_cord = find_king(board, white_turn)
    #if check_square_safety(board, king_cord, white_turn, debug):
    #    return [board, [white_turn, pawn_advanced_info], moved_pieces]
    #else:
    #    return [-6]

#Check king is alive
def check_kings(board):
    #Define
    king_W = "K"; king_B = "k"
    #Status
    W = False; B = False
    for row in board:
        for item in row:
            if item == king_W: W = True
            elif item == king_B: B = True
            if W and B: break
        if W and B: break
    if not W:
        return -1
    elif not B:
        return 1
    else:
        return 0