import Tkinter as Tk
import pieces as p
import sys
from thread import start_new_thread
from time import sleep
from chartoint import dic

debug = 0

#draw chess board
def drawBoard(Canvas):
	for x in range(0,8):
		for y in range (0,8):
			fromx = x*110
			fromy = y*110
			tox = fromx + 110
			toy = fromy + 110 
			colorcheck = x+y
			if colorcheck % 2 == 0:
				Canvas.create_rectangle(fromx, fromy, tox, toy, fill = "#E6A44E")
			else:
				Canvas.create_rectangle(fromx, fromy, tox, toy, fill = "#A3610B")
				
#draw the pieces on the board
def drawPieces(canvas, board):
	for x in range(0,8):
		for y in range(0,8):
			if board[x][y] != 0:
				board[x][y].drawSelf(canvas)
				
#update board
def updateBoard(canvas, board):
	if debug:
		print "UPDATE BOARD"
	canvas.delete('all')
	drawBoard(canvas)
	drawPieces(canvas, board)
	
#add piece to board
def addPiece(piece, board):
	if debug:
		print "ADDING PIECE TO BOARD"
	board[piece.position[0]][piece.position[1]] = piece

#windows settings
root = Tk.Tk()
root.configure(background = "white")
MainCanvas = Tk.Canvas(root, width = 880, height = 880, bg = "white")
MainCanvas.grid(row = 1, column = 1)
numbersLeft = Tk.Label(root, bg = "white", text = "\n".join("12345678"), font = ("Helvetica", 73))
numbersLeft.grid(row = 1, column = 0)
lettersTop = Tk.Label(root, bg = "white", text = "  "+("  ".join("ABCDEFGH"))+"  ", font = ("Helvetica", 65))
lettersTop.grid(row = 0, column = 1)
start_new_thread(root.mainloop,())

#initialize board
board = [[0 for x in range(8)] for x in range(8)]

#testing
towerwhite = p.Tower(2,2,"white")
board[2][2] = towerwhite
towerblack = p.Tower(2,5,"black")
addPiece(towerblack, board)
kingwhite = p.King(5,2,"white")
addPiece(kingwhite, board)

updateBoard(MainCanvas, board)
# fetch input
c = ""
while c != "quit" and c!= "exit":
	c=raw_input(">> ")
	cmd = c.split()
	try:
		if cmd[0] == "move":
			fromx = dic[cmd[1][0]]
			fromy = int(cmd[1][1])-1
			tox = dic[cmd[2][0]]
			toy = int(cmd[2][1])-1
			if debug:
				print "Bewegung von {}.{} nach {}.{}".format(fromx, fromy, tox, toy)
			if board[fromx][fromy] != 0:
				if board[fromx][fromy].checkValidTurn(tox,toy,board):
					board[fromx][fromy].updatePosition(tox,toy)
					board[tox][toy] = board[fromx][fromy]
					board[fromx][fromy] = 0
	except IndexError as i:
		print "INDEX ERROR"
	updateBoard(MainCanvas, board)