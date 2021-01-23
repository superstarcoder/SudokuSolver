def ToList(string):
	loop = 1
	puzzle = []
	for i in string:
		if i == ".":
			string[loop-1] = 0
		else:
			string[loop-1] = int(string[loop-1])
		if loop % 9 == 0:
			row = string[loop-9:loop]
			puzzle.append(row)
		loop += 1
	return puzzle
