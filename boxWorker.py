import worker

class BoxWorker(worker.Worker):
    def __init__(self, workerId, location):
        super().__init__(workerId)
        self.loc = location

    def findBox(self):
        row, col = 0, 0
        location = self.loc
        while location > 0:
            if location >= 3:
                location -= 3
                row += 1
            elif location < 3:
                col += location
                break
        return row, col

    def isValid(self):
        validNums = {x for x in range(0, 10)}
        row, col = self.findBox()
            for i in range(row*3, (row+1)*3):
                for j in range(col*3, (col+1)*3):
                    self.values.add(Worker.sudoku.puzzle[i][j])
        return self.values.issubset(validNums)

    def solve(self):
        if 0 in self.values: self.values.remove(0)
        while len(self.values) < 9:
            answer = 0
            row, col = self.findBox()
            for i in range(row*3, (row+1)*3):
                for j in range(col*3, (col+1)*3):
                try:
                    Worker.sudoku.locks[i][j].acquire()
                    answer = self.removeVals(i, j)
                    answer = self.checkNeighbors(i, j)
                    if answer: self.values.append(answer)
                finally:
                    Worker.sudoku.locks[self.loc][index].release()

    def checkNeighbors(self, row, col):
        if Worker.sudoku.puzzle[row][col]: return Worker.sudoku.puzzle[row][col]
        possibleVals = set(Worker.sudoku.notes[row][col])
        a,b = int(row/3), int(col/3)
        for i in range(a*3, (a+1)*3):
            for j in range(b*3, (b+1)*3):
                if not (i == row and j == col):
                    possibleVals -= Worker.sudoku.notes[i][j]

        if len(possibleValues) == 1:
            num = possibleValues.pop()
            Worker.sudoku.puzzle[row][col] = num
            Worker.sudoku.notes[row][col] = set()
            return num
        return 0

    def __str__(self):
        return super().__str__() + ":Row {0}".format(self.loc)

    def __repr__(self):
        return self.__str__()
