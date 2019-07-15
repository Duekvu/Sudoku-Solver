
# https://github.com/dimitri/sudoku
# https://stackoverflow.com/questions/717725/understanding-recursion

"""
             [[0, 3, 0, 0, 8, 0, 0, 0, 6],
              [5, 0, 0, 2, 9, 4, 7, 1, 0],
              [0, 0, 0, 3, 0, 0, 5, 0, 0],
              [0, 0, 5, 0, 1, 0, 8, 0, 4],
              [4, 2, 0, 8, 0, 5, 0, 3, 9],
              [1, 0, 8, 0, 3, 0, 6, 0, 0],
              [0, 0, 3, 0, 0, 7, 0, 0, 0],
              [0, 4, 1, 6, 5, 3, 0, 0, 2],
              [2, 0, 0, 0, 4, 0, 0, 6, 0]]

"""

import math
from operator import itemgetter, attrgetter
import sys
import time

def isValid(row,col,num,board):
    # Check row
    for i in range(len(board)):
        if num == board[row][i]:
            return False

    # Check Column
    for i in range(len(board)):
        if num == board[i][col]:
            return False
    

    # Check sub-boards
    curr_row = math.floor (row / 3)
    curr_col = math.floor (col / 3)

    curr_row *= 3
    curr_col *= 3

    for i in range (3):
        for j in range (3):
            if num == board[i+curr_row][j+curr_col]:
                return False

    return True

# Get the potential values for each row and column
def getPotentialValuesForEachSquare(board):
    """
        rtype: list[set]
    """
    squares = []
    for i in enumerate(range(81)):
        squares.append([0])
    for row in range(len(board)):
        for col in range(len(board)):
            if board[row][col] == 0:
                for num in range (1,10):
                    if (isValid(row,col,num,board)):
                        squares[col+row*9].append(num)

    return squares


def getRemainingSquares(board):
    squares = []
    for row in range(len(board)):
        for  col in range(len(board)):
            if board[row][col] == 0:
                squares.append((row,col))
    
    return squares

def getDegree(board, row, col, values):

    # check Column:
    degree = 0
    for i in range (len(board)):
        for val in values[col+row*9]:
            if val == board[row][i]:
                degree+=1

            if val == board[i][col]:
                degree+=1
            

    # Check sub-boards
    curr_row = math.floor (row / 3)
    curr_col = math.floor (col / 3)

    curr_row *= 3
    curr_col *= 3

    for i in range (3):
        for j in range (3):
            for val in values[col+row*9]:
                if val == board[i+curr_row][j+curr_col]:
                    degree+=1

    return degree


def sudokuSolver_1(board):
    empty_squares = getRemainingSquares(board)
    if (not len(empty_squares)):
        return True
    
    potentialValues = getPotentialValuesForEachSquare(board)


    # mrv = []

    # for square in empty_squares:
    #     mrv.append ([len(potentialValues[square[1]+square[0]*9]), (square[0],square[1])])

    # mrv = sorted(mrv,key=itemgetter(0))
    
  
    # (row,col) = mrv[0][1] # always pick the first one in the list

    (row,col) = empty_squares[0]
    values = potentialValues[col+row*9]
    for num in values:
        # print(num)
        if not isValid(row,col,num,board):
            continue
        board[row][col] = num
        if (sudokuSolver_2(board)):
            return True

        board[row][col] = 0
    
    return False



def sudokuSolver_2(board):
    empty_squares = getRemainingSquares(board)
    if (not len(empty_squares)):
        return True
    potentialValues = getPotentialValuesForEachSquare(board)
    mrv = []

    for square in empty_squares:
        mrv.append ([len(potentialValues[square[1]+square[0]*9]), (square[0],square[1])])

    mrv = sorted(mrv,key=itemgetter(0))
    
  
    (row,col) = mrv[0][1] # always pick the first one in the list

        
    values = potentialValues[col+row*9]
    for num in values:
        # print(num)
        if not isValid(row,col,num,board):
            continue
        board[row][col] = num
        if (sudokuSolver_2(board)):
            return True

        board[row][col] = 0
    
    return False

def sudokuSolver_3(board):
    empty_squares = getRemainingSquares(board)
    if (not len(empty_squares)):
        return True
    potentialValues = getPotentialValuesForEachSquare(board)

    mrv = []
    minimum = sys.maxsize

    for square in empty_squares:
        curr_len = len(potentialValues[square[1]+square[0]*9])
        if curr_len < minimum:
            minimum =  curr_len
        mrv.append ([len(potentialValues[square[1]+square[0]*9]), (square[0],square[1])])

    # mrv = sorted(mrv,key=itemgetter(0))
    # TODO: use the heuristic to break tie. 

    max_degree = 0
    for mrv_square in mrv:
        if mrv_square[0] == minimum:
            curr_degree = getDegree(board,mrv_square[1][0], mrv_square[1][1], potentialValues)
            if curr_degree > max_degree:
                (row,col) = (mrv_square[1][0], mrv_square[1][1])
            
   
    
    values = potentialValues[col+row*9]
    for num in values:
        if not isValid(row,col,num,board):
            continue
        board[row][col] = num
        if (sudokuSolver_3(board)):
            return True

        board[row][col] = 0
    
    return False

                  
def run():
    grid=   [ [0, 6, 0, 8, 0, 0, 0, 0, 0],
              [0, 0, 4, 0, 6, 0, 0, 0, 9],
              [1, 0, 0, 0, 4, 3, 0, 6, 0],
              [0, 5, 2, 0, 0, 0, 0, 0, 0],
              [0, 0, 8, 6, 0, 9, 3, 0, 0],
              [0, 0, 0, 0, 0, 0, 5, 7, 0],
              [0, 1, 0, 4, 8, 0, 0, 0, 5],
              [8, 0, 0, 0, 1, 0, 2, 0, 0],
              [0, 0, 0, 0, 0, 5, 0, 4, 0] ]
    
    start_time = time.time()
    if (sudokuSolver_3(grid)):
        print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in grid]))
    else:
        print("can't find the solution")

    print ("It took", time.time() - start_time, "seconds to solve this puzzle.")


    


run()

    
                    
                        




            

