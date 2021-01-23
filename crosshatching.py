from random import randint
import time
import copy
string = list("4...3.......6..8..........1....5..9..8....6...7.2........1.27..5.3....4.9........") #very hard
string = list(".2.....3....1..7...83.6......6.2857...9..7.........46.5...7....4....1..2.....4...") #hard
string = list("..3.2.6..9..305..1..18064....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..") #medium
""" from project euler problem 96"""
string = list("003020600900305001001806400008102900700000008006708200002609500800203009005010300") #WORKS
string = list("200080300060070084030500209000105408000000000402706000301007040720040060004010003") #WORKS
string = list("000000907000420180000705026100904000050000040000507009920108000034059000507000000")
string = list("030050040008010500460000012070502080000603000040109030250000098001020600080060020") #WORKS
string = list("300200000000107000706030500070009080900020004010800050009040301000702000000008006") #hardest in euler's problem
#string = list("")

def convertToList(ls, thing=False):
	loop = 1
	puzzle = []
	for i in ls:
		if i == ".":
			string[loop-1] = 0
		else:
			string[loop-1] = int(string[loop-1])
		if loop % 9 == 0:
			row = string[loop-9:loop]
			puzzle.append(row)
		loop += 1
	return puzzle

def showPuzzle(puzzle):
	[print (i) for i in puzzle]
	print("")

def showGrids(grids):
	[print (grid) for row in grids for grid in row]
	print("")

def convertToCols(ls):
	cols = []
	for x in range(0, 9):
		col = []
		for y in range(0, 9):
			col.append(ls[y][x])
		cols.append(col)
	return cols

def convertToGrids(ls):
	loop = 0
	grids = [[[], [], []], [[], [], []], [[], [], []]]
	for x in range(0, 9):
		for y in range(0, 9):
			grids[int(x/3)][int(y/3)].append(ls[x][y])
		loop += 1
	return grids

def crosshatching(num, puzzle, cols, grids):
	cancelled = [11 for i in range(9)]

	cpuzzle = copy.deepcopy(puzzle)
	ccols = copy.deepcopy(cols)
	cgrids = copy.deepcopy(grids)

	for row in range(0, 9):
		for col in range(0, 9):
			#print(puzzle, row)
			rowNow = puzzle[row]
			colNow = cols[col]
			gridNow = grids[int(row/3)][int(col/3)]

			if num in rowNow:
				cpuzzle[row] = cancelled
			if num in colNow:
				for row2 in range(0, 9):
					cpuzzle[row2][col] = 11
			if num in gridNow:
				cgrids[int(row/3)][int(col/3)] = cancelled
				cgrids2 = convertToPuzzle(cgrids)
				add(cgrids2, cpuzzle)
	return cpuzzle

def convertToPuzzle(grids):
	puzzle = [[] for x in range(9)]
	for gridRow in range(0, 3):
		for grid in range(0, 3):
			for item in range(0, 9):
				puzzle[int(item/3)+gridRow*3].append(grids[gridRow][grid][item])
	return puzzle

def add(ls1, ls2):
	for row in range(0, 9):
		for col in range(0, 9):
			if ls1[row][col] == 11:
				ls2[row][col] = 11

def findIndex(ls):
	for row in range(0, 9):
		if ls[row].count(0) == 1:
			return row, ls[row].index(0)
	return 111, 111

""" FIX THIS """
def findIndex2(ls):
	for gridRow in range(3):
		for row in range(3):
			if ls[gridRow][row].count(0) == 1:
				return gridRow, row, ls[gridRow][row].index(0)
	return 111, 111, 111

def findItem(ls, item):
	for row in range(0, 9):
		for col in range(0, 9):
			if ls[row][col] == item:
				return row, col

def addNum(num, cpuzzle, puzzle, stuck, steps):
	can_solve = False

	row, col = findIndex(cpuzzle)
	if not row == 111:
		puzzle[row][col] = num
		#steps.append(("Crosshatching: placed number", num, "in", "row-", row+1, "col-", col+1))
		steps += 1
		showPuzzle(puzzle)
		showPuzzle(cpuzzle)
		stuck = 0

	ccols = convertToCols(cpuzzle)
	row, col = findIndex(ccols)
	if not row == 111:
		ccols[row][col] = 100
		ccols = convertToCols(ccols)
		row, col = findItem(ccols, 100)
		puzzle[row][col] = num
		#steps.append(("Crosshatching: placed number", num, "in", "row-", row+1, "col-", col+1))
		steps += 1
		showPuzzle(puzzle)
		showPuzzle(cpuzzle)
		stuck = 0

	cgrids = convertToGrids(cpuzzle)
	gridRow, row, col = findIndex2(cgrids)
	if not row == 111:
		cgrids[gridRow][row][col] = 100
		cgrids = convertToPuzzle(cgrids)
		row, col = findItem(cgrids, 100)
		puzzle[row][col] = num
		#steps.append(("Crosshatching: placed number", num, "in", "row-", row+1, "col-", col+1))
		steps += 1
		showPuzzle(puzzle)
		showPuzzle(cpuzzle)
		stuck = 0

	return puzzle, stuck, steps

#puzzle = convertToList(string)

def execute(puzzle, steps):
	done = False
	stuck = 0
	while not done:
		for num in range(1, 10):
			stuck += 1
			cols = convertToCols(puzzle)
			grids = convertToGrids(puzzle)
			cpuzzle = crosshatching(num, puzzle, cols, grids)
			puzzle, stuck, steps = addNum(num, cpuzzle, puzzle, stuck, steps)
		if stuck > 30:
			done = True
	showPuzzle(puzzle)
	return puzzle, steps
