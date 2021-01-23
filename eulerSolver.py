import solver
import convertor
import time
def do(myTime, start, stop):
	for x in range(start, stop):
		myFile = open("problems.txt", "r")
		string = myFile.readlines()[x]
		string = string[:-1]
		print(string)
		string = list(string)
		puzzle = convertor.ToList(string)
		puzzle, oldPuzzle, solved, timeTaken, d1, d2, steps = solver.execute(puzzle)
		
		print("")
		[print (i) for i in oldPuzzle]
		print("")
		[print (i) for i in puzzle]
		print("")
		print("SOLVED:", solved)
		print("problem", x+1, "took", timeTaken, "seconds to solve")
		print("problem took", steps, "steps to solve")
		print("Sudoku's difficulty level for a human:", d1)
		print("Sudoku's difficulty level for a computer:", d2)
		print("")

		try:
			time.sleep(myTime)
		except:
			print("WARNING: THE INPUTED TIME INTERVAL DOESN'T WORK")
			time.sleep(3)

input("WELCOME TO EULER SOLVER BY DHANISH! ")
def choice1():
	print("")
	print("there are 50 sudokus")
	choice = int(input("Do you want me to solve all sudokus [1] or a given range of sudokus [2] or a particular sudoku [3]: "))
	if choice == 1:
		print("")
		myTime = int(input("what's your time interval between each sudoku? (please tell me a number. 3 is recommended): "))
		do(myTime, 0, 50)
	elif choice == 2:
		print("")
		start = int(input("tell me the starting sudoku number [inclusive]: "))
		print("")
		end = int(input("tell me the ending sudoku number [inclusive]: "))
		print("")
		myTime = int(input("what's your time interval between each sudoku? (please tell me a number. 3 is recommended): "))
		do(myTime, start-1, end)
	elif choice == 3:
		print("")
		start = int(input("tell me which sudoku u want to solve: "))
		do(0, start-1, start)
	else:
		print("HUH??")
		return
	print("")
	print("THANKS FOR USING EULERSOLVER!")
choice1()
