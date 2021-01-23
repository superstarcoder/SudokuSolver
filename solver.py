import crosshatching
import convertor
import pencilling
import time
import copy
import guessing
#string = list("003020600900305001001806400008102900700000008006708200002609500800203009005010300") #WORKS
#string = list("200080300060070084030500209000105408000000000402706000301007040720040060004010003") #WORKS
#string = list("000000907000420180000705026100904000050000040000507009920108000034059000507000000") #WORKS
#string = list("030050040008010500460000012070502080000603000040109030250000098001020600080060020") #WORKS
#string = list("200170603050000100000006079000040700000801000009050000310400000005000060906037002") #WORKS
#string = list("800003000600240300070000600000005094038000760410700000002000070005017009000900003") #WORKS
#string = list("300200000000107000706030500070009080900020004010800050009040301000702000000008006") #hardest in euler's problem
#string = list("000158000002060800030000040027030510000000000046080790050000080004070100000325000") #WORKS
#string = list("000609000590000001000001005000407003000000096080010004008074509007508100600020070") #WORKS
#string = list("4...3.......6..8..........1....5..9..8....6...7.2........1.27..5.3....4.9........")
#string = list("8.5.....2...9.1...3.........6.7..4..2...5...........6....38.....1....9...4.....7.")
#string = list("")

#puzzle = crosshatching.execute(puzzle)

def checkIfDone(puzzle):
	for row in puzzle:
		for num in row:
			if num == 0:
				return False
	return True

def checkIfDone2(pencil):
	count = 0
	for row in pencil:
		for col in row:
			if col == []:
				count += 1
	if count == 81:
		return 1
	return 0

def execute(puzzle, wantGuessing=True):
	oldPuzzle = copy.deepcopy(puzzle)
	start = time.time()
	done = False
	difficulty = 0
	crosshatching.showPuzzle(puzzle)
	steps = 0
	while not done:
		puzzle, steps = crosshatching.execute(puzzle, steps)
		puzzle, pencil, did, difficulty, steps = pencilling.execute(puzzle, difficulty, steps)
		done = checkIfDone(puzzle)
		if did == False:
			done = True

	if not any(0 in i for i in puzzle):
		if difficulty == 0:
			d1 = "very easy"
		elif difficulty == 1:
			d1 = "easy"
		elif difficulty == 2:
			d1 = "medium"
		elif difficulty == 3:
			d1 = "hard"
		elif difficulty == 4:
			d1 = "very hard"
		elif difficulty == 5:
			d1 = "super hard"
		else:
			d1 = "extreme"
		timeTaken = time.time()-start

		if timeTaken < 2:
			d2 = "super easy"
		elif timeTaken < 10:
			d2 = "very easy"
		elif timeTaken < 20:
			d2 = "easy"
		elif timeTaken < 30:
			d2 = "medium"
		elif timeTaken < 40:
			d2 = "hard"
		elif timeTaken < 50:
			d2 = "very hard"
		else:
			d2 = "super hard"
	else:
		d1 = "insane"
		d2 = "extreme"
	crosshatching.showPuzzle(oldPuzzle)
	crosshatching.showPuzzle(puzzle)
	#popping = []
	#print(steps)
	#for x in range(len(steps)):
	#	if steps[x-1] == steps[x]:
	#		popping.append(steps[x])
	#for x in popping:
	#	steps.remove(x)
	#steps2 = []
	#for x in steps:
	#	z = ""
	#	for y in x:
	#		z += str(y)+" "
	#	steps2.append(z)
		#print(z)
	#steps2 = list(set(steps2))
	solved = checkIfDone(puzzle)
	timeTaken = time.time()-start
	if solved == False and wantGuessing == True:
		start = time.time()
		puzzle = guessing.execute(0,0, puzzle)
		if not any(0 in i for i in puzzle):
			if timeTaken < 2:
				d2 = "super easy"
			elif timeTaken < 10:
				d2 = "very easy"
			elif timeTaken < 20:
				d2 = "easy"
			elif timeTaken < 30:
				d2 = "medium"
			elif timeTaken < 40:
				d2 = "hard"
			elif timeTaken < 50:
				d2 = "very hard"
			else:
				d2 = "super hard"
		else:
			d1 = "insane"
			d2 = "extreme"
	solved = checkIfDone(puzzle)
	return puzzle, oldPuzzle, solved, time.time()-start, d1, d2, steps
