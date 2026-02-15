import pygame as pg
import time
import random

pg.init()

# --- Global stuff --- #
gameRunning = True
currentScreen = "start"
i = 1
cossackX, cossackY = 1000, 400

# Timer(s)
ONE_SECOND_EVENT = pg.USEREVENT + 1
pg.time.set_timer(ONE_SECOND_EVENT, 200)

# --- Colors, fonts and images, etc. --- #
info = pg.display.Info()
WIDTH = info.current_w
HEIGHT = info.current_h
print(WIDTH, "x", HEIGHT, "Pixel")

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Cossacks 4")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

startMenuFont = pg.font.Font("assets/fonts/UncialAntiqua-Regular.ttf", 120)
buttonFont = pg.font.Font("assets/fonts/UncialAntiqua-Regular.ttf", 35)

background = pg.image.load("assets/img/background.png").convert_alpha()

# Hoomans
cossack = pg.image.load("assets/img/cossack.png").convert_alpha()
cossack = pg.transform.scale(cossack, (64, 64))

# --- General stuff --- #
def refresh():
    pg.display.flip()

def Text(text, font, text_col, x, y, center=False):
    img = font.render(text, True, text_col)
    rect = img.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(img, rect)

def Button(X, Y, WIDTH, HEIGHT, colorR, colorG, colorB, text, font, textCOL, Radius):
    borderRect = pg.Rect(0, 0, WIDTH + 20, HEIGHT + 20)
    middleRect = pg.Rect(0, 0, WIDTH, HEIGHT)

    borderRect.center = (X, Y)
    middleRect.center = (X, Y)

    pg.draw.rect(screen, (colorR - 30, colorG - 30, colorB - 30), borderRect, 0, Radius)
    pg.draw.rect(screen, (colorR, colorG, colorB), middleRect, 0, Radius)

    Text(text, font, textCOL, X, Y, True)

    return borderRect, middleRect

def generateNewDirection():
    minDirectionX  = random.randrange(-15, -6)
    minDirectionY = random.randrange(-2, -1)
    maxDirectionX  = random.randrange(6, 10)
    maxDirectionY = random.randrange(1, 2)
    return minDirectionX, minDirectionY, maxDirectionX, maxDirectionY


# --- Drawing Functions --- #
def drawStart(x, y):
    screen.blit(background, (0,0))
    Text("COSSACKS 4", startMenuFont, BLACK, WIDTH / 2, 250, True)
    start, startBorder = Button(WIDTH / 2, HEIGHT / 2 + 20, 250, 90, 150, 150, 150, "START", buttonFont, BLACK, 10)
    settings, settingsBorder = Button(WIDTH / 2, HEIGHT / 2 + 200, 250, 90, 150, 150, 150, "SETTINGS", buttonFont, BLACK, 10)

    screen.blit(cossack, (x, y))

    return start, startBorder, settings, settingsBorder

def drawGame():
    screen.fill(WHITE)
    Text("Dis is game", startMenuFont, BLACK, WIDTH / 2, HEIGHT / 2, True)

def drawSettings():
    screen.fill(WHITE)
    Text("Dis is settings", startMenuFont, BLACK, WIDTH / 2, HEIGHT / 2, True)

# ----------- Game ----------- #
start, startBorder, settings, settingsBorder = drawStart(cossackX, cossackY)
minDirectionX, minDirectionY, maxDirectionX, maxDirectionY = generateNewDirection()

while gameRunning:
    # --- Event Handling ---
    for event in pg.event.get():
        if event.type == pg.QUIT:
            gameRunning = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            mousePOS = pg.mouse.get_pos()
            if currentScreen == "start":
                if start.collidepoint(mousePOS) or startBorder.collidepoint(mousePOS):
                    currentScreen = "game"
                    drawGame()
                elif settings.collidepoint(mousePOS) or settingsBorder.collidepoint(mousePOS):
                    currentScreen = "settings"
                    drawSettings()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE and currentScreen == "settings":
                currentScreen = "start"

        # --- Cossack Logic --- #
        elif currentScreen == "start" and event.type == ONE_SECOND_EVENT:
            cossackX += random.randrange(minDirectionX, maxDirectionX)
            cossackY += random.randrange(minDirectionY, maxDirectionY)

            if cossackX <= 0 or cossackX >= 1400:
                cossackX = random.randrange(0, 1400)
                cossackY= random.randrange(0, 800)

                minDirectionX, minDirectionY, maxDirectionX, maxDirectionY = generateNewDirection()

            if cossackY <= 0 or cossackY >= 1400:
                cossackX = random.randrange(0, 1400)
                cossackY= random.randrange(0, 800)

                minDirectionX, minDirectionY, maxDirectionX, maxDirectionY = generateNewDirection()

    # --- Draw --- #
    screen.fill((0,0,0))
    if currentScreen == "start":
        drawStart(cossackX, cossackY)
    elif currentScreen == "settings":
        drawSettings()
    elif currentScreen == "game":
        drawGame()

    refresh()
    pg.time.Clock().tick(24)  # ~24 FPS