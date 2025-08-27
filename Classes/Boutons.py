import pygame as pg
from math import floor


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

    def __init__(self, screen, background=None, option=None):
        """
        Initialise la classe PosBoutons.

        Args:
            screen (pygame.Surface): Surface d'affichage pygame
            background (tuple): Dimensions du rectangle de fond
        """
        self.screen = screen
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        self.option = option
        if background is not None:
            self.background = background
        else:
            self.background = (self.width, self.height)
        if self.option == "Menu":
            self.btnSizes = {
                "1": {"nbCol": 3, "nbLigne": 7, "sep": 30},
                "2": {"nbCol": 5, "nbLigne": 9, "sep": 20},
            }
        else:
            self.btnSizes = {
                "1": {"nbCol": 5, "nbLigne": 9, "sep": 30},
                "2": {"nbCol": 7, "nbLigne": 11, "sep": 20},
                "3": {"nbCol": 9, "nbLigne": 14, "sep": 10},
            }
        self.generateData()

    def generateData(self):
        """
        Génère les données de positionnement pour tous les types de boutons.
        """
        for btnSize in self.btnSizes:
            self.generateDataForPosGen(self.btnSizes[btnSize])

    def generateDataForPosGen(self, btnSize):
        """
        Génère les données de positionnement pour un type de bouton spécifique.

        Args:
            btnSize (dict): Configuration du type de bouton à traiter

        Returns:
            dict: Configuration mise à jour avec les positions calculées
        """
        btnSize["btnSizeW"] = int(
            floor(
                (
                    self.background[0]
                    - 24
                    - (btnSize["nbCol"] * btnSize["sep"] - btnSize["sep"])
                )
                / btnSize["nbCol"]
            )
            - (
                floor(
                    (
                        self.background[0]
                        - 24
                        - (btnSize["nbCol"] * btnSize["sep"] - btnSize["sep"])
                    )
                    / btnSize["nbCol"]
                )
                % 2
            )
        )
        btnSize["btnSizeH"] = int(
            floor(
                (
                    (
                        self.background[1]
                        - 24
                        - (btnSize["nbLigne"] * btnSize["sep"] - btnSize["sep"])
                    )
                    / btnSize["nbLigne"]
                )
                - (
                    floor(
                        (
                            (
                                self.background[1]
                                - 24
                                - (btnSize["nbLigne"] * btnSize["sep"] - btnSize["sep"])
                            )
                            / btnSize["nbLigne"]
                        )
                        % 2
                    )
                )
            )
        )
        return self.generatePositions(btnSize)

    def generatePositions(self, btnSize):
        """
        Calcule les positions centrales de chaque bouton dans la grille.

        Args:
            btnSize (dict): Configuration du type de bouton

        Returns:
            dict: Configuration mise à jour avec les positions des centres des boutons
        """
        screenW = btnSize["nbCol"] * btnSize["btnSizeW"] + (
            btnSize["nbCol"] * btnSize["sep"] - btnSize["sep"]
        )
        screenH = btnSize["nbLigne"] * btnSize["btnSizeH"] + (
            btnSize["nbLigne"] * btnSize["sep"] - btnSize["sep"]
        )
        difW = (self.width - screenW) / 2
        difH = (self.height - screenH) / 2
        for loop in range(btnSize["nbLigne"]):
            for i in range(btnSize["nbCol"]):
                rect = pg.Rect(
                    difW + btnSize["btnSizeW"] * i + btnSize["sep"] * i,
                    difH + btnSize["btnSizeH"] * loop + btnSize["sep"] * loop,
                    btnSize["btnSizeW"],
                    btnSize["btnSizeH"],
                )
                # if self.option is not None:
                #     color = (5 * i + 5 * loop, 5 * i + 5 * loop, 5 * i + 5 * loop)
                #     pg.draw.rect(self.screen, color, rect)
                btnSize[str(i) + "," + str(loop)] = rect.center
        # if self.option is not None:
        #     pg.display.flip()
        #     pg.time.delay(5000)
        return btnSize

    def setScreen(self, screen, background=None):
        """
        Met à jour l'écran de référence et recalcule toutes les positions.

        Args:
            screen (pygame.Surface): Nouvelle surface d'affichage
        """
        self.screen = screen
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        if background is not None:
            self.background = background
        else:
            self.background = (self.width, self.height)
        if self.option == "Menu":
            self.btnSizes = {
                "1": {"nbCol": 3, "nbLigne": 7, "sep": 30},
                "2": {"nbCol": 5, "nbLigne": 9, "sep": 20},
            }
        else:
            self.btnSizes = {
                "1": {"nbCol": 5, "nbLigne": 9, "sep": 30},
                "2": {"nbCol": 7, "nbLigne": 11, "sep": 20},
                "3": {"nbCol": 9, "nbLigne": 14, "sep": 10},
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
        try:
            self.btnSizes[type]
        except KeyError:
            print("Type du bouton non existant")
            print(KeyError)
        try:
            self.btnSizes[type][str(coordinates[0]) + "," + str(coordinates[1])]
        except KeyError:
            print("Coordonnées du bouton non existante")
            print(KeyError)
        width = self.btnSizes[type]["btnSizeW"]
        height = self.btnSizes[type]["btnSizeH"]
        coords = self.btnSizes[type][str(coordinates[0]) + "," + str(coordinates[1])]
        return width, height, coords

    def getScreen(self):
        return self.screen


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
            coordinates (tuple): Coordonnées (colonne, ligne) dans la grille (type 1 : 0-4 - 0-8, type 2 : 0-6 - 0-10, type 3 : 0-8 - 0-13)
            type (int): Type de bouton (1, 2, ou 3)
            texte (str): Texte à afficher sur le bouton
            color (tuple): Couleur du texte en RGB
            state (str): État initial du bouton ("", "Down", "Dead")
            posBouton (PosBoutons): Instance pour les calculs de position
        """
        self.type = type
        self.posBouton = posBouton
        self.screen = self.posBouton.getScreen()
        self.coordinatesXY = coordinates
        if self.type == 1:
            self.width, self.height, self.coordinates = posBouton.getDatas(
                str(self.type), coordinates
            )
        elif self.type == 2:
            self.width, self.height, self.coordinates = posBouton.getDatas(
                str(self.type), coordinates
            )
        elif self.type == 3:
            self.width, self.height, self.coordinates = posBouton.getDatas(
                str(self.type), coordinates
            )
        self.widthtop = int(self.coordinates[0] - self.width / 2)
        self.heighttop = int(self.coordinates[1] - self.height / 2)
        self.texte = texte
        self.font = pg.font.SysFont("Arial", int(self.height * 0.85 - 10))
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
            self.screen,
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
                self.screen,
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
                self.screen,
                colorTop,
                [
                    (self.widthtop, self.heighttop),
                    (self.widthtop + self.width, self.heighttop),
                    (self.widthtop + self.width - 5, self.heighttop + 5),
                    (self.widthtop + 5, self.heighttop + 5),
                ],
            )
            pg.draw.polygon(
                self.screen,
                colorRight,
                [
                    (self.widthtop + self.width - 5, self.heighttop + 5),
                    (self.widthtop + self.width, self.heighttop),
                    (self.widthtop + self.width, self.heighttop + self.height),
                    (self.widthtop + self.width - 5, self.heighttop + self.height - 5),
                ],
            )
            pg.draw.polygon(
                self.screen,
                colorBot,
                [
                    (self.widthtop + 5, self.heighttop + self.height - 5),
                    (self.widthtop + self.width - 5, self.heighttop + self.height - 5),
                    (self.widthtop + self.width, self.heighttop + self.height),
                    (self.widthtop, self.heighttop + self.height),
                ],
            )
            pg.draw.polygon(
                self.screen,
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
                self.screen,
                colorMid,
                [
                    self.widthtop + 5,
                    self.heighttop + 5,
                    self.width - 10,
                    self.height - 10,
                ],
            )
            self.screen.blit(surf_texte, rect_texte)

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

    def getpose(self):
        return {"coord": self.coordinates, "width": self.width, "height": self.height}

    def getstate(self):
        """
        Récupère l'état actuel du bouton.

        Returns:
            str: État du bouton ("", "Down", "Dead")
        """
        return self.state

    def getCoords(self):
        return self.coordinatesXY

    def getType(self):
        return self.type

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

    def setsize(self, coordinates: tuple[int, int], posBouton, type=None):
        """
        Met à jour la taille et la position du bouton.

        Args:
            coordinates (tuple): Nouvelles coordonnées (colonne, ligne) (type 1 : 0-4 - 0-8, type 2 : 0-6 - 0-10, type 3 : 0-8 - 0-13)
            type (int, optional): Nouveau type de bouton si différent
        """
        if type is not None:
            self.type = type
        self.posBouton = posBouton
        self.coordinatesXY = coordinates
        if self.type == 1:
            self.width, self.height, self.coordinates = self.posBouton.getDatas(
                str(self.type), coordinates
            )
        elif self.type == 2:
            self.width, self.height, self.coordinates = self.posBouton.getDatas(
                str(self.type), coordinates
            )
        elif self.type == 3:
            self.width, self.height, self.coordinates = self.posBouton.getDatas(
                str(self.type), coordinates
            )
        self.widthtop = int(self.coordinates[0] - self.width / 2)
        self.heighttop = int(self.coordinates[1] - self.height / 2)
        self.font = pg.font.SysFont("Arial", int(self.height * 0.85 - 10))
