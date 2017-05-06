import threading

class Sudoku:
    
    oneToNine = {x for x in range(1, 10)}

    #Instantiate empty sudoku puzzle as 2D array.
    #0 represents empty cell. 1-9 are other values.
    def __init__(self):
        self.puzzle = []
        self.notes = []
        self.locks = []

    #Adds a row of sudoku values. Validity check for values 0-9 or default to 0 otherwise.
    def addRow(self, row):
        values = []
        note = []
        for num in row:
            values.append(num)
            if num == 0:
                note.append({x for x in range(1,10)})
            else:
                note.append(set())
        self.puzzle.append(values)
        self.notes.append(note)
        self.locks.append([threading.Lock() for x in range(0, 9)])
    
    def isSudokuPuzzle(self):
        if len(puzzle) != 9:
            return False
        for x in range(0, 9):
            if len(puzzle[x]) != 9:
                return False
            row = set()
            col = set()
            for a in puzzle:
                num = a[x]
                if num in col:
                    return False
                col.add(num)
            for num in puzzle[x]:
                if num in row:
                    return False
                row.add(num)
        for i in range(0, 3):
            for j in range(0, 3):
                square3x3 = set()
                for x in range(0, 3):
                    for y in range(0, 3):
                        num = puzzle[i*3+x][j*3+y]
                        if num in square3x3:
                            return False
                        square3x3.add(num)
        return True

    def isSolved(self):
        for x in range(0, 9):
            row = set()
            col = set()
            for a in puzzle:
                num = a[x]
                col.add(num)
            for num in puzzle[x]:
                row.add(num)
            if len(row) != 9 or len(col) != 9:
               return False
        for i in range(0, 3):
            for j in range(0, 3):
                square3x3 = set()
                for x in range(0, 3):
                    for y in range(0, 3):
                        num = puzzle[i*3+x][j*3+y]
                        if num in square3x3:
                            return False
                        square3x3.add(num)
                if len(square3x3) != 9:
                    return False
        return True

    def __str__(self):
        result = ""
        for line in self.puzzle:
            result += ','.join([str(num) for num in line])
            result += '\n'
        return result

