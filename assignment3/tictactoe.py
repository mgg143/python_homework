#Task 6: More on Classes
'''
Within the assignment3 folder, create a file called tictactoe.py.

Within this file, declare a class called TictactoeException. This should inherit from the Exception class. Add an __init__ method 
that stores an instance variable called message and then calls the __init__ method of the superclass. This is a common way of creating 
a new type of exception.

Declare also a class called Board. This should have an __init__ function that only has the self argument. It creates a list of lists, 3x3, all 
git containing " " as a value. This is stored in the variable self.board_array. Create instance variables self.turn, which is initialized to "X".
The Board class should have a class variable called valid_moves, with the value:

    valid_moves=["upper left", "upper center", "upper right", "middle left", "center", "middle right", "lower left", "lower center", "lower right"]

Add a __str__() method. This converts the board into a displayable string. You want it to show the current state of the game. The rows to be 
displayed are separated by newlines ("\n") and you also want some "|" amd "-" characters. Once you have created this method, you can display 
the board by doing a print(board).

Add a move() method. This has two arguments, self and move_string. The following strings are valid in TicTacToe: "upper left", "upper center", "upper
right", "middle left", "center", "middle right", "lower left", "lower center", and "lower right". When a string is passed, the move() method will 
check if it is one of these, and if not it will raise a TictactoeException with the message "That's not a valid move.". Then the move() method 
will check to see if the space is taken. If so, it will raise an exception with the message "That spot is taken." If neither is the case, the 
move is valid, the corresponding entry in board_array is updated with X or O, and the turn value is changed from X to O or from O to X. It 
also updates last_move, which might make it easier to check for a win.

Add a whats_next() method. This will see if the game is over. If there are 3 X's or 3 O's in a row, it returns a tuple, where the first value is 
True and the second value is either "X has won" or "O has won". If the board is full but no one has won, it returns a tuple where the first value 
is True and the second value is "Cat's Game". Otherwise, it returns a tuple where the first value is False and the second value is either "X's turn"
or "O's turn".

Implement the game within the mainline code of tictactoe.py. At the start of the game, an instance of the board class is created, and then 
the methods of the board class are used to progress through the game. Use the input() function to prompt for each move, indicating whose turn 
it is. Note that you need to call board.move() within a try block, with an except block for TictactoeException. Give appropriate information to 
the user.

Test your program by playing a few games.

On assembling this program, the assignment author found that it was too time consuming to write some of the methods.  So, here are some pieces to reuse.
Please make sure you understand them.

    def __str__(self):
        lines=[]
        lines.append(f" {self.board_array[0][0]} | {self.board_array[0][1]} | {self.board_array[0][2]} \n")
        lines.append("-----------\n")
        lines.append(f" {self.board_array[1][0]} | {self.board_array[1][1]} | {self.board_array[1][2]} \n")
        lines.append("-----------\n")
        lines.append(f" {self.board_array[2][0]} | {self.board_array[2][1]} | {self.board_array[2][2]} \n")
        return "".join(lines)
    
    def move(self, move_string):
        if not move_string in Board.valid_moves:
            raise TictactoeException("That's not a valid move.")
        move_index = Board.valid_moves.index(move_string)
        row = move_index // 3 # row
        column = move_index % 3 #column
        if self.board_array[row][column] != " ":
            raise TictactoeException("That spot is taken.")
        self.board_array[row][column] = self.turn
        if self.turn == "X":
            self.turn = "O"
        else:
            self.turn = "X"
    
    def whats_next(self):
        cat = True
        for i in range(3):
            for j in range(3):
                if self.board_array[i][j] == " ":
                    cat = False
                else:
                    continue
                break
            else:
                continue
            break
        if (cat):
            return (True, "Cat's Game.")
        win = False
        for i in range(3): # check rows
            if self.board_array[i][0] != " ":
                if self.board_array[i][0] == self.board_array[i][1] and self.board_array[i][1] == self.board_array[i][2]:
                    win = True
                    break
        if not win:
            for i in range(3): # check columns
                if self.board_array[0][i] != " ":
                    if self.board_array[0][i] == self.board_array[1][i] and self.board_array[1][i] == self.board_array[2][i]:
                        win = True
                        break
        if not win:
            if self.board_array[1][1] != " ": # check diagonals
                if self.board_array[0][0] ==  self.board_array[1][1] and self.board_array[2][2] == self.board_array[1][1]:
                    win = True
                if self.board_array[0][2] ==  self.board_array[1][1] and self.board_array[2][0] == self.board_array[1][1]:
                    win = True
        if not win:
            if self.turn == "X": 
                return (False, "X's turn.")
            else:
                return (False, "O's turn.")
        else:
            if self.turn == "O":
                return (True, "X wins!")
            else:
                return (True, "O wins!")
'''

class TictactoeException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)

class Board:
    valid_moves=["upper left", "upper center", "upper right", "middle left", "center", "middle right", "lower left", "lower center", "lower right"]
    def __init__(self):
        self.board_array = [[" ", " ", " "] for _ in range(3)]
        self.turn = "X"
        self.last_move = None
    def __str__(self):
        lines=[]
        lines.append(f" {self.board_array[0][0]} | {self.board_array[0][1]} | {self.board_array[0][2]} \n")
        lines.append("-----------\n")
        lines.append(f" {self.board_array[1][0]} | {self.board_array[1][1]} | {self.board_array[1][2]} \n")
        lines.append("-----------\n")
        lines.append(f" {self.board_array[2][0]} | {self.board_array[2][1]} | {self.board_array[2][2]} \n")
        return "".join(lines)
    def move(self, move_string):
        if not move_string in Board.valid_moves:
            raise TictactoeException("That's not a valid move.")
        move_index = Board.valid_moves.index(move_string)
        row = move_index // 3 # row
        column = move_index % 3 #column
        if self.board_array[row][column] != " ":
            raise TictactoeException("That spot is taken.")
        self.board_array[row][column] = self.turn
        self.last_move = (row, column)
        if self.turn == "X":
            self.turn = "O"
        else:
            self.turn = "X"
    def whats_next(self):
        cat = True
        for i in range(3):
            for j in range(3):
                if self.board_array[i][j] == " ":
                    cat = False
                else:
                    continue
                break
            else:
                continue
            break
        if (cat):
            return (True, "Cat's Game.")
        win = False
        for i in range(3): # check rows
            if self.board_array[i][0] != " ":
                if self.board_array[i][0] == self.board_array[i][1] and self.board_array[i][1] == self.board_array[i][2]:
                    win = True
                    break
        if not win:
            for i in range(3): # check columns
                if self.board_array[0][i] != " ":
                    if self.board_array[0][i] == self.board_array[1][i] and self.board_array[1][i] == self.board_array[2][i]:
                        win = True
                        break
        if not win:
            if self.board_array[1][1] != " ": # check diagonals
                if self.board_array[0][0] ==  self.board_array[1][1] and self.board_array[2][2] == self.board_array[1][1]:
                    win = True
                if self.board_array[0][2] ==  self.board_array[1][1] and self.board_array[2][0] == self.board_array[1][1]:
                    win = True
        if not win:
            if self.turn == "X": 
                return (False, "X's turn.")
            else:
                return (False, "O's turn.")
        else:
            if self.turn == "O":
                return (True, "X wins!")
            else:
                return (True, "O wins!")
    
if __name__ == "__main__":
    # 1. Create the instance of the board
    game_board = Board()
    game_over = False

    print("Welcome to Tic-Tac-Toe!")
    
    # 2. Start the game loop
    while not game_over:
        print(game_board)  # This calls your __str__ method
        
        # 3. Check whose turn it is
        status, message = game_board.whats_next()
        print(message)
        
        print(f"Here are the valid moves: {', '.join(Board.valid_moves)}")
        move = input("Please enter your move (e.g., 'center', 'upper left'): ").lower().strip()
        
        # 4. Try to make the move
        try:
            game_board.move(move)
            
            # 5. Check if the game ended after the move
            game_over, final_message = game_board.whats_next()
            if game_over:
                print(game_board)
                print("Game Over!")
                print(final_message)
                
        except TictactoeException as e:
            print(f"\n*** ERROR: {e.message} ***\n")