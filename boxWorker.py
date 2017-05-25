from worker import Worker

class BoxWorker(Worker):
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
                self.values.add(Worker.getCell(i, j))
        return self.values.issubset(validNums)
        
    def removePhase(self):
        row, col = self.findBox()
        for i in range(row*3, (row+1)*3):
            for j in range(col*3, (col+1)*3):
                try:
                    Worker.getLock(i, j).acquire()
                    if Worker.getCell(i, j): continue
                    self.removeVals(i, j)
                    if len(Worker.getNotes(i, j)) == 1:
                        num = Worker.getNotes(i, j).pop()
                        Worker.setCell(num, i, j)
                        self.values.add(num)
                finally:
                    Worker.getLock(i, j).release()

    def checkPhase(self):
        row, col = self.findBox()
        for i in range(row*3, (row+1)*3):
            for j in range(col*3, (col+1)*3):
                try:
                    Worker.getLock(i, j).acquire()
                    if Worker.getCell(i, j): continue
                    num = self.checkNeighbors(i, j)
                    if num: self.values.add(num)
                finally:
                    Worker.getLock(i, j).release()

    def checkNeighbors(self, row, col):
        possibleVals = set(Worker.getNotes(row, col))
        a,b = int(row/3), int(col/3)
        for i in range(a*3, (a+1)*3):
            for j in range(b*3, (b+1)*3):
                if not (i == row and j == col):
                    possibleVals -= Worker.getNotes(i, j)

        if len(possibleValues) == 1:
            num = possibleValues.pop()
            Worker.setCell(num, row, col)
            Worker.emptyNotes(row, col)
            return num

    def __str__(self):
        return super().__str__() + ":Box {0}".format(self.loc)

    def __repr__(self):
        return self.__str__()
