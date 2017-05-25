from worker import Worker

class RowWorker(Worker):

    def __init__(self, workerId, location):
        super().__init__(workerId)
        self.loc = location

    def isValid(self):
        validNums = {x for x in range(0, 10)}
        for num in Worker.sudoku.puzzle[self.loc]:
            self.values.add(num)
        return self.values.issubset(validNums)

    def removePhase(self):
        for index in range(0, 9):
            try:
                Worker.getLock(self.loc, index).acquire()
                if Worker.getCell(self.loc, index): continue
                self.removeVals(self.loc, index)
                if len(Worker.getNotes(self.loc, index)) == 1:
                    num = Worker.getNotes(self.loc, index).pop()
                    Worker.setCell(num, self.loc, index)
                    self.values.add(num)
            finally:
                Worker.getLock(self.loc, index).release()

    def checkPhase(self):
        for index in range(0, 9):
            try:
                Worker.getLock(self.loc, index).acquire()
                if Worker.getCell(self.loc, index): continue
                num = self.checkNeighbors(self.loc, index)
                if num: self.values.add(num)
            finally:
                Worker.getLock(self.loc, index).release()

    def checkNeighbors(self, row, col):
        possibleVals = set(getNotes(row, col))
        for ind in range(0, 9):
            if ind != col:
                possibleVals -= getNotes(row, ind)

        if len(possibleValues) == 1:
            num = possibleValues.pop()
            Worker.setCell(num, row, col)
            Worker.emptyNotes(row, col)
            return num

    def __str__(self):
        return super().__str__() + ":Row {0}".format(self.loc)

    def __repr__(self):
        return self.__str__()
