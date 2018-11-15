import numpy as np
from sense_hat import SenseHat
import time
import random

#if the snake encounter the reward
def appleOnMe(board, tail, x,y):
    if board[x][y] == A:
        appleIsOnBoard = False
        while not appleIsOnBoard:
          x_gen = random.randint(0,7)
          y_gen = random.randint(0,7)
          if board[x_gen][y_gen] == O:
            appleIsOnBoard = True
        board[x_gen][y_gen] = A
        return True
    return False


#check if the snake hit the border or himself
def checkLoose(board, x, y):
    if x < 0 or x >= 8:
        return True
    if y < 0 or y >= 8:
        return True
    
    if board[x][y] == C:
        return True
    return False

#move the snake in the board matrice
def moveSnake(board, x, y, tail, direction):
    #2:LEFT 3:RIGHT 1:UP 0:DOWN
    board[x][y] = O
    x_to_add = 0
    y_to_add = 0
    counter = 0

    if direction == 0:
        x_to_add += 1
    elif direction == 1:
        x_to_add -= 1
    elif direction == 2:
        y_to_add -= 1
    elif direction == 3:
        y_to_add += 1

    x += x_to_add
    y += y_to_add

    run = not checkLoose(board,x,y)
    if run:
        if appleOnMe(board,tail, x,y):
            counter+=1
            board[x-x_to_add][y-y_to_add] = C
            tail.insert(0, (x - x_to_add, y - y_to_add))
        else:

            if len(tail)>0:
                board[x-x_to_add][y-y_to_add] = C
                x_temp, y_temp = tail.pop()
                board[x_temp][y_temp] = O
                if len(tail)>0:
                    x_temp, y_temp = tail[len(tail)-1]
                    board[x_temp][y_temp] = C
                tail.insert(0,(x - x_to_add,y- y_to_add))
        board[x][y] = X
    return run, counter, x, y

def draw(board):
  board1D = np.array(board).reshape((64,3)).tolist()
  sense.set_pixels(board1D)
  
  

sense = SenseHat()

# --------- Color -------
X = [255, 0, 0]  # Red
C = [0, 255, 0] # Body  Green
O = [255, 255, 255] # Background White
A = [0, 0, 255] # Blue Apple

#Board Game
board = []
for x in range(8):
  line = []
  for y in range(8):
    line.append(O)
  board.append(line)
    

#The head of the snake is initiated to x:0 y:0 (to randomize)
board[0][0] = X
x = 0
y = 0

#The list of the snake body (used to move the snake)
tail = []
score = 0

#Initiate the reward (to randomize)
board[4][5] = A

 #2:LEFT 3:RIGHT 1:UP 0:DOWN
#Initiate the direction (to randomize)
direction = 3

run = True
while run:
  
  draw(board)
  time.sleep(0.4)
  for event in sense.stick.get_events():
    if event.action == "released":
      if event.direction == "up":
        direction = 1
      elif event.direction == "down":
        direction = 0
      elif event.direction == "right":
        direction = 3
      elif event.direction == "left":
        direction = 2
  run, score_to_add, x, y = moveSnake(board, x, y, tail, direction)
  score += score_to_add


if score == 4 and direction == 3:
  sense.show_message("EASTER EGG")
else:
  sense.show_message("GAME OVER")