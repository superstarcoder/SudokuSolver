import pygame
from random import randint

def initialize():
	global width, height, size, screen, done, fps, clock
	global grid_h, grid_v, grid1, grid2, grid3, grid4, grid5, grid6, grid7, grid8, grid9
	global BLUE, BLACK, WHITE, GREEN, RED, YELLOW, ORANGE, BLUE

	width = 1900
	height = 1000
	fps = 1000
	size = (width, height)
	#screen = pygame.display.set_mode(size, pygame.RESIZABLE)
	clock = pygame.time.Clock()

	done = False

	grid1 = [[0,0,0],[0,0,0],[0,0,0]]
	grid4 = [[0,0,0],[0,0,0],[0,0,0]]
	grid7 = [[0,0,0],[0,0,0],[0,0,0]]

	grid2 = [[0,0,0],[0,0,0],[0,0,0]]
	grid5 = [[0,0,0],[0,0,0],[0,0,0]]
	grid8 = [[0,0,0],[0,0,0],[0,0,0]]

	grid3 = [[0,0,0],[0,0,0],[0,0,0]]
	grid6 = [[0,0,0],[0,0,0],[0,0,0]]
	grid9 = [[0,0,0],[0,0,0],[0,0,0]]

	grid_h = [[grid1,grid2,grid3], [grid4,grid5,grid6], [grid7,grid8,grid9]]
	grid_v = [[grid1,grid4,grid5], [grid2,grid5,grid8], [grid3,grid6,grid9]]

	#pygame.init()

	BLACK = (0, 0, 0)
	WHITE = (255, 255, 255)
	GREEN = (0, 255, 0)
	RED = (255, 0, 0)
	YELLOW = (236, 239, 55) 
	ORANGE = (255, 191, 1)
	BLUE = (0, 22, 255)

def generate():
	global grid_h, grid_v, grid1, grid2, grid3, grid4, grid5, grid6, grid7, grid8, grid9
	grid_h = [[grid1,grid2,grid3], [grid4,grid5,grid6], [grid7,grid8,grid9]]
	grid_v = [[grid1,grid4,grid5], [grid2,grid5,grid8], [grid3,grid6,grid9]]
	row_i2 = 0
	for row in grid_h: #choose a row in the sudoku
		grid_i = 0
		for grid in row: #in that row, choose a grid
			row_i = 0
			for grid_row in grid: #in that grid, cchoose a row
				col_i = 0
				for num in grid_row: #in that row, choose a number

					if num == 0: #if the number is empty
						generated = False
						#for num2 in range(1, 10):
						loop =  0
						while not generated:
							num2 = randint(1, 9)
							#for num2 in range (1, 2):
							#check if that number is there in the grid
							booll = check(num2, grid)
							if booll == False: #if that number isn't there in the grid
								#check if the number is not there horizontally
								if grid_i == 0:
									grid20 = row[1][row_i]
									grid30 = row[2][row_i]
								elif grid_i == 1:
									grid20 = row[0][row_i]
									grid30 = row[2][row_i]
								elif grid_i == 2:
									grid20 = row[1][row_i]
									grid30 = row[0][row_i]
								#check if same no. is there horizontally
								booll = check_h(num2, row_i, grid, grid20, grid30)
								if booll == False: #if same no. is not there horizontally
								#	if grid_i == 0:
								#		grid20 = grid_v[grid_i][1]
								#		grid30 = grid_v[grid_i][2]
								#	elif grid_i == 1:
								#		grid20 = grid_v[grid_i][0]
								#		grid30 = grid_v[grid_i][2]
								#	elif grid_i == 2:
								#		grid20 = grid_v[grid_i][0]
								#		grid30 = grid_v[grid_i][1]
									#check if there is same no. vertically
									#booll = check_v(num2, col_i, grid_i, grid20, grid30)
									booll = check_v(num2, grid_i, col_i, grid)
									#if no. is perfect for putting in the sudoku
									if booll == False:
										#print (row)
										#print (grid_h[row_i2][grid_i][row_i][col_i])
										grid_h[row_i2][grid_i][row_i][col_i] = num2
										#print (grid_h[row_i2][grid_i][row_i][col_i])
										print (row_i2, grid_i, row_i, col_i)
										print (grid_h)
										generated = True
							if loop > 10:
								initialize()
								generate()
								return
							loop += 1
					col_i += 1
				row_i += 1
			grid_i += 1
		row_i2 += 1

def replace(replacement, replaced, ls):
	loop = 0
	for x in ls:
		if x == replacement:
			ls[loop] = replaced
			return ls
		loop += 1

def show():
	global grid_h
	for row in grid_h:
		for grid in row:
			print (grid)

# checks if a number exists in a grid
def check(num, grid):
	for row in grid:
		if num in row:
			return True
	return False

#check if no. is there in a list horizontally
def check_h(num, row, grid10, grid20, grid30):
	if num in grid20 or num in grid30:
		return True
	return False

#check if no. is there in a list vertically
def check_v(num, grid_i, col, grid):
	#for x in range(0, 3):
	#	print (grid20[x][col], grid30[x][col])
	#	if num == grid20[x][col] or num == grid30[x][col]:
	#		return True
	#return False
	global grid_h
	for row in range(0, 3):
		if not grid_h[row][grid_i] == grid:
			for row_i in range(0, 3):
				#print (grid_h[row][grid_i][row_i][col])
				if grid_h[row][grid_i][row_i][col] == num:
					return True
	return False

initialize()
generate()
print (grid_h)
print (grid_v)
show()
#booll = check_h(1, 0, grid1, grid2[0], grid3[0])
#print (booll)
done = True
while not done:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
	screen.fill(BLUE)
	clock.tick(fps)
	pygame.display.update()


