import pygame as pg
import random
from numpy import array

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



board = []
fnt = pg.font.Font('font.otf',70)

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
                board[i][j].hoverDraw()

def drawGridLines():
    for i in range(1,9):#iterate columns
        if i%3 == 0:
            pg.draw.line(win,(34,40,49),(i*60,0),(i*60,540),2)
    
    for i in range(1,9):#iterate rows
        if i%3 == 0:
            pg.draw.line(win,(34,40,49),(0,i*60),(540,i*60),2)


'''
def generateGame():
    xpos = [x for x in range(0,9)]
    ypos = [x for x in range(0,9)]
    for i in range(9):
        x,y = (random.choice(xpos),random.choice(ypos))
        xpos.remove(x)
        ypos.remove(y)
        val = random.randint(1,9)
        board[x][y].val = val
generateGame()
'''

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
        

def drawOnWindow():
    drawBoard()
    drawGridLines()
    drawSideButs()


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

        




def solve(board):
    empty = getNextEmptyBox(board)
    if empty == -1:
        return board
    else:
        x,y = empty
        for n in range(1,10):
            board[x][y].val = n
            if isSafe(x,y,n,board):
                end = solve(board)
                if end == -1:
                    pass
                elif type(end) == list:
                    return end
            board[x][y].val = 0
        return -1





select = 1

run = True
solving = False
while run:
    win.fill((238,238,238))
    drawOnWindow()
    if solving:
        board = solve(board)
        solving = False
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.MOUSEBUTTONDOWN:
            if type(mouseOnSide()) == int:
                select = mouseOnSide() + 1
            elif type(mouseOnBoard()) == tuple and event.button == 1:
                i,j = mouseOnBoard()
                board[i][j].val = select
                print(isSafe(i,j,select,board))
            elif type(mouseOnBoard()) == tuple and event.button == 3:
                i,j = mouseOnBoard()
                board[i][j].val = 0 
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_s:
                with open('samples.txt','a') as f:
                    for i in board:
                        f.write(str([(c.x,c.y,c.val) for c in i])+'\n')
            if event.key == pg.K_l:
                board = loadGame()
            if event.key == pg.K_a:
                solving = True
                
    if solving:
        show = fnt.render('Solving..',True,(152, 235, 52))
        pg.draw.rect(win,(0,173,181),(0,210,540,65))
        win.blit(show,(50,210))
                
    pg.display.update()

pg.quit()
