import threading

class Worker(threading.Thread):
    sudoku = None
    validEvent = threading.Event() 
    phaseSemaphore = threading.Semaphore(value=27)
    rmDirValsEvent = threading.Event()
    oneValEvent = threading.Event()
    
    validated = 0

    def __init__(self, workerId):
        threading.Thread.__init__(self)
        self.wid = workerId
        self.values = set()

    def setSudoku(entry):
        Worker.sudoku = entry
        Worker.validated = 0

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

    def evaluateCell(self, row, col):
        if Worker.sudoku.locks[row][col].acquire():
            if Worker.sudoku.puzzle[row][col] != 0:
                Worker.sudoku.locks[row][col].release()
                return Worker.sudoku.puzzle[row][col]
            else:
                num = 0
                num = self.removeVals(row, col)
                if num == 0: 
                    num = self.checkNeighbors(row, col)
                if num: Worker.sudoku.puzzle[row][col] = num        
                Worker.sudoku.locks[row][col].release()
                return num
        else:
            return 0
        
    #Removes direct impossible values
    def removeVals(self, row, col):
        #Goal is to minimize possibleValues to solve for cell value
        #Remove impossible values in same row
        for value in Worker.sudoku.puzzle[row]:
            if value in Worker.sudoku.notes[row][col]:
                Worker.sudoku.notes[row][col].remove(value)
        #Remove impossible values in same col
        for neighbor in Worker.sudoku.puzzle:
            value = neighbor[col]
            if value in Worker.sudoku.notes[row][col]:
                Worker.sudoku.notes[row][col].remove(value)
        x, y = int(row/3), int(col/3)
        for i in range(x*3, (x+1)*3):
            for j in range(y*3, (y+1)*3):
                value = Worker.sudoku.puzzle[i][j]
                if value in Worker.sudoku.notes[row][col]:
                    Worker.sudoku.notes[row][col].remove(value)
        #Check and update possible values to avoid repetitive computation
        if len(Worker.sudoku.notes[row][col]) == 1:
            num = Worker.sudoku.notes[row][col].pop()
            Worker.sudoku.puzzle[row][col] = num
            return num

    def run(self):
        if self.isValid():
            Worker.validated += 1
            if Worker.validated == 27:
                self.validEvent.set()
        Worker.checkEvent.wait()
        self.solve()
        print(self)
        print(Worker.sudoku)

    def __str__(self):
        return 'Worker {0}'.format(self.wid)

    def __repr__(self):
        return self.__str__()
