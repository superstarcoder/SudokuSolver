import crosshatching as ch
def execute(puzzle):
	pencil = {}
	for row in range(9):
		for col in range(9):
			ls = []
			if puzzle[row][col] == 0:
				cols = ch.convertToCols(puzzle)
				grids = ch.convertToGrids(puzzle)
				for num in range(1, 10):
					cpuzzle = ch.crosshatching(num, puzzle, cols, grids)
					if cpuzzle[row][col] == 0:
						ls.append(num)
			if puzzle[row][col] == 0 and len(ls) == 1:
				pencil[row, col] = ls
	if not len(pencil) == 0:
		for key, value in pencil.items():
			puzzle[key[0]][key[1]] = value[0]
	return puzzle, pencil
