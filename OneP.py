import sys, pygame, time, random

pygame.init()
size = 320, 320
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Connect Four")

WHITE = 255, 255, 255
BLACK = 0, 0, 0
YELLOW = 255, 255, 0
RED = 255, 0, 0
BLUE = 0, 0, 255

class OnePlayer:

    ##Gameplay##
    board = []
    turn = 'Y'
    score = [0, 0]
    points = [0, 0, 0, 0, 0, 0, 0] #array for AI solver
    empty = True
    ##Display##
    marker = pygame.image.load("arrow.png") #holds column marker
    markerrect = marker.get_rect()
    turn_indicator = pygame.image.load("turn.png")
    font = pygame.font.Font(None, 28)
    ###########

    #Initialize and draw board
    def __init__(self):
        screen.fill(BLUE)
        for i in range(7):
            self.board.append([])
            for j in range(6):
                self.board[i].append('E')
                pygame.draw.ellipse(screen, WHITE, [40*(i+0.5), 40*(j+0.5)+40, 40, 40]) 
        self.markerrect.left = 30
        self.markerrect.top = 300
        screen.blit(self.marker, self.markerrect)
        screen.blit(self.turn_indicator, [0, 0])
        pygame.draw.ellipse(screen, YELLOW, [110, 10, 20, 20])
        text = self.font.render("Y: 0   R: 0", 1, WHITE)
        screen.blit(text, [160, 10])
        pygame.display.flip()

    #draw board
    def print_board(self):
        screen.fill(BLUE)
        for i in range(7):
            for j in range(6):
                if self.board[i][j] == 'E':
                    pygame.draw.ellipse(screen, WHITE, [40*(i+0.5), 40*(j+0.5)+ 40, 40, 40])
                elif self.board[i][j] == 'Y':
                    pygame.draw.ellipse(screen, YELLOW, [40*(i+0.5), 40*(j+0.5)+ 40, 40, 40])
                elif self.board[i][j] == 'R':
                    pygame.draw.ellipse(screen, RED, [40*(i+0.5), 40*(j+0.5)+ 40, 40, 40])
                screen.blit(self.turn_indicator, [0, 0])
        if self.turn == 'Y':
            pygame.draw.ellipse(screen, YELLOW, [110, 10, 20, 20])
        else:
            pygame.draw.ellipse(screen, RED, [110, 10, 20, 20])
        text = self.font.render("Y: " + str(self.score[0]) +   "   R: " + str(self.score[1]), 1, WHITE)
        screen.blit(text, [160, 10])
        pygame.display.flip()
        
    #update column marker    
    def print_marker(self):
        screen.blit(self.marker, self.markerrect)
        pygame.display.flip()
        
    #move marker left    
    def moveleft(self):
        self.markerrect.left = self.markerrect.left - 40
        screen.blit(self.marker, self.markerrect) 
        pygame.display.flip()
        
    #move marker right
    def moveright(self):
        self.markerrect.right = self.markerrect.right + 40
        screen.blit(self.marker, self.markerrect) 
        pygame.display.flip()

    #place game piece
    def place_chip(self):
        self.empty = False
        i = (self.markerrect.left - 30) / 40
        for j in range(6):
            if self.board[i][5 - j] == 'E':
                if self.turn == 'Y':
                    pygame.draw.ellipse(screen, YELLOW, [40*(i+0.5), 40*((5-j)+0.5)+40, 40, 40])
                    self.board[i][5-j] = 'Y'
                elif self.turn == 'R':
                    pygame.draw.ellipse(screen, RED, [40*(i+0.5), 40*((5-j)+0.5)+40, 40, 40])
                    self.board[i][5-j] = 'R'
                screen.blit(self.marker, self.markerrect)    
                pygame.display.flip()
                return True
        return False            

    #show connection for winning pieces            
    def connect(self, i, j, x_dir, y_dir):
        if(x_dir == 0 and y_dir == 1):
            pygame.draw.line(screen, BLACK, [40*(i+1), 40*(7-j)], [40*(i+1), 40*(4-j)], 5)
            pygame.display.flip()
        elif(x_dir == 1 and y_dir == 0):
            pygame.draw.line(screen, BLACK, [40*(i+1), 40*(7-j)], [40*(i+4), 40*(7-j)], 5)
            pygame.display.flip()
        elif(x_dir == -1 and y_dir == 1):
            pygame.draw.line(screen, BLACK, [40*(i+1), 40*(7-j)], [40*(i-2), 40*(4-j)], 5)
            pygame.display.flip()
        elif(x_dir == 1 and y_dir == 1):
            pygame.draw.line(screen, BLACK, [40*(i+1), 40*(7-j)], [40*(i+4), 40*(4-j)], 5)
            pygame.display.flip()

    #recursively check for a winner            
    def check(self, depth, i, j, x_dir, y_dir):
        if(depth == 3):
            return True
        elif(j - y_dir < 0 or j - y_dir > 5 or i + x_dir < 0 or i + x_dir > 6):
            return False
        elif(self.board[i + x_dir][j - y_dir] == self.turn):
            if(self.check(depth + 1, i + x_dir, j - y_dir, x_dir, y_dir)):
                return True
        return False

    #check the board for a winner    
    def check_board(self):
        for i in range(7):
            for j in range(6):
                if(self.board[i][5-j] == self.turn):
                    for k in range(-1, 2):
                        for l in range(0, 2):
                            if(not(k == 0 and l == 0)):
                                if(self.check(0, i, 5 - j, k, l)):
                                    self.connect(i, j, k, l)
                                    if(self.turn == 'Y'):
                                        self.turn = 'R'
                                        pygame.draw.ellipse(screen, RED, [110, 10, 20, 20])
                                    else:
                                        self.turn = 'Y'
                                        pygame.draw.ellipse(screen, YELLOW, [110, 10, 20, 20])
                                    return True
        if(self.turn == 'Y'):
            self.turn = 'R'
            pygame.draw.ellipse(screen, RED, [110, 10, 20, 20])
        else:
            self.turn = 'Y'
            pygame.draw.ellipse(screen, YELLOW, [110, 10, 20, 20])
        pygame.display.update()    
        return False

    def reset_game(self):
        for i in range(7):
            for j in range(6):
                self.board[i][j] = 'E'
        self.empty = True        

    def display_winner(self):
        if self.turn == 'R':
            winner = pygame.image.load("ywins.png")
            screen.fill(WHITE)
            screen.blit(winner, [0,0])
            pygame.display.flip()
            self.score[0] = self.score[0] + 1
        else:
            winner = pygame.image.load("rwins.png")
            screen.fill(WHITE)
            screen.blit(winner, [0,0])
            pygame.display.flip()
            self.score[1] = self.score[1] + 1

        done = 1
        while done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    done = 0
                    self.reset_game()
                    self.print_board()
                else:
                    done = 1
    #####Helper functions used for AI solver#########
    def check_up(self, i, j):
        if(j - 1 < 0 or self.board[i][j-1] != self.turn):
            return 1
        else:
            return self.check_up(i, j-1) + 1

    def check_down(self, i, j):
        if(j + 1 > 5 or self.board[i][j+1] != self.turn):
            return 1
        else:
            return self.check_down(i, j+1) + 1

    def check_left(self, i, j):
        if(i - 1 < 0 or self.board[i - 1][j] != self.turn):
            return 1
        else:
            return self.check_left(i - 1, j) + 1        

    def check_right(self, i, j):
        if(i + 1 > 6 or self.board[i+1][j] != self.turn):
            return 1
        else:
            return self.check_right(i+1, j) + 1
        
    def check_leftdown(self, i, j):
        if(j + 1 > 5 or i - 1 < 0 or self.board[i - 1][j+1] != self.turn):
            return 1
        else:
            return self.check_leftdown(i - 1, j+1) + 1

    def check_rightdown(self, i, j):
        if(j + 1 > 5 or i + 1 > 6 or self.board[i + 1][j+1] != self.turn):
            return 1
        else:
            return self.check_rightdown(i + 1, j+1) + 1

    def check_leftup(self, i, j):
        if(j - 1 < 0 or i - 1 < 0 or self.board[i-1][j-1] != self.turn):
            return 1
        else:
            return self.check_leftup(i-1, j-1) + 1
        
    def check_rightup(self, i, j):
        if(j - 1 < 0 or i + 1 > 6 or self.board[i+1][j-1] != self.turn):
            return 1
        else:
            return self.check_rightup(i+1, j-1) + 1
    ####################################################################

    ##AI makes its decision based on points. each possible placement gets a points value calculated
    ##by the total number of tiles in a row. Loses points for potential tiles put in a row by the
    ##player on their next turn.
    def calc_points(self, i, j):
        vert_length = self.check_up(i, j) + self.check_down(i, j) - 1 #-1 so we dont double count
        horz_length = self.check_left(i, j) + self.check_right(i, j) - 1
        diag_length1 = self.check_leftdown(i, j) + self.check_rightup(i, j) - 1
        diag_length2 = self.check_leftup(i, j) + self.check_rightdown(i, j) - 1
        
        if(vert_length == 4 or horz_length == 4 or diag_length1 == 4 or diag_length2 == 4):
            self.points[i] = 1000
        else:
            self.points[i] = pow(vert_length, 2) + pow(horz_length, 2) + pow(diag_length1, 2) + pow(diag_length2, 2)
        self.board[i][j] = 'R'
        self.turn = 'Y'
        ##check possible moves next turn for player
        for n in range(7):
            for m in range(6):
                if(self.board[n][5-m] == 'E'):
                    Yvert_length = self.check_up(n, 5-m) + self.check_down(n, 5-m) - 1 
                    Yhorz_length = self.check_left(n, 5-m) + self.check_right(n, 5-m) - 1
                    Ydiag_length1 = self.check_leftdown(n, 5-m) + self.check_rightup(n, 5-m) - 1
                    Ydiag_length2 = self.check_leftup(n, 5-m) + self.check_rightdown(n, 5-m) - 1
                    if(Yvert_length >= 4 or Yhorz_length >= 4 or Ydiag_length1 >= 4 or Ydiag_length2 >= 4):
                        self.points[i] = self.points[i] - 250
                    else:
                        self.points[i] = self.points[i] - pow(Yvert_length, 2) + pow(Yhorz_length, 2) + pow(Ydiag_length1, 2) + pow(Ydiag_length2, 2)
                    break
        ##reset board and turn
        self.board[i][j] = 'E'
        self.turn = 'R'
        ##encourage AI to place its first tiles adjacent to the players tile
        if (i > 0 and self.board[i-1][j] == 'Y'):
            self.points[i] = self.points[i] + 4
        if (i < 6 and self.board[i+1][j] == 'Y'):
            self.points[i] = self.points[i] + 4

    #Finds what column the AI should drop its piece into            
    def find_col(self):
        maxp = -2000
        col = 0
        for i in range(7):
            for j in range(6):
                if(self.board[i][5-j] == 'E'):
                    self.calc_points(i, 5 - j)
                    break
        for i in range(7):
            if (self.points[i] > maxp):
                maxp = self.points[i]
                col = i
        return col

    #Run AI
    def AI(self):
        if(self.empty):
            self.markerrect.left = random.randint(0, 6)*40 + 30
        else:
            self.markerrect.left = self.find_col()*40 + 30
        while not(self.place_chip()):
            self.markerrect.left = random.randint(0, 6)*40 + 30
        if(self.check_board()):
            time.sleep(1)
            self.display_winner()
            self.print_board()
            self.print_marker()
