# Sudoku game
# play by rules of sudoku, if you don't know them, look them



def main():
    grid = [
        [0, 0, 7, 0, 9, 0, 4, 0, 8],
        [0, 1, 0, 0, 0, 3, 0, 9, 6],
        [4, 0, 0, 7, 8, 0, 1, 0, 0],
        [6, 2, 0, 0, 1, 9, 0, 0, 0],
        [3, 0, 8, 0, 0, 0, 9, 0, 1],
        [0, 0, 0, 6, 7, 0, 0, 4, 3],
        [0, 0, 6, 0, 4, 1, 0, 0, 9],
        [9, 4, 0, 8, 0, 0, 0, 2, 0],
        [2, 0, 5, 0, 3, 0, 6, 0, 0]]

    # converts grid of numbers to sudoku puzzle
    board = convert_board(grid)

    while is_not_solved(board):
        # displays board and allows player to make moves
        display(board)
        make_move(board)

    print("congratulations! you won at sudoku!")

#checks if game has been solved or not, returns true if any spaces are empty
def is_not_solved(board):
    if any(0 in x for x in board):
        return True
    return False


def display(board):
    # displays layout for sudoku board, lots of unicode in here, tread carefully
    ycount = 0
    xcount = 0
    for x in board:
        for y in x:
            if y != 0:
                ycount += 1
                if ycount % 3 == 0 and ycount != 9:
                    if type(y) == str:
                        print("\x1b[1;31;00m" + y + "\x1b[0m", end="\x1b[1;34;00m" + " || " + "\x1b[0m")
                    else:
                        print(y, end="\x1b[1;34;00m" + " || " + "\x1b[0m")
                elif ycount % 9 == 0:
                    if type(y) == str:
                        print("\x1b[1;31;00m" + y + "\x1b[0m")
                    else:
                        print(y)
                else:
                    if type(y) == str:
                        print("\x1b[1;31;00m" + y + "\x1b[0m", end=" | ")
                    else:
                        print(y, end=" | ")
            else:
                ycount += 1
                if ycount % 3 == 0 and ycount != 9:
                    print(" ", end="\x1b[1;34;00m" + " || " + "\x1b[0m")
                elif ycount % 9 == 0:
                    print(" ")
                else:
                    print(" ", end=" | ")
        xcount += 1
        if xcount % 3 == 0 and xcount != 9:
            print("\x1b[1;34;00m" + "-----------------------------------" + "\x1b[0m")
        elif xcount != 9:
            print("-----------------------------------")
        ycount = 0


# allows player to put move, also validates input from user
def make_move(board):
    checker = False

    while not checker:
        # collecting userinput, x, y, move
        uinput = input("enter a board location in x, y, move format")

        # creates a list which is split b
        input_list = uinput.split(",")

        # storing input as list and removing white s
        move = [int(x.strip()) for x in input_list]

        # if user entered move in correct format, check move against sudoku rules
        if validate_input(move):
            checker = sudoku_check(board, move[0] - 1, move[1] - 1, move[2])

    # actually commits the move to the board and changes the array
    board[move[1] - 1][move[0] - 1] = move[2]
    print("\n")
    return board

# checks to make sure user entered correct number of variables in input string
def validate_input(move_list):
    # validating input: user can only enter numbers 1-9
    for x in move_list:
        if x < 0 or x > 9:
            print("not a valid move, enter any number between 1 and 9")
            return False

    # check if correct number of ints in list
    if len(move_list) != 3:
        print("not correct move format, please enter: x, y, move")
        return False

    return True


# checks if both row/col and 3x3 rules are holding up
def sudoku_check(board, x, y, move):
    row_col_check = row_checker(board, x, y, move)
    box_check = box_checker(board, x, y, move)
    if not row_col_check or not box_check:
        return False
    else:
        return True


# checks each 3x3 box to see if they contain only the numbers 1-9, each occurring only once
def box_checker(board, x, y, move):
    row = 0
    col = 0
    box = []

    # add in user input
    board[y][x] = move


    # checking each box
    for n in range(3):
        for k in range(3):
            for i in range(row, row + 3):
                for j in range(col, col + 3):
                    if board[i][j] != 0:
                        # if the number appears in the 3x3, add it to the box list
                        box.append(board[i][j])

            # check if duplicates in 3x3 square
            if check_for_dup(box, 0):
                print("there is already a", move, "in that 3x3 box")
                return False

            # change column
            col += 3
            # clear box for next loop
            box.clear()
        row += 3
        col = 0

    # clear user input for now, until input is validated
    board[y][x] = 0
    return True


# check for duplicates in a list, returns false if no duplicates
def check_for_dup(slist, move):
    # converts all items to numbers and adds in the move the player made
    slist = [int(x) for x in slist]
    slist.append(move)

    # removes zeros from list
    while 0 in slist:
        slist.remove(0)

    # checks for duplicates by converting to a set and checking if the length of the set
    # is the same as the length of the list
    if len(slist) != len(set(slist)):
        # returns true if there were duplicates
        return True
    return False


# checks if there is only the numbers 1-9 in every row and column, with each number only appearing once
def row_checker(board, x, y, move):
    # makes a list from the column that the move was made in
    col = [i[x] for i in board]

    # makes a list from the row the move was made in
    row = board[y]

    # checks for duplicates in column
    if check_for_dup(col, move):
        print("There is already a", move, "in that column")
        return False

    # checks for duplicates in row
    if check_for_dup(row, move):
        print("There is already a", move, "in that row")
        return False

    # if neither have duplicates, returns true
    return True


# converts preset numbers in board to strings for formatting
def convert_board(board):
    for x in range(len(board)):
        for y in range(len(board)):
            if board[x][y] != 0:
                board[x][y] = str(board[x][y])

    return board


if __name__ == "__main__":
    main()