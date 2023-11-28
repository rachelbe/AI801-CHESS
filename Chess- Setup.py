import pygame
import sys
import chess

# Initialize pygame
pygame.init()

# Board dimensions and colors
width = 480
height = 480
cell = width // 8
white = (255, 255, 255)
black = (0, 0, 0)

# Initialize the chess board using python-chess
chess_board = chess.Board()

# Initialize font
font = pygame.font.Font(None, 36)

# Convert chess square to pixel coordinates
def chess_square_to_pixels(square):
    x = (square % 8) * cell
    y = (7 - square // 8) * cell
    return x, y

# Convert pixel coordinates to chess square
def pixels_to_chess_square(pos):
    col = pos[0] // cell
    row = 7 - (pos[1] // cell)
    return chess.square(col, row)

# Draw the chess board
def draw_board(screen):
    for row in range(8):
        for col in range(8):
            color = white if (row + col) % 2 == 0 else black
            pygame.draw.rect(screen, color, (col * cell, row * cell, cell, cell))

# Draw chess pieces
def draw_pieces(screen, board):
    grey = (128, 128, 128)  # A shade of grey for white pieces
    red = (255, 0, 0)  # RGB for red color for black pieces

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            x, y = chess_square_to_pixels(square)
            # Use red for black pieces (lowercase letters) and grey for white pieces (uppercase letters)
            piece_color = red if piece.symbol().islower() else grey
            screen.blit(font.render(piece.symbol(), True, piece_color), (x + cell // 4, y + cell // 4))

# Highlight legal moves for a selected piece
def highlight_legal_moves(screen, board, square):
    for move in board.legal_moves:
        if move.from_square == square:
            highlight_square(screen, move.to_square, (0, 255, 0, 100))  # Green color

# Function to highlight a square
def highlight_square(screen, square, color):
    x, y = chess_square_to_pixels(square)
    s = pygame.Surface((cell, cell), pygame.SRCALPHA)  # per-pixel alpha
    s.fill(color)  # notice the alpha value in the color
    screen.blit(s, (x, y))


# Evaluate board for AI
pawn_table = [
    0,  0,  0,  0,  0,  0,  0,  0,
    5, 10, 10, -20,-20, 10, 10,  5,
    5, -5,-10,  0,  0,-10, -5,  5,
    0,  0,  0, 20, 20,  0,  0,  0,
    5,  5, 10, 25, 25, 10,  5,  5,
    10, 10, 20, 30, 30, 20, 10, 10,
    50, 50, 50, 50, 50, 50, 50, 50,
    0,  0,  0,  0,  0,  0,  0,  0
]

knight_table = [
    -50,-40,-30,-30,-30,-30,-40,-50,
    -40,-20,  0,  5,  5,  0,-20,-40,
    -30,  5, 10, 15, 15, 10,  5,-30,
    -30,  0, 15, 20, 20, 15,  0,-30,
    -30,  5, 15, 20, 20, 15,  5,-30,
    -30,  0, 10, 15, 15, 10,  0,-30,
    -40,-20,  0,  0,  0,  0,-20,-40,
    -50,-40,-30,-30,-30,-30,-40,-50
]

bishop_table = [
    -20,-10,-10,-10,-10,-10,-10,-20,
    -10,  5,  0,  0,  0,  0,  5,-10,
    -10, 10, 10, 10, 10, 10, 10,-10,
    -10,  0, 10, 10, 10, 10,  0,-10,
    -10,  5,  5, 10, 10,  5,  5,-10,
    -10,  0,  5, 10, 10,  5,  0,-10,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -20,-10,-10,-10,-10,-10,-10,-20
]

rook_table = [
    0,  0,  0,  5,  5,  0,  0,  0,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    5, 10, 10, 10, 10, 10, 10,  5,
    0,  0,  0,  0,  0,  0,  0,  0
]

queen_table = [
    -20,-10,-10, -5, -5,-10,-10,-20,
    -10,  0,  5,  0,  0,  0,  0,-10,
    -10,  5,  5,  5,  5,  5,  0,-10,
     0,  0,  5,  5,  5,  5,  0, -5,
    -5,  0,  5,  5,  5,  5,  0, -5,
    -10,  0,  5,  5,  5,  5,  0,-10,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -20,-10,-10, -5, -5,-10,-10,-20
]

king_table = [
    20, 30, 10,  0,  0, 10, 30, 20,
    20, 20,  0,  0,  0,  0, 20, 20,
    -10,-20,-20,-20,-20,-20,-20,-10,
    -20,-30,-30,-40,-40,-30,-30,-20,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30
]

def evaluate_board(board):
    if board.is_checkmate():
        return float('-inf') if board.turn else float('inf')
    if board.is_stalemate() or board.is_insufficient_material():
        return 0

    eval = 0
    piece_values = {'P': 1, 'N': 3, 'B': 3.1, 'R': 5, 'Q': 9, 'K': 0}
    piece_square_tables = {
        'P': pawn_table,
        'N': knight_table,
        'B': bishop_table,
        'R': rook_table,
        'Q': queen_table,
        'K': king_table
    }

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            piece_type = piece.symbol().upper()
            value = piece_values[piece_type]
            # Add or subtract piece value
            eval += value if piece.color == chess.WHITE else -value
            # Adjust evaluation based on piece's position
            square_value = piece_square_tables.get(piece_type, [0]*64)[square]
            eval += square_value if piece.color == chess.WHITE else -square_value

    # Additional factors (e.g., pawn structure, mobility) can be added here

    return eval

# Minimax with Alpha-Beta Pruning
def minimax(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    if maximizing_player:
        max_eval = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

# Find best move for AI
def get_best_move(board, depth):
    best_move = chess.Move.null()
    best_value = float('-inf')
    alpha = float('-inf')
    beta = float('inf')

    for move in board.legal_moves:
        board.push(move)
        board_value = minimax(board, depth - 1, alpha, beta, False)
        board.pop()
        if board_value > best_value:
            best_value = board_value
            best_move = move
    return best_move

# Main function
def main():
    global font
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Chess Game")
    clock = pygame.time.Clock()
    selected_square = None
    move_from = None
    ai_color = chess.BLACK  # AI plays as black (actually red)
    ai_depth = 3            # Depth for minimax

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and chess_board.turn != ai_color:
                pos = pixels_to_chess_square(event.pos)
                if selected_square is None:
                    selected_square = pos
                    move_from = pos
                else:
                    move_to = pos
                    if move_from is not None and move_to is not None:
                        move = chess.Move(move_from, move_to)
                        if chess_board.is_legal(move):
                            print(f"Player move: {move}")
                            chess_board.push(move)
                    selected_square = None
                    move_from = None

        screen.fill(white)
        draw_board(screen)
        draw_pieces(screen, chess_board)

        
        # Highlight legal moves if a piece is selected
        if selected_square is not None and chess_board.color_at(selected_square) == chess_board.turn:
            highlight_legal_moves(screen, chess_board, selected_square)


        # AI's turn
        if chess_board.turn == ai_color:
            try:
                ai_move = get_best_move(chess_board, ai_depth)
                if ai_move:
                    print(f"AI move: {ai_move}")
                    chess_board.push(ai_move)
                else:
                    print("No valid AI move found.")
            except Exception as e:
                print(f"AI move generation error: {e}")

        if chess_board.is_checkmate() or chess_board.is_stalemate():
            print("Game Over")
            pygame.quit()
            sys.exit()

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
