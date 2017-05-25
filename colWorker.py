from worker import Worker

class ColWorker(Worker):

    def __init__(self, workerId, location):
        super().__init__(workerId)
        self.loc = location

    def isValid(self):
        validNums = {x for x in range(0, 10)}
        for row in Worker.sudoku.puzzle:
            num = row[self.loc]
            self.values.add(num)
        return self.values.issubset(validNums)

    def removePhase(self):
        for index in range(0, 9):
            try:
                Worker.getLock(index, self.loc).acquire()
                if Worker.getCell(index, self.loc): continue
                self.removeVals(index, self.loc)
                if len(Worker.getNotes(index, self.loc)) == 1:
                    num = Worker.getNotes(index, self.loc).pop()
                    Worker.setCell(num, index, self.loc)
                    self.values.add(num)
            finally:
                Worker.getLock(index, self.loc).release()

    def checkPhase(self):
        for index in range(0, 9):
            try:
                Worker.getLock(index, self.loc).acquire()
                if Worker.getCell(index, self.loc): continue
                num = self.checkNeighbors(index, self.loc)
                if num: self.values.add(num)
            finally:
                Worker.getLock(index, self.loc).release()

    def checkNeighbors(self, row, col):
        possibleVals = set(Worker.getNotes(row, col))
        for ind in range(0, 9):
            if ind != col:
                possibleVals -= getNotes(ind, col)

        if len(possibleValues) == 1:
            num = possibleValues.pop()
            Worker.setCell(num, row, col)
            Worker.emptyNotes(row, col)
            return num

    def __str__(self):
        return super().__str__() + ":Col {0}".format(self.loc)

    def __repr__(self):
        return self.__str__()
