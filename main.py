import pygame, my, input, ui, copy, math
from pygame.locals import *

pygame.init()
pygame.display.set_caption('Lotto')

my.screen.fill(my.BLUE)
pygame.display.update()

GAP = 5

IMGNAMES = ['cellBg', 'ball', 'ballHighlight', 'bgImg']
IMG = {}
for name in IMGNAMES:
	IMG[name] = pygame.image.load('assets/%s.png' %(name)).convert_alpha()

my.BALLIMG = []
for num in range(1, my.NUMBALLS + 1):
	textSurf, textRect = ui.genText(str(num), (0,0), my.BLACK, ui.FRANCOIS)
	textRect.center = my.HALFCELLSIZE
	ball = IMG['ball'].copy()
	ball.blit(textSurf, textRect)
	my.BALLIMG.append(ball)


class Control:
	def __init__(self):
		self.main()


	def main(self):
		my.input = input.Input()
		self.runGame()
	
	
	def runGame(self):
		my.gameRunning = True
		self.genBoard()
		self.hud = ui.Hud()
		while my.gameRunning:
			my.screen.blit(IMG['bgImg'], (0, 0))
			my.input.get()
			self.surf = self.boardSurf.copy()
			self.handleInput()
			my.screen.blit(self.surf, self.boardRect)

			if K_SPACE in my.input.unpressedKeys:
				self.goFaster()

			self.hud.update()
			if self.checkForWin():
				self.hud.winText.display()

			pygame.display.update()
			my.FPSCLOCK.tick(my.FPS)
			pygame.display.set_caption('Lotto' + ' ' * 10 + 'FPS: ' + str(int(my.FPSCLOCK.get_fps())))
	
	
	def genBoard(self):
		"""Generate a new self.board with every cell=True"""
		self.board = []
		for x in range(my.XCELLS):
			row = []
			for y in range(my.YCELLS):
				row.append(True)
			self.board.append(row)
		self.genBaseSurf()
		self.updateSurf()


	def genBaseSurf(self):
		"""Generate a background surf upon which balls etc will be blitted"""
		self.baseBoardSurf = pygame.Surface(my.BOARDSIZE)
		for x in range(my.XCELLS):
			for y in range(my.YCELLS):
				self.baseBoardSurf.blit(IMG['cellBg'], (x * my.CELLWIDTH, y * my.CELLHEIGHT))
		self.boardSurf = self.baseBoardSurf.copy()
		self.boardRect = self.boardSurf.get_rect()
		self.boardRect.center = (int(my.WINDOWWIDTH / 2), int(my.WINDOWHEIGHT / 2))
		my.boardRect = self.boardRect.copy()


	def updateSurf(self):
		"""Update board surf"""
		self.boardSurf = self.baseBoardSurf.copy()
		for x in range(my.XCELLS):
			for y in range(my.YCELLS):
				if self.board[x][y]:
					self.boardSurf.blit(my.BALLIMG[x + y * 10], (x * my.CELLWIDTH, y * my.CELLHEIGHT))
		self.surf = self.boardSurf.copy()


	def updateHighlight(self):
		if my.input.hoveredCell:
			x, y = my.input.hoveredCell
			self.surf.blit(IMG['ballHighlight'], (x * my.CELLWIDTH, y * my.CELLHEIGHT))
			if my.input.mousePressed == 1:
				self.surf.blit(IMG['ballHighlight'], (x * my.CELLWIDTH, y * my.CELLHEIGHT))
				self.surf.blit(IMG['ballHighlight'], (x * my.CELLWIDTH, y * my.CELLHEIGHT))


	def handleInput(self):
		self.updateHighlight()
		if my.input.hoveredCell and my.input.mouseUnpressed == 1:
			if my.input.hoveredCellNum in self.hud.ballTray.balls:
				x, y = my.input.hoveredCell
				if self.board[x][y]:
					self.board[x][y] = False
					self.updateSurf()


	def goFaster(self):
		my.BALLDROPTIME -= 0.2
		self.hud.fasterText.display()


	def checkForWin(self):
		"""Return True if all tiles are False"""
		my.ballsOnBoard = []
		for x in range(my.XCELLS):
			for y in range(my.YCELLS):
				if self.board[x][y] == True:
					my.ballsOnBoard.append(y*10 + x)
		if my.ballsOnBoard:
			return False
		return True



if __name__ == '__main__':
	control = Control()
