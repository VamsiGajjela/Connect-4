#Vamsi Gajjela

import numpy as np
import pygame
import sys
import math
import time

ROWS = 6
COLUMNS = 7

clock = pygame.time.Clock()
background=pygame.image.load('background.jpg')
#colours
WHITE = (255,255,255)
BLUE = (0,0,190)
YELLOW = (255,255,0)
RED = (220,22,0)
BLACK = (0,0,0)
ORANGE = (255,140,0)
GREY = (207,207,207)
player1wins=0
player2wins=0
intro=pygame.image.load('connect-4.0.jpg')
def make_board():
    """int->int
    Creates a board of 0s with 6 as rows value and 7 Columns 
    >>>make_board()
    board=[0. 0. 0. 0. 0. 0. 0.]
          [0. 0. 0. 0. 0. 0. 0.]
          [0. 0. 0. 0. 0. 0. 0.]
          [0. 0. 0. 0. 0. 0. 0.]
          [0. 0. 0. 0. 0. 0. 0.]
          [0. 0. 0. 0. 0. 0. 0.]
    """
    board = np.zeros((6,7))
    np.flipud(board)#Flips arrays down or up
    return board
        
def insert_coin(board, row, column, coin):
    #coin insertion
    """int->list
    Adds the new coin value to the list of rows and columns on the board for each player
    >>>insert_coin(board,6,7,1)
    board[row][column]=1
    >>>insert_coin(board,6,7,2)
    board[row][column]=2
    """
    board[row][column]=coin

def overflow_check(board, column):
    """int->int
    Checks to see if the the fifth/top row contains a value already at the given column, prevents from input it if there 
    >>>overflow_check(board,3)
    board[5][3]==0
    """
    return board[5][column]==0
    
def open_row_check(board, column):
    """int->int
    Checks for the next row that has an opening in the array of 0s, if row is occuiped then moves on to the one above 
    >>>open_row_check(board,2)
    r=3
    >>>open_row_check(board,2)
    r=1
    """
    for r in range(ROWS):
        if board[r][column]==0:
            return r

def winning_coin(board, coin):
    """int->int
    Sees if either the 1 or 2 value occurs 4 consecutive times, horizontally, vertically or diagonally in the array of 0's (rows or columns)
    >>>winning_coin(board, 1)
    1==1
    >>>winning_coin(board, 2)
    1==1
    """
    #horizontal check, only 3 of the columns can work
    for c in range(COLUMNS-3):
        for r in range(ROWS):
            if board[r][c] == coin and board[r][c+1] == coin and board[r][c+2] == coin and board [r][c+3] == coin:
                return 1==1
    #vertical check, can only be in bottom 3 rows
    for c in range(COLUMNS):
        for r in range(ROWS-3):
            if board[r][c] == coin and board[r+1][c] == coin and board[r+2][c] == coin and board [r+3][c] == coin:
                return 1==1    
    #diagonal positive slopes check (/) last point is (3,4)
    for c in range(COLUMNS-3):
        for r in range(ROWS-3):
            if board[r][c] == coin and board[r+1][c+1] == coin and board[r+2][c+2] == coin and board [r+3][c+3] == coin:
                return 1==1
    #diagonal negative slopes check (/) starts at 4th row (3)
    for c in range(COLUMNS-3):
        for r in range(3,ROWS):
            if board[r][c] == coin and board[r-1][c+1] == coin and board[r-2][c+2] == coin and board[r-3][c+3] == coin:
                return 1==1
def draw_board(board):
    """int->
    Creates a graphical display for the matrix/array of 0s
    >>>draw_board(board)
    (Interface Displays)
    >>>draw_board(board)
    (Interface Displays)
    """
    #sets background as white
    screen.fill(WHITE)
    for c in range(COLUMNS):    
        for r in range(ROWS):
            #creates a blue rectangle for board outline
            pygame.draw.rect(screen, BLUE,(c*SQSIZE,r*SQSIZE+SQSIZE,SQSIZE,SQSIZE))
            #creates a circle for each column x row
            pygame.draw.circle(screen, WHITE,(int(c*SQSIZE+50),int(r*SQSIZE+150)),int(SQSIZE/2-6))

    for c in range(COLUMNS):
        for r in range(ROWS):
            if board[r][c] == 1:
                #player 1 colour (RED)
                pygame.draw.circle(screen, RED,(int(c*SQSIZE+50),height-int(r*SQSIZE+150-SQSIZE)),int(SQSIZE/2-6))
            elif board[r][c] == 2:
                #player 2 colour (YELLOW)
                pygame.draw.circle(screen, YELLOW,(int(c*SQSIZE+50),height-int(r*SQSIZE+150-SQSIZE)),int(SQSIZE/2-6))
        pygame.display.update()

def text_objects(text, font):
    """str->(graphics)
    Reads given font and colour and assigns it to textsurface variable that can be displayed on a graphical interface
    """
    textSurface = font.render(text, True, BLACK)
    return textSurface, textSurface.get_rect()

def Large_text_display(msg, x, y):
    """str/int->(graphics)
    Takes cordinates and a message, uses comicsans font at size 25 and displays it on pygame
    >>>draw_board(board)
    (Interface Displays)
    """
    Largetext = pygame.font.SysFont("comicsansms", 30)
    Largetext = pygame.font.SysFont("comicsansms", 30)
    TextSurf, TextRect = text_objects(msg, Largetext)
    TextRect.center = ((x), (y))
    screen.blit(TextSurf, TextRect)
    pygame.display.update()


def small_text_display(msg, x, y):
    """
    Takes cordinates and a message, uses comicsans font at size 15 and displays it on pygame
    >>>draw_board(board)
    (Interface Displays)
    """
    Largetext = pygame.font.SysFont("comicsansms", 15)
    Largetext = pygame.font.SysFont("comicsansms", 15)
    TextSurf, TextRect = text_objects(msg, Largetext)
    TextRect.center = ((x), (y))
    screen.blit(TextSurf, TextRect)
    pygame.display.update()

def button(msg,x,y,w,h,ic,ac,action=None):
    '''
    Allows users to pick which option they would like to go thorugh by displaying 2 graphical buttons, either quits the program
    or runs the game, also displays texts in the buttons
    '''
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            if action == "exit":
                pygame.quit()
                quit()
            elif action == 'play':
                board = make_board()    
                #allows alternation of turns
                count=0
                #draws board (blue rectangle and white circles)
                draw_board(board)
                pygame.display.update()
                #sets the font
                font = pygame.font.SysFont("arial", 65)
                #runs the game as long as gameover = false
                turn = 0
                game(turn,board,count,font,player1wins,player2wins)

    else:
        pygame.draw.rect(screen, ic, (x, y, w, h))
    
    Smalltext = pygame.font.Font("freesansbold.ttf",20)
    textSurf, textRect = text_objects(msg, Smalltext)
    textRect.center = ((x + (w/2)), (y + (h/2)))
    screen.blit(textSurf, textRect) 

def option():
    '''
    This is the option screen, user can choose which path they want the code to follow, accesses external files and displays highscores
    as well, basically the welcome screen
    '''
    start = True
    while start == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        screen.blit(background,[0,0])
        f=open('Highscore1.txt','r')
        highscore1=f.read()
        f.close()
        f=open('Highscore2.txt','r')
        highscore2=f.read()
        f.close()
        Large_text_display(('Player 1 score: '+str(highscore1)),200,500)
        Large_text_display(('Player 2 score: '+str(highscore2)),500,500)

        Large_text_display("Welcome to connect 4", 350, 150)
        button("Exit",430, 260, 200, 100, GREY, WHITE,"exit")
        button("Play",90, 260, 200, 100, GREY, WHITE,"play")
        
        pygame.display.update()
        clock.tick(5)
        
def game(turn,board,count,font,player1wins,player2wins):
    """str/int->(graphics)
    This is the main game function, the game includes 2 players switching turns to drop their colour into their desired row to get 4 in a row
    The first to succed is considered the winner, and such displays a graphically dsplay stating that they are the winner
    """
    game_over = False

    while not game_over:

        for event in pygame.event.get():
            #so that pygame doesnt crash when you click top right 'x'
            if event.type == pygame.QUIT:
                pygame.display.quit()
                quit()
                
            #during mouse motion, this will show the coin moving around. Color of coin depends on turn
            if event.type == pygame.MOUSEMOTION:
                #creates a white board at the top so that it the coin doesn't continue to appear
                pygame.draw.rect(screen,WHITE,(0,0, width, SQSIZE))
                posx = event.pos[0]
                #red colour for red coin
                if turn == 0:
                    pygame.draw.circle(screen,RED,(posx,int(SQSIZE/2)), int(SQSIZE/2-6))
                #yellow colour for yellow coin
                else:
                    pygame.draw.circle(screen,YELLOW,(posx,int(SQSIZE/2)), int(SQSIZE/2-6))
            pygame.display.update()
            #during click
            if event.type == pygame.MOUSEBUTTONDOWN:
                #ask for player 1 input
                if turn == 0:
                    posx = event.pos[0]
                    column = int(math.floor(posx/SQSIZE))
                    #checks if top row is full
                    if overflow_check(board,column):
                        row = open_row_check(board, column)
                        insert_coin(board, row, column, 1)
                        count+=1
                        #if win is true, when turn is for player 1 prints player 1 wins
                        if winning_coin(board, 1):
                            msg = font.render('Winning Coin Player 1 Wins',0,BLACK)
                            #updates top of the screen to display the message
                            screen.blit(msg, (15,10))
                            pygame.display.update()
                            time.sleep(3)
                            player1wins+=1
                            f=open('Highscore1.txt','r')
                            numb=f.read()
                            player1wins+=int(numb)
                            f.close()
                            f=open('Highscore1.txt','w')
                            f.write(str(player1wins))
                            f.close()
                            #need to insert a range so that game doesn't immeiately close and message disspears
                            for loop in range(21000000):
                                if loop == 10:
                                    game_over = True
            
                #ask for player 2 input
                else:
                    posx = event.pos[0]
                    column = int(math.floor(posx/SQSIZE))
                    #checks if top row is full
                    if overflow_check(board, column):
                        count+=1
                        row = open_row_check(board, column)
                        insert_coin(board, row, column, 2)
                        # if win is true, when turn is for player 2 prints player 2 wins
                        if winning_coin(board, 2):
                            msg = font.render('Winning Coin Player 2 Wins',0,BLACK)
                            #updates top of the screen to display the message
                            screen.blit(msg, (15,10))
                            pygame.display.update()
                            time.sleep(3)
                            player2wins+=1
                            f=open('Highscore2.txt','r')
                            numb=f.read()
                            player2wins+=int(numb)
                            f.close()
                            f=open('Highscore2.txt','w')
                            f.write(str(player2wins))
                            f.close()
                            #need to insert a range so that game doesn't immeiately close and message disspears
                            for loop in range(21000000):
                                if loop == 10:
                                    game_over = True  
                    
                draw_board(board)
                if count==42:
                    msg = font.render('There seems to be a tie',0,BLACK)
                    screen.blit(msg, (15,10))
                    pygame.display.update()
                    time.sleep(2)
                    game_over=True
        #alternates between turns
                turn+=1
                turn = turn%2
while True:
    

    #initializes pygame
    pygame.init()
    #size of one square
    SQSIZE = 100
    
    #number of columns times sqsize
    width = COLUMNS * SQSIZE

    #number of rows times sqsize, plus one for the extra top row (for selection)
    height = (ROWS+1) * SQSIZE

    #into a tuple
    size = (width, height)
    screen = pygame.display.set_mode(size)
                
    screen.fill(WHITE)
    screen.blit(intro,[0,0])
    pygame.display.update()

    time.sleep(2)
    screen.fill(WHITE)
    
    pygame.display.update()
    Large_text_display('How to play:',350,200)
    small_text_display('Hover the mouse over the desired row and column and simply click, scrolling will allow fast drops',350,300)
    time.sleep(4)

    option()
    



