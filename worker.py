import threading

class Worker(threading.Thread):
    sudoku = None
    validEvent = threading.Event() 
    rmDirValsEvent = threading.Event()
    checkValsEvent = threading.Event()
    
    validated = 0
    phaseCount = 0

    def __init__(self, workerId):
        threading.Thread.__init__(self)
        self.wid = workerId
        self.values = set()

    def setSudoku(entry):
        Worker.sudoku = entry
        Worker.validated = 0

    def getLock(i, j):
        return Worker.sudoku.locks[i][j]

    def getNotes(i, j):
        return Worker.sudoku.notes[i][j]

    def getCell(i, j):
        return Worker.sudoku.puzzle[i][j]

    def setCell(value, i, j):
        Worker.sudoku.puzzle[i][j] = value

    def emptyNotes(i, j):
        Worker.sudoku.notes[i][j] = set()

    def isValid(self):
        return False

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

    def solve(self):
        if 0 in self.values: self.values.remove(0)
        while len(self.values) < 9:
            self.removePhase()
            Worker.phaseCount += 1
            if threading.active_count()-1 == Worker.phaseCount:
                Worker.phaseCount = 0
                self.checkValsEvent.clear()
                self.rmDirValsEvent.set()
            else:
                self.rmDirValsEvent.wait()
            #self.checkPhase()
            Worker.phaseCount += 1
            if threading.active_count()-1 == Worker.phaseCount:
                Worker.phaseCount = 0
                self.rmDirValsEvent.clear()
                self.checkValsEvent.set()
            else:
                self.checkValsEvent.wait()

    def removePhase(self):
        return None

    def checkPhase(self):
        return None
        
    #Removes direct impossible values
    def removeVals(self, row, col):
        #Goal is to minimize possibleValues to solve for cell value
        #Remove impossible values in same row
        notes = Worker.getNotes(row, col)
        for value in Worker.sudoku.puzzle[row]:
            if value in notes:
                notes.remove(value)
        #Remove impossible values in same col
        for neighbor in Worker.sudoku.puzzle:
            value = neighbor[col]
            if value in notes:
                notes.remove(value)
        x, y = int(row/3), int(col/3)
        for i in range(x*3, (x+1)*3):
            for j in range(y*3, (y+1)*3):
                Worker.setCell(value, i, j)
                if value in notes:
                    notes.remove(value)
        #Check and update possible values to avoid repetitive computation
        if len(notes) == 1:
            num = notes.pop()
            Worker.setCell(num, row, col)
            print(Worker.sudoku)
            return num

    def run(self):
        if self.isValid():
            Worker.validated += 1
            if Worker.validated == 27:
                Worker.validEvent.set()
        Worker.validEvent.wait()
        self.solve()
        print(self)
        print(Worker.sudoku)

    def __str__(self):
        return 'Worker {0}'.format(self.wid)

    def __repr__(self):
        return self.__str__()
