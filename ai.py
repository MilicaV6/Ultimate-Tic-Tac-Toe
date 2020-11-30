from random import randint
from config import *

def score(game_state):
    if game_state==O:
        return 10
    elif game_state==X:
        return -10
    else:
        return 0
    
def check_small_board_win(board):
    draw_count=0
    
    #checking if game is horizontaly or verticaly compete?
    for i in range(3):
        x_count_hor=x_count_ver=o_count_hor=o_count_ver=0
        for j in range(3):
            if board[i][j]==X:
                x_count_hor+=1
            elif board[i][j]==O:
                o_count_hor+=1
            if board[j][i]==X:
                x_count_ver+=1
            elif board[j][i]==O:
                o_count_ver+=1
            if board[i][j]=="":
                draw_count+=1
                
        if x_count_ver==3 or x_count_hor==3:
            return X
        elif o_count_hor==3 or o_count_ver==3:
            return O
        
    #checking if game is diagonaly complete.
    x_d1_count=x_d2_count=o_d1_count=o_d2_count=0
    for i in range(3):
        #main diagonal
        if board[i][i]==X:
            x_d1_count+=1
        elif board[i][i]==O:
            o_d1_count+=1
        #back diagonal
        if board[i][3-i-1]==X:
            x_d2_count+=1
        elif board[i][3-i-1]==O:
            o_d2_count+=1
            
    if x_d1_count==3 or x_d2_count==3:
        return X
    elif o_d1_count==3 or o_d2_count==3:
        return O
    
    #check if game is draw
    if draw_count==0:
        return STATUS_DRAW
   
    return STATUS_CONTINUE

def get_game_status(board):
    draw_count=0
    
    #checking if game is horizontaly or verticaly compete?
    for i in range(3):
        x_count_hor=x_count_ver=o_count_hor=o_count_ver=0
        for j in range(3):
            if board.table[i][j]==X:
                x_count_hor+=1
            elif board.table[i][j]==O:
                o_count_hor+=1
            if board.table[j][i]==X:
                x_count_ver+=1
            elif board.table[j][i]==O:
                o_count_ver+=1
            if board.table[i][j]=="":
                draw_count+=1
                
        if x_count_ver==3 or x_count_hor==3:
            return X
        elif o_count_hor==3 or o_count_ver==3:
            return O
        
    #checking if game is diagonaly complete.
    x_d1_count=x_d2_count=o_d1_count=o_d2_count=0
    for i in range(3):
        #main diagonal
        if board.table[i][i]==X:
            x_d1_count+=1
        elif board.table[i][i]==O:
            o_d1_count+=1
        #back diagonal
        if board.table[i][3-i-1]==X:
            x_d2_count+=1
        elif board.table[i][3-i-1]==O:
            o_d2_count+=1
            
    if x_d1_count==3 or x_d2_count==3:
        return X
    elif o_d1_count==3 or o_d2_count==3:
        return O
    
    #check if game is draw
    if draw_count==0:
        return STATUS_DRAW
   
    return STATUS_CONTINUE

def get_available_moves_in_board(board):
    moves=[]
    for i in range(3):
        for j in range(3):
            if board.table[i][j]=="" and board.winner==None:
                moves.append((i,j))
    return moves

def alpha_beta_pruning(board, game_state, alpha, beta, game_turn):
    if game_state!=STATUS_CONTINUE:
        return score(game_state)
    scores=[]
    moves=get_available_moves_in_board(board)
    
    for move in moves:
        board.table[move[0]][move[1]]=game_turn
        if game_turn==X:
            new_turn=O
        else:
            new_turn=X
            
        val=alpha_beta_pruning(board,get_game_status(board),alpha,beta,new_turn)
        board.table[move[0]][move[1]]=""
        if game_turn==O:
            if val>alpha:
                alpha=val
            if alpha>=beta:
                return beta
        if game_turn==X:
            if val<beta:
                beta=val
            if beta<=alpha:
                return alpha
    if game_turn==O:
        return alpha
    else:
        return beta

def determine_board(boards):
    available_boards=[]
    for i in range(3):
        for j in range (3):
            if boards[i][j].winner==None:
                available_boards.append(boards[i][j])

    return available_boards[randint(0, len(available_boards)-1)]
    
def determine_move(board,game_turn):
    a=-2
    choices=[(0,0),(0,2),(2,0),(2,2)]
    moves=get_available_moves_in_board(board)
    if len(moves)==9:
        return choices[randint(0,len(choices)-1)]
    elif len(moves)==0:
        return -1,-1
    choices=[]
    for move in moves:
        board.table[move[0]][move[1]]=game_turn
        if game_turn==X:
            new_turn=O
        else:
            new_turn=X
            
        val=alpha_beta_pruning(board,get_game_status(board),-2,2,new_turn)
        board.table[move[0]][move[1]]=""
        if val>a:
            a=val
            choices=[move]
        elif val==a:
            choices.append(move)
    return choices[randint(0,len(choices)-1)]
    