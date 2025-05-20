#Vectors (x [file], y [row])
Knight_Vectors = ((1, -2), (2, -1), (2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2))
Bishop_Vectors = ((1, -1), (1, 1), (-1, 1), (-1, -1))
Rook_Vectors = ((0, -1), (1, 0), (0, 1), (-1, 0))
Adjacent_Vectors = (Rook_Vectors+Bishop_Vectors)
White_Pawn_Vector_Move = [(0, -1)]; White_Pawn_Vector_Capture = ((-1, -1), (1, -1))
Black_Pawn_Vector_Move = [(0, 1)]; Black_Pawn_Vector_Capture = ((-1, 1), (1, 1))

#Classes
class piece:
    def __init__(self, type, is_white = True):
        self.is_white = is_white
        self.type = type
        self.moves = []
        self.special_moves = []
    def get_possible_moves(self, pos, board):
        self.moves, self.special_moves = self.type.get_possible_moves(pos, board, self.is_white)

class Pawn(object):
    def __init__(self):
        self.has_moved = False; self.en = False
    def get_possible_moves(self, pos, board, is_white, debug=False):
        movement_vector = White_Pawn_Vector_Move if is_white else Black_Pawn_Vector_Move
        capture_vector = White_Pawn_Vector_Capture if is_white else Black_Pawn_Vector_Capture
        moves = []
        special_moves = []
        square = None
        for vec in movement_vector:
            pos_file = vec[0] + pos[0]
            pos_row = vec[1] + pos[1]
            if (not (0 <= pos_file <= 7)) or (not (0 <= pos_row <= 7)): continue
            square = board[pos_row][pos_file]
            if square == "_":
                moves.append((pos_file, pos_row))
                if not self.has_moved:
                    pos_file += vec[0]
                    pos_row += vec[1]
                    if (0 <= pos_file <= 7) and (0 <= pos_row <= 7):
                        square = board[pos_row][pos_file]
                        if square == "_": special_moves.append(["Advance", (pos_file, pos_row)])
        for vec in capture_vector:
            pos_file = vec[0] + pos[0]
            pos_row = vec[1] + pos[1]
            if (not (0 <= pos_file <= 7)) or (not (0 <= pos_row <= 7)): continue
            square = board[pos_row][pos_file]
            if square != "_" and square.is_white != is_white:
                moves.append((pos_file, pos_row))
            if square == "_":
                take_pawn = board[pos_row-vec[1]][pos_file]
                if take_pawn != "_" and type(take_pawn.type) == Pawn and take_pawn.is_white != is_white and take_pawn.type.en is True:
                    special_moves.append(["En-passant", (pos_file, pos_row)])
        return moves, special_moves

class Knight(object):
    def get_possible_moves(self, pos, board, is_white):
        moves = []
        square = None
        for vec in Knight_Vectors:
            pos_file = vec[0] + pos[0]
            pos_row = vec[1] + pos[1]
            if (not (0 <= pos_file <= 7)) or (not (0 <= pos_row <= 7)): continue
            square = board[pos_row][pos_file]
            if square == "_" or square.is_white != is_white: moves.append((pos_file, pos_row))
        return moves, []

#Bishop, Rook, Queen
def repeating_vector_check(pos, board, is_white, Vectors):
    moves = []
    square = None
    for vec in Vectors:
        for idx in range(1, 8):
            pos_file = idx * vec[0] + pos[0]
            pos_row = idx * vec[1] + pos[1]
            if (not (0 <= pos_file <= 7)) or (not (0 <= pos_row <= 7)): break
            square = board[pos_row][pos_file]
            if square == "_":
                moves.append((pos_file, pos_row))
            elif square.is_white != is_white:
                moves.append((pos_file, pos_row))
                break
            else:
                break
    return moves, []

class Bishop(object):
    def get_possible_moves(self, pos, board, is_white):
        return repeating_vector_check(pos, board, is_white, Bishop_Vectors)

class Rook(object):
    def __init__(self):
        self.has_moved = False
    def get_possible_moves(self, pos, board, is_white):
        return repeating_vector_check(pos, board, is_white, Rook_Vectors)

class Queen(object):
    def get_possible_moves(self, pos, board, is_white):
        return repeating_vector_check(pos, board, is_white, Adjacent_Vectors)
#Before castle squares:
Pos_Castle_White_Start = ((0, 7), (7, 7)) #a1 Rook, h1 Rook
Pos_Castle_Black_Start = ((0, 0), (7, 0)) #a8 Rook, h8 Rook
#Must be empty squares to castle
Pos_White_Emp_Left = ((1, 7), (2, 7), (3, 7)); Pos_White_Emp_Right = ((5, 7), (6, 7))
Pos_Black_Emp_Left = ((1, 0), (2, 0), (3, 0)); Pos_Black_Emp_Right = ((5, 0), (6, 0))
class King(object):
    def __init__(self):
        self.has_moved = False
    def get_possible_moves(self, pos, board, is_white):
        moves = []
        special_moves = []
        square = None
        for vec in Adjacent_Vectors:
            pos_file = vec[0] + pos[0]
            pos_row = vec[1] + pos[1]
            if (not (0 <= pos_file <= 7)) or (not (0 <= pos_row <= 7)): continue
            square = board[pos_row][pos_file]
            if square == "_" or square.is_white != is_white: moves.append((pos_file, pos_row))
        #Castling
        if not self.has_moved:
            if is_white:
                Left_square = board[Pos_Castle_White_Start[0][1]][Pos_Castle_White_Start[0][0]]
                Right_square = board[Pos_Castle_White_Start[1][1]][Pos_Castle_White_Start[1][0]]
                Left_Empty_Square_pos = Pos_White_Emp_Left
                Right_Empty_Square_pos = Pos_White_Emp_Right
            else:
                Left_square = board[Pos_Castle_Black_Start[0][1]][Pos_Castle_Black_Start[0][0]]
                Right_square = board[Pos_Castle_Black_Start[1][1]][Pos_Castle_Black_Start[1][0]]
                Left_Empty_Square_pos = Pos_Black_Emp_Left
                Right_Empty_Square_pos = Pos_Black_Emp_Right
            Clear = True
            if Left_square != "_" and type(Left_square.type) is Rook and Left_square.type.has_moved is False:
                for file, row in Left_Empty_Square_pos:
                    if board[row][file] == "_": continue
                    else: Clear = False; break
                if Clear: special_moves.append(["O-O-O", Left_Empty_Square_pos[1]])
            Clear = True
            if Right_square != "_" and type(Right_square.type) is Rook and Right_square.type.has_moved is False:
                for file, row in Right_Empty_Square_pos:
                    if board[row][file] == "_": continue
                    else: Clear = False; break
                if Clear: special_moves.append(["O-O", Right_Empty_Square_pos[-1]])
        return moves, special_moves

#Modules for conversion
def convert_to_cord(num, is_white=True):
    row = 0
    while num > 7:
        row += 1
        num -= 8
    new_cord = (num, row) if is_white else (7-num, 7-row)
    return new_cord #Standard

file_dict_0 = {"a" : 0, "b" : 1, "c" : 2, "d" : 3, "e" : 4, "f" : 5, "g" : 6, "h" : 7}
def convert_to_idx(cord):
    file = file_dict_0.get(cord[0])
    row = 8-int(cord[1])
    new_cord = (file, row)
    return new_cord

file_dict_1 = {0 : "a", 1 : "b", 2 : "c", 3 : "d", 4 : "e", 5 : "f", 6 : "g", 7 : "h"}
def convert_to_algebraic(cord):
    file = file_dict_1.get(cord[0])
    row = 8 - cord[1]
    return file+str(row)
