import tkinter as tk
from tkinter import messagebox,simpledialog, Radiobutton, Label, Button
import time
from math import inf as infinity

HUMAN = -1
COMP = +1
board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]


# Function to heuristic evaluation of state. return: +1 if the computer wins; -1 if the human wins; 0 draw
def evaluate(state):

    if wins(state, COMP):
        score = +1
    elif wins(state, HUMAN):
        score = -1
    else:
        score = 0

    return score

# This function tests if a specific player wins. 
def wins(state, player):
    win_state = [
        [state[0][0], state[0][1], state[0][2]],
        [state[1][0], state[1][1], state[1][2]],
        [state[2][0], state[2][1], state[2][2]],
        [state[0][0], state[1][0], state[2][0]],
        [state[0][1], state[1][1], state[2][1]],
        [state[0][2], state[1][2], state[2][2]],
        [state[0][0], state[1][1], state[2][2]],
        [state[2][0], state[1][1], state[0][2]],
    ]
    if [player, player, player] in win_state:
        return True
    else:
        return False

# This function test if the human or computer wins.
def game_over(state):
  
    return wins(state, HUMAN) or wins(state, COMP)

# Each empty cell will be added into cells list.
def empty_cells(state):

    cells = []
    for x, row in enumerate(state):
        for y, cell in enumerate(row):
            if cell == 0:
                cells.append([x, y])

    return cells

# A move is valid if the chosen cell is empty.
def valid_move(x, y):

    if [x, y] in empty_cells(board):
        return True
    else:
        return False

# Set the move on board, if the coordinates are valid.
def set_move(x, y, player):
   
    if valid_move(x, y):
        board[x][y] = player
        return True
    else:
        return False

# AI function that choice the best move
def minimax(state, depth, player):
    # Initialize the best move with default values.
    if player == COMP:
        best = [-1, -1, -infinity]
    else:
        best = [-1, -1, +infinity]

    # return the score of the board.
    if depth == 0 or game_over(state):
        score = evaluate(state)
        return [-1, -1, score]

    # Explore each possible move on the board.
    for cell in empty_cells(state):
        x, y = cell[0], cell[1]
        
        # Make a move for the current player.
        state[x][y] = player

        # Recursively call minimax for the next player (-player switches between HUMAN and COMP).
        score = minimax(state, depth - 1, -player)

        # Undo the move to backtrack and try other possibilities.
        state[x][y] = 0
        score[0], score[1] = x, y

        # Update the best move if a better score is found.
        # For COMP, we maximize the score; for HUMAN, we minimize the score.
        if player == COMP:
            if score[2] > best[2]:
                best = score  # max value
        else:
            if score[2] < best[2]:
                best = score  # min value

    # Return the best move found for the current player.
    return best


# Tkinter GUI functions
# Handle a button click event for player's move.

def on_button_click(x, y):
    # Check if the move is valid and the game is not over. If so, make the human's move.
    if valid_move(x, y) and not game_over(board):
        set_move(x, y, HUMAN)
        update_board()
        if game_over(board) or not empty_cells(board):
            end_game()
            return

        root.update()
        time.sleep(0.5)
        ai_turn()
        update_board()
        if game_over(board) or not empty_cells(board):
            end_game()
# AI takes its turn using the minimax algorithm.
def ai_turn():
    depth = len(empty_cells(board))
    if depth == 0 or game_over(board):
        return

    move = minimax(board, depth, COMP)
    x, y = move[0], move[1]
    set_move(x, y, COMP)

# Update the board on the GUI.
def update_board():
    for x, row in enumerate(board):
        for y, cell in enumerate(row):
            if cell == COMP:
                buttons[x][y].config(text="X" if COMP == +1 else "O")
            elif cell == HUMAN:
                buttons[x][y].config(text="O" if HUMAN == -1 else "X")
# Handle the end of the game, display result and ask to play again.
def end_game():
    if wins(board, HUMAN):
        winner = "Human"
        messagebox.showinfo("Game Over", f"{winner} wins!")
    elif wins(board, COMP):
        winner = "Computer"
        messagebox.showinfo("Game Over", f"{winner} wins!")
    else:
        winner = "No one, it's a draw"
        messagebox.showinfo("GameOver", "DRAW!")
    
    if messagebox.askyesno("Play again", "Do you want to play again?"):
        reset_game()
    else:
        root.destroy()
# Reset the game to the initial state.
def reset_game():
    global board
    board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    for x in range(3):
        for y in range(3):
            buttons[x][y].destroy()  # Destroy the game buttons
    create_start_screen()

# Initialize the game based on player's choice (X or O).
def initialize_game():
    global HUMAN, COMP
    choice = simpledialog.askstring("Input", "Choose X or O (X goes first)", parent=root)
    if choice and choice.upper() == "O":
     
        HUMAN = +1
        COMP = -1

    elif choice and choice.upper() == "X":
       
        HUMAN = -1
        COMP = +1
    if COMP == +1:
        ai_turn()
        update_board()



# Start the game based on player's choice from start screen.
def start_game():
    global HUMAN, COMP
    player_choice = symbol_choice.get()
    if player_choice == "O":
        
        HUMAN = -1
        COMP = +1

    else:
        HUMAN = +1
        COMP = -1
        
    for widget in root.winfo_children():
        widget.destroy()

    create_game_board()
    if COMP == +1:
        ai_turn()
        update_board()

# Create the game board with buttons in the GUI.
def create_game_board():
    global buttons
    buttons = []
    for x in range(3):
        row = []
        for y in range(3):
            button = tk.Button(root, text="", font=('normal', 40), width=5, height=2,
                            command=lambda x=x, y=y: on_button_click(x, y))
            button.grid(row=x, column=y)
            row.append(button)
        buttons.append(row)

# Set the symbol choice (X or O) for the player.
def select_symbol(symbol):
    symbol_choice.set(symbol)
# Create the start screen for symbol selection.
def create_start_screen():
     for widget in root.winfo_children():
        widget.destroy()

     Label(root, text="Choose your symbol(X is first):", font=('normal', 14)).grid(row=0, column=0, columnspan=2, pady=10)
     Button(root, text="X", font=('normal', 14), width=3 , command=lambda: select_symbol("X")).grid(row=1, column=0, padx=10, pady=10)
     Button(root, text="O", font=('normal', 14), width=3 , command=lambda: select_symbol("O")).grid(row=1, column=1, padx=10, pady=10)
     Button(root, text="Start Game", font=('normal', 14), command=start_game).grid(row=2, column=0, columnspan=2, pady=20)

# Main Tkinter window setup
root = tk.Tk()
root.title("Tic Tac Toe")

symbol_choice = tk.StringVar(value="X")  # Default choice is X
create_start_screen()
root.mainloop()


