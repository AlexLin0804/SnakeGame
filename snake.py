# snake-demo.py

# Note: there is a snake tutorial from previous semesters here:
#	http://www.kosbie.net/cmu/fall-11/15-112/handouts/snake/snake.html
# But this is different in two key ways:
#	1) This uses this semester's framework (run function, and in Python3)
#	2) This uses a list of tuples to represent the snake
# You should understand both solutions, and be able to adapt that
# tutorial to use this semester's framework.

from tkinter import *
import random
import time

def init(data):
	data.rows = 10
	data.cols = 10
	data.margin = 5 # margin around grid
	data.snake = [(data.rows/2, data.cols/2)]
	data.direction = (0, +1) # (drow, dcol)
	placeFood(data)
	data.timerDelay = 250
	data.gameOver = False
	data.paused = True

	#hw4
	data.mode = "start_mode"
	data.score = 0
	data.lives = 3 

	#hw5
	data.time = 15
	data.wall = [(1,1),(1,2),(1,3)]
	placeTrap(data)






# getCellBounds from grid-demo.py
def getCellBounds(row, col, data):
	# aka "modelToView"
	# returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
	gridWidth  = data.width - 2*data.margin
	gridHeight = data.height - 2*data.margin
	x0 = data.margin + gridWidth * col / data.cols
	x1 = data.margin + gridWidth * (col+1) / data.cols
	y0 = data.margin + gridHeight * row / data.rows
	y1 = data.margin + gridHeight * (row+1) / data.rows
	return (x0, y0, x1, y1)


def mousePressed(event, data):
	if(data.mode == "start_mode"): 
		start_mode_MousePressed(event, data)
	elif(data.mode == "game_mode"): 
		game_mode_MousePressed(event, data)
	elif(data.mode == "end_mode"): 
		end_mode_MousePressed(event, data)
	elif(data.mode == "help_mode"): 
		help_mode_MousePressed(event, data)


def keyPressed(event, data):
	if(data.mode == "start_mode"): 
		start_mode_KeyPressed(event, data)
	elif(data.mode == "game_mode"): 
		game_mode_KeyPressed(event, data)
	elif(data.mode == "end_mode"): 
		end_mode_KeyPressed(event, data)
	elif(data.mode == "help_mode"): 
		help_mode_KeyPressed(event, data)


def timerFired(data):
	if(data.mode == "start_mode"): 
		start_mode_TimerFired(data)
	elif(data.mode == "game_mode"): 
		game_mode_TimerFired(data)
	elif(data.mode == "end_mode"): 
		end_mode_TimerFired(data)
	elif(data.mode == "help_mode"): 
		help_mode_TimerFired(data)
	

def redrawAll(canvas, data):
	if(data.mode == "start_mode"): 
		start_mode_RedrawAll(canvas, data)
	elif(data.mode == "game_mode"): 
		game_mode_RedrawAll(canvas, data)
	elif(data.mode == "end_mode"): 
		end_mode_RedrawAll(canvas, data)
	elif(data.mode == "help_mode"): 
		help_mode_RedrawAll(canvas, data)


####################################
# helper functions 
####################################


def takeStep(data):


	(drow, dcol) = data.direction
	(headRow, headCol) = data.snake[0]
	(newRow, newCol) = (headRow+drow, headCol+dcol)
	if ((newRow < 0) or (newRow >= data.rows) or
		(newCol < 0) or (newCol >= data.cols) or
		((newRow, newCol) in data.snake) or (data.time < 0)):

		data.gameOver = True
		data.lives -= 1
		data.snake = [(data.rows/2, data.cols/2)]
		data.time = 15
		data.mode = "end_mode"

	elif((newRow, newCol) in data.wall):
		if(drow == 0):
			drow = 1
			dcol = 0  
		elif(dcol == 0):
			dcol = 1
			drow = 0
		data.direction = (drow, dcol)

	else:
		data.snake.insert(0, (newRow, newCol))
		if (data.foodPosition == (newRow, newCol)):
			placeFood(data)
			placeTrap(data)
			data.score += 1
			data.time = 15
		else:
			# didn't eat, so remove old tail (slither forward)
			data.snake.pop()


def placeTrap(data): 
	data.trap_center = None
	row_trap = random.randint(1, data.rows-2)
	col_trap = random.randint(1, data.cols-2)
	data.trap_center = (row_trap, col_trap)


	data.direction____ = random.randint(0,1)
	if(data.direction____ == 0):
		data.wall = [(row_trap, col_trap-1),(row_trap, col_trap),(row_trap, col_trap+1)]
	elif(data.direction____ == 1):
		data.wall = [(row_trap-1, col_trap),(row_trap, col_trap),(row_trap+1, col_trap)]
	return 

def placeFood(data):
	data.foodPosition = None
	row0 = random.randint(0, data.rows-1)
	col0 = random.randint(0, data.cols-1)

	for drow in range(data.rows):
		for dcol in range(data.cols):
			row = (row0 + drow) % data.rows
			col = (col0 + dcol) % data.cols
			if (row,col) not in data.snake:
				data.foodPosition = (row, col)
				return

def drawTrap(canvas, data):
	(row, col) = data.trap_center
	if(data.trap_center != None):
		(x0,y0,x1,y1) = getCellBounds(row, col, data)
		if (data.direction____ == 0):
			canvas.create_rectangle(x0-3*data.cols, y0, x1+3*data.cols, y1, fill="yellow")
			
		elif (data.direction____ == 1):
			canvas.create_rectangle(x0, y0-3*data.cols, x1, y1+3*data.cols, fill="yellow")
		
			
def drawFood(canvas, data):
	if (data.foodPosition != None):
		(row, col) = data.foodPosition
		(x0, y0, x1, y1) = getCellBounds(row, col, data)
		canvas.create_oval(x0, y0, x1, y1, fill="green")

def drawBoard(canvas, data):
	for row in range(data.rows):
		for col in range(data.cols):
			(x0, y0, x1, y1) = getCellBounds(row, col, data)
			canvas.create_rectangle(x0, y0, x1, y1, fill="white")

def drawSnake(canvas, data):
	for (row, col) in data.snake:
		(x0, y0, x1, y1) = getCellBounds(row, col, data)
		canvas.create_oval(x0, y0, x1, y1, fill="blue")


def drawGameOver(canvas, data):
	if (data.gameOver):
		canvas.create_text(data.width/2, data.height/2, text="Game over!",
						   font="Arial 26 bold")

####################################
# modes 
####################################

def start_mode_MousePressed(event,data):
	data.mode = "game_mode"

def start_mode_KeyPressed(event,data):

	if(event.keysym == 'Return'): 
		data.mode = "game_mode"
		data.score = 0
	elif(event.keysym == 'h'): 
		data.mode = "help_mode"

def start_mode_TimerFired(data):
	pass

def start_mode_RedrawAll(canvas, data):
	canvas.create_text(data.width/2, data.height/2 - 100, text = 'Welcome Gru', font = 'Arial 30')
	canvas.create_text(data.width/2, data.height/2 +30, text = 'Press Enter to play')
	canvas.create_text(data.width/2, data.height/2 +60, text = 'Press h for help')

##########################################

def game_mode_MousePressed(event,data):
	data.paused = False

def game_mode_KeyPressed(event,data):
	if (event.keysym == "p"): 
		data.paused = True
		return
	elif (event.keysym == "r"): 
		init(data)
		return
	if (data.paused or data.gameOver): 
		return
	if (event.keysym == "Up"):	  
		data.direction = (-1, 0)
	elif (event.keysym == "Down"):  
		data.direction = (+1, 0)
	elif (event.keysym == "Left"):  
		data.direction = (0, -1)
	elif (event.keysym == "Right"): 
		data.direction = (0, +1)
	# for debugging, take one step on any keypress
	takeStep(data)

def game_mode_TimerFired(data):
	if (data.paused or data.gameOver): 
		return
	data.time -= 0.3
	takeStep(data)
	
def game_mode_RedrawAll(canvas, data):

	drawBoard(canvas, data)
	drawSnake(canvas, data)
	drawFood(canvas, data)
	drawTrap(canvas, data)
	drawGameOver(canvas, data)
	canvas.create_text(50,315, text = int(data.time), fill = 'black', font = 'Arial 20')


########################################

def end_mode_MousePressed(event,data):
	pass   
def end_mode_KeyPressed(event,data):
	if(event.keysym == 'q'): 
		data.mode = "start_mode"
	elif(event.keysym == 'Return' and data.lives != 0):
		data.gameOver = False 
		data.mode = "game_mode"


def end_mode_TimerFired(data):
	pass

def end_mode_RedrawAll(canvas, data):
	if(data.lives == 0):
		canvas.create_text(data.width/2, data.height/2 - 100, text = 'You Lose, Goodbye Gru', font = 'Arial 20')
	elif(data.lives > 0):
		canvas.create_text(data.width/2, data.height/2 - 100, text = 'You died', font = 'Arial 30')
		canvas.create_text(data.width/2, data.height/2 + 30, text = 'You score is %d' %(data.score), font = 'Arial 20')
		canvas.create_text(data.width/2, data.height/2 + 50, text = 'You have %d lives left' %(data.lives), font = 'Arial 20')
		canvas.create_text(data.width/2, data.height/2 + 90, text = 'Press Enter to restart')
	

########################################

def help_mode_MousePressed(event,data):
	pass

def help_mode_KeyPressed(event,data):
	if(event.keysym == 'q'): 
		data.mode = "start_mode"

def help_mode_TimerFired(data):
	pass

def help_mode_RedrawAll(canvas, data):
	canvas.create_text(data.width/2, data.height/2 - 100, text= 'This is the help mode',font = 'Arial 30')
	canvas.create_text(data.width/2, data.height/2 + 30, text = 'Press q to quit help mode')




####################################
# use the run function as-is
####################################

def run(width=300, height=300):
	def redrawAllWrapper(canvas, data):
		canvas.delete(ALL)
		redrawAll(canvas, data)
		canvas.update()	

	def mousePressedWrapper(event, canvas, data):
		mousePressed(event, data)
		redrawAllWrapper(canvas, data)

	def keyPressedWrapper(event, canvas, data):
		keyPressed(event, data)
		redrawAllWrapper(canvas, data)

	def timerFiredWrapper(canvas, data):
		timerFired(data)
		redrawAllWrapper(canvas, data)
		# pause, then call timerFired again
		canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
	# Set up data and call init
	class Struct(object): pass
	data = Struct()
	data.width = width
	data.height = height
	data.timerDelay = 100 # milliseconds
	init(data)
	# create the root and the canvas
	root = Tk()
	canvas = Canvas(root, width=data.width, height=data.height + 30)
	canvas.pack()
	# set up events
	root.bind("<Button-1>", lambda event:
							mousePressedWrapper(event, canvas, data))
	root.bind("<Key>", lambda event:
							keyPressedWrapper(event, canvas, data))
	timerFiredWrapper(canvas, data)
	# and launch the app
	root.mainloop()  # blocks until window is closed
	print("bye!")

run(300, 300)