""" Graphical version of sudoku solver """
import pygame
from pygame.locals import *
from random import randint
import time
import solver
import copy
import pencilling as pn
import convertor
import generator

""" initialize pygame here """
width = 1950
height = 1050
size = (width, height)
screen = pygame.display.set_mode(size, pygame.RESIZABLE)	
#screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)	
clock = pygame.time.Clock()
pygame.init()

""" main variables defined here """
done = False
touching = False
opened = False
showTime = True
#showErrors = True
showErrors = False
clearAll = False

fps = 100
start = 0
place = "menu1"
#solveMode = "pause"
solveMode = "pause"
selectPos = [0,0]
puzzle = []
sPuzzle = [[0]*9 for i in range(9)]
blackText = []
pencil = []
redText = []

BLACK = (0, 0, 0)
BROWN = (114, 31, 3)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (236, 239, 55) 
ORANGE = (255, 191, 1)
BLUE = (0, 22, 255)
LIGHT_BLUE = (112, 166, 255)
GREY = (81, 81, 81)

ZERO = (160, 255, 185)
ONE = (76, 255, 124)
TWO = (76, 255, 96)
THREE = (207, 255, 96)
FOUR = (255, 241, 96)
FIVE = (255, 178, 96)
SIX = (255, 125, 96)
SEVEN = (255, 40, 40)

""" solveMode(s)- 'pause','play','editing' """

""" all images, music and sounds are loaded here """
bg = pygame.image.load("background.png")
bg = pygame.transform.scale(bg, (1950, 1050))
bg2 = pygame.image.load("background2.png")
bg2 = pygame.transform.scale(bg2, (1950, 1050))
bg3 = pygame.image.load("background3.png")
bg3 = pygame.transform.scale(bg3, (1950, 1050))

playB = pygame.image.load("playB.png")
playB = pygame.transform.scale(playB, (200, 200))
solveB = pygame.image.load("solveB.png")
sudokuSolverB = pygame.image.load("sudokuSolverB.png")
exitB = pygame.image.load("exitB.png")
exitB = pygame.transform.scale(exitB, (55, 55))
solveCellB = pygame.image.load("solveCellB.png")
solvePuzzleB = pygame.image.load("solvePuzzleB.png")
menuB = pygame.image.load("menuB.png")
closeB = pygame.image.load("closeB.png")
clearAllB = pygame.image.load("clearAllB.png")
showPencilsB = pygame.image.load("showPencilsB.png")
loadOrSaveB = pygame.image.load("loadOrSaveB.png")
loadB = pygame.image.load("loadB.png")
saveB = pygame.image.load("saveB.png")
backB = pygame.image.load("backB.png")
startB = pygame.image.load("startB.png")
pauseB = pygame.image.load("pauseB.png")

sudoku = pygame.image.load("sudoku.png")
sudoku = pygame.transform.scale(sudoku, (900, 900))
select = pygame.image.load("select.png")
select = pygame.transform.scale(select, (106, 106))
loading = pygame.image.load("loading.png")
loading2 = pygame.image.load("loading2.png")

hoverS = pygame.mixer.Sound('hover.wav')
unhoverS = pygame.mixer.Sound('unhover.wav')
selectS = pygame.mixer.Sound('select.wav')
song1 = pygame.mixer.Sound('song2.wav')
hitS = pygame.mixer.Sound('hit.wav')

#music = pygame.mixer.music.load('music.mp3')

""" all functions go here """
def centreBlit(img, dx=0, dy=0):
	width = 1950
	height = 1050

	width2 = (0.5 * img.get_rect().width) + dx
	height2 = (0.5 * img.get_rect().height) + dy
	centre = [width/2-width2, height/2-height2]
	screen.blit(img, centre)
	
	return pygame.Rect(centre, pygame.Surface.get_size(img))
	#return img.get_rect()

def renderText(myText, myFont, mySize, myColour, pos, centre, dis=(0,0)):
	font = pygame.font.SysFont(myFont, mySize, True, False)
	text = font.render(myText, True, myColour)
	if centre == True:
		width2 = 0.5 * text.get_rect().width
		height2 = 0.5 * text.get_rect().height
		screen.blit(text, (width/2-width2+dis[0], height/2-height2+dis[1]))
		return (width2, height2)
	else:
		screen.blit(text,pos)
	width2 = text.get_rect().width
	return width2

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
		print("False")
		return False
	else:
		print("True")
		return True

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

""" main loop """
#song1.play(-1)
pygame.mixer.music.set_volume(0.1)
#pygame.mixer.music.play(-1)
while not done:
	rect0 = pygame.Rect(((1900-exitB.get_rect().width)+20, 0), pygame.Surface.get_size(exitB))

	if place == "menu1":
		screen.blit(bg,(0,0))
		rect1 = centreBlit(playB, 0, -150)

		if rect1.collidepoint(pygame.mouse.get_pos()):
			if touching == False:
				hoverS.play()
				playB = pygame.transform.scale(playB, (250, 250))
				touching = True
		elif touching == True:
			unhoverS.play()
			playB = pygame.image.load("playB.png")
			playB = pygame.transform.scale(playB, (200, 200))
			touching = False

		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				if rect1.collidepoint(pygame.mouse.get_pos()):
					selectS.play()
					place = "menu2"
				if rect0.collidepoint(pygame.mouse.get_pos()):
					done = True
			if event.type == pygame.QUIT:
				done = True
		rect1 = centreBlit(playB, 0, -150)

	elif place == "menu2":
		screen.blit(bg2,(0,0))
		rect1 = centreBlit(solveB, 0, 100)
		rect2 = centreBlit(sudokuSolverB, 0, -100)
		#screen.blit(exitB,((1900-exitB.get_rect().width)+20,0))

		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				if rect0.collidepoint(pygame.mouse.get_pos()):
					done = True
				if rect1.collidepoint(pygame.mouse.get_pos()):
					selectS.play()
					place = "solve"
					start = 0
					extra = 0
					screen.blit(loading2, (200,200))
					pygame.display.update()
					puzzle, sPuzzle = generator.execute()
					for row in range(0, 9):
						for col in range(0, 9):
							if not sPuzzle[row][col] == 0:
								blackText.append([row,col])
				if rect2.collidepoint(pygame.mouse.get_pos()):
					selectS.play()
					place = "sudokuSolver"
			if event.type == pygame.QUIT:
				done = True
				
	elif place == "sudokuSolver":
		screen.blit(bg3,(0,0))
		rect1 = pygame.Rect((150,87.5), pygame.Surface.get_size(solveCellB))
		rect2 = pygame.Rect((150,237.5), pygame.Surface.get_size(solvePuzzleB))
		rect3 = pygame.Rect((150,387.5), pygame.Surface.get_size(clearAllB))
		rect6 = pygame.Rect((150,537.5), pygame.Surface.get_size(showPencilsB))
		rect7 = pygame.Rect((150,687.5), pygame.Surface.get_size(loadOrSaveB))
		rect5 = pygame.Rect((150,837.5), pygame.Surface.get_size(menuB))

		rect4 = pygame.Rect((1495,855), pygame.Surface.get_size(closeB))

		centreBlit(sudoku)
		screen.blit(select,(530+(select.get_width()-8)*selectPos[0], 81+(select.get_height()-8)*selectPos[1]))
		pygame.draw.rect(screen, LIGHT_BLUE, [50, 75, 425, 900])
		screen.blit(solveCellB, (150,87.5))
		screen.blit(solvePuzzleB, (150,237.5))
		screen.blit(clearAllB, (150,387.5))
		screen.blit(showPencilsB, (150,537.5))
		screen.blit(loadOrSaveB, (150,687.5))
		screen.blit(menuB, (150,837.5))

		#keysNum = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]
		#keysNum = [49, 50, 51, 52, 53, 54, 55, 56, 57]
		#keysNum = range(49, 58)
		key = pygame.key.get_pressed()
		for keyNum in range(48, 58):
			if key[keyNum] and pygame.key.get_mods() & pygame.KMOD_SHIFT and not keyNum == 48:
				if not pencil == []:
					if not str(keyNum-48) in pencil[selectPos[0]][selectPos[1]]:
						if pencil[selectPos[0]][selectPos[1]] == "":
							pencil[selectPos[0]][selectPos[1]] = str(keyNum-48)
						else:
							loop = 0
							for item in pencil[selectPos[0]][selectPos[1]]:
								if int(item) > int(keyNum-48):
									#pencil[selectPos[0]][selectPos[1]].insert(loop-1, str(keyNum-48))
									string1 = pencil[selectPos[0]][selectPos[1]][:loop]
									string2 = pencil[selectPos[0]][selectPos[1]][loop:]
									string1 += str(keyNum-48)
									pencil[selectPos[0]][selectPos[1]] = string1+string2
									break
								elif int(pencil[selectPos[0]][selectPos[1]][-1]) < keyNum-48:
									pencil[selectPos[0]][selectPos[1]] += str(keyNum-48)
									break
								loop += 1
				else:
					pencil = [[""]*9 for i in range(9)]
					pencil[selectPos[0]][selectPos[1]] = str(keyNum-48)

			elif key[keyNum] and pygame.key.get_mods() & pygame.KMOD_CTRL and not keyNum == 48:
				if str(keyNum-48) in pencil[selectPos[0]][selectPos[1]]:
					pencil[selectPos[0]][selectPos[1]] = list(pencil[selectPos[0]][selectPos[1]])
					pencil[selectPos[0]][selectPos[1]].remove(str(keyNum-48))
					b = ""
					for x in pencil[selectPos[0]][selectPos[1]]: b += x
					pencil[selectPos[0]][selectPos[1]] = b

			elif key[keyNum]:
				sPuzzle[selectPos[0]][selectPos[1]] = keyNum-48
				if not keyNum == 48:
					selectS.play()
					blackText.append([selectPos[0], selectPos[1]])
					puzzle = []
					if not pencil == []:
						rawPencil = []
						sPuzzle, rawPencil = pn.refresh(sPuzzle)
						#pencil = [[] for i in range(9)]
						pencil = []
						for row in range(0, 9):
							sub = []
							for col in range(0, 9):
								string = ""
								for item in rawPencil[row][col]:
									string += str(item)
								sub.append(string)
							pencil.append(sub)

		for row in range(-4, 5):
			for col in range(-4, 5):
				if not sPuzzle[row+4][col+4] == 0:
					if [row+4, col+4] in blackText:
						renderText(str(sPuzzle[row+4][col+4]), "aharoni", 80, BLACK, False, True, ((row)*99, (col)*99))
					else:
						renderText(str(sPuzzle[row+4][col+4]), "aharoni", 80, BLUE, False, True, ((row)*99, (col)*99))

		if opened == True:
			pygame.draw.rect(screen, LIGHT_BLUE, [1475, 75, 400, 900])
			screen.blit(closeB, (1495, 855))
			width2 = renderText("SOLVED:", "aharoni", 50, BLUE, (1485, 95), False)
			if solved == False:
				renderText("False", "aharoni", 50, RED, (1475+width2+10, 95), False)
			else:
				renderText("True", "aharoni", 50, GREEN, (1475+width2+10, 95), False)
			renderText("DIFFICULTY:", "aharoni", 50, BLUE, (1485, 170), False)

			renderText("For a human:", "aharoni", 50, BLACK, (1485, 245), False)
			d1Ls1 = [ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, RED]
			d1Ls2 = ["very easy", "easy", "medium", "hard", "very hard", "super hard", "extreme", "insane"]
			if d1 == "insane":
				renderText(d1+"-guesswork", "aharoni", 45, d1Ls1[d1Ls2.index(d1)], (1485, 320), False)
			else:
				renderText(d1, "aharoni", 50, d1Ls1[d1Ls2.index(d1)], (1485, 320), False)

			renderText("For a computer:", "aharoni", 50, BLACK, (1485, 395), False)
			d2Ls1 = [ZERO, ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN]
			d2Ls2 = ["super easy", "very easy", "easy", "medium", "hard", "very hard", "super hard", "extreme"]
			renderText(d2, "aharoni", 50, d2Ls1[d2Ls2.index(d2)], (1485, 470), False)

			renderText("TIME:", "aharoni", 50, BLUE, (1485, 545), False)
			renderText(str(round(timeTaken, 4)) + " SECONDS", "aharoni", 50, GREEN, (1485, 620), False)

			renderText("STEPS:", "aharoni", 50, BLUE, (1485, 695), False)
			renderText(str(steps) + " STEPS", "aharoni", 50, YELLOW, (1485, 770), False)

		#screen.blit(select,(530+(select.get_width()-8)*0, 81+(select.get_height()-8)*0))
		#renderText("123456789", "aharoni", 25, GREY, (535+(select.get_width()-8)*0, 81+(select.get_height()-8)*0), False)
		#renderText("123456789", "aharoni", 25, GREY, (535+(select.get_width()-8)*1, 81+(select.get_height()-8)*0), False)
		if not pencil == []:
			for row in range(0, 9):
				for col in range(0, 9):
					if not pencil[row][col] == "":
						renderText(pencil[row][col], "aharoni", 25, GREY, (537.5+(select.get_width()-8)*row, 91+(select.get_height()-8)*col), False)

		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				#exit button
				if rect0.collidepoint(pygame.mouse.get_pos()):
					done = True
				#solve cell button
				if rect1.collidepoint(pygame.mouse.get_pos()):
					screen.blit(loading, (200,200))
					pygame.display.update()
					if puzzle == []:
						puzzle = copy.deepcopy(sPuzzle)
						puzzle, oldPuzzle, solved, timeTaken, d1, d2, steps = solver.execute(puzzle)
						sPuzzle[selectPos[0]][selectPos[1]] = puzzle[selectPos[0]][selectPos[1]]
						opened = True
					else:
						sPuzzle[selectPos[0]][selectPos[1]] = puzzle[selectPos[0]][selectPos[1]]
				#solve puzzle button
				if rect2.collidepoint(pygame.mouse.get_pos()):
					screen.blit(loading, (200,200))
					pygame.display.update()
					if puzzle == []:
						sPuzzle, oldPuzzle, solved, timeTaken, d1, d2, steps = solver.execute(sPuzzle)
						opened = True
					else:
						sPuzzle = copy.deepcopy(puzzle)
					sPuzzle, rawPencil = pn.refresh(sPuzzle)
					pencil = []
					for row in range(0, 9):
						sub = []
						for col in range(0, 9):
							string = ""
							for item in rawPencil[row][col]:
								string += str(item)
							sub.append(string)
						pencil.append(sub)
					#showPencilsB = pygame.image.load("hidePencilsB.png")
				#clear all button
				if rect3.collidepoint(pygame.mouse.get_pos()):
					puzzle = []
					pencil = []
					sPuzzle = [[0]*9 for i in range(9)]
					blackText = []
					redText = []
				#menu button
				if rect5.collidepoint(pygame.mouse.get_pos()):
					puzzle = []
					pencil = []
					sPuzzle = [[0]*9 for i in range(9)]
					blackText = []
					redText = []
					opened = False
					place = "menu1"
				#back(close) button
				if opened == True and rect4.collidepoint(pygame.mouse.get_pos()):
					opened = False
				#showPencils button
				if rect6.collidepoint(pygame.mouse.get_pos()):
					rawPencil = []
					sPuzzle, rawPencil = pn.refresh(sPuzzle)
					#pencil = [[] for i in range(9)]
					if pencil == []:
						pencil = []
						for row in range(0, 9):
							sub = []
							for col in range(0, 9):
								string = ""
								for item in rawPencil[row][col]:
									string += str(item)
								sub.append(string)
							pencil.append(sub)
						showPencilsB = pygame.image.load("hidePencilsB.png")
					else:
						pencil = []
						showPencilsB = pygame.image.load("showPencilsB.png")
				if rect7.collidepoint(pygame.mouse.get_pos()):
					oldPlace = "sudokuSolver"
					place = "loadOrSave1"
					
			if event.type == pygame.QUIT:
				done = True
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_DOWN and not selectPos[1] == 8:
					selectPos[1] += 1
				if event.key == pygame.K_UP and not selectPos[1] == 0:
					selectPos[1] -= 1
				if event.key == pygame.K_RIGHT and not selectPos[0] == 8:
					selectPos[0] += 1
				if event.key == pygame.K_LEFT and not selectPos[0] == 0:
					selectPos[0] -= 1
	elif place == "loadOrSave1":
		screen.blit(bg3,(0,0))
		screen.blit(backB,(0,0))
		rect1 = centreBlit(loadB, 0, 100)
		rect2 = centreBlit(saveB, 0, -100)
		rect3 = pygame.Rect((0,0), pygame.Surface.get_size(backB))
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				if rect0.collidepoint(pygame.mouse.get_pos()):
					done = True
				if rect1.collidepoint(pygame.mouse.get_pos()):
					name = ""
					font = pygame.font.Font(None, 100)
					error = False
					place = "load1"
				if rect2.collidepoint(pygame.mouse.get_pos()):
					name = ""
					font = pygame.font.Font(None, 100)
					saved = False
					place = "save1"
				if rect3.collidepoint(pygame.mouse.get_pos()):
					place = oldPlace
			if event.type == pygame.QUIT:
				done = True
	elif place == "save1":
		screen.blit(bg3,(0,0))
		screen.blit(backB,(0,0))
		rect1 = pygame.Rect((0,0), pygame.Surface.get_size(backB))
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				if rect0.collidepoint(pygame.mouse.get_pos()):
					done = True
				if rect1.collidepoint(pygame.mouse.get_pos()):
					place = oldPlace
			if event.type == pygame.KEYDOWN and saved == False:
				if event.unicode.isalpha():
					name += event.unicode
				if event.key == K_BACKSPACE:
					name = name[:-1]
				if event.key == K_RETURN and not name == "":
					try:
						created_file = open("gui"+name+".txt","w+")
						created_file.close()
						write_file = open("gui"+name+".txt", "w")
						save = ""
						for row in range(0, 9):
							for col in range(0, 9):
								save += str(sPuzzle[col][row])
						write_file.write(save)
						write_file.close()
						saved = True
						place = oldPlace
					except:
						saved = None
				if event.type == pygame.QUIT:
					done = True
		#def renderText(myText, myFont, mySize, myColour, pos, centre, dis=(0,0)):
		if saved == False:
			renderText("TYPE THE FILE WHERE YOU WANT TO SAVE THE SUDOKU", "aharoni", 50, BLUE, False, True, (0, -200))
			block = font.render(name, True, (0, 0, 0))
			rect = block.get_rect()
			rect.center = screen.get_rect().center
			screen.blit(block, rect)
		elif saved == True:
			renderText("YOUR SUDOKU WAS SAVED TO FILE \"" +name+ "\"", "aharoni", 80, GREEN, False, True)
		else:
			renderText("ERROR", "aharoni", 200, RED, False, True)

	elif place == "load1":
		screen.blit(bg3,(0,0))
		screen.blit(backB,(0,0))
		rect1 = pygame.Rect((0,0), pygame.Surface.get_size(backB))
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				if rect0.collidepoint(pygame.mouse.get_pos()):
					done = True
				if rect1.collidepoint(pygame.mouse.get_pos()):
					place = oldPlace
			if event.type == pygame.KEYDOWN:
				if event.unicode.isalpha():
					name += event.unicode
				if event.key == K_BACKSPACE:
					name = name[:-1]
				if event.key == K_RETURN and not name == "":
					try:
						opened_file = open("gui"+name+".txt","r")
						txtPuzzle = list(str(opened_file.read()))
						txtPuzzle = convertor.ToList(txtPuzzle)
						sPuzzle = [[0]*9 for i in range(9)]
						for row in range(0, 9):
							for col in range(0, 9):
								sPuzzle[col][row] = txtPuzzle[row][col]
								if not txtPuzzle[row][col] == 0:
									blackText.append([col,row])
						opened_file.close()
						place = oldPlace
					except:
						error = True
				if event.type == pygame.QUIT:
					done = True
		#def renderText(myText, myFont, mySize, myColour, pos, centre, dis=(0,0)):
		if not error:
			renderText("TYPE THE FILE WHICH YOU WANT TO OPEN", "aharoni", 50, BLUE, False, True, (0, -200))
			block = font.render(name, True, (0, 0, 0))
			rect = block.get_rect()
			rect.center = screen.get_rect().center
			screen.blit(block, rect)
		else:
			renderText("ERROR", "aharoni", 200, RED, False, True)

	elif place == "solve":
		screen.blit(bg3,(0,0))
		rect1 = pygame.Rect((150,87.5), pygame.Surface.get_size(solveCellB))
		rect2 = pygame.Rect((150,237.5), pygame.Surface.get_size(solvePuzzleB))
		rect3 = pygame.Rect((150,387.5), pygame.Surface.get_size(clearAllB))
		rect6 = pygame.Rect((150,537.5), pygame.Surface.get_size(showPencilsB))
		rect7 = pygame.Rect((150,687.5), pygame.Surface.get_size(loadOrSaveB))
		rect5 = pygame.Rect((150,837.5), pygame.Surface.get_size(menuB))

		rect4 = pygame.Rect((1495,855), pygame.Surface.get_size(closeB))

		centreBlit(sudoku)
		screen.blit(select,(530+(select.get_width()-8)*selectPos[0], 81+(select.get_height()-8)*selectPos[1]))
		pygame.draw.rect(screen, LIGHT_BLUE, [50, 75, 425, 900])
		screen.blit(solveCellB, (150,87.5))
		screen.blit(solvePuzzleB, (150,237.5))
		screen.blit(clearAllB, (150,387.5))
		screen.blit(showPencilsB, (150,537.5))
		screen.blit(loadOrSaveB, (150,687.5))
		screen.blit(menuB, (150,837.5))

		pygame.draw.rect(screen, LIGHT_BLUE, [1475, 75, 400, 900])
		if solveMode == "pause" or solveMode == "editing":
			screen.blit(startB, (1560,87.5))
		else:
			screen.blit(pauseB, (1560,87.5))
		rect8 = pygame.Rect((1560,87.5), pygame.Surface.get_size(startB))

		#keysNum = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]
		#keysNum = [49, 50, 51, 52, 53, 54, 55, 56, 57]
		#keysNum = range(49, 58)
		key = pygame.key.get_pressed()
		for keyNum in range(48, 58):
			if key[keyNum] and pygame.key.get_mods() & pygame.KMOD_SHIFT and not keyNum == 48 and not solveMode == "pause":
				if not pencil == []:
					if not str(keyNum-48) in pencil[selectPos[0]][selectPos[1]]:
						if pencil[selectPos[0]][selectPos[1]] == "":
							pencil[selectPos[0]][selectPos[1]] = str(keyNum-48)
						else:
							loop = 0
							for item in pencil[selectPos[0]][selectPos[1]]:
								if int(item) > int(keyNum-48):
									#pencil[selectPos[0]][selectPos[1]].insert(loop-1, str(keyNum-48))
									string1 = pencil[selectPos[0]][selectPos[1]][:loop]
									string2 = pencil[selectPos[0]][selectPos[1]][loop:]
									string1 += str(keyNum-48)
									pencil[selectPos[0]][selectPos[1]] = string1+string2
									break
								elif int(pencil[selectPos[0]][selectPos[1]][-1]) < keyNum-48:
									pencil[selectPos[0]][selectPos[1]] += str(keyNum-48)
									break
								loop += 1
				else:
					pencil = [[""]*9 for i in range(9)]
					pencil[selectPos[0]][selectPos[1]] = str(keyNum-48)

			elif key[keyNum] and pygame.key.get_mods() & pygame.KMOD_CTRL and not keyNum == 48 and not solveMode == "pause":
				try:
					if str(keyNum-48) in pencil[selectPos[0]][selectPos[1]]:
						pencil[selectPos[0]][selectPos[1]] = list(pencil[selectPos[0]][selectPos[1]])
						pencil[selectPos[0]][selectPos[1]].remove(str(keyNum-48))
						b = ""
						for x in pencil[selectPos[0]][selectPos[1]]: b += x
						pencil[selectPos[0]][selectPos[1]] = b
				except:
					pass

			elif key[keyNum] and not solveMode == "pause":
				print(puzzle)
				if not [selectPos[0],selectPos[1]] in blackText or solveMode == "editing":
					sPuzzle[selectPos[0]][selectPos[1]] = keyNum-48
				if not keyNum == 48:
					selectS.play()
					if solveMode == "editing" and [selectPos[0], selectPos[1]] not in blackText:
						blackText.append([selectPos[0], selectPos[1]])
					#elif solveMode == "play" and showErrors == True and not clear(keyNum-48, selectPos[0], selectPos[1], sPuzzle) and not [selectPos[0], selectPos[1]] in redText:
					elif solveMode == "play" and showErrors == True and not sPuzzle[selectPos[0]][selectPos[1]] == puzzle[selectPos[0]][selectPos[1]] and not [selectPos[0], selectPos[1]] in redText:
						redText.append([selectPos[0], selectPos[1]])
						print("")
						for row in sPuzzle: print(row)
				else:
					if [selectPos[0], selectPos[1]] in redText:
						redText.remove([selectPos[0], selectPos[1]])
					elif [selectPos[0], selectPos[1]] in blackText:
						blackText.remove([selectPos[0], selectPos[1]])
				if not solveMode == "play":
					puzzle = []
				if not pencil == []:
					rawPencil = []
					sPuzzle, rawPencil = pn.refresh(sPuzzle)
					#pencil = [[] for i in range(9)]
					pencil = []
					for row in range(0, 9):
						sub = []
						for col in range(0, 9):
							string = ""
							for item in rawPencil[row][col]:
								string += str(item)
							sub.append(string)
						pencil.append(sub)

		for row in range(-4, 5):
			for col in range(-4, 5):
				if not sPuzzle[row+4][col+4] == 0:
					if [row+4, col+4] in redText:
						renderText(str(sPuzzle[row+4][col+4]), "aharoni", 80, RED, False, True, ((row)*99, (col)*99))
					elif [row+4, col+4] in blackText:
						renderText(str(sPuzzle[row+4][col+4]), "aharoni", 80, BLACK, False, True, ((row)*99, (col)*99))
					else:
						renderText(str(sPuzzle[row+4][col+4]), "aharoni", 80, BLUE, False, True, ((row)*99, (col)*99))

		if opened == True:
			pass
	#		screen.blit(closeB, (1495, 855))
	#		width2 = renderText("SOLVED:", "aharoni", 50, BLUE, (1485, 95), False)
	#		if solved == False:
	#			renderText("False", "aharoni", 50, RED, (1475+width2+10, 95), False)
	#		else:
	#			renderText("True", "aharoni", 50, GREEN, (1475+width2+10, 95), False)
	#		renderText("DIFFICULTY:", "aharoni", 50, BLUE, (1485, 170), False)
#
#			renderText("For a human:", "aharoni", 50, BLACK, (1485, 245), False)
#			d1Ls1 = [ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, RED]
#			d1Ls2 = ["very easy", "easy", "medium", "hard", "very hard", "super hard", "extreme", "insane"]
#			renderText(d1, "aharoni", 50, d1Ls1[d1Ls2.index(d1)], (1485, 320), False)
#
#			renderText("For a computer:", "aharoni", 50, BLACK, (1485, 395), False)
#			d2Ls1 = [ZERO, ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN]
#			d2Ls2 = ["super easy", "very easy", "easy", "medium", "hard", "very hard", "super hard", "extreme"]
#			renderText(d2, "aharoni", 50, d2Ls1[d2Ls2.index(d2)], (1485, 470), False)
#
#			renderText("TIME:", "aharoni", 50, BLUE, (1485, 545), False)
#			renderText(str(round(timeTaken, 4)) + " SECONDS", "aharoni", 50, GREEN, (1485, 620), False)
#
#			renderText("STEPS:", "aharoni", 50, BLUE, (1485, 695), False)
#			renderText(str(steps) + " STEPS", "aharoni", 50, YELLOW, (1485, 770), False)

		#screen.blit(select,(530+(select.get_width()-8)*0, 81+(select.get_height()-8)*0))
		#renderText("123456789", "aharoni", 25, GREY, (535+(select.get_width()-8)*0, 81+(select.get_height()-8)*0), False)
		#renderText("123456789", "aharoni", 25, GREY, (535+(select.get_width()-8)*1, 81+(select.get_height()-8)*0), False)
		if not pencil == []:
			for row in range(0, 9):
				for col in range(0, 9):
					if not pencil[row][col] == "":
						renderText(pencil[row][col], "aharoni", 25, GREY, (537.5+(select.get_width()-8)*row, 91+(select.get_height()-8)*col), False)

		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				#exit button
				if rect0.collidepoint(pygame.mouse.get_pos()):
					done = True
				#solve cell button
				if rect1.collidepoint(pygame.mouse.get_pos()):
					screen.blit(loading, (200,200))
					pygame.display.update()
					if puzzle == []:
						puzzle = copy.deepcopy(sPuzzle)
						puzzle, oldPuzzle, solved, timeTaken, d1, d2, steps = solver.execute(puzzle)
						sPuzzle[selectPos[0]][selectPos[1]] = puzzle[selectPos[0]][selectPos[1]]
					else:
						sPuzzle[selectPos[0]][selectPos[1]] = puzzle[selectPos[0]][selectPos[1]]
				#solve puzzle button
				if rect2.collidepoint(pygame.mouse.get_pos()):
					screen.blit(loading, (200,200))
					pygame.display.update()
					if puzzle == []:
						sPuzzle, oldPuzzle, solved, timeTaken, d1, d2, steps = solver.execute(sPuzzle)
					else:
						sPuzzle = copy.deepcopy(puzzle)
					sPuzzle, rawPencil = pn.refresh(sPuzzle)
					pencil = []
					for row in range(0, 9):
						sub = []
						for col in range(0, 9):
							string = ""
							for item in rawPencil[row][col]:
								string += str(item)
							sub.append(string)
						pencil.append(sub)
					#showPencilsB = pygame.image.load("hidePencilsB.png")
				#clear all button
				if rect3.collidepoint(pygame.mouse.get_pos()):
					solveMode = "editing"
					puzzle = []
					pencil = []
					sPuzzle = [[0]*9 for i in range(9)]
					blackText = []
					redText = []
				#menu button
				if rect5.collidepoint(pygame.mouse.get_pos()):
					puzzle = []
					pencil = []
					sPuzzle = [[0]*9 for i in range(9)]
					blackText = []
					redText = []
					opened = False
					place = "menu1"
				#back(close) button
				if opened == True and rect4.collidepoint(pygame.mouse.get_pos()):
					opened = False
				#showPencils button
				if rect6.collidepoint(pygame.mouse.get_pos()):
					rawPencil = []
					sPuzzle, rawPencil = pn.refresh(sPuzzle)
					#pencil = [[] for i in range(9)]
					if pencil == []:
						pencil = []
						for row in range(0, 9):
							sub = []
							for col in range(0, 9):
								string = ""
								for item in rawPencil[row][col]:
									string += str(item)
								sub.append(string)
							pencil.append(sub)
						showPencilsB = pygame.image.load("hidePencilsB.png")
					else:
						pencil = []
						showPencilsB = pygame.image.load("showPencilsB.png")
				#load or save button
				if rect7.collidepoint(pygame.mouse.get_pos()):
					oldPlace = "solve"
					place = "loadOrSave1"
				#start button
				if rect8.collidepoint(pygame.mouse.get_pos()):
					if solveMode == "pause" or solveMode == "editing": #when you are in pause
						pauseStart = time.time()
						solveMode = "play"
						if puzzle == []:
							screen.blit(loading2, (200,200))
							pygame.display.update()
							puzzle, sPuzzle, solved, timeTaken, d1, d2, steps = solver.execute(sPuzzle)
					else: #when you are in play
						#start = start-(time.time()-pauseStart)
						extra += (time.time()-pauseStart)
						solveMode = "pause"
					
			if event.type == pygame.QUIT:
				done = True
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_DOWN and not selectPos[1] == 8:
					selectPos[1] += 1
				if event.key == pygame.K_UP and not selectPos[1] == 0:
					selectPos[1] -= 1
				if event.key == pygame.K_RIGHT and not selectPos[0] == 8:
					selectPos[0] += 1
				if event.key == pygame.K_LEFT and not selectPos[0] == 0:
					selectPos[0] -= 1

		if start == 0 and solveMode == "play":
			start = time.time()
		gameTime = (time.time()-start)-extra
		if solveMode == "play":
			renderText("Time: "+str(round(gameTime)), "aharoni", 100, BLUE, (1485, 245), False)
	screen.blit(exitB,((1900-exitB.get_rect().width)+20,0))
	clock.tick(fps)
	pygame.display.update()

"""remember to make puzzle = [], sPuzzle = [], blackText = [], opened = False after changing place"""
