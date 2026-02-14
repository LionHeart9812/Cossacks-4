import pygame as pg

pg.init()

# --- Colors, fonts and images, etc. --- #
info = pg.display.Info()
WIDTH = info.current_w
HEIGHT = info.current_h

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

startMenuFont = pg.font.Font("assets/fonts/UncialAntiqua-Regular.ttf", 120)
buttonFont = pg.font.Font("assets/fonts/UncialAntiqua-Regular.ttf", 35)

# --- General stuff --- #
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Cossacks 4")

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
    refresh()

    return borderRect, middleRect

# Global variables
gameRunning = True


# --- Drawing Variabels --- #
def drawStart():
    screen.fill(WHITE)
    Text("COSSACKS 4", startMenuFont, BLACK, WIDTH / 2, 250, True)
    start, startBorder = Button(WIDTH / 2, HEIGHT / 2 + 20, 250, 90, 150, 150, 150, "START", buttonFont, BLACK, 10)
    settings, settingsBorder = Button(WIDTH / 2, HEIGHT / 2 + 200, 250, 90, 150, 150, 150, "SETTINGS", buttonFont, BLACK, 10)
    refresh()

    return start, startBorder, settings, settingsBorder

def drawGame():
    screen.fill(WHITE)
    Text("Dis is game", startMenuFont, BLACK, WIDTH / 2, HEIGHT / 2, True)
    refresh()

def drawSettings():
    screen.fill(WHITE)
    Text("Dis is settings", startMenuFont, BLACK, WIDTH / 2, HEIGHT / 2, True)
    refresh()

# ----------- Game ----------- #
start, startBorder, settings, settingsBorder = drawStart()

while gameRunning == True:
    for event in pg.event.get():
        mousePOS = pg.mouse.get_pos()

        if event.type == pg.QUIT:
            gameRunning = False

        if event.type == pg.MOUSEBUTTONDOWN and (start.collidepoint(mousePOS) or startBorder.collidepoint(mousePOS)):
            drawGame()

        if event.type == pg.MOUSEBUTTONDOWN and (settings.collidepoint(mousePOS) or settingsBorder.collidepoint(mousePOS)):
            drawSettings()

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                drawStart()