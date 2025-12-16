import cv2 as cv
import numpy as np
import imutils
from skimage.segmentation import clear_border
from sudoku import Sudoku
import pytesseract

capture = cv.imread("sudoku.png")
grayscale = cv.cvtColor(capture, cv.COLOR_BGR2GRAY)
# pytesseract.pytesseract.tesseract_cmd = r'{enter the file path of your tesseract executable here}'
solved = capture.copy()

class Processor:
    def __init__(self, image):
        # Bind the following variables to their appropriate values for the Processor class:
        # self.image, self.board, self.stepX, self.stepY, self.empties
        # DO NOT CHANGE THE INITIAL PARAMETERS OF THE __init__ function
        pass


    def get_digit(cell, debug=False):

        # Given the variables "lower" and "upper", what should the value of these variables be?
        lower = None
        upper = None


        thresh = cv.threshold(cell, lower, upper, cv.THRESH_BINARY | cv.THRESH_OTSU)[1]
        thresh = clear_border(thresh)

        # Find the and grab the contours of the thresholded cell
        thresh_copy = None

        # What contour hierarchy flag do you need to get just the parent contours?
        flag = None

        contours = cv.findContours(thresh_copy, flag, cv.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        

        mask = np.zeros(thresh.shape, dtype="uint8")
        
        # Ensure that contours exist

        # Get the largest contour by area, defined by the variable "major"
        major = max(contours, key=cv.contourArea)
        cv.drawContours(mask, [major], -1, 255, -1)
        
        # Get the height and width of the thresholded cell
        (h, w) = None

        # Get the percent of all pixels filled in a cell
        percentFilled = cv.countNonZero(mask) / float(w * h)
        
        # If less than 3% of the cell is filled, then return None as it will not output a valid digit
        
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
                startX = None
                startY = None

                # Get the ending value for the pixel intervals
                endX = None
                endY = None

                row.append((startX, startY, endX, endY))

                # Get the cell corresponding to the starting and ending intervals at some cell at (x, y)
                cell = None
                digit = None
                
                if digit is not None:
                    digit = cv.resize(digit, (28, 28))

                    # Extract the text from the cell
                    text = None

                    # Check if the cell holds a string, and only perform the next operation if a string is present
                    # Replace the value of a specified cell at (x, y) in the currently empty board with the value on the cell image
                    
                else:
                    # Add the cell to the empties list
                    pass

                cells.append(row)

    def solve_puzzle(self):
        # Write the lines of code that uses the Sudoku object from another Python file and solves the Sudoku puzzle.
        pass

    def insert_values(self):
        # Write the lines of code to go over and put text on empty cells that represent the correct values to place in them
        pass


while True:
        
    blurred = cv.GaussianBlur(grayscale, (5, 5), 0)
    threshold = cv.threshold(blurred, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)[1]
    processor = Processor(threshold)

    result = processor.insert_values()

    cv.imshow("Sudoku", result)
    key = cv.waitKey(0) & 0xFF

    if key == ord('q'):
        break
