import helper
import random


PLAYER_A = "1"
PLAYER_B = "2"
BOTH_WIN = "3"
NO_WINNER = "0"

'''creat a board for a givven number
of rows and columns'''
def init_board(rows, columns):
    board=list()
    for i in range(rows):
        board_row=list()
        for j in range(columns):
            board_row.append(helper.WATER)
        board.append(board_row)
    return board

'''return the respectiv coordinates for a given
name of location '''
def cell_loc(name):
    if len(name)>2 and len(name)<4:
       row=int(name[1])*10+int(name[2])-1
    else:
        row=int(name[1])-1
    if ord(name[0])>96:
        column=ord(name[0])-ord('a')
    else:
        column=ord(name[0])-ord('A')   
    coordinate=(row,column)
    return coordinate


'''check if a givven location is valid 
for placing a givven battleship'''
def valid_ship(board, size, loc):
    if loc[0]<0 or loc[0]>helper.NUM_ROWS:
        return False
    if loc[1]<0 or loc[1]>26:
        return False    
    if loc[0]<=len(board)-size and loc[1]<=len(board[0]):
        for i in range(size):
            if board[loc[0]+i][loc[1]]==helper.WATER:
              continue
            else:
              return False
    else:
        return False
    return True

'''update a givven board 
with a givven location for a ship'''
def update_board(board, size, loc):
        for i in range(size):
            board[loc[0]+i][loc[1]]=helper.SHIP 

'''return the list of available ships for the game'''
def create_ship_sizes(rows,columns):
    return helper.SHIP_SIZES
            
'''generate a board and add ships 
to the locations of the player's choise'''     
def create_player_board(rows, columns,ship_sizes):
    board=init_board(rows,columns)
    ship_num=0
    for size in ship_sizes:
        while 1:
          loc=cell_loc(helper.get_input("choose location for ship in size",str(size)))       
          if loc==None or valid_ship(board, size, loc)==False:                      
             helper.print_board(board)
             print("you enterd invalid location, try again!")
             continue
          else:
            update_board(board, size, loc) 
            ship_num+=1
            if ship_num<len(ship_sizes):
               helper.print_board(board)
            break
    return board

'''generate a board withe ships 
in random locations'''
def create_computer_board(rows, columns,ship_sizes):
    board=init_board(rows,columns)
    locations=list()
    for i in range(rows):
        for j in range(columns):
            locations.append((i,j))
    for size in ship_sizes:
            locations2=list()
            if size<=rows:
             for i in range(rows-size+1):
               for j in range(columns):
                   if (i,j) in locations:
                     locations2.append((i,j))
                   else:
                       continue
             loc=helper.choose_ship_location(board, size, locations2)         
             update_board(board, size, loc)
             for r in range(size):
                   locations.remove((loc[0]+r,loc[1]))
            else:
                continue
    return board

'''update the board acording to the
attacking choise of the player'''
def fire_torpedo(board, loc):
    if board[loc[0]][loc[1]]==helper.SHIP:
        board[loc[0]][loc[1]]=helper.HIT_SHIP
        return board
    elif board[loc[0]][loc[1]]==helper.WATER:
        board[loc[0]][loc[1]]=helper.HIT_WATER
        return board

'''check if the location chosen
for attack is in range and not repetitive'''
def is_torpedo_valid(board,loc):
    if loc[0]<0 or loc[0]>helper.NUM_ROWS:
        print("invalid input, try again! ")
        return False
    if loc[1]<0 or loc[1]>26:
        print("invalid input, try again! ")
        return False
    if loc[0]>len(board) or loc[1]>len(board[0]):
        print("torpedo was out of range!")
        return False
    else:
        return True

'''create a version of the computer's current board 
that only the targets that were hit are visible'''
def make_invisible(board,invisible,rows,columns):
    for i in range(rows):
        for j in range(columns):
            if board[i][j]==helper.HIT_SHIP:
                invisible[i][j]=helper.HIT_SHIP
            if board[i][j]==helper.HIT_WATER:
                invisible[i][j]=helper.HIT_WATER
    
'''update the player's board with
a random attack by the computer'''
def computer_strike(board,invisible,rows,columns):
    locations=list()
    for i in range(rows):
        for j in range(columns):
            if invisible[i][j]==helper.WATER: 
              locations.append((i,j))
    loc=helper.choose_torpedo_target(invisible,locations)
    if board[loc[0]][loc[1]]==helper.SHIP:
        board[loc[0]][loc[1]]=helper.HIT_SHIP
        invisible[loc[0]][loc[1]]=helper.HIT_SHIP
    elif board[loc[0]][loc[1]]==helper.WATER:
        invisible[loc[0]][loc[1]]=helper.HIT_WATER
        board[loc[0]][loc[1]]=helper.HIT_WATER 

'''return the sum of the slots
that all the ships are occupying'''
def ships_down(ship_sizes):
    sum=0
    for size in ship_sizes:
        sum+=size
    return sum

'''check if there is awinner and
return indication accordingly'''
def who_won(board1,board2,rows,columns,ship_sizes):
    sum1=0
    sum2=0
    all_ships=ships_down(ship_sizes)
    for i in range(rows):
        for j in range(columns):
            sum1+=(board1[i][j]==helper.HIT_SHIP)
            sum2+=(board2[i][j]==helper.HIT_SHIP)
    if sum1==all_ships and sum2==all_ships:
        return BOTH_WIN
    elif sum1==all_ships:
        return PLAYER_B
    elif sum2==all_ships:
        return PLAYER_A
    else:
        return NO_WINNER


'''main is managing the game's turns and
display the game's graphics for the player'''
def main():
   while 1:
        rows=helper.NUM_ROWS
        columns=helper.NUM_COLUMNS
        board=init_board(rows,columns)
        helper.print_board(board)
        ship_sizes=create_ship_sizes(rows,columns)
        board1=create_player_board(rows,columns,ship_sizes)
        board2=create_computer_board(rows,columns,ship_sizes)
        invisible1=init_board(rows, columns)
        invisible2=init_board(rows, columns)
        helper.print_board(board1,invisible1)
        while 1:
         while 1:

           loc=cell_loc(helper.get_input("choose where to strike"))
           if is_torpedo_valid(board2,loc):
               break
           else:
               continue
         fire_torpedo(board2, loc)
         make_invisible(board2,invisible2,rows,columns)
         make_invisible(board1,invisible1,rows,columns)
         computer_strike(board1,invisible1,rows,columns)
         status = who_won(board1,board2,rows,columns,ship_sizes)
         if status==NO_WINNER:
            helper.print_board(board1,invisible2)
            continue
         if status==BOTH_WIN:
            helper.print_board(board1,board2)
            answer=helper.get_input("both players won! play again? ")
         else:
            helper.print_board(board1,board2)
            answer=helper.get_input("the winner is player "+status+" play again? ")
         while 1:
            if answer !='Y' and answer !='N':
                answer=helper.get_input("invalid answer, play again? ")
                continue
            else:
                break
         if answer=='Y':
                break
         elif answer=='N':
                return
         else:
                continue
        

    


if __name__ == "__main__":
    main()
    