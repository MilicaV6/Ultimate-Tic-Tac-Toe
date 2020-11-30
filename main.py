from game import *
from game import Board
from ai import *
from tkinter import *
from config import *
import time


root=Tk()
root.geometry("700x700+0+0")

boards=[[None for j in range(3)]for i in range(3)]
active_boards=boards
class Application:
    first_gamer_turn=None
    gamer_turn=None
    computer_turn=None
    label_names=[]
    def __init__(self,master):
        frame=Frame(master,width=750,height=750,bg="dark red")
        frame.grid()
        k=0
       
        for i in range(3):
           
            for j in range(3):
                board=Board(frame,i,j)
                board.frame.grid()
                boards[i][j]=board
                print(board.frame)
                label_name=[]
                for k in range (3):
                    row=[]                   
                    for l in range (3):
                        board.cells[k][l].button.bind("<Button-1>",self.gamer_turn)
             
        Application.first_gamer_turn=messagebox.askyesno("Who wants to start?","Do you want to start first?")       
        Application.gamer_turn=True if Application.first_gamer_turn else False
        Application.computer_turn=False if Application.first_gamer_turn else True

        if Application.first_gamer_turn==False:
            self.ai_turn(boards[randint(0,8)][randint(0,8)])
        
        master.mainloop()
   

    def gamer_turn(self,event):
        if Application.gamer_turn:
            for k in range(3):
                for l in range (3):
                    helper_board=boards[k][l]
            
                    for i in range(3):
                        for j in range (3):
                            
                            if  helper_board.cells[i][j].button==event.widget and  helper_board.table[i][j]=="" and helper_board.cells[i][j].button['state']!=DISABLED :
                                    helper_board.frame.config(bg="yellow")
                                    if Application.first_gamer_turn:
                                        helper_board.table[i][j]=X
                                    else:
                                        helper_board.table[i][j]=O
                                    helper_board.update_board()
                                # root.after(3000, set_enabled(i,j))
                                    set_enabled(i,j)
                                    if helper_board!=boards[i][j]:
                                        helper_board.frame.config(bg="violet")
                                    Application.computer_turn=True
                                    if boards[i][j].winner==None:                                        
                                        self.ai_turn(boards[i][j])
                                    else:
                                        self.ai_turn(determine_board(boards))
                                        




               
    def ai_turn(self,concrete_board):
        if Application.computer_turn:
            if Application.first_gamer_turn:
                move=determine_move(concrete_board,O)
                if move[0]!=-1:
                    concrete_board.table[move[0]][move[1]]=O
            elif Application.first_gamer_turn==False:
                move=determine_move(concrete_board,X)
                if move[0]!=-1:
                    concrete_board.table[move[0]][move[1]]=X
            #self.gamer_turn=True
            concrete_board.update_board()
            set_enabled(move[0],move[1])
            #if concrete_board!=boards[move[0]][move[1]]:
                #concrete_board.frame.config(bg="violet")
            Application.gamer_turn=True

def update_game_board(board):

    board.frame.config(bg="yellow")
    
        

def set_enabled(i,j):
    if boards[i][j].winner==None:
        for k in range(3):
            for l in range (3):
                    if (k!=i or l!=j):
                        temp_board=boards[k][l]
                        for m in range(3):
                            for n in range(3):
                                temp_board.cells[m][n].button.config(state=DISABLED)
                        boards[k][l].frame.config(bg="violet")  
                        temp_board.active=False          
                    elif k==i and l==j:
                        temp_board=boards[k][l]
                        for m in range(3):
                            for n in range(3):
                                temp_board.cells[m][n].button.config(state=NORMAL)
                            
        boards[i][j].frame.config(bg="yellow")
    else:
         for k in range(3):
            for l in range (3):
                    if (k!=i or l!=j):
                        temp_board=boards[k][l]
                        for m in range(3):
                            for n in range(3):
                                temp_board.cells[m][n].button.config(state=NORMAL)
                        temp_board.frame.config(bg="yellow")

g=Application(root)
