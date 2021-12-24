import pygame as pg
import random
from numpy import array
import copy

pg.init()

win = pg.display.set_mode((600,540))
pg.display.set_caption('Sudoku')



class Cell:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.val = 0
        self.rect = pg.Rect(self.x,self.y,60,60)
        self.font = pg.font.Font('font.otf',30)

    def draw(self):
        pg.draw.rect(win,(160,160,160),self.rect,1)
        if self.val != 0:
            show = self.font.render(str(self.val),True,(0,173,181))
            win.blit(show,(self.x+18,self.y+18))
    def hoverDraw(self):
        pg.draw.rect(win,(204,229,255),self.rect)
        pg.draw.rect(win,(160,160,160),self.rect,1)
        if self.val != 0:
            show = self.font.render(str(self.val),True,(0,173,181))
            win.blit(show,(self.x+18,self.y+18))
    def sideDraw(self):
        pg.draw.rect(win,(153,204,255),self.rect)
        # pg.draw.rect(win,(0,0,0),self.rect,2)
        if self.val != 0:
            show = self.font.render(str(self.val),True,(0,173,181))
            win.blit(show,(self.x+18,self.y+18))
    def selectDraw(self):
        pg.draw.rect(win,(255,204,204),self.rect)
        # pg.draw.rect(win,(0,0,0),self.rect,2)
        if self.val != 0:
            show = self.font.render(str(self.val),True,(0,173,181))
            win.blit(show,(self.x+18,self.y+18))
    def copy(self):
        copyobj = Cell(self.x,self.y)
        copyobj.__dict__['val'] = copy.deepcopy(self.val)
        return copyobj



board = []

for i in range(9):
    col = []
    for j in range(9):
        col.append(Cell(i*60,j*60))
    board.append(col)
    col = []

def mouseOnBoard():
    for i in range(9):
        for j in range(9):
            if board[i][j].rect.collidepoint(pg.mouse.get_pos()):
                return (i,j)




def drawBoard():
    for i in range(9):
        for j in range(9):
            if (i,j) != mouseOnBoard():
                board[i][j].draw()
            else:
                if startSolving == False:
                    board[i][j].hoverDraw()
                else:
                    board[i][j].draw()

def drawGridLines():
    for i in range(1,9):#iterate columns
        if i%3 == 0:
            pg.draw.line(win,(34,40,49),(i*60,0),(i*60,540),2)
    
    for i in range(1,9):#iterate rows
        if i%3 == 0:
            pg.draw.line(win,(34,40,49),(0,i*60),(540,i*60),2)



def loadGame():
    board = []
    l = []
    with open('samples.txt','r') as f:
        l = f.readlines()
        l = [eval(a) for a in l]
    col = []
    for i in l:
        for j in i:
            c = Cell(j[0],j[1])
            c.val = j[2]
            col.append(c)
        board.append(col)
        col = []
    return board



sideButs = [Cell(540,60*y) for y in range(9)]
for i in range(1,10):
    sideButs[i-1].val = i

def mouseOnSide():
    for i in range(9):
        if sideButs[i].rect.collidepoint(pg.mouse.get_pos()):
                return i

def drawSideButs():
    for i in sideButs:
        if i.val != select:
            i.sideDraw()
        else:
            i.selectDraw()

pointer = None       

def drawOnWindow():
    global win
    global pointer
    drawBoard()
    drawGridLines()
    if startSolving == False:
        drawSideButs()
    else:
        x,y = win.get_size()
        if x == 600:
            win = pg.display.set_mode((540,540))
    if pointer != None:
        pg.draw.rect(win,(0,200,0),(pointer[0]*60,pointer[1]*60,60,60),3)



def getNextEmptyBox(board):
    for i in range(9):
        for j in range(9):
            if board[i][j].val == 0:
                return (i,j)
    return -1

def getBigBoxes(board):
    board_copy = array(board)
    l = []
    for i in range(3):
        l.append(((board_copy[i*3:(i+1)*3,0:3]).ravel()).tolist())
        l.append(((board_copy[i*3:(i+1)*3,3:6]).ravel()).tolist())
        l.append(((board_copy[i*3:(i+1)*3,6:9]).ravel()).tolist())
    return l
    



def isSafe(x,y,n,board):
    count = 0
    for i in range(9):
        if board[x][i].val == n:
            count += 1   
    for i in range(9):
        if board[i][y].val == n:
            count += 1
    
    boxes = getBigBoxes(board)
    boxes_val = []
    for i in boxes:
        boxes_val.append([x.val for x in i])
    
    for i in range(3):
        if i*3 <= x < (i+1)*3:
            for j in range(3):
                if j*3 <= y < (j+1)*3:
                    box_num = j+i*3

    count += boxes_val[box_num].count(n)    

    if count == 3:
        return True
    else:
        return False

        



prev_states = []
def printBoard(board):
    for i in board:
        print([j.val for j in i])

def createCopy(l):
    c = []
    for i in l:
        c.append([x.copy() for x in i])
    return c


def solve(board,i):
    global pointer 
    empty = getNextEmptyBox(board)
    if empty == -1:
        return board
    else:
        x,y = empty
        pointer = (x,y)
        for n in range(i+1,10):
            board[x][y].val = n
            # printBoard([board[0],])
            if isSafe(x,y,n,board):
                c = createCopy(board)
                c[x][y].val = 0
                prev_states.append((c,n))
                return board
            board[x][y].val = 0
        return -1




select = 1

run = True
ret = None
startSolving = False
backtracked = False
def main():
    global board
    global run
    global select
    global startSolving
    global ret
    while run:
        win.fill((238,238,238))
        drawOnWindow()
        if startSolving:
            if type(ret) == list:
                board = ret[:]    
            if ret == -1:
                ret = solve(*prev_states.pop(-1))
            else:
                if ret == None:
                    ret = solve(board,0)
                else:
                    ret = solve(ret,0)
                    
                
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if startSolving == False:
                    if type(mouseOnSide()) == int:
                        select = mouseOnSide() + 1
                    elif type(mouseOnBoard()) == tuple and event.button == 1:
                        i,j = mouseOnBoard()
                        board[i][j].val = select
                    elif type(mouseOnBoard()) == tuple and event.button == 3:
                        i,j = mouseOnBoard()
                        board[i][j].val = 0 
            if event.type == pg.KEYDOWN:
                if startSolving == False:
                    if event.key == pg.K_s:
                        with open('samples.txt','a') as f:
                            for i in board:
                                f.write(str([(c.x,c.y,c.val) for c in i])+'\n')
                    if event.key == pg.K_l:
                        board = loadGame()
                    if event.key == pg.K_a:
                        startSolving = True



        pg.display.update()

    pg.quit()

main()
