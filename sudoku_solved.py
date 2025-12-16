import time

class Sudoku:
    def __init__(self, matrix):
        # Write the one-liner code to initialize the matrix in the Sudoku class
        # Be sure to replace the 'pass' word below with your code
        self.matrix = matrix
    
    def next_empty(self):
        # Find the first empty cell of a Sudoku matrix using 2D nested iteration
        # Be sure to replace the 'pass' word below with your code
        for i in range(9):
            for j in range(9):
                if self.matrix[i][j] == 0:
                    return i, j
        return None, None
        

    def can_put(self, number, i, j):

        # Write 2 conditions that return False if a number exists in the row/column of a cell
        if number in self.matrix[i]:
            return False
        if number in [self.matrix[k][j] for k in range(9)]:
            return False
        # Get the starting rows and columns for a cell block, given the coordinates at i and j

        row_start = (i // 3) * 3
        col_start = (j // 3) * 3

        for i in range(3):
            for j in range(3):
                # Check if a number exists in the cell block location, return False if so.
                if self.matrix[row_start+i][col_start+j] == number:
                    return False
                
        return True
    
    def solve(self):

        # Get the row and column values of an empty cell
        row, col = self.next_empty()
        # Check if all empty cells have been covered, if so then the Sudoku board is solved
        if row == None:
            return True
        # Get the starting rows and columns for a cell block, given cell coordinates at i and j
        row_start = (row // 3) * 3
        col_start = (col // 3) * 3
        # Get the cell block
        cell_block = [array[j+col_start] for j in range(3) for array in self.matrix[row_start:row_start+3]]
        # Get all numbers that are not in a cellblock
        cell_candidates = [number for number in range(1, 10) if number not in cell_block]
        # Iterate over all numbers that are not in the cell block
        for candidate in cell_candidates:
            # Determine if a number can be placed in an empty cell
            if self.can_put(candidate, row, col):
                
                # Set the value at the matrix to be equal to the number
                self.matrix[row][col] = candidate
                # Determine if solutions for the next possible empty cells can be found, if so then the Sudoku board can be solved
                if self.solve():
                    return True
                # Reset the empty cell's value to be 0 and continue on to the next number in the iteration object
                self.matrix[row][col] = 0

        # Return false if Sudoku board is unsolvable, this happens when no number suffices for placement in an empty cell
        return False


    
matrix = [
[ 1, 0, 0, 0, 0, 0, 0, 0, 6 ],
[ 0, 2, 0, 0, 0, 0, 0, 5, 0 ],
[ 0, 0, 3, 0, 0, 0, 4, 0, 0 ],
[ 0, 0, 0, 0, 7, 0, 0, 0, 0 ],
[ 9, 8, 7, 0, 5, 0, 3, 2, 1 ],
[ 0, 0, 0, 0, 9, 0, 0, 0, 0 ],
[ 0, 0, 4, 0, 3, 0, 7, 0, 0 ],
[ 0, 5, 0, 0, 2, 0, 0, 8, 0 ],
[ 6, 0, 0, 0, 1, 0, 0, 0, 9 ]]

sudoku = Sudoku(matrix)

start = time.perf_counter()
print(sudoku.solve())
print(matrix)
end = time.perf_counter()
dur1 = end - start
print("ELAPSED (in ms): ", (dur1)*1000)


