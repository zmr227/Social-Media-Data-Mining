# sudoku solver module

# define a default sudoku board for testing
default = [[0 ,0 ,0 ,3 ,0 ,0 ,2 ,0 ,0 ],  
            [0 ,0 ,0 ,0 ,0 ,8 ,0 ,0 ,0 ],
            [0 ,7 ,8 ,0 ,6 ,0 ,3 ,4 ,0 ],
            [0 ,4 ,2 ,5 ,1 ,0 ,0 ,0 ,0 ],
            [1 ,0 ,6 ,0 ,0 ,0 ,4 ,0 ,9 ],
            [0 ,0 ,0 ,0 ,8 ,6 ,1 ,5 ,0 ],
            [0 ,3 ,5 ,0 ,9 ,0 ,7 ,6 ,0 ],
            [0 ,0 ,0 ,7 ,0 ,0 ,0 ,0 ,0 ],
            [0 ,0 ,9 ,0 ,0 ,5 ,0 ,0 ,0 ]]

class SudokuSolver(object):
    
    def __init__(self, board):
        self.board = board

    # print out the sudoku board in particular format
    def printBoard(self):
        print("-------------------------")
        for x in range(9):
            if x % 3 == 0:
                print("-------------------------")
            for y in range(9):
                if y % 3 == 0:
                    print("|", end=" ")
                print(self.board[x][y], end=" ")
            print("|")
        print("-------------------------")
            
    # check if the user-defined sudoku board is valid
    def isValidSudoku(self):
        row = [-1]
        col = [-1]
        cell = [-1]

        for i in range(9):
            row.append(set())
            col.append(set())
            cell.append(set())
            
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] != 0:
                    n = self.board[i][j]
                    k = (i // 3) * 3 + (j // 3)
                    if i in row[n] or j in col[n] or k in cell[n]:
                        return False
                    else:
                        row[n].add(i)
                        col[n].add(j)
                        cell[n].add(k)
        return True

    # check if all cells are filled with non-zero digits
    def allSolved(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] == 0:
                    return False
        return True

    # figure out all possible solution for a particular cell in terms of a dictionary
    # valid[i] == 0 means board[x][y] cannot be set to i
    def checkValid(self, x, y):
        if not self.board: return False
        valid = {}
        for i in range(1, 10):
            valid[i] = 1  # 1 means valid, 0 means invalid

        for j in range(9):
            # check row
            if self.board[x][j]: valid[self.board[x][j]] = 0
            # check col
            if self.board[j][y]: valid[self.board[j][y]] = 0

        # check 3*3 grid
        start_row = x - x % 3
        start_col = y - y % 3
        for i in range(3):
            for j in range(3):
                if self.board[start_row+i][start_col+j]:
                    valid[self.board[start_row+i][start_col+j]] = 0

        for i in range(1, 10):
            if valid[i]: valid[i] = i
        return valid
    
    # solve the given board with back tracking
    def solveSudoku(self):
        # check input validity
        if not self.isValidSudoku():
            print("Invalid input data.")
            return
        # print the solution board if it's solved
        if self.allSolved():
            print("Board Solved Successfully!")
            self.printBoard()
            return 
        
        # find the next zero cell to solve
        row, col = 0, 0
        for x in range (0, 9):
            for y in range (0, 9):
                if self.board[x][y] == 0:
                    row = x
                    col = y
                    break
                
        dic = {}
        dic = self.checkValid(row, col)
        for num in range(1, 10):
            if dic[num] != 0:
                self.board[row][col] = dic[num]
                self.solveSudoku()
        # back tracking
        self.board[row][col] = 0
        

# accept user inputs and check validity
def getInput():
        # by default, the unset cells will remain 0
        board = [[0 for _ in range(9)] for _ in range(9)]
        i = 0
        while i < 9:
            val = input("please type in row " + str(i+1) + ': ').split(" ")
            for idx, n in enumerate(val):
                if n.isdigit() and 0 <= int(n) <= 9:
                    board[i][idx] = int(n)
                else:
                    i -= 1  # re-enter this row
                    print("Error, input should be digits from 0 to 9.")
                    break
            i += 1
        print("Your input sudoku board looks like: \n")
        data = SudokuSolver(board)
        data.printBoard()

        return board

# allow user to choose from two input methods:
    # test the module with default data or type in their own sudoku board
def selectInputMethod():  
    print('*** 1: Use the default sudoku.')
    print('*** 2: Input your own sudoku, please seperate elements with space.\n')
    while True:
        choice = input('Please select an input method：1 or 2\n')
        if choice == '1':
            data = default
            break
        elif choice == '2':
            while True:
                data = getInput()
                check = input('Confirm? Y or N\n')
                if check == 'Y' or check == 'y':
                    break
            break
        else:
            print('Error, please enter 1 or 2.')
    return data

def main():
    try:
        sudoku = selectInputMethod()
        data = SudokuSolver(sudoku)
        data.printBoard()
        data.solveSudoku()
    except:
        print("Error")

if __name__ == "__main__":
    main()