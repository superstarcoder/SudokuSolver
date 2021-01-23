import solver
import pencilling as pn
import copy
from random import randint
def execute(r, c, puzzle):
	if r>8:
		return puzzle

	if puzzle[r][c] == 0:
		for num in '123456789':
			num = int(num)
			if clear(num, r, c, puzzle):
				puzzle[r][c] = num
				print(puzzle)
				c += 1
				if c > 8:
					r += 1
					c = 0
				sol = execute(r, c, puzzle)
				if sol:
					return sol
				c -= 1
				if c < 0:
					r -= 1
					c = 8
				puzzle[r][c] = 0
	else:
		c += 1
		if c > 8:
			r += 1
			c = 0
		return execute(r, c, puzzle)

def clear(num, r, c, puzzle):
	cols = convertToCols(puzzle)
	grids = convertToGrids(puzzle)
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
	if cpuzzle[r][c] == 11:
		return 0
	else:
		return 1

def add(ls1, ls2):
	for row in range(0, 9):
		for col in range(0, 9):
			if ls1[row][col] == 11:
				ls2[row][col] = 11


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

def convertToPuzzle(grids):
	puzzle = [[] for x in range(9)]
	for gridRow in range(0, 3):
		for grid in range(0, 3):
			for item in range(0, 9):
				puzzle[int(item/3)+gridRow*3].append(grids[gridRow][grid][item])
	return puzzle
