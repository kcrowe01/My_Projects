import sys, pygame, time

pygame.init()
size = 320, 320
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Connect Four")

WHITE = 255, 255, 255
BLACK = 0, 0, 0
YELLOW = 255, 255, 0
RED = 255, 0, 0
BLUE = 0, 0, 255

class TwoPlayer:

    ##Gameplay##
    board = []
    turn = 'Y'
    score = [0, 0]
    last_added = [0,0] #handles undo
    undone = True
    ##Display##
    marker = pygame.image.load("arrow.png")
    markerrect = marker.get_rect()
    turn_indicator = pygame.image.load("turn.png")
    font = pygame.font.Font(None, 28)
    ###########
    
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
        
    def print_marker(self):
        screen.blit(self.marker, self.markerrect)
        pygame.display.flip()
        
    def moveleft(self):
        self.markerrect.left = self.markerrect.left - 40
        screen.blit(self.marker, self.markerrect) 
        pygame.display.flip()

    def moveright(self):
        self.markerrect.right = self.markerrect.right + 40
        screen.blit(self.marker, self.markerrect) 
        pygame.display.flip()

    def place_chip(self):
        i = (self.markerrect.left - 30) / 40
        for j in range(6):
            if self.board[i][5 - j] == 'E':
                if self.turn == 'Y':
                    pygame.draw.ellipse(screen, YELLOW, [40*(i+0.5), 40*((5-j)+0.5)+40, 40, 40])
                    self.board[i][5-j] = 'Y'
                    self.last_added[0] = i
                    self.last_added[1] = 5 - j
                elif self.turn == 'R':
                    pygame.draw.ellipse(screen, RED, [40*(i+0.5), 40*((5-j)+0.5)+40, 40, 40])
                    self.board[i][5-j] = 'R'
                    self.last_added[0] = i
                    self.last_added[1] = 5 - j
                self.undone = False
                screen.blit(self.marker, self.markerrect)    
                pygame.display.flip()
                return True
        return False            
            
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
            
    def check(self, depth, i, j, x_dir, y_dir):
        if(depth == 3):
            return True
        elif(j - y_dir < 0 or j - y_dir > 5 or i + x_dir < 0 or i + x_dir > 6):
            return False
        elif(self.board[i + x_dir][j - y_dir] == self.turn):
            if(self.check(depth + 1, i + x_dir, j - y_dir, x_dir, y_dir)):
                return True
        return False
    
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

    def undo(self):
        self.undone = True
        self.board[self.last_added[0]][self.last_added[1]] = 'E'
        if self.turn == 'Y':
            self.turn = 'R'
        else:
            self.turn = 'Y'
        self.print_board()
        screen.blit(self.marker, self.markerrect)
        pygame.display.flip()

    def reset_game(self):
        for i in range(7):
            for j in range(6):
                self.board[i][j] = 'E'

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
        
