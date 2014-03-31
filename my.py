import pygame

DEBUGMODE = True

FPS = 60
FPSCLOCK = pygame.time.Clock()
WINDOWWIDTH = 1080
WINDOWHEIGHT = 720
loadingScreen = pygame.image.load('assets/fullscreenLoadingScreen.png')
if DEBUGMODE:
	screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
if not DEBUGMODE:
	screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), FULLSCREEN)

CELLWIDTH, CELLHEIGHT = 40, 40
CELLSIZE = (CELLWIDTH, CELLHEIGHT)
HALFCELLSIZE = (int(CELLWIDTH / 2), int(CELLHEIGHT / 2))
XCELLS = 10
YCELLS = 10
BOARDX, BOARDY = XCELLS * CELLWIDTH, YCELLS * CELLHEIGHT
BOARDSIZE = (BOARDX, BOARDY)

NUMBALLS = 100
BALLDROPTIME = 3 # time between ball drops
MAXBALLSINTRAY = 5


# Colours     R    G    B  ALPHA
WHITE     = (255, 255, 255, 255)
BLACK     = (  0,   0,   0, 255)
RED       = (255,   0,   0, 255)
DARKRED   = (220,   0,   0, 255)
BLUE      = (  0,   0, 255, 255)
SKYBLUE   = (135, 206, 250, 255)
YELLOW    = (255, 250,  17, 255)
GREEN     = (  0, 255,   0, 255)
ORANGE    = (255, 165,   0, 255)
DARKGREEN = (  0, 155,   0, 255)
DARKGREY  = ( 60,  60,  60, 255)
LIGHTGREY = (180, 180, 180, 255)
BROWN     = (139,  69,  19, 255)
DARKBROWN = (100,  30,   0, 255)
BROWNBLACK= ( 50,  0,    0, 255)
CREAM     = (255, 255, 204, 255)