import solver
import convertor
import time
#string = list("003020600900305001001806400008102900700000008006708200002609500800203009005010300") #WORKS
#string = list("200080300060070084030500209000105408000000000402706000301007040720040060004010003") #WORKS
#string = list("000000907000420180000705026100904000050000040000507009920108000034059000507000000") #WORKS
#string = list("030050040008010500460000012070502080000603000040109030250000098001020600080060020") #WORKS
#string = list("200170603050000100000006079000040700000801000009050000310400000005000060906037002") #WORKS
#string = list("800003000600240300070000600000005094038000760410700000002000070005017009000900003") #WORKS

string = list("300200000000107000706030500070009080900020004010800050009040301000702000000008006") #hardest in euler's problem

#string = list("000158000002060800030000040027030510000000000046080790050000080004070100000325000") #WORKS
#string = list("000609000590000001000001005000407003000000096080010004008074509007508100600020070") #WORKS
#string = list("4...3.......6..8..........1....5..9..8....6...7.2........1.27..5.3....4.9........")
#string = list("8.5.....2...9.1...3.........6.7..4..2...5...........6....38.....1....9...4.....7.")
#string = list("000000000000000000000000000000000000000000000000000000000000000000000000000000000")
#string = list("001007090590080001030000080000005800050060020004100000080000030100020079020700400")
#string = list("000537000065000340300060005070903080080000030050608010400020009021000650000376000")

#myFile = open("problems.txt", "r")
#string = myFile.readlines()[49]
#string = myFile.readlines()[6]
#string = list(string[:-1])
input("HELLO AND WELCOME TO MY SUDOKU SOLVER BY DHANISH")
choice = input("DO YOU WANT ME TO SHOW YOU AN EXAMPLE [1] OR DO YOU WANT ME TO SOLVE YOUR SUDOKU? [2]: ")
if choice == "2":
	print("")
	print("okay tell me the sudoku in one line as numbers. The blank parts being '0' or a '.' ")
	string = list(input(">>>>"))
	puzzle = convertor.ToList(string)
	puzzle, oldPuzzle, solved, timeTaken, d1, d2, steps = solver.execute(puzzle)
elif choice == "1":
	print("")
	choice = input("Do you want an example form euler's problems [1] or no [2]: ")
	if choice == "1":
		import eulerSolver
	else:
		print("OKAY")
		puzzle = convertor.ToList(string)
		puzzle, oldPuzzle, solved, timeTaken, d1, d2, steps = solver.execute(puzzle)
try:
	print("")
	[print (i) for i in oldPuzzle]
	print("")
	[print (i) for i in puzzle]
	print("")
	print("SOLVED:", solved)
	print("problem", "took", timeTaken, "seconds to solve")
	print("problem took", steps, "steps to solve")
	print("Sudoku's difficulty level for a human:", d1)
	print("Sudoku's difficulty level for a computer:", d2)
	print("")
except NameError:
	pass
