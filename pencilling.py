import crosshatching as ch
import copy
import time
import itertools

"""1. Single-candidate squares
   2. Single-square candidates
   3. Number claiming
   4. Pairs
   5. Triples
   EXTREME
   6. Excluded Candidates
   7. Box-line reduction """

def refresh(puzzle):
	pencil = []
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
			pencil.append(ls)

	pencil2 = [[] for x in range(9)]
	loop = 0
	for i in pencil:
		pencil2[int(loop/9)].append(i)
		loop += 1
	return puzzle, pencil2

def rule1(puzzle, pencil, steps): #single-candidate squares
	applied = False
	for row in range(0, 9):
		for col in range(0, 9):
			if len(pencil[row][col]) == 1:
				puzzle[row][col] = pencil[row][col][0]
				#steps.append(("Single-candidate squares: placed number", pencil[row][col][0], "in cell (%r,%r)" % (row+1, col+1)))
				puzzle, pencil = refresh(puzzle)
				applied = True
	return puzzle, pencil, applied, steps

def rule2(puzzle, pencil, steps): #single-square candidate
	applied = False
	for num in range(1, 10):

		row, col = findIndex(pencil, num)		
		if not row == 111:
			puzzle[row][col] = num
			#steps.append(("Single-square candidate: placed number", num, "in", "cell (%r,%r)" % (row+1, col+1)))
			puzzle, pencil = refresh(puzzle)
			applied = True

		pencilCols = ch.convertToCols(pencil)
		row, col = findIndex(pencilCols, num)		
		if not row == 111:
			pencilCols[row][col] = [100]
			pencilCols = ch.convertToCols(pencilCols)
			row, col = findItem(pencilCols, [100])
			puzzle[row][col] = num
			#steps.append(("Single-square candidate: placed number", num, "in", "cell (%r,%r)" % (row+1, col+1)))
			puzzle, pencil = refresh(puzzle)
			applied = True

		pencilGrids = ch.convertToGrids(pencil)
		gridRow, row, col = findIndex2(pencilGrids, num)
		if not row == 111:
			pencilGrids[gridRow][row][col] = [100]
			pencilGrids = ch.convertToPuzzle(pencilGrids)
			row, col = findItem(pencilGrids, [100])
			puzzle[row][col] = num
			#steps.append(("Single-square candidate: placed number", num, "in", "cell (%r,%r)" % (row+1, col+1)))
			puzzle, pencil = refresh(puzzle)
			applied = True
	return puzzle, pencil, applied, steps

def findIndex(ls, num):
	for row in range(0, 9):
		count = 0
		for col in range(0, 9):
			if num in ls[row][col]:
				count += 1
				row2 = row
				col2 = col
		if count == 1:
			return row2, col2
	return 111, 111

def findIndex2(ls, num):
	for gridRow in range(3):
		for grid in range(3):
			count = 0
			for col in range(9):
				if num == ls[gridRow][grid][col]:
					count += 1
					gridRow2 = gridRow
					grid2 = grid
					col2 = col
			if count == 1:
				return gridRow, grid2, col2
	return 111, 111, 111

def findItem(ls, item):
	for row in range(0, 9):
		for col in range(0, 9):
			if ls[row][col] == item:
				return row, col

"""
012 345 678
--- X-- ---
--- -X- ---
--- --X ---
X-- --- ---
"""
def rule3(puzzle, pencil, steps): #number claiming
	print("")
	print("RULE3")
	print("")
	applied = False
	for gridRow in range(0, 3):
		for grid in range(0, 3):
			box = [[],[],[]]
			pencilGrids = ch.convertToGrids(pencil)
			for loop in range(9):
				box[int(loop/3)].append(pencilGrids[gridRow][grid][loop])
			ch.showPuzzle(pencil)
			boxCols = convertBoxToCols(box)
			for row in range(0, 3):
				for num in range(1, 10):
					ls = [0,1,2]
					ls.remove(row)

					pencilGrids = ch.convertToGrids(pencil)
					box = [[],[],[]]
					for loop in range(9):
						box[int(loop/3)].append(pencilGrids[gridRow][grid][loop])
					boxCols = convertBoxToCols(box)
					if any(num in i for i in box[row]) and not any(num in i for i in box[ls[0]]) and not any(num in i for i in box[ls[1]]):
						for item in range(0, 3):
							if num in box[row][item]:
								itemLoc = item
						if itemLoc == 0:
							thing = [itemLoc+grid*3, itemLoc+1+grid*3, itemLoc+2+grid*3]
						elif itemLoc == 1:
							thing = [itemLoc+grid*3, itemLoc+1+grid*3, itemLoc-1+grid*3]
						else:
							thing = [itemLoc+grid*3, itemLoc-1+grid*3, itemLoc-2+grid*3]
						#print("watch")
						#print(thing)
						for x in thing:
							print(pencil[row+gridRow*3][x])
						for x in range(0, 9):
							if not x in thing and num in pencil[row+gridRow*3][x]:
								pencil[row+gridRow*3][x].remove(num)
								#steps.append(("Number claiming: removed", num, "from candidate list in cell (%r,%r)" % (row+gridRow+1, x+1)))
								steps += 1
								applied = True
								#print ("YEAHHHHHHHHHHHHHHHHHHHH")
								#print(row+grid*3, x)

					pencilGrids = ch.convertToGrids(pencil)
					box = [[],[],[]]
					for loop in range(9):
						box[int(loop/3)].append(pencilGrids[gridRow][grid][loop])
					boxCols = convertBoxToCols(box)
					if any(num in i for i in boxCols[row]) and not any(num in i for i in boxCols[ls[0]]) and not any(num in i for i in boxCols[ls[1]]):
						for item in range(0, 3):
							if num in boxCols[row][item]:
								itemLoc = item
						if itemLoc == 0:
							thing = [itemLoc+gridRow*3, itemLoc+1+gridRow*3, itemLoc+2+gridRow*3]
						elif itemLoc == 1:
							thing = [itemLoc+gridRow*3, itemLoc+1+gridRow*3, itemLoc-1+gridRow*3]
						else:
							thing = [itemLoc+gridRow*3, itemLoc-1+gridRow*3, itemLoc-2+gridRow*3]
						for x in range(0, 9):
							if not x in thing and num in pencil[x][row+grid*3]:
								pencil[x][row+grid*3].remove(num)
								#steps.append(("Number claiming: removed", num, "from candidate list in cell (%r,%r)" % (x+1, row+grid*3+1)))
								steps += 1
								pencilGrids = ch.convertToGrids(pencil)
								applied = True
								#print ("YEAHHHHHHHHHHHHHHHHHHHH")
								#print(row+gridRow*3, x)
	return puzzle, pencil, applied, steps

def convertBoxToCols(box):
	cols = []
	for x in range(0, 3):
		col = []
		for y in range(0, 3):
			col.append(box[y][x])
		cols.append(col)
	return cols

def findIndexBox(ls, num):
	for x in range(0, 3):
		for y in range(0, 3):
			if ls[x][y] == num:
				return x, y
	return 111, 111

def rule4(puzzle, pencil, steps): #pairs
	applied = False
	
	for row in range(0, 9):
		for loc1 in range(0, 9):
			twin1 = pencil[row][loc1]
			proceed = False
			if len(twin1) == 2:
				for loc2 in range(0, 9):
					twin2 = pencil[row][loc2]
					if twin2 == twin1 and not loc2 == loc1:
						proceed = True
						loc3 = loc2
			if proceed == True:
				twin2 = pencil[row][loc3]
				for num in twin1:
					col3 = 0
					for x in pencil[row]:
						if num in x and not col3 == loc1 and not col3 == loc3:
							pencil[row][col3].remove(num)
							#steps.append(("Pairs:", twin1, "in cells (%r,%r) and (%r,%r). Removed", num, "from candidate list in cell (%r,%r)" % (row+1, loc1+1, row+1, loc3+1, row+1, col3+1)))
							steps += 1
							applied = True
							print("RULE4")
							print(twin1, twin2)
							ch.showPuzzle(pencil)
						col3 += 1

	pencilCols = ch.convertToCols(pencil)
	for row in range(0, 9):
		for loc1 in range(0, 9):
			twin1 = pencilCols[row][loc1]
			proceed = False
			if len(twin1) == 2:
				for loc2 in range(0, 9):
					twin2 = pencilCols[row][loc2]
					if twin2 == twin1 and not loc2 == loc1:
						proceed = True
						loc3 = loc2
			if proceed == True:
				twin2 = pencilCols[row][loc3]
				for num in twin1:
					col3 = 0
					for x in pencilCols[row]:
						if num in x and not col3 == loc1 and not col3 == loc3:
							pencilCols[row][col3].remove(num)
							#steps.append(("Pairs:", twin1, "in cells (%r,%r) and (%r,%r). Removed", num, "from candidate list in cell (%r,%r)" % (loc1+1, row+1, loc3+1, row+1, col3+1, row+1)))
							steps += 1
							applied = True
							print("RULE4")
							print(twin1, twin2)
							ch.showPuzzle(pencil)
						col3 += 1
	pencil = ch.convertToCols(pencilCols)
	
	pencilGrids = ch.convertToGrids(pencil)
	for gridRow in range(0, 3):
		for grid in range(0, 3):
			for loc1 in range(0, 9):
				twin1 = pencilGrids[gridRow][grid][loc1]
				proceed = False
				if len(twin1) == 2:
					for loc2 in range(0, 9):
						twin2 = pencilGrids[gridRow][grid][loc2]
						if twin2 == twin1 and not loc2 == loc1:
							proceed = True
							loc3 = loc2
				if proceed == True:
					twin2 = pencilGrids[gridRow][grid][loc3]
					for num in twin1:
						col3 = 0
						for x in pencilGrids[gridRow][grid]:
							if num in x and not col3 == loc1 and not col3 == loc3:
								pencilGrids[gridRow][grid][col3].remove(num)
								applied = True
								steps += 1
								print("RULE4")
								print(twin1, twin2)
								ch.showPuzzle(pencil)
							col3 += 1
	pencil = ch.convertToPuzzle(pencilGrids)
				
	return puzzle, pencil, applied, steps

def checkTwins(ls1, ls2):
	if ls1[0] in ls2 and ls1[1] in ls2:
		return True
	else:
		return False

def rule5(puzzle, pencil, steps): #triples
	applied = False
	for row in range(0, 9):
		for loc1 in range(0, 9):
			triple1 = pencil[row][loc1]
			for loc2 in range(0, 9):
				triple2 = pencil[row][loc2]
				for loc3 in range(0, 9):
					triple3 = pencil[row][loc3]
					if not loc3 == loc2 and not loc2 == loc1 and not loc1 == loc3 and not triple1 == [] and not triple2 == [] and not triple3 == []:
						if checkTriple(triple1, triple2, triple3) == True:
							locations = [loc1, loc2, loc3]
							ls = checkTriple(triple1, triple2, triple3, True)
							for x in range(0, 9):
								if not x in locations:
									for num in ls:
										if num in pencil[row][x]:
											pencil[row][x].remove(num)
											#steps.append(("Triples: ",triple1,"in cell (%r,%r),(%r,%r),(%r,%r). Removed", num, "from candidate list in cell (%r,%r)" % (row+1,loc1+1,row+1,loc2+1,row+1,loc3+1,row+1,x+1)))
											steps += 1
											applied = True
	for row in range(0, 9):
		pencilCols = ch.convertToCols(pencil)
		for loc1 in range(0, 9):
			triple1 = pencilCols[row][loc1]
			for loc2 in range(0, 9):
				triple2 = pencilCols[row][loc2]
				for loc3 in range(0, 9):
					triple3 = pencilCols[row][loc3]
					if not loc3 == loc2 and not loc2 == loc1 and not loc1 == loc3 and not triple1 == [] and not triple2 == [] and not triple3 == []:
						if checkTriple(triple1, triple2, triple3) == True:
							locations = [loc1, loc2, loc3]
							ls = checkTriple(triple1, triple2, triple3, True)
							for x in range(0, 9):
								if not x in locations:
									for num in ls:
										if num in pencilCols[row][x]:
											pencilCols[row][x].remove(num)
											#steps.append(("Triples: ",triple1,"in cell (%r,%r),(%r,%r),(%r,%r). Removed", num, "from candidate list in cell (%r,%r)" % (loc1+1,row+1,loc2+1,row+1,loc3+1,row+1,x+1,row+1)))
											steps += 1
											applied = True
		pencil = ch.convertToCols(pencilCols)

	pencilGrids = ch.convertToGrids(pencil)
	for gridRow in range(0, 3):
		for grid in range(0, 3):
			for loc1 in range(0, 9):
				triple1 = pencilGrids[gridRow][grid][loc1]
				for loc2 in range(0, 9):
					triple2 = pencilGrids[gridRow][grid][loc2]
					for loc3 in range(0, 9):
						triple3 = pencilGrids[gridRow][grid][loc3]
						if not loc3 == loc2 and not loc2 == loc1 and not loc1 == loc3 and not triple1 == [] and not triple2 == [] and not triple3 == []:
							if checkTriple(triple1, triple2, triple3) == True:
								locations = [loc1, loc2, loc3]
								ls = checkTriple(triple1, triple2, triple3, True)
								for x in range(0, 9):
									if not x in locations:
										for num in ls:
											if num in pencilGrids[gridRow][grid][x]:
												pencilGrids[gridRow][grid][x].remove(num)
												steps += 1
												applied = True

	pencil = ch.convertToPuzzle(pencilGrids)
	if applied == True:
		print("RULE5")
		ch.showPuzzle(pencil)
	return puzzle, pencil, applied, steps

def checkTriple(triple1, triple2, triple3, getLs=False):
	ls = []
	for x in triple1:
		if not x in ls:
			ls.append(x)
	for x in triple2:
		if not x in ls:
			ls.append(x)
	for x in triple3:
		if not x in ls:
			ls.append(x)
	if getLs == False:
		if len(ls) == 3:
			#print(triple1, triple2, triple3, ls)
			return True
		else:
			return False
	else:
		if len(ls) == 3:
			#print(triple1, triple2, triple3, ls)
			return ls
		else:
			return ls
#excluded candidates
def rule6(puzzle, pencil, steps):
	applied = False
	for row in range(0, 9):
		for col in range(0, 9):
			candidate = pencil[row][col]
			if len(candidate) > 2:
				for r in range(2, len(candidate)-1):
					combs = itertools.combinations(candidate, r)
					for part in combs:
						locs = [col]
						for col2 in range(0, 9):
							if col2 not in locs:
								if checkLists(pencil[row][col2], part):
									locs.append(col2)
						if len(locs) == r:
							for col3 in range(0, 9):
								if col3 not in locs:
									pencil, applied, steps = modifyLists(pencil, row, col3, part, applied, steps, "row")
									#applied = True
									print("DID IT")
	pencilCols = ch.convertToCols(pencil)
	for row in range(0, 9):
		for col in range(0, 9):
			candidate = pencilCols[row][col]
			if len(candidate) > 2:
				for r in range(2, len(candidate)-1):
					combs = itertools.combinations(candidate, r)
					for part in combs:
						locs = [col]
						for col2 in range(0, 9):
							if col2 not in locs:
								if checkLists(pencilCols[row][col2], part):
									locs.append(col2)
						if len(locs) == r:
							for col3 in range(0, 9):
								if col3 not in locs:
									pencilCols, applied, steps = modifyLists(pencilCols, row, col3, part, applied, steps, "col")
									#applied = True
									print("DID IT")
	pencil = ch.convertToCols(pencilCols)

	pencilGrids = ch.convertToGrids(pencil)
	for gridRow in range(0, 3):
		for grid in range(0, 3):
			for item in range(0, 9):
				candidate = pencilGrids[gridRow][grid][item]
				if len(candidate) > 2:
					for r in range(2, len(candidate)-1):
						combs = itertools.combinations(candidate, r)
						for part in combs:
							locs = [item]
							for col2 in range(0, 9):
								if col2 not in locs:
									if checkLists(pencilGrids[gridRow][grid][col2], part):
										locs.append(col2)
							if len(locs) == r:
								for col3 in range(0, 9):
									if col3 not in locs:
										pencilGrids, applied, steps = modifyLists(pencilGrids, gridRow, grid, part, applied, steps, "grid", col3)
										#applied = True
										print("DID IT")
	pencil = ch.convertToPuzzle(pencilGrids)

	return puzzle, pencil, applied, steps

def checkLists(ls1, ls2):
	for x in ls2:
		if x in ls1:
			return True
	return False

def modifyLists(ls1, row, col, ls2, applied, steps, typee, extra=None): #ls1[row][col] will be modified by items in ls2
	if extra == None:
		for x in ls2:
			if x in ls1[row][col]:
				ls1[row][col].remove(x)
				if applied == False:
					applied = True
					steps += 1
					#if typee == "row":
					#	steps.append(("Excluded Candidates: removed", num, "from candidate list in cell (%r,%r)" % row+1, col+1))
					#elif typee == "col":
					#	steps.append(("Excluded Candidates: removed", num, "from candidate list in cell (%r,%r)" % col+1, row+1))
	else:
		for x in ls2:
			if x in ls1[row][col][extra]:
				ls1[row][col][extra].remove(x)
				if applied == False:
					applied = True
					steps += 1
	return ls1, applied, steps

#Box-line reduction
def rule7(puzzle, pencil, steps):
	applied = False
	penGri = convertToPenGri(pencil)
	for row in range(0, 9):
		for num in range(1, 10):
			for part in range(0, 3):
				proceed1 = False
				for item in range(0, 3):
					if num in penGri[row][part][item]:
						proceed1 = True
				if proceed1:
					ls = [0,1,2]
					ls.remove(part)
					if not any(num in i for i in penGri[row][ls[0]]) and not any(num in i for i in penGri[row][ls[1]]):
						ls1 = [0,3,6]
						ls2 = [1,4,7]
						ls3 = [2,5,8]
						if row in ls1:
							penGri, applied, steps = remove2(penGri, row+1, part, num, applied, steps)
							penGri, applied, steps = remove2(penGri, row+2, part, num, applied, steps)
						if row in ls2:
							penGri, applied, steps = remove2(penGri, row-1, part, num, applied, steps)
							penGri, applied, steps = remove2(penGri, row+1, part, num, applied, steps)
						if row in ls3:
							penGri, applied, steps = remove2(penGri, row-1, part, num, applied, steps)
							penGri, applied, steps = remove2(penGri, row-2, part, num, applied, steps)
	pencil = convertToPen(penGri)

	pencilCols = ch.convertToCols(pencil)
	penGri = convertToPenGri(pencilCols)
	for row in range(0, 9):
		for num in range(1, 10):
			for part in range(0, 3):
				proceed1 = False
				for item in range(0, 3):
					if num in penGri[row][part][item]:
						proceed1 = True
				if proceed1:
					ls = [0,1,2]
					ls.remove(part)
					if not any(num in i for i in penGri[row][ls[0]]) and not any(num in i for i in penGri[row][ls[1]]):
						ls1 = [0,3,6]
						ls2 = [1,4,7]
						ls3 = [2,5,8]
						if row in ls1:
							penGri, applied, steps = remove2(penGri, row+1, part, num, applied, steps)
							penGri, applied, steps = remove2(penGri, row+2, part, num, applied, steps)
						if row in ls2:
							penGri, applied, steps = remove2(penGri, row-1, part, num, applied, steps)
							penGri, applied, steps = remove2(penGri, row+1, part, num, applied, steps)
						if row in ls3:
							penGri, applied, steps = remove2(penGri, row-1, part, num, applied, steps)
							penGri, applied, steps = remove2(penGri, row-2, part, num, applied, steps)
	pencilCols = convertToPen(penGri)
	pencil = ch.convertToCols(pencilCols)
	return puzzle, pencil, applied, steps

def convertToPenGri(pencil):
	penGri = []
	for row in range(0, 9):
		penGri.append(split(pencil[row], 3))
	return penGri

def convertToPen(penGri):
	pencil = []
	for row in penGri:
		part2 = []
		for part in row:
			part2 += part
		pencil.append(part2)
	return pencil

def split(ls, parts):
	loop = 1
	ls2 = []
	for i in ls:
		if loop % parts == 0:
			row = ls[loop-parts:loop]
			ls2.append(row)
		loop += 1
	return ls2

def remove2(ls, row, part, num, applied, steps):
	for item in range(0, 3):
		if num in ls[row][part][item]:
			ls[row][part][item].remove(num)
			if applied == False:
				applied = True
				steps += 1
	return ls, applied, steps

def check(dif, applied, difficulty):
	if applied == True and difficulty < dif:
		difficulty = dif
	return difficulty

def XWings(puzzle, pencil, steps):
	applied = False
	for num in range(1, 10):
		for row1 in range(0, 9):
			for col1 in range(0, 9):
				if num in pencil[row1][col1]:
					for col2 in range(0, 9):
						if not col1 == col2 and num in pencil[row1][col2]:
							for row2 in range(0, 9):
								for col3 in range(0, 9):
									if num in pencil[row2][col3] and col3 == col1:
										for col4 in range(0, 9):
											if not col3 == col4 and num in pencil[row2][col4] and col4 == col1:
												pencil, applied, steps = remove(pencil, row1, [col1, col2], num, steps)
												pencil, applied, steps = remove(pencil, row2, [col3, col4], num, steps)
												pencil, applied = ch.convertToCols(pencil)
												pencil, applied, steps = remove(pencil, col1, [row1, row3], num, steps)
												pencil, applied, steps = remove(pencil, col2, [row2, row4], num, steps)
												pencil, applied = ch.convertToCols(pencil)
												#steps.append(("X-wings: steps not available"))
												
	return puzzle, pencil, applied, steps

def remove(pencil, row, save, num, steps):
	applied = False
	for x in range(0, 9):
		if not x in save:
			pencil[row][x].remove(num)
			applied = True
			steps += 1
	return pencil, applied, steps

def execute(pencil, difficulty, steps):
	puzzle, pencil = refresh(pencil)
	oldPencil = copy.deepcopy(pencil)
	ch.showPuzzle(pencil)

	applied = False
	stuck = 0
	while applied == False:
		puzzle, pencil, applied, steps = rule1(puzzle, pencil, steps)
		difficulty = check(1, applied, difficulty)

		if applied == False:
			puzzle, pencil, applied, steps = rule2(puzzle, pencil, steps)
			difficulty = check(2, applied, difficulty)

			if applied == False:
				puzzle, pencil, applied2, steps = rule3(puzzle, pencil, steps)

				if applied == False:
					puzzle, pencil, applied2, steps = rule4(puzzle, pencil, steps)
					difficulty = check(3, applied, difficulty)

					if applied2 == False:
						puzzle, pencil, applied2, steps = rule5(puzzle, pencil, steps)
						difficulty = check(4, applied2, difficulty)

						if applied2 == False:
							puzzle, pencil, applied2, steps = rule7(puzzle, pencil, steps)
							difficulty = check(5, applied2, difficulty)

							#if applied2 == False:
							puzzle, pencil, applied2, steps = rule6(puzzle, pencil, steps)
							difficulty = check(6, applied2, difficulty)
									#puzzle, pencil, applied2 = hiddenRule4(puzzle, pencil)

							#puzzle, pencil, applied2, steps = XWings(puzzle, pencil, steps)
							if applied2 == False:
								stuck += 1
								if stuck > 3:
									applied = True
		#if not stuck == 0:
					#			elif applied2 == True:
					#				stuck = 0
	puzzle, pencil = refresh(puzzle)
	ch.showPuzzle(oldPencil)
	ch.showPuzzle(pencil)
	did = True
	if pencil == oldPencil:
		did = False

	return puzzle, pencil, did, difficulty, steps
