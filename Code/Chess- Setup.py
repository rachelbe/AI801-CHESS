import pygame
import random
import sys

pygame.init()

# hardcoded vals for board (with black and white color set)
width = 480
height = 480
cell = width // 8
white = (255, 255, 255)
black = (0, 0, 0)

#piece dictionary
#i put a capital letter but can be replaced with a graphic or png in the future , just to visualize the board
pieces = {
        'r': 'R', 'n': 'N', 'b': 'B', 'q': 'Q',
        'k': 'K', 'p': 'P', 'R': 'R', 'N': 'N',
        'B': 'B', 'Q': 'Q', 'K': 'K', 'P': 'P'
}

#board set up 
initialBoard = [
    ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
    ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
    ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
]

# set up the chess board
def drawBoard(screen,board):
    for row in range(8):
        for col in range(8):
            color = white if (row + col) % 2 == 0 else black
            pygame.draw.rect(screen, color, (col * cell, row * cell, cell, cell))
            piece = pieces.get(board[row][col], '')
            if piece:
                screen.blit(font.render(piece, True, black if color == white else white),
                            (col * cell + cell // 4, row * cell + cell // 4))
                            
# pieces on board
def drawPieces(screen, board):
    for row in range(8):
        for col in range(8):
            piece = pieces.get(board[row][col], '')
            if piece:
                screen.blit(font.render(piece, True, black), (col * cell + cell // 4, row * cell + cell // 4))
# Main function
def main():
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Chess Board")
    
    clock = pygame.time.Clock() #use pygame clock 
    
    turn = True  # if  its the players turn (this can be used when adding the AI/computer element)

# keeps window open until you close it
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((255, 255, 255))
        
        drawBoard(screen,initialBoard)
        drawPieces(screen,initialBoard)
        
        pygame.display.flip()
        clock.tick(30)



if __name__ == "__main__":
    font = pygame.font.Font(None, 36)
    main()