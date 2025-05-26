import pygame
import sys
import chess

WIDTH, HEIGHT = 480, 480
SQ_SIZE = WIDTH // 8
FPS = 60

WHITE = (220, 240, 220)
BROWN = (72, 114, 144)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("IA COMIENZA")
clock = pygame.time.Clock()

pygame.font.init()
FONT_SIZE = 20
FONT = pygame.font.SysFont('Arial', FONT_SIZE, bold=True)
TEXT_COLOR = (0, 0, 0)

pieces = {}
for filename in ['black-king.png', 'white-queen.png', 'white-king.png',
                'white-rook.png', 'black-rook.png', 'white-bishop.png',
                'black-bishop.png', 'white-knight.png', 'black-knight.png',
                'white-pawn.png', 'black-pawn.png']:
    try:
        key = filename[:-4]
        image = pygame.image.load(f"piezas/{filename}")
        pieces[key] = pygame.transform.scale(image, (SQ_SIZE, SQ_SIZE))
    except pygame.error as e:
        print(f"Advertencia: No se pudo cargar la imagen {filename}.")
        print(e)


def draw_board(selected_square=None):
    colors = [WHITE, BROWN]
    for r in range(8):
        for c in range(8):
            color = colors[(r + c) % 2]
            pygame.draw.rect(screen, color, pygame.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


    if selected_square is not None:
        col = chess.square_file(selected_square)
        row = 7 - chess.square_rank(selected_square)
        s = pygame.Surface((SQ_SIZE, SQ_SIZE), pygame.SRCALPHA)
        s.fill((0, 255, 0, 40))
        screen.blit(s, (col * SQ_SIZE, row * SQ_SIZE))

    for r in range(8):
        y_pos = r * SQ_SIZE + SQ_SIZE // 2 - FONT_SIZE // 2
        text_surface = FONT.render(str(8 - r), True, TEXT_COLOR)
        screen.blit(text_surface, (5, y_pos))

    for c in range(8):
        x_pos = c * SQ_SIZE + SQ_SIZE // 2 - FONT_SIZE // 4
        text_surface = FONT.render(chr(ord('a') + c), True, TEXT_COLOR)
        screen.blit(text_surface, (x_pos, HEIGHT - FONT_SIZE - 5))

def draw_pieces(board):
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            row = 7 - (square // 8)
            col = square % 8
            color_str = 'white' if piece.color == chess.WHITE else 'black'
            type_str = {
                'K': 'king',
                'Q': 'queen',
                'R': 'rook',
                'B': 'bishop',
                'N': 'knight',
                'P': 'pawn',
            }.get(piece.symbol().upper(), None)
            if type_str:
                key = f"{color_str}-{type_str}"
                if key in pieces:
                    screen.blit(pieces[key], pygame.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

PIECE_VALUES = {
    chess.KING: 0,
    chess.QUEEN: 9,
    chess.ROOK: 5,
    chess.BISHOP: 3,
    chess.KNIGHT: 3,
    chess.PAWN: 1,
}

def evaluate_board(board):
    if board.is_checkmate():
        return 9999 if board.turn == chess.BLACK else -9999
    elif board.is_stalemate() or board.is_insufficient_material():
        return 0

    value = 0
    white_king_sq = None
    black_king_sq = None

    for sq in chess.SQUARES:
        piece = board.piece_at(sq)
        if piece:
            val = PIECE_VALUES.get(piece.piece_type, 0)
            if piece.color == chess.WHITE:
                value += val
                if piece.piece_type == chess.KING:
                    white_king_sq = sq
            else:
                value -= val
                if piece.piece_type == chess.KING:
                    black_king_sq = sq

    if black_king_sq:
        row, col = divmod(black_king_sq, 8)

        if (row in [0, 7]) and (col in [0, 7]):
            value += 2

        black_king_mobility = 0
        temp_board = board.copy()
        for move in temp_board.legal_moves:
            if temp_board.piece_at(move.from_square) == chess.Piece(chess.KING, chess.BLACK):
                black_king_mobility += 1
        value -= 0.3 * black_king_mobility

        for sq in chess.SQUARES:
            piece = board.piece_at(sq)
            if piece and piece.color == chess.WHITE:
                dist = chess.square_distance(sq, black_king_sq)
                value += max(0, (7 - dist) * 0.2)

        if white_king_sq:
            dist = chess.square_distance(white_king_sq, black_king_sq)
            value += max(0, (7 - dist) * 0.3)

    return value

def minimax(board, depth, alpha, beta, is_maximizing):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board), None

    best_move = None
    if is_maximizing:
        max_eval = -float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval, _ = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval, _ = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move

def main():
    board = chess.Board(None)

    board.set_piece_at(chess.E1, chess.Piece(chess.KING, chess.WHITE))
    board.set_piece_at(chess.D1, chess.Piece(chess.QUEEN, chess.WHITE))

    board.set_piece_at(chess.E8, chess.Piece(chess.KING, chess.BLACK))
    board.turn = chess.BLACK

    player_turn = True
    selected_square = None
    valid_moves_for_selected_piece = []

    running = True
    game_over_display = False
    game_result_printed = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and player_turn and not game_over_display:
                x, y = pygame.mouse.get_pos()
                col = x // SQ_SIZE
                row = y // SQ_SIZE
                square = chess.square(col, 7 - row)
                piece = board.piece_at(square)

                if selected_square is None:
                    if piece and piece.color == chess.BLACK:
                        selected_square = square
                        valid_moves_for_selected_piece = [m for m in board.legal_moves if m.from_square == square]
                else:
                    move = chess.Move(selected_square, square)
                    if move in valid_moves_for_selected_piece:
                        print(f"Jugador (Negras): {board.san(move)}")
                        board.push(move)
                        player_turn = False
                    selected_square = None
                    valid_moves_for_selected_piece = []


        if not game_over_display:
            if not player_turn and not board.is_game_over():
                _, move = minimax(board, depth=4, alpha=-float('inf'), beta=float('inf'), is_maximizing=True)
                if move:
                    print(f"IA (Blancas): {board.san(move)}")
                    board.push(move)
                player_turn = True

            if board.is_checkmate():
                game_over_display = True
                if not game_result_printed:
                    print("Las piezas blancas han dado jaque mate.")
                    game_result_printed = True
            elif board.is_stalemate():
                game_over_display = True
                if not game_result_printed:
                    print("Rey ahogado")
                    game_result_printed = True
            elif board.is_insufficient_material():
                game_over_display = True
                if not game_result_printed:
                    print("Empate - Tablas")
                    game_result_printed = True

        draw_board(selected_square)
        draw_pieces(board)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

