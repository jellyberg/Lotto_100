import pygame, my, math, random, time

pygame.init()

my.selectionBoxGroup = pygame.sprite.GroupSingle()
my.pulseLights = pygame.sprite.Group()

BASICFONT = pygame.font.Font('freesansbold.ttf', 12)
PRETTYFONT = None
BIGFONT   = None
MEGAFONT  = None

MILKDROP = pygame.font.Font('fonts/milkdrop.ttf', 25)
FRANCOIS = pygame.font.Font('fonts/francois.ttf', 15)
GAP = 5
TOOLTIPWORDSPERLINE = 6  # subtract 1!


def genText(text, topLeftPos, colour, font=BASICFONT):
	surf = font.render(text, 1, colour)
	rect = surf.get_rect()
	rect.topleft = topLeftPos
	return (surf, rect)


class Hud:
	"""Keep track of all different UI elements and update them all with my.hud.update()"""
	def __init__(self):
		self.ballTray = BallTray()
		self.fasterText = AlertText('Faster!')
		self.winText = AlertText('Congratulations Mum, you won!')

	def update(self):
		self.ballTray.update()
		self.fasterText.update()
		self.winText.update()



class Button:
	"""A button, can be clickable, can have tooltip. When clicked, self.isClicked=True"""
	def __init__(self, text, style, screenPos, isClickable=0, isTitle=0, screenPosIsTopRight=0, tooltip=None):
		"""style is redundant atm, tooltip should be a string"""
		self.text, self.style, self.screenPos, self.isClickable, self.posIsTopRight = \
		(text, style, screenPos, isClickable, screenPosIsTopRight)
		if isTitle:
			self.textSurf = BIGFONT.render(self.text, 1, my.LIGHTGREY)
		else:
			self.textSurf = BASICFONT.render(self.text, 1, my.WHITE)
		# CREATE BASIC SURF
		self.padding = 10 # might be controlled by 'style' eventually
		self.buttonSurf = pygame.Surface((self.textSurf.get_width() + self.padding,
										  self.textSurf.get_height() + self.padding))
		self.buttonSurf.fill(my.BROWN)
		self.buttonSurf.blit(self.textSurf, (int(self.padding /2), int(self.padding /2)))
		self.currentSurf = self.buttonSurf
		self.rect = pygame.Rect(self.screenPos, self.buttonSurf.get_size())
		# CREATE ADDITIONAL SURFS
		if isClickable:
			# MOUSE HOVER
			self.hoverSurf = pygame.Surface(self.buttonSurf.get_size())
			self.hoverSurf.fill(my.DARKBROWN)
			self.hoverSurf.blit(self.textSurf, (int(self.padding /2), int(self.padding /2)))
			# MOUSE CLICK
			self.clickSurf = pygame.Surface(self.buttonSurf.get_size())
			self.clickSurf.fill(my.BROWNBLACK)
			self.clickSurf.blit(self.textSurf, (int(self.padding /2), int(self.padding /2)))
			self.isClicked = False
		self.hasTooltip = False
		if tooltip:
			self.hasTooltip = True
			self.tooltip = Tooltip(tooltip, (self.rect.right + GAP, self.rect.top))

	def simulate(self, userInput):
		if self.isClickable or self.hasTooltip: self.handleClicks(userInput)
		if self.hasTooltip: self.tooltip.simulate(self.isHovered)
		self.draw()

	def draw(self):
		if self.posIsTopRight:
			self.rect.topright = self.screenPos
		else:
			self.rect.topleft = self.screenPos
		my.screen.blit(self.currentSurf, self.rect)

	def handleClicks(self, userInput=None):
		self.isClicked = False
		self.isHovered = False
		if self.rect.collidepoint(my.input.mousePos):
			if userInput.mousePressed == 1:
				self.currentSurf = self.clickSurf
			else:
				self.currentSurf = self.hoverSurf
				self.isHovered = True
		else:
			self.currentSurf = self.buttonSurf
		if userInput.mouseUnpressed == True and self.rect.collidepoint(my.input.mousePos):
			self.isClicked = True



class Tooltip:
	"""A multiline text box, displayed when isHovered=True"""
	def __init__(self, text, pos, font=BASICFONT):
		self.pos, self.text, self.font = pos, text, font
		self.x, self.y = pos
		self.alpha = 0
		self.newTooltip()
		self.lastText = self.text
		self.lockAlpha = False
		self.fadeRate = 20


	def newTooltip(self):
		# GET TEXT OBJS
		self.textObjs, self.textHeight = self.genTextObjs(self.text)
		self.textWidth = self.getLongestTextLine(self.textObjs)
		# CREATE SURF
		self.surf = pygame.Surface((self.textWidth + GAP * 3, self.textHeight + GAP * 2))
		pygame.draw.rect(self.surf, my.CREAM, (GAP, 0, self.surf.get_width() - GAP, self.surf.get_height()))
		pygame.draw.polygon(self.surf, my.CREAM, [(0, 10), (GAP, 5), (GAP, 15)])
		for i in range(len(self.textObjs)):
			self.surf.blit(self.textObjs[i][0], self.textObjs[i][1])
		self.surf.set_colorkey(my.BLACK)
		self.rect = self.surf.get_rect()
		self.rect.topleft = self.pos
		

	def simulate(self, isHovered, blitToLand=False):
		if self.text != self.lastText:
			self.newTooltip()
		if isHovered:
			if self.alpha < 200: self.alpha += 20
		elif self.alpha > 0 and not self.lockAlpha:
			self.alpha -= self.fadeRate
		if self.alpha > 0:
			self.surf.set_alpha(self.alpha)
			if not blitToLand:
				my.screen.blit(self.surf, self.rect)
			if blitToLand:
				my.surf.blit(self.surf, self.rect)
		self.lastText = self.text


	def genTextObjs(self, text):
		wordList = text.split()
		extraWords = wordList[:]
		numLines = int(math.ceil(len(wordList) / TOOLTIPWORDSPERLINE))
		newText = [] # a list of strings, each line having one string
		textObjs = [] # a list of two item lists, each list having a surf and rect object for a line
		# GENERATE LIST OF STRINGS
		for lineNum in range(0, numLines-1):
			line = ''
			for wordNum in range(0, TOOLTIPWORDSPERLINE):
				currentWord = wordList[lineNum * (TOOLTIPWORDSPERLINE) + wordNum]
				line = line + currentWord + ' '
				extraWords.remove(currentWord)
			newText.append(line)
		lastLine = ' '.join(extraWords)
		newText.append(lastLine)
		# CONVERT STRINGS TO TEXT SURFS AND RECTS
		testText, testRect = genText(newText[0], (0, 0), my.BLACK, self.font)
		textHeight = testText.get_height()
		totalHeight = textHeight * (len(newText)) + GAP * (len(newText))
		for lineNum in range(len(newText)):
			surf, rect = genText(newText[lineNum], (GAP * 2, textHeight * lineNum + GAP * lineNum + GAP),
								 my.DARKGREY, self.font)
			textObjs.append([surf, rect])
		return textObjs, totalHeight


	def getLongestTextLine(self, textObjs):
		longestLineWidth = 0
		for i in range(len(textObjs)):
			if textObjs[i][1].width > longestLineWidth:
				longestLineWidth = textObjs[i][1].width
		return longestLineWidth



class BallTray:
	"""
	Balls are dropped in here, then slowly move along as more balls drop in.
	If a ball on the board is clicked and it is in the BallTray, it is removed from the board
	"""
	def __init__(self):
		self.balls = []
		self.timeOfLastDrop = time.time()
		self.surf = pygame.Surface((my.BALLIMG[0].get_width() * my.MAXBALLSINTRAY, my.BALLIMG[0].get_height()))


	def update(self):
		if time.time() - self.timeOfLastDrop >= my.BALLDROPTIME:
			self.dropBall()
		self.updateSurf()
		my.screen.blit(self.surf, self.rect)


	def updateSurf(self):
		"""Regenerate self.surf and self.rect"""
		self.surf.fill(my.DARKGREY)
		alpha = 255
		for i in range(len(self.balls)):
			img = my.BALLIMG[self.balls[i] - 1]
			self.surf.blit(img, (i * my.BALLIMG[0].get_width(), 0))
		self.rect = self.surf.get_rect()
		self.rect.midtop = (int(my.WINDOWWIDTH / 2), GAP)


	def dropBall(self):
		"""Add a new ball into the ball tray"""
		newBall = random.choice(my.ballsOnBoard)
		self.balls = [newBall] + self.balls
		self.timeOfLastDrop = time.time()
		while len(self.balls) > my.MAXBALLSINTRAY:
			del self.balls[-1]


class AlertText:
	"""Text appears on screen and zooms in"""
	def __init__(self, text):
		self.baseSurf, self.rect = genText(text, (0,0), my.WHITE, FRANCOIS)
		self.baseWidth, self.baseHeight = self.baseSurf.get_size()
		self.show = False


	def update(self):
		if self.show:
			self.scale += 0.3
			width = int(self.baseWidth * self.scale)
			height = int(self.baseHeight * self.scale)
			self.surf = pygame.transform.scale(self.baseSurf, (width, height))
			self.rect = self.surf.get_rect()
			self.rect.center = (int(my.WINDOWWIDTH / 2), int(my.WINDOWHEIGHT / 2))
			self.rect.y -= self.yHeight
			self.yHeight +=1
			my.screen.blit(self.surf, self.rect)
			if self.scale > 30:
				self.show = False




	def display(self):
		"""Display the alert on the screen"""
		self.show = True
		self.alpha = 255
		self.rect.center = (int(my.WINDOWWIDTH / 2), int(my.WINDOWHEIGHT / 2))
		self.surf = self.baseSurf.copy()
		self.scale = 1.0
		self.yHeight = 0
