import pygame
import random
import sys
import chess
import os

# Initialize Pygame
pygame.init()

# Hardcoded values for the board
width = 480
height = 480
cell = width // 8
white = (193,205,205)
black = (131,139,139)
highlight_color = (255, 255, 0)  # Yellow for highlight

# Load images
def load_images(path):
    pieces_images = {}
    pieces = ['bishop', 'king', 'knight', 'pawn', 'queen', 'rook']
    for piece in pieces:
        for color in ['b', 'w']:
            image_path = os.path.join(path, f'{color}_{piece}.png')
            pieces_images[f'{color}_{piece}'] = pygame.image.load(image_path).convert_alpha()
            pieces_images[f'{color}_{piece}'] = pygame.transform.scale(pieces_images[f'{color}_{piece}'], (cell, cell))
    return pieces_images

# Initialize a chess board
board = chess.Board()

# Function to draw highlighted moves
def draw_highlights(screen, board, square):
    moves = list(board.legal_moves)
    for move in moves:
        if move.from_square == square:
            end_row, end_col = divmod(move.to_square, 8)
            pygame.draw.rect(screen, highlight_color, (end_col * cell, end_row * cell, cell, cell), 5)

# Function to draw the board and pieces
def draw_board(screen, pieces_images):
    for row in range(8):
        for col in range(8):
            color = white if (row + col) % 2 == 0 else black
            pygame.draw.rect(screen, color, (col * cell, row * cell, cell, cell))
            piece = board.piece_at(chess.square(col, row))
            if piece:
                piece_color = 'w' if piece.color else 'b'
                piece_type = {
                    'R': 'rook', 'N': 'knight', 'B': 'bishop',
                    'Q': 'queen', 'K': 'king', 'P': 'pawn'
                }[piece.symbol().upper()]
                screen.blit(pieces_images[f'{piece_color}_{piece_type}'], (col * cell, row * cell))

# Function to display game status
def display_status(screen, board):
    font = pygame.font.SysFont(None, 36)
    if board.is_checkmate():
        text = font.render('Checkmate', True, (255, 0, 0))
    elif board.is_stalemate():
        text = font.render('Stalemate', True, (255, 0, 0))
    elif board.is_check():
        text = font.render('Check', True, (255, 255, 0))
    else:
        text = font.render('', True, (0, 0, 0))
    screen.blit(text, (0, 0))


# Main game loop
def main():
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Chess")

    clock = pygame.time.Clock() #use pygame clock 

    turn = True  # if  its the players turn (this can be used when adding the AI/computer element)

    # Path to the image directory
    image_path = 'C:/Users/jcfre/OneDrive/Desktop/Pygame Chess Setup/imgs'
    pieces_images = load_images(image_path)

    running = True
    selected_piece = None
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Handle mouse click events
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                col, row = x // cell, y // cell
                square = chess.square(col, row)
                if selected_piece and chess.Move(selected_piece, square) in board.legal_moves:
                    board.push(chess.Move(selected_piece, square))
                    selected_piece = None
                elif board.piece_at(square):
                    selected_piece = square

        # Draw the board and pieces
        draw_board(screen, pieces_images)

        # Highlight legal moves
        if selected_piece is not None:
            draw_highlights(screen, board, selected_piece)

        # Display game status
        display_status(screen, board)

        # Update the display
        pygame.display.flip()
        clock.tick(30)

        # Check for game end conditions
        if board.is_checkmate():
            print("Checkmate!")
            running = False
        elif board.is_stalemate():
            print("Stalemate!")
            running = False

    pygame.quit()


if __name__ == "__main__":
    main()
