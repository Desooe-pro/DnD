import random, os, sys, pygame_widgets, pygame as pg, config as config, Classes.MenuDnD as Menu
from math import floor

from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from pygame_widgets.progressbar import ProgressBar
from config import sauvegarder_config

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
loop = 0
def_type = ""
mana_uti = ""
temp = 0
afficheMenu = False

volume = dataConfig["volume"]
phrasesClass = config.load_phrases(dataConfig["langue"])

class PosBoutons:
    """
    Classe responsable du calcul et de la gestion des positions des boutons.
    
    Cette classe génère automatiquement les positions et tailles des boutons
    en fonction de la taille de l'écran et du type de bouton demandé.
    
    Attributes:
        screen (pygame.Surface): Surface d'affichage pygame
        width (int): Largeur de l'écran
        height (int): Hauteur de l'écran
        btnSizes (dict): Dictionnaire contenant les configurations pour chaque type de bouton
    """
    
    def __init__(self, screen):
        """
        Initialise la classe PosBoutons.
        
        Args:
            screen (pygame.Surface): Surface d'affichage pygame
        """
        self.screen = screen
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        self.btnSizes = {
            '1': {'nbCol': 5, 'nbLigne': 9, 'sep': 30},
            '2': {'nbCol': 7, 'nbLigne': 11, 'sep': 20},
            '3': {'nbCol': 9, 'nbLigne': 14, 'sep': 10}
        }
        self.generateData()

    def generateData(self):
        """
        Génère les données de positionnement pour tous les types de boutons.
        """
        self.generateDataForPosGen(self.btnSizes['1'])
        self.generateDataForPosGen(self.btnSizes['2'])
        self.generateDataForPosGen(self.btnSizes['3'])

    def generateDataForPosGen(self, btnSize):
        """
        Génère les données de positionnement pour un type de bouton spécifique.
        
        Args:
            btnSize (dict): Configuration du type de bouton à traiter
            
        Returns:
            dict: Configuration mise à jour avec les positions calculées
        """
        btnSize['btnSizeW'] = int(floor((self.width - 24 - (btnSize['nbCol'] * btnSize['sep'] - btnSize['sep'])) / btnSize['nbCol']) - (
                floor((self.width - 24 - (btnSize['nbCol'] * btnSize['sep'] - btnSize['sep'])) / btnSize['nbCol']) % 2))
        btnSize['btnSizeH'] = int(floor(((self.height - 24 - (btnSize['nbLigne'] * btnSize['sep'] - btnSize['sep'])) / btnSize['nbLigne']) - (
            floor(((self.height - 24 - (btnSize['nbLigne'] * btnSize['sep'] - btnSize['sep'])) / btnSize['nbLigne']) % 2))))
        return self.generatePositions(btnSize)

    def generatePositions(self, btnSize):
        """
        Calcule les positions centrales de chaque bouton dans la grille.
        
        Args:
            btnSize (dict): Configuration du type de bouton
            
        Returns:
            dict: Configuration mise à jour avec les positions des centres des boutons
        """
        screenW = btnSize['nbCol'] * btnSize['btnSizeW'] + (btnSize['nbCol'] * btnSize['sep'] - btnSize['sep'])
        screenH = btnSize['nbLigne'] * btnSize['btnSizeH'] + (btnSize['nbLigne'] * btnSize['sep'] - btnSize['sep'])
        difW = (self.width - screenW) / 2
        difH = (self.height - screenH) / 2
        for loop in range(btnSize['nbLigne']):
            for i in range(btnSize['nbCol']):
                rect = pg.Rect(difW + btnSize['btnSizeW'] * i + btnSize['sep'] * i, 
                              difH + btnSize['btnSizeH'] * loop + btnSize['sep'] * loop, 
                              btnSize['btnSizeW'], btnSize['btnSizeH'])
                btnSize[str(i) + "," + str(loop)] = rect.center
        return btnSize

    def setScreen(self, screen):
        """
        Met à jour l'écran de référence et recalcule toutes les positions.
        
        Args:
            screen (pygame.Surface): Nouvelle surface d'affichage
        """
        self.screen = screen
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        self.btnSizes = {
            '1': {'nbCol': 5, 'nbLigne': 9, 'sep': 30},
            '2': {'nbCol': 7, 'nbLigne': 11, 'sep': 20},
            '3': {'nbCol': 9, 'nbLigne': 14, 'sep': 10}
        }
        self.generateData()
    
    def getDatas(self, type: str, coordinates):
        """
        Récupère les données de position et de taille pour un bouton spécifique.
        
        Args:
            type (str): Type de bouton ('1', '2', ou '3')
            coordinates (tuple): Coordonnées (colonne, ligne) du bouton dans la grille
            
        Returns:
            tuple: (largeur, hauteur, coordonnées_du_centre)
        """
        width = self.btnSizes[type]['btnSizeW']
        height = self.btnSizes[type]['btnSizeH']
        coords = self.btnSizes[type][str(coordinates[0]) + ',' + str(coordinates[1])]
        return width, height, coords

class Bouton:
    """
    Classe représentant un bouton interactif avec effets visuels 3D.

    Cette classe gère l'affichage, l'état et les interactions d'un bouton
    avec des effets visuels de relief et de survol.

    Attributes:
        type (int): Type de bouton (1, 2, ou 3)
        posBouton (PosBoutons): Instance de PosBoutons pour les calculs de position
        width (int): Largeur du bouton
        height (int): Hauteur du bouton
        coordinates (tuple): Coordonnées du centre du bouton
        widthtop (int): Position x du coin supérieur gauche
        heighttop (int): Position y du coin supérieur gauche
        texte (str): Texte affiché sur le bouton
        font (pygame.font.Font): Police utilisée pour le texte
        color (tuple): Couleur du texte (RGB)
        state (str): État du bouton ("", "Down", "Dead")
    """

    def __init__(self, coordinates, type, texte, color, state, posBouton):
        """
        Initialise un nouveau bouton.

        Args:
            coordinates (tuple): Coordonnées (colonne, ligne) dans la grille
            type (int): Type de bouton (1, 2, ou 3)
            texte (str): Texte à afficher sur le bouton
            color (tuple): Couleur du texte en RGB
            state (str): État initial du bouton ("", "Down", "Dead")
            posBouton (PosBoutons): Instance pour les calculs de position
        """
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
        """
        Affiche le bouton avec ses effets visuels 3D selon son état actuel.

        Le bouton change d'apparence selon son état :
        - Normal : relief classique
        - Survol : effet d'éclairage inversé
        - Down : bouton enfoncé
        - Dead : bouton noir (inactif)
        """
        center_rect = pg.draw.rect(
            screen,
            (179, 179, 179),
            [self.widthtop + 5, self.heighttop + 5, self.width - 10, self.height - 10],
        )
        surf_texte = self.font.render(self.texte, 1, self.color)
        rect_texte = surf_texte.get_rect()
        rect_texte.center = center_rect.center
        mouse = pg.mouse.get_pos()

        # Couleurs par défaut (état normal)
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
            # État enfoncé
            if self.state == "Down":
                colorMid = (69, 69, 69)
                colorTop = (140, 140, 140)
                colorRight = (30, 30, 30)
                colorBot = (10, 10, 10)
                colorLeft = (120, 120, 120)

            # État survol
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

            # Dessin des bords 3D
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

            # Dessin du centre et du texte
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
        """
        Vérifie si la souris est positionnée sur le bouton.

        Args:
            mousePose (tuple): Position (x, y) de la souris

        Returns:
            bool: True si la souris est sur le bouton, False sinon
        """
        return (
                self.widthtop <= mousePose[0] <= self.widthtop + self.width
                and self.heighttop <= mousePose[1] <= self.heighttop + self.height
        )

    def getwidth(self):
        """
        Récupère les limites horizontales du bouton.

        Returns:
            list: [position_gauche, position_droite]
        """
        return [self.widthtop, self.widthtop + self.width]

    def getheight(self):
        """
        Récupère les limites verticales du bouton.

        Returns:
            list: [position_haute, position_basse]
        """
        return [self.heighttop, self.heighttop + self.height]

    def getstate(self):
        """
        Récupère l'état actuel du bouton.

        Returns:
            str: État du bouton ("", "Down", "Dead")
        """
        return self.state

    def setstate(self, state):
        """
        Modifie l'état du bouton.

        Args:
            state (str): Nouvel état ("", "Down", "Dead")
        """
        if state in ["", "Down", "Dead"]:
            self.state = state

    def settexte(self, texte):
        """
        Modifie le texte affiché sur le bouton.

        Args:
            texte (str): Nouveau texte à afficher
        """
        if type(texte) == str:
            self.texte = texte

    def setsize(self, coordinates, posBouton, type=None):
        """
        Met à jour la taille et la position du bouton.

        Args:
            coordinates (tuple): Nouvelles coordonnées (colonne, ligne)
            type (int, optional): Nouveau type de bouton si différent
        """
        if type is not None:
            self.type = type
        self.posBouton = posBouton
        if self.type == 1:
            self.width, self.height, self.coordinates = self.posBouton.getDatas(str(self.type), coordinates)
        elif self.type == 2:
            self.width, self.height, self.coordinates = self.posBouton.getDatas(str(self.type), coordinates)
        elif self.type == 3:
            self.width, self.height, self.coordinates = self.posBouton.getDatas(str(self.type), coordinates)
        self.widthtop = int(self.coordinates[0] - self.width / 2)
        self.heighttop = int(self.coordinates[1] - self.height / 2)
        self.font = pg.font.SysFont("Arial", int(self.width * 0.25 - 10))

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

# Initialisation des instances principales
posBouton = PosBoutons(screen)

# Création des boutons principaux
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

# Variables et instances pour l'interface
histo = 1
barreDeVie = BarreDeVie("Banshee", 200)
BTNFR = BTNLangue(150, 150, 200, 50, "img")
menu = Menu.EscapeMenu(
    floor(screen.get_width() / 6),
    floor(screen.get_height() / 6),
    floor(screen.get_width() / 3 * 2),
    floor(screen.get_height() / 3 * 2),
    screen,
    Bouton(
        (6, 10),
        3,
        "Appliquer",
        (255, 255, 255),
        "",
        posBouton
    ),
    posBouton
)
bgColor = (0, 0, 0)

# Boucle principale du jeu
while running:
    clock.tick(30)
    width = screen.get_width()
    height = screen.get_height()
    pg.draw.rect(screen, bgColor, [0, 0, width, height])
    bouton_Jouer.setsize((2, 4), posBouton)
    bouton_quit.setsize((6, 10), posBouton)
    menu.setParams(floor(width / 6), floor(height / 6), floor(width / 3 * 2), floor(height / 3 * 2), screen, posBouton)
    
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
