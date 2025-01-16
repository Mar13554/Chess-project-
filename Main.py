#Imports
from Operations import board_print, move, check_kings
#Pieces (including empty space)
_ = "_"
P = "P"; p = "p"; N = "N"; n = "n"
B = "B"; b = "b"; R = "R"; r = "r"
Q = "Q"; q = "q"; K = "K"; k = "k"
#Set board with strings
board = [[r, n, b, q, k, b, n, r], #8 (0)
         [p, p, p, p, p, p, p, p], #7 (1)
         [_, _, _, _, _, _, _, _], #6 (2)
         [_, _, _, _, _, _, _, _], #5 (3)
         [_, _, _, _, _, _, _, _], #4 (4)
         [_, _, _, _, _, _, _, _], #3 (5)
         [P, P, P, P, P, P, P, P], #2 (6)
         [R, N, B, Q, K, B, N, R]  #1 (7)
         ]
         #0, 1, 2, 3, 4, 5, 6, 7
#Status
player_white_pieces = None
white_turn = True
def start_new_game_status(debug):
    global board, white_turn
    pawn_advanced_info = [None, [None]]
    moved_piece = [False, False, False, False, False, False] #First two kings and  four rooks
    while True:
        board_print(board)
        match check_kings(board):
            case -1:
                print("Black wins, by murder!"); break
            case 1:
                print("White wins, by murder!"); break
            case 0: pass
        if white_turn: print("White turn")
        else: print("Black turn")
        notation = input("Enter move (in proper notation): ")
        if notation == "-1": break
        #Enpassant
        if pawn_advanced_info[0] == white_turn: pawn_advanced_info = [None, [None]]
        if debug: print(pawn_advanced_info)
        new_board = move(notation, board, white_turn, pawn_advanced_info[1], moved_piece, debug)

        match new_board[0]:
            case -1: print("Error, please input proper move/notation")
            case -2: print("Error, proper notation needed")
            case -3: print("Capture impossible")
            case -4: print("Couldn't find piece")
            case -5: print("Can't castle")
            case -6: print("King in danger")
            case -10:
                if white_turn: print("Checkmate, White wins!"); break
                else: print("Checkmate, Black wins!"); break
            case _:
                print("Move made")
                if new_board[1][1] is not None: pawn_advanced_info = new_board[1]
                board = new_board[0].copy()
                moved_piece = new_board[2]
                #Switch
                white_turn = False if white_turn else True

def intro_menu():
    i = input("Play, 1; Settings, 2: \n")
    if i == "1":
        debug = input("Enter debug mode? 'Y' for yes: ")
        debug = True if debug == "Y" else False
        start_new_game_status(debug)
    intro_menu()
intro_menu()