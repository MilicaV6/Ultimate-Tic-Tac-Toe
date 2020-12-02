from random import *
from config import *
import math
import sys
import copy

def choose_board(boards_dict, opponent_move):
    if(opponent_move==(-1,-1)):
        return boards_dict[4]

def move(current_board,board_state,opponent_move,flag,boards_dict,opp_block,boards):
    if(opponent_move== (-1,-1)):
        current_board=boards[1][1]
        return (1,1)
    mark=flag
    other=getOpp(flag)
    #possible_cells=get_valid_cells(current_board,board_state,opponent_move,boards_dict,opp_block,boards)
    possible_cells=( get_available_moves_in_board(current_board,boards_dict,board_state))
    shuffle(possible_cells)
   
    idx=possible_cells[0]
    best_value=-math.inf
    depth=0
    node_count=0
    while best_value!=math.inf and node_count<10000:
        depth+=1
        best_value=-math.inf
        for cell in possible_cells:
            bstat=board_state[:]
            update_board_stat(current_board,bstat,cell,flag,boards_dict)
            temp=alpha_beta(current_board,bstat,depth,-math.inf,math.inf,True,cell,node_count,boards_dict,opp_block,boards,flag)
            if temp>best_value:
                best_value=temp
                idx=cell
            current_board.table[cell[0]][cell[1]]=""
            #board_state[(get_key(boards_dict,current_board))]=None
        my_move=idx
        return my_move
       
def getOpp( flag):
        if flag == X:
            return O
        return X
def update_board_stat(board_game,board_stat,move,flag,boards_dict):
    board_game.table[move[0]][move[1]] = flag
    block_no = get_key(boards_dict,board_game)
    row = move[0]
    column = move[1]
    is_done = 0
    prev_block=None
    #board.table[move[0]][move[1]]=flag
    status=check_small_board_win(board_game)
    if board_stat[block_no] == None:
        if status==X:
            is_done=1
            #board_state[get_key(boards_dict,board)]=X
        elif status==O:
            is_done=1
            #get_key(boards_dict,board)]=O
        if is_done:
            prev_block=board_stat[block_no]
            board_stat[block_no] = flag
        empty_cells = []
        for i in range(3):
            for j in range(3):
                if board_game.table[i][j] == "":
                    empty_cells.append((i, j))
        if len(empty_cells) == 0 and not is_done:
            prev_block=board_stat[block_no]
            board_stat[block_no] = STATUS_DRAW
    return 
   
    
        

def get_key(dict,val): 
        for key, value in dict.items(): 
            if val == value: 
                return key 
    
        return "key doesn't exist"
def score(game_state):
    if game_state==O:
        return math.inf
    elif game_state==X:
        return -math.inf
    else:
        return 0

def get_game_score(game_state,mark):
    tree_matrix=getTreeMatrix()
    for i in tree_matrix:
        aivount=0
        plcount=0
        for j in i :
            if game_state[j]==mark:
                aivount+=1
            elif game_state[j]==getOpp(mark):
                plcount+=1
        if aivount==3:
            return math.inf
        elif plcount==3:
            return -math.inf
    return 0



#def remove_dangerous_cells(opp_block,)

def getEmptyCells( gameBoard, blocksAllowed, blockStat,boards,boards_dict):
        cells = []
        for block in blocksAllowed:
            
            for k in range(3):
                for l in range(3):
                    if(gameBoard.table[k][l] == "" and boards_dict[block]==boards[k][l]):
                        cells.append((k,l))

        if cells == []:
            block = [0,1,2,3,4,5,6,7,8]
            blocksAllowed = []
            for i in block:
                if blockStat[i]==None:
                    blocksAllowed.append(i)

            for block in blocksAllowed:
               
                for k in range(3):
                    for l in range(3):
                        if(gameBoard.table[k][l] == ""):
                            cells.append((k,l))

        return cells


def get_blocks_from_cells(move_by_opponent,current_board_game,boards_dict,board_stat):
    row, column = move_by_opponent[0], move_by_opponent[1]
    valid_blocks = []
    if row == 0 and column == 0:
        valid_blocks = [0, 1, 3]
    elif row == 0 and column == 2:
        valid_blocks = [1, 2, 5]
    elif row == 2 and column == 0:
        valid_blocks = [3, 6, 7]
    elif row == 2 and column == 2:
        valid_blocks = [5, 7, 8]
    else:
        valid_blocks = [3 * row + column]

    valid_cells = []
    for i in valid_blocks:
        if board_stat[i] != None:
            continue
        
        for j in range(3):
            for k in range(3):
                if current_board_game.table[j][k] == None:
                    valid_cells.append((j,k))
    if len(valid_cells) == 0:
        for i in range(3):
            for j in range(3):
                if get_key(boards_dict,current_board_game) == None and current_board_game.table[i][j] == "":
                    valid_cells.append((i, j))

    easy_move = []
    for i in valid_cells:
        if board_stat[(i[0]%3) * 3 + i[1]%3] != None:
            valid_cells.remove(i)
            easy_move.append(i)
    if len(valid_cells) == 0:
        valid_cells = easy_move
    shuffle(valid_cells)
    return valid_cells

def determine_next_board(move,boards):
    available_boards=[]
    for i in range (3):
        for j in range (3):
            if(i==move[0] and j== move[1] and boards[i][j].winner==None ):
                return boards[i][j]
            elif boards[i][j].winner==None:
                available_boards.append(boards[i][j])

    return available_boards[randint(0,len(available_boards)-1)]
    


def alpha_beta(board_game,game_state,depth,alpha,beta,flag,node,node_count,boards_dict,opp_block,boards,mark):
    node_count+=1
    
   
    if is_terminal(game_state,board_game,boards_dict):
        return get_game_score(game_state,mark)
    if depth==0:
        return get_heuristic_value(board_game,game_state,mark,boards_dict)
    next_block=determine_next_board(node,boards)
    children=get_available_moves_in_board(next_block,boards_dict,game_state)
    #children=get_blocks_from_cells(node,board_game,boards_dict,game_state)
    if flag:
        val=-math.inf
        for child in children:
            new_board_stat=game_state[:]
            update_board_stat(next_block,new_board_stat,child,mark if flag else getOpp(mark),boards_dict)
            val=max(val,alpha_beta(next_block,new_board_stat,depth-1,alpha,beta,False,child,node_count,boards_dict,opp_block,boards,mark))
            
            alpha=max(alpha,val)
            next_block.table[child[0]][child[1]]=""
            if beta<=alpha:
                break
        return val
    else:
        val=math.inf
        for child in children:
            new_board_stat=game_state[:]
            update_board_stat(next_block,new_board_stat,child,mark if flag else getOpp(mark),boards_dict)
            val=min(val,alpha_beta(next_block,new_board_stat,depth-1,alpha,beta,True,child,node_count,boards_dict,opp_block,boards,getOpp(mark)))
            beta=min(beta,val)
            next_block.table[child[0]][child[1]]=""
            if beta<=alpha:
                break
        return val
     


def is_terminal(game_state,board_game,boards_dict):
    for i in range(9):

        if(game_state[i]==None):
            return False
    return True





def heuristic2(board_game,board_stat,mark,boards,boards_dict):
        finalHeuristic = H = 0
        wins = losses = blanks = bonus = 0
        row=0
        col=0
        for i in range(3):
            for j in range(3):
                if board_game==boards[i][j]:
                    row=i
                    col=j
        xlist=[]
        for i in range(3):
            for j in range(3):
               xlist.append((i,j))
        blockbonus=0
        winnigcombs=getTreeMatrix()
        for combination in winnigcombs:
            wins=losses=blanks=bonus=0
            for j in combination:
                r=xlist[j][0]
                c=xlist[j][1]
                if board_stat[r][c]==mark:
                    wins+=1
                    if r and c in (1,4,7):
                        bonus=get_middle_cell_bonus()
                elif board_stat[r][c]==None:
                    blanks+=1
                else:
                    losses+=1

            if wins == 1 and losses == 2:
                bonus += 10
            H += self.heuristicMatrix[wins][losses] + bonus
        return H


        

def get_heuristic_value(board_game,game_state,mark,boards_dict):
    heuristic=0
    heuristic_matrix=getHeuristicMatrix()
    threematrix=getTreeMatrix()
    for i in threematrix:
        aicount=0
        plcount=0
        for j in i:
            if game_state[j]==mark:
                aicount+=1
            elif game_state[j]==getOpp(mark):
                plcount+=1
        heuristic+=100*heuristic_matrix[aicount][plcount]
    for i in range(3):
        for j in range(3):
    
            if(game_state[3 * i + j])!=None:
                continue
            for three in threematrix:
                aicount=0
                plcount=0
                for idx in three:
                   
                    if(boards_dict[idx].table[i][j]==mark):
                        aicount+=1
                    elif board_game.table[i][j]==getOpp(mark):
                        plcount+=1
                    
                        
            heuristic+=heuristic_matrix[aicount][plcount]
    return heuristic



def check_big_board_status(boards):
    draw_count=0
    
    #checking if game is horizontaly or verticaly compete?
    for i in range(3):
        x_count_hor=x_count_ver=o_count_hor=o_count_ver=0
        for j in range(3):
            check_small_board_win(boards[i][j])
            if boards[i][j].winner==X:
                x_count_hor+=1
            elif boards[i][j].winner==O:
                o_count_hor+=1
            if boards[j][i].winner==X:
                x_count_ver+=1
            elif boards[j][i].winner==O:
                o_count_ver+=1
            if boards[i][j].winner==None:
                draw_count+=1
                
        if x_count_ver==3 or x_count_hor==3:
            return X
        elif o_count_hor==3 or o_count_ver==3:
            return O
        
    #checking if game is diagonaly complete.
    x_d1_count=x_d2_count=o_d1_count=o_d2_count=0
    for i in range(3):
        check_small_board_win(boards[i][i])
        #main diagonal
        if boards[i][i].winner==X:
            x_d1_count+=1
        elif boards[i][i].winner==O:
            o_d1_count+=1
        #back diagonal
        check_small_board_win(boards[i][3-i-1])
        if boards[i][3-i-1].winner==X:
            x_d2_count+=1
        elif boards[i][3-i-1].winner==O:
            o_d2_count+=1
            
    if x_d1_count==3 or x_d2_count==3:
        return X
    elif o_d1_count==3 or o_d2_count==3:
        return O
    
    #check if game is draw
    if draw_count==0:
        return STATUS_DRAW
   
    return None

def get_boards_states(boards):
    game_states=[]
    check_big_board_status(boards)
    for i in range(3):
        for j in range(3):
            if boards[i][j].winner==X:
                game_states.append(X)
            elif boards[i][j].winner==O:
                game_states.append(O)
            elif boards[i][j].winner==STATUS_DRAW:
                game_states.append(STATUS_DRAW)

            else:
                game_states.append(None)
    return game_states

def check_small_board_win(board):
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
            board.winner=X
            return X
        elif o_count_hor==3 or o_count_ver==3:
            board.winner=O
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
        board.winner=X
        return X
    elif o_d1_count==3 or o_d2_count==3:
        board.winner=O
        return O
    
    #check if game is draw
    if draw_count==0:
        board.winner=STATUS_DRAW
        return STATUS_DRAW
    board.winner=None
    return None

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
   
    return None

def get_available_moves_in_board(board,boards_dict,blockStat):
    moves=[]
    for i in range(3):
        for j in range(3):
            if board.table[i][j]=="" and board.winner==None:
                moves.append((i,j))

    if moves == []:
            block = [0,1,2,3,4,5,6,7,8]
            blocksAllowed = []
            for i in block:
                if blockStat[i]==None:
                    blocksAllowed.append(i)

            for block in blocksAllowed:
               
                for k in range(3):
                    for l in range(3):
                        if(boards_dict[block].table[k][l] == ""):
                            moves.append((k,l))
    return moves



    
def getHeuristicMatrix():
    return [[0,-10,-100,-1000],[10,0,0],[100,0,0],[1000]]
def getTreeMatrix():
    return [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
def get_outher_block_weight():
    return 100
def get_middle_cell_bonus():
    return 5