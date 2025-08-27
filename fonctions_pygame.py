import random, os, sys, pygame_widgets, pygame as pg, config as config, Classes.MenuDnD as Menu
from math import floor

from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from pygame_widgets.progressbar import ProgressBar
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
loop = 0
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


# Initialisation des instances principales
posBouton = PosBoutons(screen)

# Création des boutons principaux
bouton_Jouer = Bouton((2, 4), 1, "Jouer", (0, 200, 0), "", posBouton)
bouton_quit = Bouton((6, 10), 2, "Quit", (255, 255, 255), "", posBouton)

# Variables et instances pour l'interface
histo = 1
barreDeVie = BarreDeVie("Banshee", 200)
BTNFR = BTNLangue(150, 150, 200, 50, "img")
menu = False

bgColor = (0, 0, 0)

# Boucle principale du jeu
while running:
    clock.tick(30)
    width = screen.get_width()
    height = screen.get_height()
    pg.draw.rect(screen, bgColor, [0, 0, width, height])
    bouton_Jouer.setsize((2, 4), posBouton)
    bouton_quit.setsize((6, 10), posBouton)
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
