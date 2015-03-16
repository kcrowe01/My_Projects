class 2Player:
    
    board = []
    def __init__():
        screen.fill(BLUE)
        for i in range(7):
            board.append([])
            for j in range(6):
                board[i].append('E')
                pygame.draw.ellipse(screen, WHITE, [40*(i+0.5), 40*(j+0.5)+40, 40, 40]) 
        markerrect.left = 30
        markerrect.top = 300
        screen.blit(marker, markerrect)
        screen.blit(turn_indicator, [0, 0])
        pygame.draw.ellipse(screen, YELLOW, [110, 10, 20, 20])
        text = font.render("Y: 0   R: 0", 1, WHITE)
        screen.blit(text, [160, 10])
        pygame.display.flip()
        
