import pygame
import math

# Constants for representing the players and empty cells
EMPTY = "-"
PLAYER_X = "X"
PLAYER_O = "O"

# Initialize Pygame
pygame.init()

# Set up the game window
width = 600
height = 650  # Increased height to accommodate the status message
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Kaushik vs Computer")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
light_gray = (200, 200, 200)
background_color = (30, 30, 30)

# Board size and cell dimensions
board_size = 3
cell_size = width // board_size

# Font for displaying text
font = pygame.font.Font(None, 100)
small_font = pygame.font.Font(None, 50)

# Function to draw the game board
def draw_board(board, winning_combination=None):
    for i in range(board_size):
        for j in range(board_size):
            x = j * cell_size
            y = i * cell_size + 50  # Adjust y position to leave space at the top
            rect_color = light_gray if (i + j) % 2 == 0 else white
            pygame.draw.rect(screen, rect_color, (x, y, cell_size, cell_size))
            
            cell_center = (x + cell_size // 2, y + cell_size // 2)
            if board[i * board_size + j] == PLAYER_X:
                text = font.render("X", True, red)
                text_rect = text.get_rect(center=cell_center)
                screen.blit(text, text_rect)
            elif board[i * board_size + j] == PLAYER_O:
                text = font.render("O", True, blue)
                text_rect = text.get_rect(center=cell_center)
                screen.blit(text, text_rect)
    
    if winning_combination:
        for index in winning_combination:
            x = (index % board_size) * cell_size
            y = (index // board_size) * cell_size + 50  # Adjust y position to leave space at the top
            pygame.draw.rect(screen, green, (x, y, cell_size, cell_size), 5)

# Function to check if a player has won
def check_winner(board):
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
        [0, 4, 8], [2, 4, 6]  # diagonals
    ]

    for combination in winning_combinations:
        if board[combination[0]] == board[combination[1]] == board[combination[2]] != EMPTY:
            return board[combination[0]], combination

    if EMPTY not in board:
        return "tie", None

    return None, None

# Function to evaluate the game board
def evaluate(board):
    winner, _ = check_winner(board)

    if winner == PLAYER_X:
        return 1
    elif winner == PLAYER_O:
        return -1
    else:
        return 0

# Minimax function with alpha-beta pruning
def minimax(board, depth, alpha, beta, maximizing_player):
    winner, _ = check_winner(board)
    if winner is not None or depth == 0:
        return evaluate(board)

    if maximizing_player:
        max_eval = -math.inf
        for i in range(9):
            if board[i] == EMPTY:
                board[i] = PLAYER_X
                eval_score = minimax(board, depth - 1, alpha, beta, False)
                board[i] = EMPTY
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
        return max_eval
    else:
        min_eval = math.inf
        for i in range(9):
            if board[i] == EMPTY:
                board[i] = PLAYER_O
                eval_score = minimax(board, depth - 1, alpha, beta, True)
                board[i] = EMPTY
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
        return min_eval

# Function to find the best move using minimax with alpha-beta pruning
def find_best_move(board):
    best_score = -math.inf
    best_move = None

    for i in range(9):
        if board[i] == EMPTY:
            board[i] = PLAYER_X
            move_score = minimax(board, 9, -math.inf, math.inf, False)
            board[i] = EMPTY

            if move_score > best_score:
                best_score = move_score
                best_move = i

    return best_move

# Function to display restart button
def display_restart_button():
    restart_text = small_font.render("Restart", True, white)
    restart_rect = restart_text.get_rect(center=(width // 2, height - 50))
    pygame.draw.rect(screen, red, restart_rect.inflate(20, 10))
    screen.blit(restart_text, restart_rect)
    return restart_rect

# Game board
board = [EMPTY] * 9

# Game loop
running = True
game_over = False
winning_combination = None
while running:
    screen.fill(background_color)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX = event.pos[0]
            mouseY = event.pos[1]

            if height - 100 < mouseY < height and game_over:
                # Restart the game
                board = [EMPTY] * 9
                game_over = False
                winning_combination = None
            else:
                clicked_row = (mouseY - 50) // cell_size  # Adjust for top space
                clicked_col = mouseX // cell_size
                if clicked_row >= 0 and clicked_row < board_size and board[clicked_row * board_size + clicked_col] == EMPTY:
                    clicked_index = clicked_row * board_size + clicked_col

                    if board[clicked_index] == EMPTY:
                        board[clicked_index] = PLAYER_O
                        winner, winning_combination = check_winner(board)
                        if winner is not None:
                            game_over = True
                        else:
                            # AI's turn
                            ai_move = find_best_move(board)
                            board[ai_move] = PLAYER_X
                            winner, winning_combination = check_winner(board)
                            if winner is not None:
                                game_over = True

    draw_board(board, winning_combination)

    # Display game status message at the top of the screen
    if game_over:
        if winner == "tie":
            text = font.render("It's a tie!", True, white)
        else:
            text = font.render("Player " + winner + " wins!", True, white)
        text_rect = text.get_rect(center=(width // 2, 25))  # Adjust position to be at the top
        screen.blit(text, text_rect)
        restart_button_rect = display_restart_button()

    pygame.display.flip()

pygame.quit()
