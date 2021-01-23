from random import randint
import pencilling as pn

def generate(d):
	global rows
	generated = False
	while not generated:
		# just generate the empty sudoku
		rows = []
		for y in range(0, 9):
			row = []
			for x in range(0, 9):
				row.append(0)
			rows.append(row)

		#rows = [[0]*9 for i in range(9)]
		for ROW in range(0, 9):
			for COL in range(0, 9):

				# generate the columns from the rows
				columns = []
				for col2 in range(0, 9):
					col = []
					for row in range(0, 9):
						col.append(rows[row][col2])
					columns.append(col)

				# here we generate the grids from the rows
				starts = [0, 3, 6]
				grids = []
				for ystart in starts:
					row_grid = []
					for xstart in starts:
						grid = []
						for y in range(0, 3):
							for x in range(0, 3):
								grid.append(rows[y + ystart][xstart + x])
						row_grid.append(grid)
					grids.append(row_grid)

				colNow = rows[ROW]
				rowNow = columns[COL]
				gridNow = grids[int(ROW/3)][int(COL/3)]
				num = 0
				max_loop = 100
				loop = 0
				while num in rowNow or num in colNow or num in gridNow:
					num = randint(1, 9)	
					loop += 1
					if ROW == 8 and COL == 8:
						generated = True
					if loop > max_loop:
						break
				rows[ROW][COL] = num
				if loop > max_loop:
					break
			if loop > max_loop:
				break
	for i in rows: print(i)
	print("")
	#ls = [1,2,2]
	ls = [1,1,2,2,2]
	for row in range(0, 9):
		for col in range(0, 9):
			x = randint(0, len(ls)-1)
			if ls[x] == 1:
				rows[row][col] = 0
	for i in rows: print(i)
	return rows

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

def replace(replacement, replaced, ls):
	loop = 0
	for x in ls:
		if x == replacement:
			ls[loop] = replaced
			return ls
		loop += 1

def check(num, grid):
	for row in grid:
		if num in row:
			return True
	return False



#initialize()
def execute():
	rows1 = generate(1)
	new = []
	for row in range(0, 9):
		new += rows1[row]
	print(new)
	import solver
	rows, oldRows, solved, timeTaken, d1, d2, steps = solver.execute(rows1, False)
	print("problem", "took", timeTaken, "seconds to solve")
	print("problem", "took", steps, "steps to solve")
	print("")
	print("Sudoku's difficulty level for a human:", d1)
	print("Sudoku's difficulty level for a computer:", d2)
	print("")
	if d1 == "insane":
		rows, pencil = pn.refresh(rows)
		for row in range(0, 9):
			for col in range(0, 9):
				if not pencil[row][col] == []:
					oldRows[row][col] = rows1[row][col]
		rows, oldRows, solved, timeTaken, d1, d2, steps = solver.execute(oldRows, False)
		print("problem", "took", timeTaken, "seconds to solve")
		print("problem", "took", steps, "steps to solve")
		print("")
		print("Sudoku's difficulty level for a human:", d1)
		print("Sudoku's difficulty level for a computer:", d2)
		print("")
	for row in rows:
		print(row)
	if not d1 == "insane":
		return rows, oldRows
	else:
		rows, oldRows = execute()
		return rows, oldRows

if __name__ == "__main__":
	sol, prob = execute()
