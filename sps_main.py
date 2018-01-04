import pygame, sys, random
from pygame.locals import *

WINDOWWIDTH = 640
WINDOWHEIGHT = 480
FPS = 30

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BRIGHTBLUE = (0, 50, 255)
DARKTURQUOISE = (3, 54, 73)
GREEN = (0, 204, 0)

BGCOLOR = DARKTURQUOISE
TILECOLOR = GREEN
TEXTCOLOR = WHITE
BOARDCOLOR = BRIGHTBLUE
BASICFONTSIZE = 20
BUTTONCOLOR = WHITE
BUTTONTEXTCOLOR = BLACK
MESSAGECOLOR = WHITE

BOARDWIDTH = 2
BOARDHEIGHT = 2
TILESIZE = 80

XMARGIN = int((WINDOWWIDTH - (TILESIZE * BOARDWIDTH + (BOARDWIDTH - 1))) / 2)
YMARGIN = int((WINDOWHEIGHT - (TILESIZE * BOARDHEIGHT + (BOARDHEIGHT - 1))) / 2)

LEFT = 'left'
RIGHT = 'right'
UP = 'up'
DOWN = 'down'


def checkForQuit():
    for event in pygame.event.get(QUIT):
        terminate()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            terminate()
        pygame.event.post(event)


def terminate():
    pygame.quit()
    sys.exit()


def drawTile(tilex, tiley, number):
    left, top = getLeftTopOfTile(tilex, tiley)
    pygame.draw.rect(DISPLAYSURF, TILECOLOR, (left, top, TILESIZE, TILESIZE))
    textSurf = BASICFONT.render(str(number), True, TEXTCOLOR)
    textRect = textSurf.get_rect()
    textRect.center = left + int(TILESIZE/2) , top + int(TILESIZE/2)
    DISPLAYSURF.blit(textSurf, textRect)

def getLeftTopOfTile(tileX, tileY):
    left = XMARGIN + (tileX * TILESIZE) + (tileX -1)
    top = YMARGIN + (tileY * TILESIZE) + (tileY -1)
    return (left, top)

def makeText(text, color, bgcolor, top, left):
    # create the Surface and Rect objects for some text.
    textSurf = BASICFONT.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)


def drawBoard(board, msg):
    DISPLAYSURF.fill(BGCOLOR)
    if msg:
        textSurf, textRect = makeText(msg, MESSAGECOLOR, BGCOLOR, 5, 5)
        DISPLAYSURF.blit(textSurf, textRect)
    for tilex in range(len(board)):
        for tiley in range(len(board[0])):
            if board[tilex][tiley]:
                drawTile(tilex, tiley, board[tilex][tiley])

    left, top = getLeftTopOfTile(0, 0)
    width = BOARDWIDTH * TILESIZE
    height = BOARDHEIGHT * TILESIZE
    pygame.draw.rect(DISPLAYSURF, BOARDCOLOR, \
                     (left-5, top-5, width+11, height+11), 4)

def getSpotClicked(board, x, y):
    for tileX in range(len(board)):
        for tileY in range(len(board[0])):
            left, top = getLeftTopOfTile(tileX, tileY)
            tileRect = pygame.Rect(left, top, TILESIZE, TILESIZE)
            if tileRect.collidepoint(x, y):
                return (tileX, tileY)
    return (None, None)

def getBlankPosition(board):
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if board[x][y] == None:
                return (x, y)

def isValidMove(board, move):
    blankx , blanky = getBlankPosition(board)
    return (move == UP and blanky != len(board[0]) - 1) or \
           (move == DOWN and blanky != 0) or \
           (move == LEFT and blankx != len(board) -1) or \
           (move == RIGHT and blankx != 0)

def makeMove(board, move):

    blankx, blanky = getBlankPosition(board)

    if move == UP:
        board[blankx][blanky], board[blankx][blanky + 1] =  \
            board[blankx][blanky + 1], board[blankx][blanky]
    elif move == DOWN:
        board[blankx][blanky], board[blankx][blanky - 1] = \
            board[blankx][blanky - 1], board[blankx][blanky]
    elif move == LEFT:
        board[blankx][blanky], board[blankx + 1][blanky] = \
            board[blankx + 1][blanky], board[blankx][blanky]
    elif move == RIGHT:
        board[blankx][blanky], board[blankx - 1][blanky] = \
            board[blankx - 1][blanky], board[blankx][blanky]

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Slide Puzzle')
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)

    board = [[3,2], [1, None]]
    solvedboard = [[1,3], [2, None]]

    while True:
        slideTo = None
        msg = ''
        if board == solvedboard:
            msg = 'Solved'

        drawBoard(board, msg)
        checkForQuit()

        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                spotx, spoty = getSpotClicked(board, event.pos[0], event.pos[1])
                blankx, blanky = getBlankPosition(board)
                if spotx == blankx + 1 and spoty == blanky:
                    slideTo = LEFT
                elif spotx == blankx - 1 and spoty == blanky:
                    slideTo = RIGHT
                elif spotx == blankx and spoty == blanky + 1:
                    slideTo = UP
                elif spotx == blankx and spoty == blanky - 1:
                    slideTo = DOWN
            elif event.type == KEYUP:
                if event.key in (K_LEFT, K_a) and isValidMove(board, LEFT):
                    slideTo = LEFT
                elif event.key in (K_RIGHT, K_d) and isValidMove(board, RIGHT):
                    slideTo = RIGHT
                elif event.key in (K_UP, K_w) and isValidMove(board, UP):
                    slideTo = UP
                elif event.key in (K_DOWN, K_s) and isValidMove(board, DOWN):
                    slideTo = DOWN

        if slideTo:
            makeMove(board, slideTo)

        pygame.display.update()
        FPSCLOCK.tick(FPS)



if __name__ == '__main__':
    main()

