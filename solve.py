import sys, threading, pdb

from sudoku import Sudoku
from rowWorker import RowWorker
from colWorker import ColWorker
from boxWorker import BoxWorker
from worker import Worker

if __name__ == '__main__':
    if len(sys.argv) == 1:
        sys.exit()
    elif len(sys.argv) > 1:
        for inputFile in sys.argv:
            if inputFile == 'solve.py':
                continue
            else:
                f = open(inputFile, 'r')
                sudo = Sudoku()
                for line in f:
                    row = line.strip().split(',')
                    if len(row) != 9: sys.exit() #invalid number of values for sudoku
                    try:
                        sudo.addRow([int(num) for num in row])
                    except:
                        sys.exit()
                threads = []
                wid = 0
                for location in range(0, 9):
                    threads.append(RowWorker(location*3, location))
                    threads.append(ColWorker(location*3+1, location))
                    threads.append(BoxWorker(location*3+2, location))

                Worker.setSudoku(sudo)
                print(Worker.sudoku)
                for thread in threads:
                    thread.start()
                
                 
