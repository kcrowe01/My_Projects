from TwoP import TwoPlayer
from OneP import OnePlayer
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

screen.fill(WHITE)
font = pygame.font.Font(None, 28)
text = font.render("Welcome to Connect Four", 1, BLUE)
screen.blit(text, [40, 10])
text = font.render("Press 1 For Single Player", 1, RED)
screen.blit(text, [20, 120])
text = font.render("Press 2 For Multiple Players", 1, RED)
screen.blit(text, [20, 150])
pygame.display.update()

players = 0
initialized = False

while not initialized:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                players = 1
                game = OnePlayer()
                initialized = True
            if event.key == pygame.K_2:
                players = 2
                game = TwoPlayer()
                initialized = True



while 1:
    for event in pygame.event.get():
        if(players == 1 and game.turn == 'R'):
            game.print_board()
            game.AI()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            game.print_board()
            if event.key == pygame.K_LEFT:
                    if game.markerrect.left > 30:
                        game.moveleft()
            if event.key == pygame.K_RIGHT:
                    if game.markerrect.right < 290:
                        game.moveright()
            game.print_marker()            
            if event.key == pygame.K_SPACE:
                if(game.place_chip()):
                    if (game.check_board()):
                        time.sleep(1) ##allow player to see the connection
                        game.display_winner()
                        game.print_board()
                        game.print_marker()
            if (event.key == pygame.K_BACKSPACE and game.undone == False and
                players == 2):
                game.undo()
            if (event.key == pygame.K_r):
                game.reset_game()
                game.print_board()
