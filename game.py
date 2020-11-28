from tkinter import*
from tkinter import messagebox
from ai import *
from config import *


def white_board():
    board=[["" for i in range(3)] for i in range (3)]
    return board

def game_over(game_status):
    if game_status==X:
        messagebox.showinfo("Result", "You won! Play again.")
    elif game_status==O:
        messagebox.showinfo("Result", "Computer won. Retry?")
    else:
        messagebox.showinfo("Result","Tie!")
class Cell:
    cell_position=0
    def __init__(self, master,k,l):
        self.frame=Frame(master,height=30,width=30, bg="light gray")
        self.button=Button(self.frame,text="",justify=CENTER, height=1,width=3, font=FONT)
        #self.button['state']=DISABLED
        #if(self.button['state']!=NORMAL):
        #    print("pozdravi")
        self.frame.grid(row=k,column=l,padx=4,pady=4)
        self.button.pack()
        
        self.cell_label="cell"+str(Cell.cell_position)
        self.button_tag=self.button
class Board:
    
   # frame=None
    def __init__(self,master,i,j):
        self.frame=Frame(master,height=100,width=100,bg="violet")
        self.frame.grid(row=i, column=j, padx=3, pady=3)
        
        self.board=white_board()
        self.game_status=STATUS_CONTINUE
        self.grid=[]
        self.cells=[[Cell(self.frame,l,k) for k in range (3)]for l in range(3)]
               
            
    #     #true for user turn
        self.gamer_turn=True
        if not self.gamer_turn:
            self.ai_turn()
        
                    
    def check_if_in_board(self,event):
        for i in range (3):
            for j in range (3):
              #  if self.label_names[i][j]==event.widget:
                    self.frame.config(bg="yellow")
                    return True
    
    def update_board(self):
        for i in range(3):
            for j in range(3):
                self.cells[i][j].button.config(text=str(self.board[i][j]))

        self.game_status=get_game_status(self.board)
        print(self.game_status)
        if self.game_status!=STATUS_CONTINUE:
            game_over(self.game_status)
            self.board=white_board()
            for i in range(3):
                for j in range(3):
                    self.cells[i][j].button.config(text=self.board[i][j])
            self.gamer_turn=messagebox.askyesno("Who wants to start?", "Do you want to start first?")
            if not self.gamer_turn:
                self.ai_turn()                
                
  
            
        
            
        
        

