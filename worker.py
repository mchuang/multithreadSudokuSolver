import threading

class Worker(threading.Thread):
    sudoku = None
    checkEvent = threading.Event() 
    validated = 0

    def __init__(self, workerId, job, location):
        threading.Thread.__init__(self)
        self.wid = workerId
        self.job = job
        self.loc = location
        self.values = set()

    def setSudoku(entry):
        Worker.sudoku = entry
        Worker.validated = 0

    def isValid(self):
        validNums = {x for x in range(0, 10)}
        if self.loc >= 9 or self.loc < 0:
            return False
        if self.job == 0: #row
            for num in Worker.sudoku.puzzle[self.loc]:
                self.values.add(num)
            return self.values.issubset(validNums)
        elif self.job == 1: #col
            for row in Worker.sudoku.puzzle:
                num = row[self.loc]
                self.values.add(num)
            return self.values.issubset(validNums)
        elif self.job == 2: #box
            row, col = self.findBox()
            for i in range(row*3, (row+1)*3):
                for j in range(col*3, (col+1)*3):
                    self.values.add(Worker.sudoku.puzzle[i][j])
            return self.values.issubset(validNums)
        else:
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
            answer = 0
            if self.job == 0 or self.job == 1: 
                for index in range(0, 9):
                    if self.job == 0:
                        answer = self.evaluateCell(self.loc, index)
                    elif self.job == 1:
                        answer = self.evaluateCell(index, self.loc)
                    if answer: self.values.add(answer)
            elif self.job == 2:
                row, col = self.findBox()
                for i in range(row*3, (row+1)*3):
                    for j in range(col*3, (col+1)*3):
                        answer = self.evaluateCell(i, j)
                        if answer: self.values.add(answer)
            else:
                break

    def evaluateCell(self, row, col):
        if Worker.sudoku.locks[row][col].acquire(timeout=3):
            if Worker.sudoku.puzzle[row][col] != 0:
                Worker.sudoku.locks[row][col].release()
                return Worker.sudoku.puzzle[row][col]
            else:
                if len(Worker.sudoku.notes[row][col]) == 0: print("zerp")
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
                if len(Worker.sudoku.notes[row][col]) == 0: print("zeroed out0")
        #Remove impossible values in same col
        for neighbor in Worker.sudoku.puzzle:
            value = neighbor[col]
            if value in Worker.sudoku.notes[row][col]:
                Worker.sudoku.notes[row][col].remove(value)
                if len(Worker.sudoku.notes[row][col]) == 0: print("zeroed out1")
        x, y = int(row/3), int(col/3)
        for i in range(x*3, (x+1)*3):
            for j in range(y*3, (y+1)*3):
                value = Worker.sudoku.puzzle[i][j]
                if value in Worker.sudoku.notes[row][col]:
                    Worker.sudoku.notes[row][col].remove(value)
                    if len(Worker.sudoku.notes[row][col]) == 0: print("zeroed out2")
        #Check and update possible values to avoid repetitive computation
        if len(Worker.sudoku.notes[row][col]) == 1:
            num = Worker.sudoku.notes[row][col].pop()
            #Worker.sudoku.puzzle[row][col] = num
            return num
        return 0

    #Checks for single possible value among neighbors
    def checkNeighbors(self, row, col):
        possibleValues = set(Worker.sudoku.notes[row][col])
        if self.job == 0 or self.job == 1:    
            for ind in range(0, 9):
                if self.job == 0 and ind != col:
                    if Worker.sudoku.locks[row][ind].acquire(timeout=1):
                        possibleValues -= Worker.sudoku.notes[row][ind]
                        Worker.sudoku.locks[row][ind].release()
                    else:
                        return 0
                elif self.job == 1 and ind != row: 
                    if Worker.sudoku.locks[ind][col].acquire(timeout=1):
                        possibleValues -= Worker.sudoku.notes[ind][col]
                        Worker.sudoku.locks[ind][col].release()
                    else:
                        return 0
        elif self.job == 2:
            a,b = int(row/3), int(col/3)
            for i in range(a*3, (a+1)*3):
                for j in range(b*3, (b+1)*3):
                    if not (i == row and j == col):
                        if Worker.sudoku.locks[i][j].acquire(timeout=1):
                            possibleValues -= Worker.sudoku.notes[i][j]
                            Worker.sudoku.locks[i][j].release()
                        else:
                            return 0

        if len(possibleValues) == 1:
            num = possibleValues.pop()
            #Worker.sudoku.puzzle[row][col] = num
            Worker.sudoku.notes[row][col] = set()
            return num
        return 0

    def run(self):
        if self.isValid():
            Worker.validated += 1
            if Worker.validated == 27:
                self.checkEvent.set()
        Worker.checkEvent.wait()
        self.solve()
        print(self)
        print(Worker.sudoku)

    def __str__(self):
        return 'Worker {0}:{1}:{2}'.format(self.wid, self.job, self.loc)

    def __repr__(self):
        return self.__str__()
