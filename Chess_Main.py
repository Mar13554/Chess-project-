from Chess_modules import convert_to_idx, convert_to_algebraic, piece, Pawn, Knight, Bishop, Rook, Queen, King, file_dict_0
import copy
Dict_Pieces = {King: "K", Queen: "Q", Rook: "R", Bishop: "B", Knight: "N", Pawn: "P"}
Special_Pieces = [King, Rook, Pawn]
#Castling: Rook (Old), Rook (New)
Castle_W_Q = ((0, 7), (3, 7)); Castle_W_K = ((7, 7), (5, 7))
Castle_B_Q = ((0, 0), (3, 0)); Castle_B_K = ((7, 0), (5, 0))

T = True; F = False
def P(x):
    C = x.isupper()
    x = x.upper()
    #White
    match x:
        case "K": return piece(King(), C)
        case "Q": return piece(Queen(), C)
        case "R": return piece(Rook(), C)
        case "B": return piece(Bishop(), C)
        case "N": return piece(Knight(), C)
        case "P": return piece(Pawn(), C)
        case _: return "_"

class Board:
    def __init__(self):
        self.board = [
            [P("r"), P("n"), P("b"), P("q"), P("k"), P("b"), P("n"), P("r")],
            [P("p"), P("p"), P("p"), P("p"), P("p"), P("p"), P("p"), P("p")],
            [P("_"), P("_"), P("_"), P("_"), P("_"), P("_"), P("_"), P("_")],
            [P("_"), P("_"), P("_"), P("_"), P("_"), P("_"), P("_"), P("_")],
            [P("_"), P("_"), P("_"), P("_"), P("_"), P("_"), P("_"), P("_")],
            [P("_"), P("_"), P("_"), P("_"), P("_"), P("_"), P("_"), P("_")],
            [P("P"), P("P"), P("P"), P("P"), P("P"), P("P"), P("P"), P("P")],
            [P("R"), P("N"), P("B"), P("Q"), P("K"), P("B"), P("N"), P("R")]
        ]
        self.move = 1
        self.turn_is_white = True
        self.find_all_moves()
    #Modules
    def clear_temp(self, is_white, promote): #Turn the "en" back to False or promate pawn
        for row in range(8):
            for file in range(8):
                square = self.board[row][file]
                if square != "_" and type(square.type) == Pawn:
                    if square.is_white == is_white: square.type.en = False
                    if ((row == 0) or (row == 7)):
                        match promote:
                            case "Q":
                                self.board[row][file] = piece(Queen(), not is_white)
                            case "R":
                                self.board[row][file] = piece(Rook(), not is_white)
                            case "B":
                                self.board[row][file] = piece(Bishop(), not is_white)
                            case "N":
                                self.board[row][file] = piece(Knight(), not is_white)

    def find_all_moves(self):
        for row in range(8):
            for file in range(8):
                square = self.board[row][file]
                if square != "_": square.get_possible_moves((file, row), self.board)

    def convert_to_cords(self, notation):
        # Special (Castling)
        if notation == "O-O": pass
        if notation == "O-O-O": pass
        #Define
        file_start = None; row_start = None
        # Find piece type
        Notation_dict = {"K": King, "Q": Queen, "R": Rook, "B": Bishop, "N": Knight}
        piece_type = Notation_dict.get(notation[0])
        if piece_type == None:
            file_start = file_dict_0.get(notation[0])
            piece_type = Pawn
        # Get destination square
        length = len(notation)
        if notation[-1] in ["+", "#"]:
            pos_end = convert_to_idx(notation[length-3:length-1])
        else:
            pos_end = convert_to_idx(notation[length-2:length])
        pass
    #WIP

    #Use
    def return_board(self, flipped, out=False):
        board = copy.deepcopy(self.board)
        #Replace with letters
        for row in range(8):
            for file in range(8):
                square = board[row][file]
                if square != "_":
                    colour = square.is_white
                    square = Dict_Pieces.get(type(square.type))
                    if not colour: square = square.lower()
                board[row][file] = square
        #Flip if needed
        if flipped:
            def flip(board):
                temp_board = []
                for file in range(len(board[0])):
                    temp_list = []
                    for row in range(len(board) - 1, -1, -1):
                        temp_list.append(board[row][file])
                    temp_board.append(temp_list)
                return temp_board
            flip_one = flip(board)
            flip_two = flip(flip_one)
            board = flip_two
        if out:
            for i in board: print(i)
        else: return board

    def check_king_alive(self):
        White_King_Alive = False; Black_King_Alive = False
        for row in self.board:
            for square in row:
                if square == "_": continue
                if type(square.type) == King:
                    if square.is_white:
                        White_King_Alive = True
                    else:
                        Black_King_Alive = True
                if White_King_Alive and Black_King_Alive: break
        if White_King_Alive and Black_King_Alive:
            return 0
        elif White_King_Alive:
            return 1
        else: return -1

    def make_move(self, start_cord, end_cord, promote="Q"):
        #Decomplie
        Start_Square = self.board[start_cord[1]][start_cord[0]]
        End_Square = self.board[end_cord[1]][end_cord[0]]
        #Check
        if Start_Square == "_": return -1 #Empty square selected
        if Start_Square.is_white != self.turn_is_white: return -1 #Wrong colour piece selected
        if End_Square != "_" and End_Square.is_white == self.turn_is_white: return -1  #Captured own piece
        Type = type(Start_Square.type)
        if end_cord in Start_Square.moves: #Is standard move
            if Type in Special_Pieces:
                Start_Square.type.has_moved = True
            self.board[start_cord[1]][start_cord[0]] = "_"
            self.board[end_cord[1]][end_cord[0]] = Start_Square
        else:
            if Type is Pawn:
                Found = False
                for i in Start_Square.special_moves:
                    if end_cord == i[1]:
                        if i[0] == "Advance":
                            Found = True
                            Start_Square.type.has_moved = True
                            Start_Square.type.en = True
                            self.board[start_cord[1]][start_cord[0]] = "_"
                            self.board[end_cord[1]][end_cord[0]] = Start_Square
                            break
                        elif i[0] == "En-passant":
                            Found = True
                            self.board[start_cord[1]][start_cord[0]] = "_"
                            self.board[end_cord[1]][end_cord[0]] = Start_Square
                            if self.turn_is_white: self.board[end_cord[1]+1][end_cord[0]] = "_"
                            else: self.board[end_cord[1]-1][end_cord[0]] = "_"
                            break
                if not Found: return -1
            elif Type is King:
                Castle = None
                for i in Start_Square.special_moves:
                    if i == "O-O":
                        if Start_Square.is_white: Castle = Castle_W_K
                        else: Castle = Castle_B_K
                        break
                    elif i == "O-O-O":
                        if Start_Square.is_white: Castle = Castle_W_Q
                        else: Castle = Castle_B_Q
                        break
                if Castle != None:
                    self.board[start_cord[1]][start_cord[0]] = "_" #Remove Previous Square
                    self.board[end_cord[1]][end_cord[0]] = Start_Square #King
                    Start_Square.type.has_moved = True
                    Rook = self.board[Castle[0][1]][Castle[0][0]] #Save old rook
                    self.board[Castle[0][1]][Castle[0][0]] = "_" #Remove Rook square
                    self.board[Castle[1][1]][Castle[1][0]] = Rook #Replace
                else: return -1
            else: return -1
        #Update
        if self.turn_is_white:
            self.turn_is_white = False
        else:
            self.turn_is_white = True
            self.move += 1
        self.clear_temp(self.turn_is_white, promote)
        self.find_all_moves()
        return 0

#Debug
Main_Board = Board()
Main_Board.find_all_moves()
def debug_moves(algebraic):
    cord = convert_to_idx(algebraic)
    for i in Main_Board.board[cord[1]][cord[0]].moves:
        print(convert_to_algebraic(i))
    for i in Main_Board.board[cord[1]][cord[0]].special_moves:
        print(i)