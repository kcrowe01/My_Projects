import sys, pygame, time

print "running connect four"

pygame.init()
size = 320, 320
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Connect Four")

WHITE = 255, 255, 255
BLACK = 0, 0, 0
YELLOW = 255, 255, 0
RED = 255, 0, 0
BLUE = 0, 0, 255
board = []
screen.fill(BLUE)
for i in range(7):
    board.append([])
    for j in range(6):
        board[i].append('E')
        pygame.draw.ellipse(screen, WHITE, [40*(i+0.5), 40*(j+0.5)+40, 40, 40]) 
pygame.display.flip()
#new_turn = True
marker = pygame.image.load("arrow.png")
markerrect = marker.get_rect()
marker.set_colorkey(WHITE)
markerrect.left = 30
markerrect.top = 300
screen.blit(marker, markerrect)
turn_indicator = pygame.image.load("turn.png")
turn = 'Y'
screen.blit(turn_indicator, [0, 0])
pygame.draw.ellipse(screen, YELLOW, [110, 10, 20, 20])
font = pygame.font.Font(None, 28)
text = font.render("Y: 0   R: 0", 1, WHITE)
screen.blit(text, [160, 10])
pygame.display.flip()
score = [0, 0]
last_added = [0,0]
undone = True
################################################################################
def print_board(board, turn, score):
    screen.fill(BLUE)
    for i in range(7):
        for j in range(6):
            if board[i][j] == 'E':
                pygame.draw.ellipse(screen, WHITE, [40*(i+0.5), 40*(j+0.5)+ 40, 40, 40])
            elif board[i][j] == 'Y':
                pygame.draw.ellipse(screen, YELLOW, [40*(i+0.5), 40*(j+0.5)+ 40, 40, 40])
            elif board[i][j] == 'R':
                pygame.draw.ellipse(screen, RED, [40*(i+0.5), 40*(j+0.5)+ 40, 40, 40])
            screen.blit(turn_indicator, [0, 0])
    if turn == 'Y':
        pygame.draw.ellipse(screen, YELLOW, [110, 10, 20, 20])
    else:
        pygame.draw.ellipse(screen, RED, [110, 10, 20, 20])
    text = font.render("Y: " + str(score[0]) +   "   R: " + str(score[1]), 1, WHITE)
    screen.blit(text, [160, 10])
    pygame.display.flip()
################################################################################
def place_chip(markerrect, board, turn):
    i = (markerrect.left - 30) / 40
    for j in range(6):
        if board[i][5 - j] == 'E':
            if turn == 'Y':
                pygame.draw.ellipse(screen, YELLOW, [40*(i+0.5), 40*((5-j)+0.5)+40, 40, 40])
                board[i][5-j] = 'Y'
                turn = 'R'
                last_added[0] = i
                last_added[1] = 5-j
            elif turn == 'R':
                pygame.draw.ellipse(screen, RED, [40*(i+0.5), 40*((5-j)+0.5)+40, 40, 40])
                board[i][5-j] = 'R'
                turn = 'Y'
                last_added[0] = i
                last_added[1] = 5-j
            pygame.display.flip()
            return turn
    return turn
################################################################################
#CHECKER FUNCTIONS#
def check_up(i, j, turn):
    if j < 3:
        return False
    elif board[i][j-1] == turn and board[i][j-2] == turn and board[i][j-3] == turn:
        return True
    else:
        return False
def check_up_left(i, j, turn):
    if j < 3 or i < 3:
        return False
    elif board[i-1][j-1] == turn and board[i-2][j-2] == turn and board[i-3][j-3] == turn:
        return True
    else:
        return False
def check_up_right(i, j, turn):
    if j < 3 or i > 3: 
        return False
    elif board[i+1][j-1] == turn and board[i+2][j-2] == turn and board[i+3][j-3] == turn:
        return True
    else:
        return False
def check_left(i, j, turn):
    if i < 3:
        return False
    elif board[i-1][j] == turn and board[i-2][j] == turn and board[i-3][j] == turn:
        return True
    else:
        return False
    
################################################################################
#checks for a winner depending on turn#
def check_board(board, turn):
    """turn is switched in place_chip function so
        switch back for this function"""
    if turn == 'Y':
        turn = 'R'
    else:
        turn = 'Y'
    for i in range(7):
        for j in range(6):
            if board[i][5 - j] == turn:
                if check_up(i, 5 - j, turn):
                    pygame.draw.line(screen, BLACK, [40*(i+1), 40*(6-j)+40], [40*(i+1), 40*(3-j)+40], 5)
                    pygame.display.flip()
                    return True
                elif check_up_left(i, 5 - j, turn):
                    pygame.draw.line(screen, BLACK, [40*(i+1), 40*(6-j)+40], [40*(i-2), 40*(3-j)+40], 5)
                    pygame.display.flip()
                    return True
                elif check_up_right(i,5 - j, turn):
                    pygame.draw.line(screen, BLACK, [40*(i+1), 40*(6-j)+40], [40*(i+4), 40*(3-j)+40], 5)
                    pygame.display.flip()
                    return True
                elif check_left(i,5 - j, turn):
                    pygame.draw.line(screen, BLACK, [40*(i+1), 40*(6-j)+40], [40*(i-2), 40*(6-j)+40], 5)
                    pygame.display.flip()
                    return True
    return False
################################################################################
def display_winner(turn):
    if turn == 'R':
        winner = pygame.image.load("ywins.png")
        screen.fill(WHITE)
        screen.blit(winner, [0,0])
        pygame.display.flip()
        score[0] = score[0] + 1
    else:
        winner = pygame.image.load("rwins.png")
        screen.fill(WHITE)
        screen.blit(winner, [0,0])
        pygame.display.flip()
        score[1] = score[1] + 1

    done = 1
    while done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                done = 0
            else:
                done = 1
    return score
################################################################################
def reset_game():
    for i in range(7):
        for j in range(6):
            board[i][j] = 'E'
################################################################################
while 1:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            print_board(board, turn, score)
            if event.key == pygame.K_LEFT:
                    if markerrect.left > 30:
                        markerrect.left = markerrect.left - 40
            if event.key == pygame.K_RIGHT:
                    if markerrect.right < 290:
                        markerrect.right = markerrect.right + 40
            screen.blit(marker, markerrect) 
            pygame.display.flip()
            if event.key == pygame.K_SPACE:
                turn = place_chip(markerrect, board, turn)
                undone = False
                if check_board(board, turn):
                    time.sleep(1)
                    score = display_winner(turn)
                    reset_game()
                    print_board(board, turn, score)
                    screen.blit(marker, markerrect)
                    pygame.display.flip()
                if turn == 'Y':
                    pygame.draw.ellipse(screen, YELLOW, [110, 10, 20, 20])
                else:
                    pygame.draw.ellipse(screen, RED, [110, 10, 20, 20])
                pygame.display.flip()
            if event.key == pygame.K_BACKSPACE and undone == False:
                undone = True
                board[last_added[0]][last_added[1]] = 'E'
                print last_added[1]
                if turn == 'Y':
                    turn = 'R'
                else:
                    turn = 'Y'
                print_board(board, turn, score)
                screen.blit(marker, markerrect)
                pygame.display.flip()
