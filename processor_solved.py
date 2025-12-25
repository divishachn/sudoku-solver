import cv2 as cv
import numpy as np
import imutils
from skimage.segmentation import clear_border
from sudoku import Sudoku
import pytesseract

capture = cv.imread("sudoku.png")
grayscale = cv.cvtColor(capture, cv.COLOR_BGR2GRAY)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
solved = capture.copy()

class Processor:
    def __init__(self, image):
        # Bind the following variables to their appropriate values for the Processor class:
        # self.image, self.board, self.stepX, self.stepY, self.empties
        # DO NOT CHANGE THE INITIAL PARAMETERS OF THE __init__ function
        self.image = image
        self.board = np.zeros((9, 9), dtype=np.uint8)
        self.stepX = self.image.shape[1] // 9
        self.stepY = self.image.shape[0] // 9
        self.empties = []

    def get_digit(self, cell, debug=False):

        # Given the variables "lower" and "upper", what should the value of these variables be?
        lower = 0
        upper = 255


        thresh = cv.threshold(cell, lower, upper, cv.THRESH_BINARY | cv.THRESH_OTSU)[1]
        thresh = clear_border(thresh)

        # Find the and grab the contours of the thresholded cell
        thresh_copy = thresh.copy()

        # What contour hierarchy flag do you need to get just the parent contours?
        flag = cv.RETR_EXTERNAL

        contours = cv.findContours(thresh_copy, flag, cv.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        

        mask = np.zeros(thresh.shape, dtype="uint8")
        
        # Ensure that contours exist
        if len(contours) == 0:
            return None
        # Get the largest contour by area, defined by the variable "major"
        major = max(contours, key=cv.contourArea)
        cv.drawContours(mask, [major], -1, 255, -1)
        
        # Get the height and width of the thresholded cell
        (h, w) = thresh.shape

        # Get the percent of all pixels filled in a cell
        percentFilled = cv.countNonZero(mask) / float(w * h)
        
        # If less than 3% of the cell is filled, then return None as it will not output a valid digit
        if (percentFilled < 0.03):
            return None

        digit = cv.bitwise_and(thresh, thresh, mask=mask)
        if debug == True:
            cv.imshow("Digit", digit)
            cv.waitKey(0)
        return digit
    
    def extract_board(self):
        cells = []

        for y in range(0, 9):
            row = []
            for x in range(0, 9):

                # Get the starting value for the pixel intervals
                startX = x * self.stepX 
                startY = y * self.stepY

                # Get the ending value for the pixel intervals
                endX = (x + 1) * self.stepX
                endY = (y + 1) * self.stepY

                row.append((startX, startY, endX, endY))

                # Get the cell corresponding to the starting and ending intervals at some cell at (x, y)
                cell = self.image[startY:endY, startX:endX]
                digit = self.get_digit(cell)
            
                #print(digit)

                if digit is not None:
                    digit = cv.resize(digit, (28, 28))

                    # Extract the text from the cell
                    text = pytesseract.image_to_string(digit, config="--psm 6 -c tessedit_char_whitelist=0123456789")

                    # Check if the cell holds a string, and only perform the next operation if a string is present
                    # Replace the value of a specified cell at (x, y) in the currently empty board with the value on the cell image
                    if text != "":
                        self.board[y, x] = int(text)

                else:
                    # Add the cell to the empties list
                    self.empties.append((y, x))

                cells.append(row)
        return self.board

    def solve_puzzle(self):
        # Write the lines of code that uses the Sudoku object from another Python file and solves the Sudoku puzzle.
        matrix = self.extract_board().tolist()
        sudoku_solver = Sudoku(matrix)
        sudoku_solver.solve()
        return matrix

    def insert_values(self):
        # Write the lines of code to go over and put text on empty cells that represent the correct values to place in them
        mat = self.solve_puzzle()
        print(mat)
        print(self.empties)
        for empty in self.empties:
            x, y = empty
            originX = self.stepX * x + (self.stepX // 2)
            originY = self.stepY * y + (self.stepY // 2)
            cv.putText(solved, str(mat[x][y]), (originY, originX), cv.FONT_HERSHEY_COMPLEX, 1, (0, 100, 0), 1)
        return solved



while True:
        
    blurred = cv.GaussianBlur(grayscale, (5, 5), 0)
    threshold = cv.threshold(blurred, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)[1]
    processor = Processor(threshold)

    result = processor.insert_values()

    cv.imshow("Sudoku", result)
    key = cv.waitKey(0) & 0xFF

    if key == ord('q'):
        break
