
# https://stackoverflow.com/questions/717725/understanding-recursion

import math
from operator import itemgetter, attrgetter
import pygame
import sys
import time
import argparse

pygame.font.init()
class Helper:
    def isValid(self,row,col,num,board):
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
    def getPotentialValuesForEachSquare(self,board):
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
                        if (self.isValid(row,col,num,board)):
                            squares[col+row*9].append(num)

        return squares


    def getRemainingSquares(self,board):
        squares = []
        for row in range(len(board)):
            for  col in range(len(board)):
                if board[row][col] == 0:
                    squares.append((row,col))
            
        return squares

    def getDegree(self,board, row, col, values):

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


class Grid:
    # board = \
    # [[8, 0, 0, 0, 0, 0, 0, 0, 0],
    #  [0, 0, 3, 6, 0, 0, 0, 0, 0],
    #  [0, 7, 0, 0, 9, 0, 2, 0, 0],
    #  [0, 5, 0, 0, 0, 7, 0, 0, 0],
    #  [0, 0, 0, 0, 4, 5, 7, 0, 0],
    #  [0, 0, 0, 1, 0, 0, 0, 3, 0],
    #  [0, 0, 1, 0, 0, 0, 0, 6, 8],
    #  [0, 0, 8, 5, 0, 0, 0, 1, 0],
    #  [0, 9, 0, 0, 0, 0, 4, 0, 0]]
    # This grid above will take like forever........ Need to improve my algorithm 
    board=   \
              [ [0, 6, 0, 8, 0, 0, 0, 0, 0],
              [0, 0, 4, 0, 6, 0, 0, 0, 9],
              [1, 0, 0, 0, 4, 3, 0, 6, 0],
              [0, 5, 2, 0, 0, 0, 0, 0, 0],
              [0, 0, 8, 6, 0, 9, 3, 0, 0],
              [0, 0, 0, 0, 0, 0, 5, 7, 0],
              [0, 1, 0, 4, 8, 0, 0, 0, 5],
              [8, 0, 0, 0, 1, 0, 2, 0, 0],
              [0, 0, 0, 0, 0, 5, 0, 4, 0] ]
    
    def __init__(self, rows, cols, width, height, win):
        self.rows = rows
        self.cols = cols
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.model = None
        self.update_model()
        self.selected = None
        self.win = win
        self.helper = Helper()

    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]


    def draw(self):
        # Draw Grid Lines
        gap = self.width / 9
        for i in range(self.rows+1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(self.win, (0,0,0), (0, i*gap), (self.width, i*gap), thick)
            pygame.draw.line(self.win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)

        # Draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(self.win)
        
    def sudokuSolver_1(self):
        
        empty_squares = self.helper.getRemainingSquares(self.model)
        if (not len(empty_squares)):
            return True
        
        potentialValues = self.helper.getPotentialValuesForEachSquare(self.model)

        (row,col) = empty_squares[0]
        values = potentialValues[col+row*9]
        for num in values:
            # print(num)
            if not self.helper.isValid(row,col,num,self.model):
                continue
            self.model[row][col] = num
            self.cubes[row][col].set(num)
            self.cubes[row][col].draw_change(self.win, True)
            self.update_model()
            pygame.display.update()
            pygame.time.delay(100)
            if (self.sudokuSolver_1()):
                return True

            self.model[row][col] = 0
            self.cubes[row][col].set(0)
            self.update_model()
            self.cubes[row][col].draw_change(self.win, False)
            pygame.display.update()
            pygame.time.delay(100)
        
        return False

    def sudokuSolver_3(self):
        empty_squares = self.helper.getRemainingSquares(self.model)
        if (not len(empty_squares)):
            return True
        potentialValues = self.helper.getPotentialValuesForEachSquare(self.model)

        mrv = []
        minimum = sys.maxsize

        for square in empty_squares:
            curr_len = len(potentialValues[square[1]+square[0]*9])
            if curr_len < minimum:
                minimum =  curr_len
            mrv.append ([len(potentialValues[square[1]+square[0]*9]), (square[0],square[1])])


        max_degree = 0
        for mrv_square in mrv:
            if mrv_square[0] == minimum:
                curr_degree = self.helper.getDegree(self.model,mrv_square[1][0], mrv_square[1][1], potentialValues)
                if curr_degree > max_degree:
                    (row,col) = (mrv_square[1][0], mrv_square[1][1])
                
    
        
        values = potentialValues[col+row*9]
        for num in values:
            if not self.helper.isValid(row,col,num,self.model):
                continue
            self.model[row][col] = num
            self.cubes[row][col].set(num)
            self.cubes[row][col].draw_change(self.win, True)
            self.update_model()
            pygame.display.update()
            pygame.time.delay(50)
            if (self.sudokuSolver_3()):
                return True

            self.model[row][col] = 0
            self.cubes[row][col].set(0)
            self.update_model()
            self.cubes[row][col].draw_change(self.win, False)
            pygame.display.update()
            pygame.time.delay(50)
        
        return False


class Cube:
    def __init__(self, value, row, col, width, height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, win):
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, (128,128,128))
            win.blit(text, (x+5, y+5))
        elif not(self.value == 0):
            text = fnt.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))

        if self.selected:
            pygame.draw.rect(win, (255,0,0), (x,y, gap ,gap), 3)

    def draw_change(self, win, g=True):
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap
        pygame.draw.rect(win, (255, 255, 255), (x, y, gap, gap), 0)

        text = fnt.render(str(self.value), 1, (0, 0, 0))
        win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))
        if g:
            pygame.draw.rect(win, (0, 255, 0), (x, y, gap, gap), 3)
        else:
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)

    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val

def redraw_window(win, board, time, strikes):
    win.fill((255,255,255))
    fnt = pygame.font.SysFont("comicsans", 40)
    text = fnt.render("Time: " + format_time(time), 1, (0,0,0))
    win.blit(text, (540 - 160, 560))
    text = fnt.render("X " * strikes, 1, (255, 0, 0))
    win.blit(text, (20, 560))
    board.draw()

def format_time(secs):
    sec = secs%60
    minute = secs//60
    hour = minute//60

    mat = " " + str(minute) + ":" + str(sec)
    return mat

def main():
    if len(sys.argv) < 2:
        print( 'Missing argument')
        print ('Usage: python sudoku.py {a,b}')
        return 

    lvl = sys.argv[1]   
    if lvl != 'a' and lvl != 'b':
        print ('Usage: python sudoku.py {a,b}')
        sys.exit(0)

    
    win = pygame.display.set_mode((540,600))

    pygame.display.set_caption("Sudoku"+" "+ lvl)
    board = Grid(9, 9, 540, 540, win)
    run = True
    strikes = 0

    start = time.time()

    while run:
        play_time = round(time.time() - start)
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if lvl == 'b':
                        board.sudokuSolver_1()
                    if lvl == 'a':
                        board.sudokuSolver_3()
        
        redraw_window(win, board, play_time, strikes)
        pygame.display.update()
      


    


main()

    
                    
                        




            

