import copy  # Library for the function deep copy vital for iteration process
from datetime import datetime  # Library to calculate the duration of solution process
import itertools  # Library to get permutations
from PIL import ImageFont  # Library to create image (for export)
from PIL import Image  # Library to create image (for export)
from PIL import ImageDraw  # Library to create image (for export)
import re


class Sudoku(object):

    def __init__(self, data: str=None):

        self.clues = 0  # count the number of clues to define difficulty
        self.materix = {}
        self.count = 0
        self.step = 1
        # Start counting the time

        # Declare step variable

        # Dictionaries for index names, index, choices
        # all will be saved to the respective step
        self.index_name = {}
        self.index = {}
        self.choices = {}
        self.next_step = True
        self.data = data
        self.mainMatrix = self.get_matrix()
        if not self.mainMatrix[0]:
            raise ValueError(self.mainMatrix[1])

        # Save to the first step
        self.write_ex(self.mainMatrix, 0)
        self.write_ex(self.mainMatrix, 1)

    def finished(self, matrix, time, count, difficult):
        # Function to export the solution into the image

        font = ImageFont.truetype("arial.ttf", 40)
        # Define the font of the text

        text_red = "\n".join(
            "".join(
                f"  {matrix[row][column]}" for column in range(9)
            ) for row in range(9)
        )
        text_black = "\n".join(
            "".join(
                f"  {matrix[row][column]}" if self.materix[0][row][column] else "    " for column in range(9)
            ) for row in range(9)
        )
        long = 27
        # Count one line length to define the picture width

        height = 9
        # Count how many new lines to define picture height

        img = Image.new("RGBA", (long * 20, height * 70), (255, 255, 255))
        # Create the image
        # with white background

        draw = ImageDraw.Draw(img)
        draw.text((20, 20), text_red, (250, 0, 0), font=font)
        draw.text((20, 20), text_black, (0, 0, 0), font=font)
        # Draw the string of the sudoku solution

        for thick in range(4):
            # A loop for drawing thick lines between numbers

            draw.line((25, 20 + thick * 123) + (int(long * 16) - 8, 20 + thick * 123), fill=(0, 0, 0), width=3)
            # Draw horizontal lines

            draw.line((25 + thick * 133, 20) + (25 + thick * 133, 10 + height * 42), fill=(0, 0, 0), width=3)
            # Draw vertical lines

        for thin in range(10):
            # A loop for drawing thin lines between numbers

            draw.line((25, 20 + thin * int(123 / 3)) + (int(long * 16) - 8, 20 + thin * int(123 / 3)),
                      fill=(0, 0, 0),
                      width=1)
            # Draw horizontal lines

            draw.line((25 + thin * int(133 / 3) + 2, 20) + (25 + thin * int(133 / 3) + 2, 10 + height * 42),
                      fill=(0, 0, 0),
                      width=1)
            # Draw vertical lines

        text = f"""Solved in {time}
    {count} iterations taken.
    Difficulty: {difficult}"""
        # Create the text of the solution duration,
        # number of iterations and difficulty

        draw.text((20, height * 52), text, (0, 0, 0), font=font)
        # Write text

        img.save("Solved sudoku.png")

        return open("Solved sudoku.png", "rb")

    def get_matrix(self):
        # Import sudoku 2D array from Excel file

        matrix = []
        # Create 2D array
        # Define global variable clues to count difficulty of a puzzle
        if not self.data:
            return False, "Empty"
        else:
            rows = self.data.split("\n")
            if len(rows) != 9:
                return False, f"matrix incorrect {rows}"
            for row in rows:
                try:
                    matrix_row = list(map(int, re.findall("\d", row)))
                    if len(matrix_row) != 9:
                        raise ValueError
                    matrix.append(matrix_row)
                except ValueError:

                    return False, f"rows incorrect {row}"

        return matrix  # return the array

    def write_ex(self, matrix, step):
        self.materix[step] = copy.deepcopy(matrix)
        # Write the current solution to the dictionary for this step

    @staticmethod
    def choice_index(matrix):
        # Function to choose the row, column or 3x3 cell with maximum number of clues

        matrix_to_choose = []
        # Create the 1D array with maximum number of clues

        lines1, cols1, cells1 = 10, 10, 10
        line = [0]*9
        col = [0]*9
        cell = [0]*9
        # Initialise the 1D arrays samples

        index_name = ""
        index_col, index_line, index_cel, index = 10, 10, 10, 0
        # Initialise indexes

        for row in range(9):
            line[row] = matrix[row].count(0)
            # Check the lines, if zero element - increase the difficulty for this line

            lines2 = line[row]
            if lines2 < lines1 and lines2 != 0:
                lines1 = lines2
                # If number of zeros is lower, but not 0 - define a new index

                index_name = "line"
                # Index name needed afterwards to define the method of input the 1D array

                index = row
                index_line = lines1
                # Write the index

                matrix_to_choose = list(matrix[row])
                # Write the 1D array

        for row in range(0, 9):
            col[row] = matrix[row].count(0)
            # Check the columns for number of zero elements

        for column in range(0, 9):
            # Iterate through column-arrays to identify the least number of zero elements

            if col[column] < cols1 and col[column] != 0:
                cols1 = col[column]
                # If number of zeros is lower, but not 0 - define a new index

                if cols1 < index_line:
                    index_name = "col"
                    index = col.index(cols1)
                    index_col = cols1
                # Index name needed afterwards to define the method of input the 1D array

        if index_name == "col":
            matrix_to_choose = []
            for column in range(0, 9):
                matrix_to_choose.append(matrix[column][index - 1])
                # Write a 1D array of choice

        m_cel = [0] * 9
        # Initialise a sample 1D array for 3x3 cell

        for cell_index in range(0, 9):
            for cell_x in range(0, 3):
                x = cell_x + (cell_index // 3) * 3

                for cell_y in range(0, 3):
                    y = cell_y + (cell_index - (cell_index // 3) * 3) * 3
                    if matrix[x][y] == 0:
                        cell[cell_index] += 1
                    m_cel[cell_x * 3 + cell_y] = matrix[x][y]
            cell[cell_index] = m_cel.count(0)

            cells2 = cell[cell_index]

            # Compare previous cell and current
            if cells2 < cells1 and cells2 != 0:
                cells1 = cells2
                if cells1 < index_col:
                    if cells1 < index_line:
                        # If number of zeros is less than in rows and columns - choose cell 1D array

                        index_name = "cell"
                        index = cell_index
                        matrix_to_choose = list(m_cel)
                        # Write to the 1D array for export

        return index_name, index, matrix_to_choose

    @staticmethod
    def insert(m, choice, index_n, index):
        # Function to insert the chosen 1D array

        if index_n == "line":
            # If index name is row (line)

            m[index] = choice
            # Insert the chosen array to the index-1 row

        elif index_n == "col":
            # If the name is column

            for row in range(0, 9):
                m[row][index] = choice[row]
                # Insert 1D array into the line

        elif index_n == "cell":
            # If the chosen array is for 3x3 cell

            for row in range(0, 3):
                for column in range(0, 3):
                    # index - index of the cell
                    x = row + index // 3 * 3
                    y = column + (index - index // 3 * 3) * 3

                    m[x][y] = choice[row * 3 + column]

        return m  # Return modified matrix

    def check(self, matrix):
        # Function to check for any violations in the sudoku matrix

        for rows in range(0, 9):
            # check through lines

            checker = list(matrix[rows])
            # Create a list of row

            for _ in range(checker.count(0)):
                checker.remove(0)
                # Remove zeros from checker

            # Check if there is no repetitions in the checker
            if len(set(checker)) != len(checker):
                return False

        for column in range(9):
            # The check for repetitions in columns

            checker = []
            # Clear the checker list

            for row in range(9):
                number = matrix[row][column]
                if number != 0:
                    checker.append(number)

            if len(set(checker)) != len(checker):
                # If repetition - go out
                return False

        for cell in range(9):
            # Check for repetitions in 3x3 cells
            checker = list()
            for row in range(3):
                for column in range(3):
                    x = row + cell // 3 * 3
                    y = column + (cell - cell // 3 * 3) * 3
                    number = matrix[x][y]

                    if number != 0:
                        checker.append(number)

            if len(set(checker)) != len(checker):
                # If repetition - go out
                return False

        # Save the current matrix to the current step
        self.write_ex(matrix, self.step + 1)
        self.next_step = True
        return True

    def difficulty(self):
        # Function for defining the difficulty
        # depending on the number of clues

        if self.clues >= 46:
            return "Extremely easy"
        elif 36 <= self.clues < 46:
            return "Easy"
        elif 32 <= self.clues <= 35:
            return "Medium"
        elif 28 <= self.clues <= 31:
            return "Difficult"
        else:
            return "Evil"

    def solve(self):

        # Declare the number of iterations
        self.count = 0
        start = datetime.now()
        while True:

            # Increase the number of iterations
            self.count += 1

            # If there was a mistake in the
            # initial data - break the loop
            if self.step == 0:
                break

            # If the solution for the previous step was found - go to the next
            if self.next_step:

                # Get the 2D array of sudoku for the step
                self.mainMatrix = list(self.materix[self.step])

                # Choose the place with the least number of zeros,
                # write the index, its name and the 1D array
                self.index_name[self.step], self.index[self.step], choice = self.choice_index(self.mainMatrix)
                other = list()

                # Creating a list of missing digits
                for j in range(1, 10):
                    if j not in choice:
                        other.append(j)
                # Finding all existing permutations
                # Define temporary choices and permanent (which then saved to the step)
                choices_temp = []
                self.choices[self.step] = []

                for i in itertools.permutations(other, len(other)):
                    # Output array is of all permutations
                    # added then to the list
                    choices_temp.append(list(i))

                # Creating an element in a dictionary for this step
                # with all available combinations for matrix to replace
                for temporary in range(len(choices_temp)):
                    temp = list(choice)
                    # Get the choice with missing elements

                    for item in range(len(choice)):
                        if temp[item] == 0:
                            # if the element is 0, than replace it from the permutations
                            temp[item] = choices_temp[temporary].pop()

                    # choices variable contains all available permutations
                    # for each step
                    self.choices[self.step].append(temp)

            else:
                # If we need to check another permutation
                # Get the saved matrix
                self.mainMatrix = self.materix[self.step]

                if len(self.choices[self.step]) == 0:
                    # If there is no more permutations -
                    # Go backwards one step

                    del self.materix[self.step]
                    self.step -= 1
                    continue

            # This inserts the choice with permutation into the 2D sudoku array
            self.mainMatrix = self.insert(self.mainMatrix, self.choices[self.step].pop(), self.index_name[self.step],
                                          index=self.index[self.step])

            # Then it checked for repetitions
            while not self.check(self.mainMatrix):
                # If there is violation of the rule

                if len(self.choices[self.step]) > 0:
                    # If there are any permutations left

                    # Insert another permutation
                    self.mainMatrix = self.insert(self.mainMatrix,
                                                  self.choices[self.step].pop(),
                                                  self.index_name[self.step],
                                                  index=self.index[self.step])

                else:
                    # if there are no more elements in permutations,
                    # delete everything after this step

                    whatToDelete = []
                    # Get written steps after the current one

                    for key in self.choices.keys():
                        # Iterate through choices

                        if key >= self.step:
                            # Get the steps to delete
                            whatToDelete.append(key)

                    # Delete saved information
                    for steps in whatToDelete:
                        del self.choices[steps]
                        del self.index[steps]
                        del self.index_name[steps]

                    # Decrease the step
                    self.step -= 2

                    # If no more choices in the 1st step (if initial data is wrong)
                    if self.step != -1:
                        try:
                            del self.materix[self.step + 2]
                        except:
                            pass
                    self.next_step = False
                    break

            # Increase the step
            self.step += 1

            finish = False

            if sum(map(sum, self.mainMatrix)) == 405:
                break

        # Count the working time
        time = datetime.now() - start

        text_time = f"{time.seconds}s : {time.microseconds / 1000} ms."

        # Create the image of the solution for export
        return self.finished(self.mainMatrix, text_time, self.count, self.difficulty())


def solve_puzzle(data: str):
    try:
        return Sudoku(data=data).solve()
    except ValueError as err:
        return f"Error {err}"
