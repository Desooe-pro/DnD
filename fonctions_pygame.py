import random, os, sys, pygame_widgets, pygame as pg, config as config, Classes.MenuDnD as Menu
from math import floor

from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from pygame_widgets.progressbar import ProgressBar
from config import sauvegarder_config

os.environ["SDL_VIDEO_CENTERED"] = "1"

dataConfig = config.charger_config()
newConfig = dataConfig
pg.init()
screen = pg.display.set_mode((int(dataConfig["width"]), int(dataConfig["height"])))
clock = pg.time.Clock()
running = True
running2 = True
hugeassfont = pg.font.SysFont("Arial", 150, 1, 0)
hugeassfontplus = pg.font.SysFont("Arial", 160, 1, 0)
bigfont = pg.font.SysFont("Arial", 40)
font = pg.font.SysFont("Arial", 30)
smallfont = pg.font.SysFont("Arial", 20)
vsmallfont = pg.font.SysFont("Arial", 14)
atkfont = pg.font.SysFont("Arial", 17)
width = screen.get_width()
height = screen.get_height()
replay = False
ask = False
perso = 0
selecPerso = False
selecNOM = False
selecPV = False
selecMana = False
selecForce = False
selecDef = False
selecMD = False
name = ""
pv = 0
mana = 0
force = 0
game_over = 0
loop = 0
def_type = ""
mana_uti = ""
temp = 0
afficheMenu = False

volume = dataConfig["volume"]
phrasesClass = config.load_phrases(dataConfig["langue"])

class PosBoutons:
    def __init__(self, screen):
        self.screen = screen
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        self.btnSizes = {'1': {'nbCol': 5, 'nbLigne': 9, 'sep': 30}, '2': {'nbCol': 7, 'nbLigne': 11, 'sep': 20}, '3':{'nbCol': 9, 'nbLigne': 14, 'sep': 10}}
        self.generateData()
        print("Init")
        print(self.btnSizes['1'])
        print(self.btnSizes['2'])
        print(self.btnSizes['3'])

    def generateData(self):
        self.generateDataForPosGen(self.btnSizes['1'])
        self.generateDataForPosGen(self.btnSizes['2'])
        self.generateDataForPosGen(self.btnSizes['3'])

    def generateDataForPosGen(self, btnSize):
        btnSize['btnSizeW'] = int(floor((self.width - 24 - (btnSize['nbCol'] * btnSize['sep'] - btnSize['sep'])) / btnSize['nbCol']) - (
                floor((self.width - 24 - (btnSize['nbCol'] * btnSize['sep'] - btnSize['sep'])) / btnSize['nbCol']) % 2))
        btnSize['btnSizeH'] = int(floor(((self.height - 24 - (btnSize['nbLigne'] * btnSize['sep'] - btnSize['sep'])) / btnSize['nbLigne']) - (
            floor(((self.height - 24 - (btnSize['nbLigne'] * btnSize['sep'] - btnSize['sep'])) / btnSize['nbLigne']) % 2))))
        return self.generatePositions(btnSize)

    def generatePositions(self, btnSize):
        screenW = btnSize['nbCol'] * btnSize['btnSizeW'] + (btnSize['nbCol'] * btnSize['sep'] - btnSize['sep'])
        screenH = btnSize['nbLigne'] * btnSize['btnSizeH'] + (btnSize['nbLigne'] * btnSize['sep'] - btnSize['sep'])
        difW = (self.width - screenW) / 2
        difH = (self.height - screenH) / 2
        for loop in range(btnSize['nbLigne']):
            for i in range(btnSize['nbCol']):
                rect = pg.Rect(difW + btnSize['btnSizeW'] * i + btnSize['sep'] * i, difH + btnSize['btnSizeH'] * loop + btnSize['sep'] * loop, btnSize['btnSizeW'],
                               btnSize['btnSizeH'])
                btnSize[str(i) + "," + str(loop)] = rect.center
        return btnSize

    def setScreen(self, screen):
        self.screen = screen
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        self.btnSizes = {'1': {'nbCol': 5, 'nbLigne': 7, 'sep': 30}, '2': {'nbCol': 5, 'nbLigne': 9, 'sep': 20}, '3':{'nbCol': 7, 'nbLigne': 12, 'sep': 10}}
        self.generateData()
        print("Set")
        print(self.btnSizes['1'])
        print(self.btnSizes['2'])
        print(self.btnSizes['3'])
    
    def getDatas(self, type :str , coordinates):
        width = self.btnSizes[type]['btnSizeW']
        height = self.btnSizes[type]['btnSizeH']
        coords = self.btnSizes[type][str(coordinates[0]) + ',' + str(coordinates[1])]
        return width, height, coords

class Bouton:
    def __init__(
        self, coordinates, type, texte, color, state, posBouton
    ):
        self.type = type
        self.posBouton = posBouton
        if self.type == 1:
            self.width, self.height, self.coordinates = posBouton.getDatas(str(self.type), coordinates)
        elif self.type == 2:
            self.width, self.height, self.coordinates = posBouton.getDatas(str(self.type), coordinates)
        elif self.type == 3:
            self.width, self.height, self.coordinates = posBouton.getDatas(str(self.type), coordinates)
        self.widthtop = int(self.coordinates[0] - self.width / 2)
        self.heighttop = int(self.coordinates[1] - self.height / 2)
        self.texte = texte
        self.font = pg.font.SysFont("Arial", int(self.width * 0.25 - 10))
        self.color = color
        self.state = state

    def affiche_bouton(self):
        center_rect = pg.draw.rect(
            screen,
            (179, 179, 179),
            [self.widthtop + 5, self.heighttop + 5, self.width - 10, self.height - 10],
        )
        surf_texte = self.font.render(self.texte, 1, self.color)
        rect_texte = surf_texte.get_rect()
        rect_texte.center = center_rect.center
        mouse = pg.mouse.get_pos()
        colorMid = (129, 129, 129)
        colorTop = (200, 200, 200)
        colorRight = (90, 90, 90)
        colorBot = (70, 70, 70)
        colorLeft = (180, 180, 180)

        if self.state == "Dead":
            pg.draw.rect(
                screen,
                (0, 0, 0),
                [self.widthtop, self.heighttop, self.width, self.height],
            )

        else:
            if self.state == "Down":
                colorMid = (69, 69, 69)
                colorTop = (140, 140, 140)
                colorRight = (30, 30, 30)
                colorBot = (10, 10, 10)
                colorLeft = (120, 120, 120)

            elif (
                self.widthtop <= mouse[0] <= self.widthtop + self.width
                and self.heighttop <= mouse[1] <= self.heighttop + self.height
                and not self.state == "Down"
            ):
                colorMid = (120, 120, 120)
                colorTop = (70, 70, 70)
                colorRight = (150, 150, 150)
                colorBot = (180, 180, 180)
                colorLeft = (90, 90, 90)

            pg.draw.polygon(
                screen,
                colorTop,
                [
                    (self.widthtop, self.heighttop),
                    (self.widthtop + self.width, self.heighttop),
                    (self.widthtop + self.width - 5, self.heighttop + 5),
                    (self.widthtop + 5, self.heighttop + 5),
                ],
            )
            pg.draw.polygon(
                screen,
                colorRight,
                [
                    (self.widthtop + self.width - 5, self.heighttop + 5),
                    (self.widthtop + self.width, self.heighttop),
                    (self.widthtop + self.width, self.heighttop + self.height),
                    (self.widthtop + self.width - 5, self.heighttop + self.height - 5),
                ],
            )
            pg.draw.polygon(
                screen,
                colorBot,
                [
                    (self.widthtop + 5, self.heighttop + self.height - 5),
                    (self.widthtop + self.width - 5, self.heighttop + self.height - 5),
                    (self.widthtop + self.width, self.heighttop + self.height),
                    (self.widthtop, self.heighttop + self.height),
                ],
            )
            pg.draw.polygon(
                screen,
                colorLeft,
                [
                    (self.widthtop, self.heighttop),
                    (self.widthtop + 5, self.heighttop + 5),
                    (self.widthtop + 5, self.heighttop + self.height - 6),
                    (self.widthtop, self.heighttop + self.height - 1),
                ],
            )

            pg.draw.rect(
                screen,
                colorMid,
                [
                    self.widthtop + 5,
                    self.heighttop + 5,
                    self.width - 10,
                    self.height - 10,
                ],
            )
            screen.blit(surf_texte, rect_texte)

    def isOn(self, mousePose):
        return (
            self.widthtop <= mousePose[0] <= self.widthtop + self.width
            and self.heighttop <= mousePose[1] <= self.heighttop + self.height
        )

    def getwidth(self):
        return [self.widthtop, self.widthtop + self.width]

    def getheight(self):
        return [self.heighttop, self.heighttop + self.height]

    def getstate(self):
        return self.state

    def setstate(self, state):
        if state in ["", "Down", "Dead"]:
            self.state = state

    def settexte(self, texte):
        if type(texte) == str:
            self.texte = texte

    def setsize(self, coordinates, type = None):
        if type is not None:
            self.type = type
        self.posBouton = posBouton
        if self.type == 1:
            self.width, self.height, self.coordinates = posBouton.getDatas(str(self.type), coordinates)
        elif self.type == 2:
            self.width, self.height, self.coordinates = posBouton.getDatas(str(self.type), coordinates)
        elif self.type == 3:
            self.width, self.height, self.coordinates = posBouton.getDatas(str(self.type), coordinates)
        self.widthtop = int(self.coordinates[0] - self.width / 2)
        self.heighttop = int(self.coordinates[1] - self.height / 2)
        self.font = pg.font.SysFont("Arial", int(self.width * 0.25 - 10))


class BarreDeVie:
    def __init__(self, name, pv):
        self.name = name
        self.pv = pv
        self.heightBar = 60

    def Affiche(self):
        self.AfficheBar()
        self.AfficheNom()

    def AfficheBar(self):
        width = screen.get_width()
        progressBar = ProgressBar(
            screen,
            int(width / 4),
            self.heightBar,
            int(width / 2),
            18,
            lambda: self.pv,
            curved=True,
            completedColour=(200, 0, 0),
        )
        pg.draw.polygon(
            screen,
            (218, 165, 32),
            [
                (width / 16 * 4 + 2, self.heightBar - 1),
                (width / 16 * 4 - 4, self.heightBar - 1),
                (width / 16 * 4 - 16, self.heightBar + 9),
                (width / 16 * 4 - 4, self.heightBar + 18),
                (width / 16 * 4 + 2, self.heightBar + 18),
                (width / 16 * 4 - 3, self.heightBar + 9),
            ],
        )
        pg.draw.polygon(
            screen,
            (255, 215, 0),
            [
                (width / 16 * 4 - 3, self.heightBar + 9),
                (width / 16 * 4 - 16, self.heightBar + 9),
                (width / 16 * 4 - 4, self.heightBar + 18),
                (width / 16 * 4 + 2, self.heightBar + 18),
            ],
        )

        pg.draw.polygon(
            screen,
            (218, 165, 32),
            [
                (width / 16 * 12 - 2, self.heightBar - 1),
                (width / 16 * 12 + 4, self.heightBar - 1),
                (width / 16 * 12 + 16, self.heightBar + 9),
                (width / 16 * 12 + 4, self.heightBar + 18),
                (width / 16 * 12 - 2, self.heightBar + 18),
                (width / 16 * 12 + 3, self.heightBar + 9),
            ],
        )
        pg.draw.polygon(
            screen,
            (255, 215, 0),
            [
                (width / 16 * 12 + 3, self.heightBar + 9),
                (width / 16 * 12 + 16, self.heightBar + 9),
                (width / 16 * 12 + 4, self.heightBar + 18),
                (width / 16 * 12 - 2, self.heightBar + 18),
            ],
        )
        pygame_widgets.update(ev)

    def AfficheNom(self):
        middle = self.heightBar - 30
        width = screen.get_width()
        nom = pg.font.SysFont("Arial", 34).render(self.name, True, (200, 200, 200))
        nom_rect = nom.get_rect(center=(width / 2, middle))
        nomWidth = nom.get_width()
        Gauche = width / 2 - nomWidth / 2 - 20
        Droite = width / 2 + nomWidth / 2 + 20
        pg.draw.polygon(
            screen,
            (174, 132, 25),
            [
                (Gauche - 8, middle - 4),
                (Gauche + 6, middle - 18),
                (Droite - 6, middle - 18),
                (Droite + 8, middle - 4),
                (Droite + 8, middle + 4),
                (Droite - 6, middle + 18),
                (Gauche + 6, middle + 18),
                (Gauche - 8, middle + 4),
            ],
        )
        pg.draw.polygon(
            screen,
            (218, 165, 32),
            [
                (Gauche - 12, middle),
                (Gauche - 8, middle),
                (Gauche - 8, middle + 4),
                (Gauche + 6, middle + 18),
                (Droite - 6, middle + 18),
                (Droite + 8, middle + 4),
                (Droite + 8, middle),
                (Droite + 12, middle),
                (Droite + 12, middle + 10),
                (Droite, middle + 22),
                (Gauche, middle + 22),
                (Gauche - 12, middle + 10),
            ],
        )
        pg.draw.polygon(
            screen,
            (218, 165, 32),
            [
                (Gauche - 12, middle),
                (Gauche - 8, middle),
                (Gauche - 8, middle - 4),
                (Gauche + 6, middle - 18),
                (Droite - 6, middle - 18),
                (Droite + 8, middle - 4),
                (Droite + 8, middle),
                (Droite + 12, middle),
                (Droite + 12, middle - 10),
                (Droite, middle - 22),
                (Gauche, middle - 22),
                (Gauche - 12, middle - 10),
            ],
        )
        pg.draw.polygon(
            screen,
            (255, 215, 0),
            [
                (Gauche - 18, middle),
                (Gauche - 12, middle),
                (Gauche - 12, middle + 6),
                (Gauche + 4, middle + 22),
                (Droite - 4, middle + 22),
                (Droite + 12, middle + 6),
                (Droite + 12, middle),
                (Droite + 18, middle),
                (Droite + 18, middle + 8),
                (Droite, middle + 26),
                (Gauche, middle + 26),
                (Gauche - 18, middle + 8),
            ],
        )
        pg.draw.polygon(
            screen,
            (255, 215, 0),
            [
                (Gauche - 18, middle),
                (Gauche - 12, middle),
                (Gauche - 12, middle - 6),
                (Gauche + 4, middle - 22),
                (Droite - 4, middle - 22),
                (Droite + 12, middle - 6),
                (Droite + 12, middle),
                (Droite + 18, middle),
                (Droite + 18, middle - 8),
                (Droite, middle - 26),
                (Gauche, middle - 26),
                (Gauche - 18, middle - 8),
            ],
        )
        screen.blit(nom, nom_rect)

    def setPv(self, pv):
        self.pv = pv


class BTNLangue:
    def __init__(self, widthpos, heighttop, width, height, img):
        self.widthpos = widthpos
        self.heighttop = heighttop
        self.width = width
        self.height = height
        self.img = img  # Gérer la récupération de l'image

    def Afficher(self):
        pg.draw.rect(
            screen,
            (120, 120, 120),
            [self.widthpos, self.heighttop, self.width, self.height],
        )
        pg.draw.rect(
            screen,
            (140, 140, 140),
            [self.widthpos + 5, self.heighttop + 5, self.width - 10, self.height - 10],
        )
        pg.draw.polygon(
            screen,
            (200, 200, 200),
            [
                (self.widthpos, self.heighttop),
                (self.widthpos + self.width - 1, self.heighttop),
                (self.widthpos + self.width - 6, self.heighttop + 5),
                (self.widthpos + 5, self.heighttop + 5),
            ],
        )
        pg.draw.polygon(
            screen,
            (180, 180, 180),
            [
                (self.widthpos, self.heighttop),
                (self.widthpos + 5, self.heighttop + 5),
                (self.widthpos + 5, self.heighttop + self.height - 5),
                (self.widthpos, self.heighttop + self.height),
            ],
        )
        pg.draw.polygon(
            screen,
            (100, 100, 100),
            [
                (self.widthpos + 5, self.heighttop + self.height - 5),
                (self.widthpos + self.width - 5, self.heighttop + self.height - 5),
                (self.widthpos + self.width, self.heighttop + self.height),
                (self.widthpos, self.heighttop + self.height),
            ],
        )

posBouton = PosBoutons(screen)

bouton_Jouer = Bouton(
    (2, 4),
    1,
    "Jouer",
    (0, 200, 0),
    "",
    posBouton
)
bouton_quit = Bouton(
    (6, 10),
    2,
    "Quit",
    (255, 255, 255),
    "",
    posBouton
)
histo = 1
barreDeVie = BarreDeVie("Banshee", 200)
BTNFR = BTNLangue(150, 150, 200, 50, "img")
menu = Menu.EscapeMenu(
    screen.get_width() / 6,
    screen.get_height() / 6,
    screen.get_width() / 3 * 2,
    screen.get_height() / 3 * 2,
    screen,
    Bouton(
        (
            6, 10
        ),
        3,
        "Appliquer",
        (255, 255, 255),
        "",
        posBouton
    ),
    posBouton
)
bgColor = (0, 0, 0)

while running:
    clock.tick(30)
    width = screen.get_width()
    height = screen.get_height()
    pg.draw.rect(screen, bgColor, [0, 0, width, height])
    bouton_Jouer.setsize((2, 4))
    bouton_quit.setsize((6, 10))
    menu.setParams(width / 6, height / 6, width / 3 * 2, height / 3 * 2, screen, posBouton)
    for ev in pg.event.get():
        if ev.type == pg.QUIT:
            pg.quit()
            running = False
            sys.exit()

        if ev.type == pg.MOUSEBUTTONDOWN:
            mouse = pg.mouse.get_pos()
            if afficheMenu:
                if menu.getBouton().isOn(mouse) and not menu.getBouton().getstate() in [
                    "Down",
                    "Dead",
                ]:
                    sauvegarder_config(newConfig)
                    afficheMenu = not afficheMenu
            else:
                if bouton_quit.isOn(mouse) and not bouton_quit.getstate() in [
                    "Down",
                    "Dead",
                ]:
                    pg.quit()
                    running = False
                    sys.exit()

        if ev.type == pg.KEYDOWN:
            if ev.key == pg.K_ESCAPE:
                afficheMenu = True
            elif ev.key == pg.K_BACKSPACE:
                mana_uti = mana_uti[:-1]
            elif ev.key == pg.K_RETURN:
                selecMD = True

        if ev.type == pg.TEXTINPUT:
            mana_uti += ev.text

    bouton_quit.affiche_bouton()
    bouton_Jouer.affiche_bouton()
    barreDeVie.Affiche()
    if afficheMenu:
        res = menu.Afficher()
        if res["end"] == 1:
            newConfig = res["config"]
            menu.setActive(res["onglet"])
            screen = pg.display.set_mode(
                (int(newConfig["width"]), int(newConfig["height"]))
            )
            posBouton.setScreen(screen)
        elif res["end"] == 2:
            afficheMenu = res["Menu"]

    pg.display.update()
