import worker

class ColWorker(worker.Worker):

    def __init__(self, workerId, location):
        super().__init__(workerId)
        self.loc = location

    def isValid(self):
        validNums = {x for x in range(0, 10)}
        for row in Worker.sudoku.puzzle:
            num = row[self.loc]
            self.values.add(num)
        return self.values.issubset(validNums)

    def solve(self):
        if 0 in self.values: self.values.remove(0)
        while len(self.values) < 9:
            answer = 0
            for index in range(0, 9):
                try:
                    Worker.sudoku.locks[index][self.loc].acquire()
                    answer = self.removeVals(index, self.loc)
                    answer = self.checkNeighbors(index, self.loc)
                    if answer: self.values.append(answer)
                finally:
                    Worker.sudoku.locks[index][self.loc].release()

    def checkNeighbors(self, row, col):
        if Worker.sudoku.puzzle[row][col]: return Worker.sudoku.puzzle[row][col]
        possibleVals = set(Worker.sudoku.notes[row][col])
        for ind in range(0, 9):
            if ind != row:
                possibleVals -= Worker.sudoku.notes[ind][col]

        if len(possibleValues) == 1:
            num = possibleValues.pop()
            Worker.sudoku.notes[row][col] = set()
            return num
        return 0

    def __str__(self):
        return super().__str__() + ":Col {0}".format(self.loc)

    def __repr__(self):
        return self.__str__()
