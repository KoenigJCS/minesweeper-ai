import pygame
import ctypes
import random
from array import *

from pygame.event import wait

pygame.init()

white = (255,255,255)
black = (0,0,0)

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
purple = (255,0,255)
gray = (100,100,100)

run = False

def makeScreen(y, x, scale, mineAr):
    gameDisplay = pygame.display.set_mode((x*scale,y*scale))
    gameDisplay.fill(black)
    pygame.display.set_caption('Minesweener')
    for row in range (0,x):
            for col in range (0, y):
                #if mineAr[col][row] == 1:
                #    pygame.draw.rect(gameDisplay, red, ((row*scale,col*scale),(row*scale+scale,col*scale+scale)))
                #else:
                #   pygame.draw.rect(gameDisplay, green, ((row*scale,col*scale),(row*scale+scale,col*scale+scale)))
                pygame.draw.rect(gameDisplay, gray, ((row*scale,col*scale),(row*scale+scale,col*scale+scale)))
                if row == x-1:
                    pygame.draw.line(gameDisplay, black, (0, col*scale),(x*scale, col*scale), 1)
            pygame.draw.line(gameDisplay, black, (row*scale, 0),(row*scale, y*scale), 1)
    pygame.draw.line(gameDisplay, black, (0, y*scale),(x*scale, y*scale), 1)
    pygame.draw.line(gameDisplay, black, (x*scale, 0),(x*scale, y*scale), 1)
    return gameDisplay


def mineArray(r,c,dif):
    maxMines = round((r*c*dif)/20)
    mines = [[0]*c for row in range(r)]
    while maxMines > 0:
        randR = round(random.random()*(r-1))
        randC = round(random.random()*(c-1))
        if (mines[randR][randC] == 0):                  
                mines[randR][randC] = 1
                maxMines -= 1
                
    return mines

def checkAround(r, c, mines):
    count = 0
    searchX = [-1,2]
    searchY = [-1,2]

    if(r == 0):
        searchX[0] = 0
    if(r == len(mines)-1):
        searchX[1] = 1
    if(c == 0):
        searchY[0] = 0
    if(c == len(mines[r])-1):
        searchY[1] = 1
    for rowS in range(searchX[0],searchX[1]):
                for colS in range(searchY[0],searchY[1]):
                    if mines[r+rowS][c+colS] == 1:
                        count += 1
    return count

def checkZeroRadius(r,c,scale, gameDisplay, mines, x, y):
    searchX = [-1,2]
    searchY = [-1,2]

    if(r == 0):
        searchX[0] = 0
    if(r == len(mines)-1):
        searchX[1] = 1
    if(c == 0):
        searchY[0] = 0
    if(c == len(mines[r])-1):
        searchY[1] = 1
    for rowS in range(searchX[0],searchX[1]):
            for colS in range(searchY[0],searchY[1]):
                if (not rowS==r) and (not colS==c) and (not mines[r][c]==-1):
                    checkCell(scale, gameDisplay, mines, x+scale*rowS,y+scale*colS)

def checkCell(scale, gameDisplay, mines, x, y):
    font = pygame.font.Font('freesansbold.ttf', round(scale/2))
    row = round(x//scale)
    col = round(y//scale)
    mineColorArray = [black,(0,0,255),(0,255,0),(255,127,0),(255,255,0),(255,255,255),(0,127,127),(255,0,255),(255,0,0)]
    neighbors = checkAround(col,row, mines)
    numb = str(neighbors)
    color = mineColorArray[neighbors]
    if mines[col][row] == 1:
        color = black
        numb = 'X'
    else:
        mines[col][row]=-1
    #if neighbors == 0:
    #    checkZeroRadius(row,col,scale, gameDisplay, mines, x, y)
    pygame.draw.rect(gameDisplay, (200,200,200), ((row*scale+1,col*scale+1),(scale-1,scale-1)))
    text = font.render(numb, True, color)
    textRect = text.get_rect()
    textRect.center = ((row*scale)+(scale//2), (col*scale)+(scale//2))
    gameDisplay.blit(text, textRect)


def start():
    rows = int(input("How many Rows:\n"))
    coll = int(input("How many Collums:\n"))
    dificulty = int(input("Say your dificulty from 1 to 10:\n"))
    if(rows<1 or coll<1 or dificulty<1 or dificulty>10):
        rows = 10
        coll = 10
        dificulty = 5
    user32 = ctypes.windll.user32
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    scale = 1
    if rows > coll:
        scale = (screensize[1]*.8)//rows
    else:
        scale = (screensize[1]*.8)//coll
    mineAr = mineArray(rows,coll,dificulty)
    gameScr = makeScreen(rows,coll,scale,mineAr)
    run = True
    d=(0,0,0)
    while run:
        mouse_pos = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
                quit()

        pygame.display.update()
        if mouse_buttons[0] and d[0] == 0:
            d=(1,mouse_pos[0],mouse_pos[1])
        if not mouse_buttons[0] and round(abs(d[1]-mouse_pos[0])*2//scale) == 0 and round(abs(d[2]-mouse_pos[1])*22//scale) == 0 and d[0]==1:
            checkCell(scale, gameScr, mineAr,d[1],d[2])
            d=(0,0,0)
        elif mouse_buttons[0] == False:
            d=(0,0,0)
    

    

start()


