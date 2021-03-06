import pygame
from random import randint

def initialize():
	global width, height, size, screen, done, fps, clock, rows
	global BLUE, BLACK, WHITE, GREEN, RED, YELLOW, ORANGE, BLUE

	rows = []
	width = 1900
	height = 1000
	fps = 1000
	size = (width, height)
	#screen = pygame.display.set_mode(size, pygame.RESIZABLE)
	clock = pygame.time.Clock()

	done = False

	#pygame.init()

	BLACK = (0, 0, 0)
	WHITE = (255, 255, 255)
	GREEN = (0, 255, 0)
	RED = (255, 0, 0)
	YELLOW = (236, 239, 55) 
	ORANGE = (255, 191, 1)
	BLUE = (0, 22, 255)

def generate():
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

#def show():
#	global grid_h
#	for row in grid_h:
#		for grid in row:
#			print (grid)

# checks if a number exists in a grid
def check(num, grid):
	for row in grid:
		if num in row:
			return True
	return False



initialize()
generate()
print (rows)
for i in rows: print (i)

#print (grid_h)
#print (grid_v)
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


