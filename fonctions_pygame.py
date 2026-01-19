import random, os, sys, pygame_widgets, pygame as pg, config as config, Classes.MenuDnD as Menu
from math import floor

from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from pygame_widgets.progressbar import ProgressBar
from pygame_widgets.mouse import Mouse, MouseState
from config import sauvegarder_config

from Classes.Boutons import Bouton, PosBoutons

os.environ["SDL_VIDEO_CENTERED"] = "1"

# Configuration et initialisation
dataConfig = config.charger_config()
newConfig = dataConfig
pg.init()
screen = pg.display.set_mode((int(dataConfig["width"]), int(dataConfig["height"])))
clock = pg.time.Clock()
running = True
running2 = True

# Configuration des polices
hugeassfont = pg.font.SysFont("Arial", 150, 1, 0)
hugeassfontplus = pg.font.SysFont("Arial", 160, 1, 0)
bigfont = pg.font.SysFont("Arial", 40)
font = pg.font.SysFont("Arial", 30)
smallfont = pg.font.SysFont("Arial", 20)
vsmallfont = pg.font.SysFont("Arial", 14)
atkfont = pg.font.SysFont("Arial", 17)

# Variables globales de l'interface
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
def_type = ""
mana_uti = ""
temp = 0
afficheMenu = False

volume = dataConfig["volume"]
phrasesClass = config.load_phrases(dataConfig["langue"])


class BarreDeVie:
    """
    Classe représentant une barre de vie avec un design décoratif.

    Cette classe affiche une barre de progression pour les points de vie
    avec des éléments décoratifs dorés et le nom du personnage.

    Attributes:
        name (str): Nom du personnage affiché
        pv (int): Points de vie actuels (de 0 à 100)
        heightBar (int): Position verticale de la barre de vie
    """

    def __init__(self, name, pv):
        """
        Initialise une nouvelle barre de vie.

        Args:
            name (str): Nom du personnage
            pv (int): Points de vie initiaux (de 0 à 100)
        """
        self.name = name
        self.pv = pv
        self.heightBar = 60

    def Affiche(self):
        """
        Affiche la barre de vie complète (barre + nom).
        """
        self.AfficheBar()
        self.AfficheNom()

    def AfficheBar(self):
        """
        Affiche la barre de progression des points de vie avec ses décorations dorées.
        """
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

        # Décoration dorée gauche
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

        # Décoration dorée droite
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
        """
        Affiche le nom du personnage dans un cadre décoratif doré au-dessus de la barre de vie.
        """
        middle = self.heightBar - 30
        width = screen.get_width()
        nom = pg.font.SysFont("Arial", 34).render(self.name, True, (200, 200, 200))
        nom_rect = nom.get_rect(center=(width / 2, middle))
        nomWidth = nom.get_width()
        Gauche = width / 2 - nomWidth / 2 - 20
        Droite = width / 2 + nomWidth / 2 + 20

        # Cadre décoratif pour le nom - fond bronze
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

        # Bordures dorées du cadre
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

        # Contour doré extérieur
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
        """
        Met à jour les points de vie affichés.

        Args:
            pv (int): Nouveaux points de vie (de 0 à 100)
        """
        self.pv = pv


class BTNLangue:
    """
    Classe représentant un bouton de sélection de langue avec effet 3D.

    Cette classe crée un bouton spécialisé pour la sélection de langue
    avec un design en relief et la possibilité d'afficher une image.

    Attributes:
        widthpos (int): Position horizontale du bouton
        heighttop (int): Position verticale du bouton
        width (int): Largeur du bouton
        height (int): Hauteur du bouton
        img (str): Référence vers l'image à afficher
    """

    def __init__(self, widthpos, heighttop, width, height, img):
        """
        Initialise un nouveau bouton de langue.

        Args:
            widthpos (int): Position x du coin supérieur gauche
            heighttop (int): Position y du coin supérieur gauche
            width (int): Largeur du bouton
            height (int): Hauteur du bouton
            img (str): Référence vers l'image du drapeau/langue
        """
        self.widthpos = widthpos
        self.heighttop = heighttop
        self.width = width
        self.height = height
        self.img = img  # Gérer la récupération de l'image

    def Afficher(self):
        """
        Affiche le bouton de langue avec son effet 3D et ses bordures en relief.

        Le bouton est dessiné avec des effets d'ombre et de lumière pour créer
        un aspect tridimensionnel réaliste.
        """
        # Fond du bouton
        pg.draw.rect(
            screen,
            (120, 120, 120),
            [self.widthpos, self.heighttop, self.width, self.height],
        )

        # Zone centrale du bouton
        pg.draw.rect(
            screen,
            (140, 140, 140),
            [self.widthpos + 5, self.heighttop + 5, self.width - 10, self.height - 10],
        )

        # Bord supérieur (éclairé)
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

        # Bord gauche (éclairé)
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

        # Bord inférieur (ombré)
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


# class SelectStats:
#     def __init__(self, Screen, x, y, Width, Height):
#         self.fond = []
#         self.screen = Screen
#         self.x = x
#         self.y = y
#         self.width = Width
#         self.height = Height
#         self.PVMana = {"max": 3000, "PV": 1500, "mana": 1500}
#         self.values = {"max": 100, "total": 3, "force": 1, "def": 1, "crit": 1}
#         self.topLeftW = None
#         self.topLeftH = None
#         self.rect = None
#         self.btnFont = None
#         self.mouse = False
#         self.click = False
#         self.positions = {
#             "PV": {
#                 "x": 0,
#                 "y": 0,
#                 "height": 0,
#                 "width": 0,
#                 "btnH": 0,
#                 "btnW": 0,
#                 "couleurRemplissage": (220, 20, 20),
#             },  # Red
#             "mana": {
#                 "x": 0,
#                 "y": 0,
#                 "height": 0,
#                 "width": 0,
#                 "btnH": 0,
#                 "btnW": 0,
#                 "couleurRemplissage": (20, 20, 220),
#             },  # Blue
#             "force": {
#                 "x": 0,
#                 "y": 0,
#                 "height": 0,
#                 "width": 0,
#                 "btnH": 0,
#                 "btnW": 0,
#                 "couleurRemplissage": (220, 140, 20),
#             },  # Orange
#             "def": {
#                 "x": 0,
#                 "y": 0,
#                 "height": 0,
#                 "width": 0,
#                 "btnH": 0,
#                 "btnW": 0,
#                 "couleurRemplissage": (20, 180, 20),
#             },  # Green
#             "crit": {
#                 "x": 0,
#                 "y": 0,
#                 "height": 0,
#                 "width": 0,
#                 "btnH": 0,
#                 "btnW": 0,
#                 "couleurRemplissage": (180, 20, 180),
#             },  # Purple/Magenta
#         }
#         self.boutons = {
#             "PV": {
#                 "positif": {
#                     "10": {
#                         "coords": (0, 0, 0, 0),
#                         "Top": [],
#                         "Right": [],
#                         "Bottom": [],
#                         "Left": [],
#                         "text": "",
#                     },
#                     "50": {
#                         "coords": (0, 0, 0, 0),
#                         "Top": [],
#                         "Right": [],
#                         "Bottom": [],
#                         "Left": [],
#                         "text": "",
#                     },
#                     "100": {
#                         "coords": (0, 0, 0, 0),
#                         "Top": [],
#                         "Right": [],
#                         "Bottom": [],
#                         "Left": [],
#                         "text": "",
#                     },
#                 },
#                 "negatif": {
#                     "10": {
#                         "coords": (0, 0, 0, 0),
#                         "Top": [],
#                         "Right": [],
#                         "Bottom": [],
#                         "Left": [],
#                         "text": "",
#                     },
#                     "50": {
#                         "coords": (0, 0, 0, 0),
#                         "Top": [],
#                         "Right": [],
#                         "Bottom": [],
#                         "Left": [],
#                         "text": "",
#                     },
#                     "100": {
#                         "coords": (0, 0, 0, 0),
#                         "Top": [],
#                         "Right": [],
#                         "Bottom": [],
#                         "Left": [],
#                         "text": "",
#                     },
#                 },
#                 "jauge": {
#                     "base": {
#                         "Fond": (0, 0, 0, 0),
#                         "Top": [],
#                         "Right": [],
#                         "Bottom": [],
#                         "Left": [],
#                     },
#                     "remplissage": (0, 0, 0, 0),
#                 },
#             },
#             "mana": {
#                 "positif": {
#                     "10": {
#                         "coords": (0, 0, 0, 0),
#                         "Top": [],
#                         "Right": [],
#                         "Bottom": [],
#                         "Left": [],
#                         "text": "",
#                     },
#                     "50": {
#                         "coords": (0, 0, 0, 0),
#                         "Top": [],
#                         "Right": [],
#                         "Bottom": [],
#                         "Left": [],
#                         "text": "",
#                     },
#                     "100": {
#                         "coords": (0, 0, 0, 0),
#                         "Top": [],
#                         "Right": [],
#                         "Bottom": [],
#                         "Left": [],
#                         "text": "",
#                     },
#                 },
#                 "negatif": {
#                     "10": {
#                         "coords": (0, 0, 0, 0),
#                         "Top": [],
#                         "Right": [],
#                         "Bottom": [],
#                         "Left": [],
#                         "text": "",
#                     },
#                     "50": {
#                         "coords": (0, 0, 0, 0),
#                         "Top": [],
#                         "Right": [],
#                         "Bottom": [],
#                         "Left": [],
#                         "text": "",
#                     },
#                     "100": {
#                         "coords": (0, 0, 0, 0),
#                         "Top": [],
#                         "Right": [],
#                         "Bottom": [],
#                         "Left": [],
#                         "text": "",
#                     },
#                 },
#                 "jauge": {
#                     "base": {
#                         "Fond": (0, 0, 0, 0),
#                         "Top": [],
#                         "Right": [],
#                         "Bottom": [],
#                         "Left": [],
#                     },
#                     "remplissage": (0, 0, 0, 0),
#                 },
#             },
#             "force": {
#                 "positif": {
#                     "1": {
#                         "coords": (0, 0, 0, 0),
#                         "Top": [],
#                         "Right": [],
#                         "Bottom": [],
#                         "Left": [],
#                         "text": "",
#                     },
#                     "5": {
#                         "coords": (0, 0, 0, 0),
#                         "Top": [],
#                         "Right": [],
#                         "Bottom": [],
#                         "Left": [],
#                         "text": "",
#                     },
#                     "10": {
#                         "coords": (0, 0, 0, 0),
#                         "Top": [],
#                         "Right": [],
#                         "Bottom": [],
#                         "Left": [],
#                         "text": "",
#                     },
#                 },
#                 "negatif": {
#                     "1": {
#                         "coords": (0, 0, 0, 0),
#                         "Top": [],
#                         "Right": [],
#                         "Bottom": [],
#                         "Left": [],
#                         "text": "",
#                     },
#                     "5": {
#                         "coords": (0, 0, 0, 0),
#                         "Top": [],
#                         "Right": [],
#                         "Bottom": [],
#                         "Left": [],
#                         "text": "",
#                     },
#                     "10": {
#                         "coords": (0, 0, 0, 0),
#                         "Top": [],
#                         "Right": [],
#                         "Bottom": [],
#                         "Left": [],
#                         "text": "",
#                     },
#                 },
#                 "jauge": {
#                     "base": {
#                         "Fond": (0, 0, 0, 0),
#                         "Top": [],
#                         "Right": [],
#                         "Bottom": [],
#                         "Left": [],
#                     },
#                     "remplissage": (0, 0, 0, 0),
#                 },
#             },
#             "def": {
#                 "positif": {
#                     "1": {
#                         "coords": (0, 0, 0, 0),
#                         "Top": [],
#                         "Right": [],
#                         "Bottom": [],
#                         "Left": [],
#                         "text": "",
#                     },
#                     "5": {
#                         "coords": (0, 0, 0, 0),
#                         "Top": [],
#                         "Right": [],
#                         "Bottom": [],
#                         "Left": [],
#                         "text": "",
#                     },
#                     "10": {
#                         "coords": (0, 0, 0, 0),
#                         "Top": [],
#                         "Right": [],
#                         "Bottom": [],
#                         "Left": [],
#                         "text": "",
#                     },
#                 },
#                 "negatif": {
#                     "1": {
#                         "coords": (0, 0, 0, 0),
#                         "Top": [],
#                         "Right": [],
#                         "Bottom": [],
#                         "Left": [],
#                         "text": "",
#                     },
#                     "5": {
#                         "coords": (0, 0, 0, 0),
#                         "Top": [],
#                         "Right": [],
#                         "Bottom": [],
#                         "Left": [],
#                         "text": "",
#                     },
#                     "10": {
#                         "coords": (0, 0, 0, 0),
#                         "Top": [],
#                         "Right": [],
#                         "Bottom": [],
#                         "Left": [],
#                         "text": "",
#                     },
#                 },
#                 "jauge": {
#                     "base": {
#                         "Fond": (0, 0, 0, 0),
#                         "Top": [],
#                         "Right": [],
#                         "Bottom": [],
#                         "Left": [],
#                     },
#                     "remplissage": (0, 0, 0, 0),
#                 },
#             },
#             "crit": {
#                 "positif": {
#                     "1": {
#                         "coords": (0, 0, 0, 0),
#                         "Top": [],
#                         "Right": [],
#                         "Bottom": [],
#                         "Left": [],
#                         "text": "",
#                     },
#                     "5": {
#                         "coords": (0, 0, 0, 0),
#                         "Top": [],
#                         "Right": [],
#                         "Bottom": [],
#                         "Left": [],
#                         "text": "",
#                     },
#                     "10": {
#                         "coords": (0, 0, 0, 0),
#                         "Top": [],
#                         "Right": [],
#                         "Bottom": [],
#                         "Left": [],
#                         "text": "",
#                     },
#                 },
#                 "negatif": {
#                     "1": {
#                         "coords": (0, 0, 0, 0),
#                         "Top": [],
#                         "Right": [],
#                         "Bottom": [],
#                         "Left": [],
#                         "text": "",
#                     },
#                     "5": {
#                         "coords": (0, 0, 0, 0),
#                         "Top": [],
#                         "Right": [],
#                         "Bottom": [],
#                         "Left": [],
#                         "text": "",
#                     },
#                     "10": {
#                         "coords": (0, 0, 0, 0),
#                         "Top": [],
#                         "Right": [],
#                         "Bottom": [],
#                         "Left": [],
#                         "text": "",
#                     },
#                 },
#                 "jauge": {
#                     "base": {
#                         "Fond": (0, 0, 0, 0),
#                         "Top": [],
#                         "Right": [],
#                         "Bottom": [],
#                         "Left": [],
#                     },
#                     "remplissage": (0, 0, 0, 0),
#                 },
#             },
#         }
#         self.posTexteJauges = {}
#         self.genererRects()
#
#     def genererRects(self):
#         self.topLeftW = self.x - int(self.width / 2)
#         self.topLeftH = self.y - int(self.height / 2)
#         self.rect = pg.Rect(self.topLeftW, self.topLeftH, self.width, self.height)
#         self.genererPos()
#
#     def genererPos(self):
#         nbChoix = len(self.positions)
#         topLeftW = self.topLeftW + 40
#         topLeftH = self.topLeftH + 40
#         Width = self.width - 80
#         Height = self.height - 80
#         bloc = (Width - 40, floor((Height - 40) / nbChoix))
#         i = 0
#         if self.fond:
#             self.fond = []
#         for j in self.positions:
#             rect = pg.Rect(topLeftW + 20, topLeftH + 20 + bloc[1] * i, bloc[0], bloc[1])
#             temp = self.positions[j]
#             temp["x"] != 0 or temp.update({"x": rect.centerx})
#             temp["y"] != 0 or temp.update({"y": rect.centery})
#             temp["width"] != 0 or temp.update({"width": floor(Width / 2)})
#             temp["height"] != 0 or temp.update({"height": floor(Height / 24)})
#             temp["btnW"] != 0 or temp.update({"btnW": floor(Height / 19)})
#             temp["btnH"] != 0 or temp.update({"btnH": floor(Height / 19)})
#             self.fond.append(rect)
#             i += 1
#         self.genererJauge()
#
#     def genererJauge(self, update=False):
#         for loop in self.positions:
#             if self.btnFont is None :
#                 self.btnFont = pg.font.SysFont(
#                     "Arial", floor(self.positions[loop]["btnW"] * 0.5)
#                 )
#             if loop == "PV":
#                 pourcentage = self.PVMana["PV"] / self.PVMana["max"]
#             elif loop == "mana":
#                 pourcentage = self.PVMana["mana"] / self.PVMana["max"]
#             elif loop == "force":
#                 pourcentage = self.values["force"] / 98
#             elif loop == "def":
#                 pourcentage = self.values["def"] / 98
#             elif loop == "crit":
#                 pourcentage = self.values["crit"] / 25
#             else:
#                 pourcentage = 0
#             LeftWidth = floor(
#                 self.positions[loop]["x"] - self.positions[loop]["width"] / 2
#             )
#             topHeight = floor(
#                 self.positions[loop]["y"] - self.positions[loop]["height"] / 2
#             )
#             RightWidth = floor(
#                 self.positions[loop]["x"] + self.positions[loop]["width"] / 2
#             )
#             topRightHeight = floor(
#                 self.positions[loop]["y"] - self.positions[loop]["height"] / 2
#             )
#             bottomLeftWidth = floor(
#                 self.positions[loop]["x"] - self.positions[loop]["width"] / 2
#             )
#             bottomLeftHeight = floor(
#                 self.positions[loop]["y"] + self.positions[loop]["height"] / 2
#             )
#             bottomRightWidth = floor(
#                 self.positions[loop]["x"] + self.positions[loop]["width"] / 2
#             )
#             bottomHeight = floor(
#                 self.positions[loop]["y"] + self.positions[loop]["height"] / 2
#             )
#             self.boutons[loop]["jauge"]["base"]["Fond"] = (
#                 LeftWidth,
#                 topHeight,
#                 self.positions[loop]["width"],
#                 self.positions[loop]["height"],
#             )
#             self.boutons[loop]["jauge"]["remplissage"] = (
#                 LeftWidth + 1,
#                 topHeight + 1,
#                 floor(self.positions[loop]["width"] * pourcentage) - 1,
#                 self.positions[loop]["height"] - 1,
#             )
#             self.boutons[loop]["jauge"]["base"]["Top"] = [
#                 (LeftWidth - 5, topHeight - 5),
#                 (RightWidth + 5, topRightHeight - 5),
#                 (RightWidth, topRightHeight),
#                 (LeftWidth, topHeight),
#             ]
#             self.boutons[loop]["jauge"]["base"]["Right"] = [
#                 (RightWidth + 5, topRightHeight - 5),
#                 (bottomRightWidth + 5, bottomHeight + 5),
#                 (bottomRightWidth, bottomHeight),
#                 (RightWidth, topRightHeight),
#             ]
#             self.boutons[loop]["jauge"]["base"]["Bottom"] = [
#                 (bottomRightWidth + 5, bottomHeight + 5),
#                 (bottomLeftWidth - 5, bottomLeftHeight + 5),
#                 (bottomLeftWidth, bottomLeftHeight),
#                 (bottomRightWidth, bottomHeight),
#             ]
#             self.boutons[loop]["jauge"]["base"]["Left"] = [
#                 (bottomLeftWidth - 5, bottomLeftHeight + 5),
#                 (LeftWidth - 5, topHeight - 5),
#                 (LeftWidth, topHeight),
#                 (bottomLeftWidth, bottomLeftHeight),
#             ]
#             if loop == "PV" or loop == "mana":
#                 self.posTexteJauges[loop] = self.btnFont.render(
#                         str(self.PVMana[loop]), True, (255, 255, 255)
#                     )
#             elif loop == "force" or loop == "def" or loop == "crit":
#                 self.posTexteJauges[loop] = self.btnFont.render(
#                     str(self.values[loop]), True, (255, 255, 255)
#                 )
#         if not update:
#             self.genererBoutons()
#
#     def genererBoutons(self):
#         for loop in self.positions:
#             i = 0
#             for j in self.boutons[loop]["positif"]:
#                 i += 1
#                 LeftWidth = floor(
#                     self.positions[loop]["x"]
#                     + self.positions[loop]["width"] / 2
#                     + self.positions[loop]["btnW"] * (i - 1)
#                     + (10 * i + 5)
#                 )
#                 RightWidth = floor(
#                     self.positions[loop]["x"]
#                     + self.positions[loop]["width"] / 2
#                     + self.positions[loop]["btnW"] * i
#                     + (10 * i + 5)
#                 )
#                 topHeight = floor(
#                     self.positions[loop]["y"] - self.positions[loop]["btnH"] / 2
#                 )
#                 bottomHeight = floor(
#                     self.positions[loop]["y"] + self.positions[loop]["btnH"] / 2
#                 )
#                 self.boutons[loop]["positif"][j]["coords"] = (
#                     LeftWidth,
#                     topHeight,
#                     self.positions[loop]["btnW"],
#                     self.positions[loop]["btnH"],
#                 )
#                 self.boutons[loop]["positif"][j]["Top"] = [
#                     (LeftWidth - 2, topHeight - 2),
#                     (RightWidth + 2, topHeight - 2),
#                     (RightWidth, topHeight),
#                     (LeftWidth, topHeight),
#                 ]
#                 self.boutons[loop]["positif"][j]["Right"] = [
#                     (RightWidth + 2, topHeight - 2),
#                     (RightWidth + 2, bottomHeight + 2),
#                     (RightWidth, bottomHeight),
#                     (RightWidth, topHeight),
#                 ]
#                 self.boutons[loop]["positif"][j]["Bottom"] = [
#                     (RightWidth + 2, bottomHeight + 2),
#                     (LeftWidth - 2, bottomHeight + 2),
#                     (LeftWidth, bottomHeight),
#                     (RightWidth, bottomHeight),
#                 ]
#                 self.boutons[loop]["positif"][j]["Left"] = [
#                     (LeftWidth - 2, bottomHeight + 2),
#                     (LeftWidth - 2, topHeight - 2),
#                     (LeftWidth, topHeight),
#                     (LeftWidth, bottomHeight),
#                 ]
#                 self.boutons[loop]["positif"][j]["text"] = "+" + str(j)
#             i = 0
#             for j in self.boutons[loop]["negatif"]:
#                 i += 1
#                 LeftWidth = floor(
#                     self.positions[loop]["x"]
#                     - self.positions[loop]["width"] / 2
#                     - self.positions[loop]["btnW"] * (i)
#                     - (10 * i + 5)
#                 )
#                 RightWidth = floor(
#                     self.positions[loop]["x"]
#                     - self.positions[loop]["width"] / 2
#                     - self.positions[loop]["btnW"] * (i - 1)
#                     - (10 * i + 5)
#                 )
#                 topHeight = floor(
#                     self.positions[loop]["y"] - self.positions[loop]["btnH"] / 2
#                 )
#                 bottomHeight = floor(
#                     self.positions[loop]["y"] + self.positions[loop]["btnH"] / 2
#                 )
#                 self.boutons[loop]["negatif"][j]["coords"] = (
#                     LeftWidth,
#                     topHeight,
#                     self.positions[loop]["btnW"],
#                     self.positions[loop]["btnH"],
#                 )
#                 self.boutons[loop]["negatif"][j]["Top"] = [
#                     (LeftWidth - 2, topHeight - 2),
#                     (RightWidth + 2, topHeight - 2),
#                     (RightWidth, topHeight),
#                     (LeftWidth, topHeight),
#                 ]
#                 self.boutons[loop]["negatif"][j]["Right"] = [
#                     (RightWidth + 2, topHeight - 2),
#                     (RightWidth + 2, bottomHeight + 2),
#                     (RightWidth, bottomHeight),
#                     (RightWidth, topHeight),
#                 ]
#                 self.boutons[loop]["negatif"][j]["Bottom"] = [
#                     (RightWidth + 2, bottomHeight + 2),
#                     (LeftWidth - 2, bottomHeight + 2),
#                     (LeftWidth, bottomHeight),
#                     (RightWidth, bottomHeight),
#                 ]
#                 self.boutons[loop]["negatif"][j]["Left"] = [
#                     (LeftWidth - 2, bottomHeight + 2),
#                     (LeftWidth - 2, topHeight - 2),
#                     (LeftWidth, topHeight),
#                     (LeftWidth, bottomHeight),
#                 ]
#                 self.boutons[loop]["negatif"][j]["text"] = "-" + str(j)
#
#     def Afficher(self):
#         pg.draw.rect(self.screen, (40, 40, 40), self.rect, border_radius=20)
#         i = 0
#         for j in self.boutons:
#             i += 1
#             rectJauge = pg.draw.rect(
#                 self.screen, (10, 10, 10), self.boutons[j]["jauge"]["base"]["Fond"]
#             )
#             pg.draw.polygon(
#                 self.screen, (100, 100, 100), self.boutons[j]["jauge"]["base"]["Top"]
#             )
#             pg.draw.polygon(
#                 self.screen, (70, 70, 70), self.boutons[j]["jauge"]["base"]["Right"]
#             )
#             pg.draw.polygon(
#                 self.screen, (60, 60, 60), self.boutons[j]["jauge"]["base"]["Bottom"]
#             )
#             pg.draw.polygon(
#                 self.screen, (90, 90, 90), self.boutons[j]["jauge"]["base"]["Left"]
#             )
#             pg.draw.rect(
#                 self.screen,
#                 self.positions[j]["couleurRemplissage"],
#                 self.boutons[j]["jauge"]["remplissage"],
#             )
#             surf_txt = self.posTexteJauges[j]
#             rect_txt = surf_txt.get_rect()
#             rect_txt.center = rectJauge.center
#             self.screen.blit(surf_txt, rect_txt)
#             colors = {}
#             for k in self.boutons[j]["positif"]:
#                 active = hovered = False
#                 if j == "PV":
#                     if self.PVMana["PV"] + int(k) <= self.PVMana["max"] - 250:
#                         # Active button - bright gold with proper lighting
#                         active = True
#                         if self.isOnBtn(j, "positif", k):
#                             # Active hovered button - bright gold with proper lighting
#                             hovered = True
#                     else:
#                         # Inactive button - darker, muted gold
#                         active = hovered = False
#                 elif j == "mana":
#                     if self.PVMana["mana"] + int(k) <= self.PVMana["max"] - 250:
#                         # Active button - bright gold with proper lighting
#                         active = True
#                         if self.isOnBtn(j, "positif", k):
#                             # Active hovered button - bright gold with proper lighting
#                             hovered = True
#                     else:
#                         # Inactive button - darker, muted gold
#                         active = hovered = False
#                 elif j == "force" or j == "def":
#                     if self.values["total"] + int(k) <= self.values["max"] - 2:
#                         # Active button - bright gold with proper lighting
#                         active = True
#                         if self.isOnBtn(j, "positif", k):
#                             # Active hovered button - bright gold with proper lighting
#                             hovered = True
#                     else:
#                         # Inactive button - darker, muted gold
#                         active = hovered = False
#                 elif j == "crit":
#                     if (
#                         self.values["total"] + int(k) <= self.values["max"] - 2
#                         and self.values["crit"] + int(k) <= 25
#                     ):
#                         # Active button - bright gold with proper lighting
#                         active = True
#                         if self.isOnBtn(j, "positif", k):
#                             # Active hovered button - bright gold with proper lighting
#                             hovered = True
#                     else:
#                         # Inactive button - darker, muted gold
#                         active = hovered = False
#
#                 if hovered:
#                     colors = {
#                         "Fond": (40, 40, 40),
#                         "Top": (139, 69, 19),
#                         "Right": (218, 165, 32),
#                         "Bottom": (255, 215, 0),
#                         "Left": (184, 134, 11),
#                     }
#                 elif active:
#                     colors = {
#                         "Fond": (40, 40, 40),
#                         "Top": (255, 215, 0),
#                         "Right": (184, 134, 11),
#                         "Bottom": (139, 69, 19),
#                         "Left": (218, 165, 32),
#                     }
#                 else:
#                     colors = {
#                         "Fond": (40, 40, 40),
#                         "Top": (120, 100, 50),
#                         "Right": (80, 60, 30),
#                         "Bottom": (60, 40, 20),
#                         "Left": (100, 80, 40),
#                     }
#                 if colors:
#                     rect = pg.draw.rect(
#                         self.screen,
#                         colors["Fond"],
#                         self.boutons[j]["positif"][k]["coords"],
#                     )
#                     center = rect.center
#                     pg.draw.polygon(
#                         self.screen, colors["Top"], self.boutons[j]["positif"][k]["Top"]
#                     )
#                     pg.draw.polygon(
#                         self.screen,
#                         colors["Right"],
#                         self.boutons[j]["positif"][k]["Right"],
#                     )
#                     pg.draw.polygon(
#                         self.screen,
#                         colors["Bottom"],
#                         self.boutons[j]["positif"][k]["Bottom"],
#                     )
#                     pg.draw.polygon(
#                         self.screen,
#                         colors["Left"],
#                         self.boutons[j]["positif"][k]["Left"],
#                     )
#                     surf_txt = self.btnFont.render(
#                         self.boutons[j]["positif"][k]["text"], True, colors["Top"]
#                     )
#                     rect_txt = surf_txt.get_rect()
#                     rect_txt.center = center
#                     self.screen.blit(surf_txt, rect_txt)
#
#             for k in self.boutons[j]["negatif"]:
#                 active = hovered = False
#                 if j == "PV":
#                     if self.PVMana["PV"] - int(k) <= self.PVMana["max"] - 250:
#                         # Active button - bright gold with proper lighting
#                         active = True
#                         if self.isOnBtn(j, "negatif", k):
#                             # Active hovered button - bright gold with proper lighting
#                             hovered = True
#                     else:
#                         # Inactive button - darker, muted gold
#                         active = hovered = False
#                 elif j == "mana":
#                     if self.PVMana["mana"] - int(k) <= self.PVMana["max"] - 250:
#                         # Active button - bright gold with proper lighting
#                         active = True
#                         if self.isOnBtn(j, "negatif", k):
#                             # Active hovered button - bright gold with proper lighting
#                             hovered = True
#                     else:
#                         # Inactive button - darker, muted gold
#                         active = hovered = False
#                 elif j == "force" or j == "def":
#                     if (
#                         self.values["total"] - int(k) <= self.values["max"] - 2
#                         and self.values[j] - int(k) >= 1
#                     ):
#                         # Active button - bright gold with proper lighting
#                         active = True
#                         if self.isOnBtn(j, "negatif", k):
#                             # Active hovered button - bright gold with proper lighting
#                             hovered = True
#                     else:
#                         # Inactive button - darker, muted gold
#                         active = hovered = False
#                 elif j == "crit":
#                     if (
#                         self.values["total"] - int(k) <= self.values["max"] - 2
#                         and self.values["crit"] - int(k) >= 1
#                     ):
#                         # Active button - bright gold with proper lighting
#                         active = True
#                         if self.isOnBtn(j, "negatif", k):
#                             # Active hovered button - bright gold with proper lighting
#                             hovered = True
#                     else:
#                         # Inactive button - darker, muted gold
#                         active = hovered = False
#
#                 if hovered:
#                     colors = {
#                         "Fond": (40, 40, 40),
#                         "Top": (139, 69, 19),
#                         "Right": (218, 165, 32),
#                         "Bottom": (255, 215, 0),
#                         "Left": (184, 134, 11),
#                     }
#                 elif active:
#                     colors = {
#                         "Fond": (40, 40, 40),
#                         "Top": (255, 215, 0),
#                         "Right": (184, 134, 11),
#                         "Bottom": (139, 69, 19),
#                         "Left": (218, 165, 32),
#                     }
#                 else:
#                     colors = {
#                         "Fond": (40, 40, 40),
#                         "Top": (120, 100, 50),
#                         "Right": (80, 60, 30),
#                         "Bottom": (60, 40, 20),
#                         "Left": (100, 80, 40),
#                     }
#
#                 if colors:
#                     rect = pg.draw.rect(
#                         self.screen,
#                         colors["Fond"],
#                         self.boutons[j]["negatif"][k]["coords"],
#                     )
#                     center = rect.center
#                     pg.draw.polygon(
#                         self.screen, colors["Top"], self.boutons[j]["negatif"][k]["Top"]
#                     )
#                     pg.draw.polygon(
#                         self.screen,
#                         colors["Right"],
#                         self.boutons[j]["negatif"][k]["Right"],
#                     )
#                     pg.draw.polygon(
#                         self.screen,
#                         colors["Bottom"],
#                         self.boutons[j]["negatif"][k]["Bottom"],
#                     )
#                     pg.draw.polygon(
#                         self.screen,
#                         colors["Left"],
#                         self.boutons[j]["negatif"][k]["Left"],
#                     )
#                     surf_txt = self.btnFont.render(
#                         self.boutons[j]["negatif"][k]["text"], True, colors["Top"]
#                     )
#                     rect_txt = surf_txt.get_rect()
#                     rect_txt.center = center
#                     self.screen.blit(surf_txt, rect_txt)
#         self.click = False
#
#     def isOnBtn(self, stat, signe, quantite):
#         rect = pg.Rect(self.boutons[stat][signe][quantite]["coords"])
#         if type(self.mouse) != bool and rect.collidepoint(self.mouse):
#             if self.click:
#                 self.isClicked(stat, signe, quantite)
#             return True
#         else:
#             return False
#
#     def isClicked(self, stat, signe, quantite):
#         if signe == "positif":
#             if stat == "PV":
#                 self.PVMana["PV"] += int(quantite)
#                 self.PVMana["mana"] -= int(quantite)
#             elif stat == "mana":
#                 self.PVMana["mana"] += int(quantite)
#                 self.PVMana["PV"] -= int(quantite)
#             elif stat == "force" or stat == "def" or stat == "crit":
#                 self.values["total"] += int(quantite)
#                 self.values[stat] += int(quantite)
#         elif signe == "negatif":
#             if stat == "PV":
#                 self.PVMana["PV"] -= int(quantite)
#                 self.PVMana["mana"] += int(quantite)
#             elif stat == "mana":
#                 self.PVMana["mana"] -= int(quantite)
#                 self.PVMana["PV"] += int(quantite)
#             elif stat == "force" or stat == "def" or stat == "crit":
#                 self.values["total"] -= int(quantite)
#                 self.values[stat] -= int(quantite)
#         self.click = False
#         self.genererJauge(True)
#
#     def update(self, Screen, x, y, Width, Height):
#         self.screen = Screen
#         self.x = x
#         self.y = y
#         self.width = Width
#         self.height = Height
#         self.positions = {
#             "PV": {
#                 "x": 0,
#                 "y": 0,
#                 "height": 0,
#                 "width": 0,
#                 "btnH": 0,
#                 "btnW": 0,
#                 "couleurRemplissage": (220, 20, 20),
#             },  # Red
#             "mana": {
#                 "x": 0,
#                 "y": 0,
#                 "height": 0,
#                 "width": 0,
#                 "btnH": 0,
#                 "btnW": 0,
#                 "couleurRemplissage": (20, 20, 220),
#             },  # Blue
#             "force": {
#                 "x": 0,
#                 "y": 0,
#                 "height": 0,
#                 "width": 0,
#                 "btnH": 0,
#                 "btnW": 0,
#                 "couleurRemplissage": (220, 140, 20),
#             },  # Orange
#             "def": {
#                 "x": 0,
#                 "y": 0,
#                 "height": 0,
#                 "width": 0,
#                 "btnH": 0,
#                 "btnW": 0,
#                 "couleurRemplissage": (20, 180, 20),
#             },  # Green
#             "crit": {
#                 "x": 0,
#                 "y": 0,
#                 "height": 0,
#                 "width": 0,
#                 "btnH": 0,
#                 "btnW": 0,
#                 "couleurRemplissage": (180, 20, 180),
#             },  # Purple/Magenta
#         }
#         self.rect = None
#         self.btnFont = None
#         self.topLeftW = None
#         self.topLeftH = None
#         self.fond = []
#         self.genererRects()
#
#     def setMouse(self, mouse):
#         self.mouse = mouse
#
#     def setClick(self, click):
#         self.click = click


# Initialisation des instances principales


class StatsModel :
    """Gère uniquement la logique métier des stats"""

    def __init__(self) :
        self.PVMana = {"max" : 3000, "PV" : 1500, "mana" : 1500}
        self.values = {"max" : 100, "total" : 3, "force" : 1, "def" : 1, "crit" : 1}

    def can_modify_stat(self, stat_type, operation, amount) :
        """Centralise toute la logique de validation"""
        if stat_type == "PV" :
            if operation == "add" :
                return self.PVMana["PV"] + amount <= self.PVMana["max"] - 250
            else :
                return self.PVMana["PV"] - amount >= 0

        elif stat_type == "mana" :
            if operation == "add" :
                return self.PVMana["mana"] + amount <= self.PVMana["max"] - 250
            else :
                return self.PVMana["mana"] - amount >= 0

        elif stat_type in ["force", "def"] :
            if operation == "add" :
                return self.values["total"] + amount <= self.values["max"] - 2
            else :
                return (self.values["total"] - amount >= 0 and
                        self.values[stat_type] - amount >= 1)

        elif stat_type == "crit" :
            if operation == "add" :
                return (self.values["total"] + amount <= self.values["max"] - 2 and
                        self.values["crit"] + amount <= 25)
            else :
                return (self.values["total"] - amount >= 0 and
                        self.values["crit"] - amount >= 1)
        return False

    def modify_stat(self, stat_type, operation, amount) :
        """Applique les modifications après validation"""
        if not self.can_modify_stat(stat_type, operation, amount) :
            return False

        modifier = amount if operation == "add" else -amount

        if stat_type == "PV" :
            self.PVMana["PV"] += modifier
            self.PVMana["mana"] -= modifier
        elif stat_type == "mana" :
            self.PVMana["mana"] += modifier
            self.PVMana["PV"] -= modifier
        else :
            self.values[stat_type] += modifier
            self.values["total"] += modifier

        return True


class Button :
    """Représente un bouton avec ses états et coordonnées 3D"""
    GOLD_COLORS = {
        "active" : {"Fond" : (40, 40, 40), "Top" : (255, 215, 0), "Right" : (184, 134, 11),
                    "Bottom" : (139, 69, 19), "Left" : (218, 165, 32)},
        "hovered" : {"Fond" : (40, 40, 40), "Top" : (139, 69, 19), "Right" : (218, 165, 32),
                     "Bottom" : (255, 215, 0), "Left" : (184, 134, 11)},
        "inactive" : {"Fond" : (40, 40, 40), "Top" : (120, 100, 50), "Right" : (80, 60, 30),
                      "Bottom" : (60, 40, 20), "Left" : (100, 80, 40)}
    }

    def __init__(self, coords, text, stat_type, operation, amount) :
        self.coords = coords  # (x, y, width, height)
        self.text = text
        self.stat_type = stat_type
        self.operation = operation
        self.amount = amount
        self.surfaces_3d = self._calculate_3d_surfaces()

    def _calculate_3d_surfaces(self) :
        """Calcule les surfaces 3D une seule fois"""
        x, y, w, h = self.coords
        return {
            "Top" : [(x - 2, y - 2), (x + w + 2, y - 2), (x + w, y), (x, y)],
            "Right" : [(x + w + 2, y - 2), (x + w + 2, y + h + 2), (x + w, y + h), (x + w, y)],
            "Bottom" : [(x + w + 2, y + h + 2), (x - 2, y + h + 2), (x, y + h), (x + w, y + h)],
            "Left" : [(x - 2, y + h + 2), (x - 2, y - 2), (x, y), (x, y + h)]
        }

    def get_state(self, model, mouse_pos) :
        """Détermine l'état actuel du bouton"""
        is_active = model.can_modify_stat(self.stat_type, self.operation, self.amount)
        is_hovered = is_active and self._is_mouse_over(mouse_pos)

        if is_hovered :
            return "hovered"
        elif is_active :
            return "active"
        else :
            return "inactive"

    def _is_mouse_over(self, mouse_pos) :
        """Vérifie si la souris survole le bouton"""
        if not mouse_pos or mouse_pos == False :
            return False
        x, y, w, h = self.coords
        mx, my = mouse_pos
        return x <= mx <= x + w and y <= my <= y + h

    def handle_click(self, model) :
        """Gère le clic sur le bouton"""
        return model.modify_stat(self.stat_type, self.operation, self.amount)


class StatBlock :
    """Représente un bloc complet : fond + jauge + boutons"""

    def __init__(self, name, fond_rect, positions_config) :
        self.name = name
        self.fond_rect = fond_rect
        self.positions = positions_config
        self.jauge_surfaces = self._calculate_jauge_3d()
        self.buttons = self._create_buttons()

    def _calculate_jauge_3d(self) :
        """Calcule les surfaces 3D de la jauge (identique à l'original)"""
        left_width = floor(self.positions["x"] - self.positions["width"] / 2)
        top_height = floor(self.positions["y"] - self.positions["height"] / 2)
        right_width = floor(self.positions["x"] + self.positions["width"] / 2)
        bottom_height = floor(self.positions["y"] + self.positions["height"] / 2)

        return {
            "base" : (left_width, top_height, self.positions["width"], self.positions["height"]),
            "remplissage_base" : (left_width + 1, top_height + 1, -1, self.positions["height"] - 1),
            "Top" : [(left_width - 5, top_height - 5), (right_width + 5, top_height - 5),
                     (right_width, top_height), (left_width, top_height)],
            "Right" : [(right_width + 5, top_height - 5), (right_width + 5, bottom_height + 5),
                       (right_width, bottom_height), (right_width, top_height)],
            "Bottom" : [(right_width + 5, bottom_height + 5), (left_width - 5, bottom_height + 5),
                        (left_width, bottom_height), (right_width, bottom_height)],
            "Left" : [(left_width - 5, bottom_height + 5), (left_width - 5, top_height - 5),
                      (left_width, top_height), (left_width, bottom_height)]
        }

    def _create_buttons(self) :
        """Crée les boutons positifs et négatifs avec le bon ordre"""
        buttons = {"positif" : {}, "negatif" : {}}

        # Valeurs selon le type de stat
        if self.name in ["PV", "mana"] :
            values = ["10", "50", "100"]
        else :  # force, def, crit
            values = ["1", "5", "10"]

        # Boutons positifs (à droite de la jauge)
        for i, value in enumerate(values) :
            left_width = floor(
                self.positions["x"] + self.positions["width"] / 2 +
                self.positions["btnW"] * i + (10 * (i + 1) + 5)
            )
            right_width = floor(
                self.positions["x"] + self.positions["width"] / 2 +
                self.positions["btnW"] * (i + 1) + (10 * (i + 1) + 5)
            )
            top_height = floor(self.positions["y"] - self.positions["btnH"] / 2)
            bottom_height = floor(self.positions["y"] + self.positions["btnH"] / 2)

            coords = (left_width, top_height, self.positions["btnW"], self.positions["btnH"])
            buttons["positif"][value] = Button(coords, "+" + value, self.name, "add", int(value))

        # Boutons négatifs (à gauche de la jauge, ordre: -10, -5, -1)
        for i, value in enumerate(values) :
            left_width = floor(
                self.positions["x"] - self.positions["width"] / 2 -
                self.positions["btnW"] * (i + 1) - (10 * (i + 1) + 5)
            )
            right_width = floor(
                self.positions["x"] - self.positions["width"] / 2 -
                self.positions["btnW"] * i - (10 * (i + 1) + 5)
            )
            top_height = floor(self.positions["y"] - self.positions["btnH"] / 2)
            bottom_height = floor(self.positions["y"] + self.positions["btnH"] / 2)

            coords = (left_width, top_height, self.positions["btnW"], self.positions["btnH"])
            buttons["negatif"][value] = Button(coords, "-" + value, self.name, "subtract", int(value))

        return buttons

    def get_jauge_percentage(self, model) :
        """Calcule le pourcentage de remplissage de la jauge"""
        if self.name == "PV" :
            return model.PVMana["PV"] / model.PVMana["max"]
        elif self.name == "mana" :
            return model.PVMana["mana"] / model.PVMana["max"]
        elif self.name == "force" :
            return model.values["force"] / 98
        elif self.name == "def" :
            return model.values["def"] / 98
        elif self.name == "crit" :
            return model.values["crit"] / 25
        return 0

    def get_current_value(self, model) :
        """Retourne la valeur actuelle à afficher"""
        if self.name in ["PV", "mana"] :
            return model.PVMana[self.name]
        else :
            return model.values[self.name]


class SelectStatsRefactored :
    """Version refactorisée maintenant les mêmes fonctionnalités"""

    def __init__(self, Screen, x, y, Width, Height) :
        self.screen = Screen
        self.x = x
        self.y = y
        self.width = Width
        self.height = Height

        # Modèle de données
        self.model = StatsModel()

        # Interface
        self.mouse = False
        self.click = False
        self.btnFont = None
        self.text_cache = {}

        # Génération de la structure
        self._generate_layout()

    def _generate_layout(self) :
        """Génère la disposition exacte de l'original"""
        # Calculs identiques à genererRects()
        self.topLeftW = self.x - int(self.width / 2)
        self.topLeftH = self.y - int(self.height / 2)
        self.rect = pg.Rect(self.topLeftW, self.topLeftH, self.width, self.height)

        # Calculs identiques à genererPos()
        stat_names = ["PV", "mana", "force", "def", "crit"]
        colors = [(220, 20, 20), (20, 20, 220), (220, 140, 20), (20, 180, 20), (180, 20, 180)]

        topLeftW = self.topLeftW + 40
        topLeftH = self.topLeftH + 40
        Width = self.width - 80
        Height = self.height - 80
        bloc = (Width - 40, floor((Height - 40) / len(stat_names)))

        self.fond = []
        self.stat_blocks = {}

        for i, (name, color) in enumerate(zip(stat_names, colors)) :
            # Fond du bloc
            fond_rect = pg.Rect(topLeftW + 20, topLeftH + 20 + bloc[1] * i, bloc[0], bloc[1])
            self.fond.append(fond_rect)

            # Configuration de position (identique à l'original)
            positions_config = {
                "x" : fond_rect.centerx,
                "y" : fond_rect.centery,
                "width" : floor(Width / 2),
                "height" : floor(Height / 24),
                "btnW" : floor(Height / 19),
                "btnH" : floor(Height / 19),
                "couleurRemplissage" : color
            }

            # Création du bloc stat
            self.stat_blocks[name] = StatBlock(name, fond_rect, positions_config)

        # Font pour les textes
        if self.btnFont is None :
            btn_size = list(self.stat_blocks.values())[0].positions["btnW"]
            self.btnFont = pg.font.SysFont("Arial", floor(btn_size * 0.5))

    def _get_cached_text(self, text, color) :
        """Cache les rendus de texte"""
        key = (str(text), color)
        if key not in self.text_cache :
            self.text_cache[key] = self.btnFont.render(str(text), True, color)
        return self.text_cache[key]

    def _invalidate_cache(self) :
        """Invalide le cache quand les valeurs changent"""
        self.text_cache.clear()

    def Afficher(self) :
        """Affichage identique à l'original mais optimisé"""
        # Fond principal
        pg.draw.rect(self.screen, (40, 40, 40), self.rect, border_radius = 20)

        for block in self.stat_blocks.values() :
            self._render_stat_block(block)

        self.click = False

    def _render_stat_block(self, block) :
        """Rendu d'un bloc stat complet"""
        # Jauge de base
        pg.draw.rect(self.screen, (10, 10, 10), block.jauge_surfaces["base"])
        pg.draw.polygon(self.screen, (100, 100, 100), block.jauge_surfaces["Top"])
        pg.draw.polygon(self.screen, (70, 70, 70), block.jauge_surfaces["Right"])
        pg.draw.polygon(self.screen, (60, 60, 60), block.jauge_surfaces["Bottom"])
        pg.draw.polygon(self.screen, (90, 90, 90), block.jauge_surfaces["Left"])

        # Remplissage de la jauge
        percentage = block.get_jauge_percentage(self.model)
        if percentage > 0 :
            base_x, base_y, _, base_h = block.jauge_surfaces["remplissage_base"]
            fill_width = floor(block.positions["width"] * percentage) - 1
            remplissage_rect = (base_x, base_y, fill_width, base_h)
            pg.draw.rect(self.screen, block.positions["couleurRemplissage"], remplissage_rect)

        # Texte de la jauge
        current_value = block.get_current_value(self.model)
        text_surface = self._get_cached_text(current_value, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.center = (block.positions["x"], block.positions["y"])
        self.screen.blit(text_surface, text_rect)

        # Boutons
        for button_dict in [block.buttons["positif"], block.buttons["negatif"]] :
            for button in button_dict.values() :
                self._render_button(button)

    def _render_button(self, button) :
        """Rendu d'un bouton avec état"""
        state = button.get_state(self.model, self.mouse)
        colors = Button.GOLD_COLORS[state]

        # Fond du bouton
        rect = pg.draw.rect(self.screen, colors["Fond"], button.coords)

        # Bordures 3D
        pg.draw.polygon(self.screen, colors["Top"], button.surfaces_3d["Top"])
        pg.draw.polygon(self.screen, colors["Right"], button.surfaces_3d["Right"])
        pg.draw.polygon(self.screen, colors["Bottom"], button.surfaces_3d["Bottom"])
        pg.draw.polygon(self.screen, colors["Left"], button.surfaces_3d["Left"])

        # Texte du bouton
        text_surface = self._get_cached_text(button.text, colors["Top"])
        text_rect = text_surface.get_rect()
        text_rect.center = rect.center
        self.screen.blit(text_surface, text_rect)

        # Gestion des clics
        if state != "inactive" and button._is_mouse_over(self.mouse) and self.click :
            if button.handle_click(self.model) :
                self._invalidate_cache()

    def setMouse(self, mouse) :
        self.mouse = mouse

    def setClick(self, click) :
        self.click = click

    def update(self, Screen, x, y, Width, Height) :
        """Mise à jour avec nouvelles dimensions"""
        self.screen = Screen
        self.x = x
        self.y = y
        self.width = Width
        self.height = Height
        self.btnFont = None
        self.text_cache.clear()
        self._generate_layout()


# Alias pour compatibilité
SelectStats = SelectStatsRefactored


posBouton = PosBoutons(screen)

# Création des boutons principaux
bouton_Jouer = Bouton((2, 4), 1, "Jouer", (0, 200, 0), "", posBouton)
bouton_quit = Bouton((6, 10), 2, "Quit", (255, 255, 255), "", posBouton)
bouton_stats = Bouton((5, 10), 2, "Stats", (255, 255, 255), "", posBouton)

slider = SelectStats(
    screen,
    screen.get_width() / 2,
    screen.get_height() / 2,
    screen.get_width() / 2,
    screen.get_height(),
)

# Variables et instances pour l'interface
histo = 1
barreDeVie = BarreDeVie("Banshee", 200)
BTNFR = BTNLangue(150, 150, 200, 50, "img")
menu = False
afficheStats = False

bgColor = (0, 0, 0)

# Boucle principale du jeu
while running:
    clock.tick(30)
    width = screen.get_width()
    height = screen.get_height()
    pg.draw.rect(screen, bgColor, [0, 0, width, height])
    bouton_Jouer.setsize((2, 4), posBouton)
    bouton_quit.setsize((6, 10), posBouton)
    bouton_stats.setsize((5, 10), posBouton)
    if menu:
        menu.setParams(
            floor(width / 6),
            floor(height / 6),
            floor(width / 3 * 2),
            floor(height / 3 * 2),
            screen,
        )

    for ev in pg.event.get():
        if ev.type == pg.QUIT:
            pg.quit()
            running = False
            sys.exit()
        if afficheStats:
            slider.setMouse(pg.mouse.get_pos())

        if ev.type == pg.MOUSEBUTTONDOWN:
            mouse = pg.mouse.get_pos()
            if afficheStats:
                slider.setClick(True)
                slider.setMouse(mouse)
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
                elif bouton_stats.isOn(mouse):
                    afficheStats = not afficheStats

        if ev.type == pg.KEYDOWN:
            if ev.key == pg.K_ESCAPE:
                if not menu:
                    menu = Menu.EscapeMenu(
                        floor(screen.get_width() / 6),
                        floor(screen.get_height() / 6),
                        floor(screen.get_width() / 3 * 2),
                        floor(screen.get_height() / 3 * 2),
                        screen,
                    )
                afficheMenu = True
            elif ev.key == pg.K_BACKSPACE:
                mana_uti = mana_uti[:-1]
            elif ev.key == pg.K_RETURN:
                selecMD = True

        if ev.type == pg.TEXTINPUT:
            mana_uti += ev.text

    barreDeVie.Affiche()
    if afficheStats:
        slider.Afficher()
    else:
        bouton_Jouer.affiche_bouton()
    bouton_stats.affiche_bouton()
    bouton_quit.affiche_bouton()
    if afficheMenu:
        res = menu.Afficher()
        if res["end"] == 1:
            newConfig = res["config"]
            menu.setActive(res["onglet"])
            screen = pg.display.set_mode(
                (int(newConfig["width"]), int(newConfig["height"]))
            )
            posBouton.setScreen(screen)
            slider.update(
                screen,
                screen.get_width() / 2,
                screen.get_height() / 2,
                screen.get_width() / 2 - 20,
                screen.get_height() - 40,
            )
        elif res["end"] == 2:
            afficheMenu = res["Menu"]

    pg.display.update()
