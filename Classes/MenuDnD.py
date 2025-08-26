import sys, pygame as pg, pygame.gfxdraw, config
from math import floor


class EscapeMenu:
    """
    Classe principale du menu d'échappement (menu pause/paramètres).
    
    Cette classe gère l'affichage du menu principal avec ses différents onglets
    (Général, Graphisme, Audio, Contrôles, Quitter) et les interactions utilisateur.
    
    Attributes:
        screen (pygame.Surface): Surface d'affichage pygame
        config (dict): Configuration actuelle du jeu chargée depuis le fichier config
        posBouton (PosBoutons): Instance pour la gestion des positions des boutons
        widthpos (int): Position horizontale du menu
        heightpos (int): Position verticale du menu
        width (int): Largeur du menu
        height (int): Hauteur du menu
        bouton (Bouton): Bouton "Appliquer" pour sauvegarder les modifications
        nav (NavMenu): Instance de navigation entre les onglets
        activeParam (str): Nom de l'onglet actuellement actif
    """
    
    def __init__(self, widthpos, heightpos, width, height, screen, boutonAppliquer, posBouton):
        """
        Initialise le menu d'échappement principal.
        
        Args:
            widthpos (int): Position x du coin supérieur gauche du menu
            heightpos (int): Position y du coin supérieur gauche du menu
            width (int): Largeur du menu
            height (int): Hauteur du menu
            screen (pygame.Surface): Surface d'affichage pygame
            boutonAppliquer (Bouton): Bouton pour appliquer les modifications
            posBouton (PosBoutons): Instance pour la gestion des positions
        """
        self.screen = screen
        self.config = config.charger_config()
        self.posBouton = posBouton
        self.widthpos = widthpos
        self.heightpos = heightpos
        self.width = width
        self.height = height
        self.bouton = boutonAppliquer
        self.nav = NavMenu(
            self.widthpos,
            self.heightpos,
            self.width,
            self.height,
            ["Général", "Graphisme", "Audio", "Contrôles", "Quitter"],
            self.screen,
            self.bouton,
        )
        self.activeParam = "Général"

    def Afficher(self):
        """
        Affiche le menu et gère la boucle d'événements principale.
        
        Cette méthode gère l'affichage du menu, les clics de souris sur les boutons,
        les changements d'onglets et les modifications de paramètres.
        
        Returns:
            dict: Dictionnaire contenant les informations de sortie :
                - "end": 1 pour appliquer les changements, 2 pour fermer le menu
                - "config": Configuration mise à jour (si end=1)
                - "onglet": Nom de l'onglet actif (si end=1)
                - "Menu": False pour fermer le menu (si end=2)
        """
        running = True
        while running:
            # Fond noir complet
            pg.draw.rect(
                self.screen,
                (0, 0, 0),
                (0, 0, self.screen.get_width(), self.screen.get_height()),
            )
            ongletActif = self.nav.getNameActive()
            self.bouton.setsize((6, 10), self.posBouton)
            
            # Fond du menu avec coins arrondis
            pg.draw.rect(
                self.screen,
                (80, 80, 80),
                [self.widthpos, self.heightpos, self.width, self.height],
                border_radius=20,
            )
            self.nav.Afficher(self.activeParam)
            self.bouton.affiche_bouton()

            for ev in pg.event.get():
                if ev.type == pg.QUIT:
                    pg.quit()
                    running = False
                    sys.exit()

                if ev.type == pg.MOUSEBUTTONDOWN:
                    mouse = pg.mouse.get_pos()
                    
                    # Clic sur le bouton Appliquer
                    if self.bouton.isOn(mouse) and not self.bouton.getstate() in [
                        "Down",
                        "Dead",
                    ]:
                        config.sauvegarder_config(self.config)
                        return {
                            "end": 1,
                            "config": self.config,
                            "onglet": self.nav.getNameActive(),
                        }
                    
                    # Clic sur les boutons d'onglets
                    btns = self.nav.getBoutons()
                    for loop in range(len(btns)):
                        if btns[loop].isOn(mouse):
                            self.setActive(btns[loop].getName())
                            ongletActif = self.nav.getNameActive()
                    
                    # Gestion spéciale pour l'onglet Graphisme
                    if ongletActif == "Graphisme":
                        AllCoords = self.nav.getSurfaceLignes("Graphisme")
                        for i in list(AllCoords.keys()):
                            WL, HL, WR, HR = AllCoords[i]
                            if WL <= mouse[0] <= WR and HL <= mouse[1] <= HR:
                                txt = i.split(" (")
                                x = txt[0].split(" x ")
                                self.config["width"] = x[0]
                                self.config["height"] = x[1]
                                return {
                                    "end": 1,
                                    "config": self.config,
                                    "onglet": self.nav.getNameActive(),
                                }

                if ev.type == pg.KEYDOWN:
                    if ev.key == pg.K_ESCAPE:
                        return {"end": 2, "Menu": False}
            pg.display.update()
        return None

    def setParams(self, widthpos, heightpos, width, height, screen, posBouton):
        """
        Met à jour les paramètres de taille et position du menu.
        
        Args:
            widthpos (int): Nouvelle position x
            heightpos (int): Nouvelle position y
            width (int): Nouvelle largeur
            height (int): Nouvelle hauteur
            screen (pygame.Surface): Nouvelle surface d'affichage
            posBouton (PosBoutons): Instance mise à jour pour les positions
        """
        self.screen = screen
        self.widthpos = widthpos
        self.heightpos = heightpos
        self.width = width
        self.height = height
        self.posBouton = posBouton
        self.nav.setParams(
            self.widthpos, self.heightpos, self.width, self.height, self.screen
        )

    def getBouton(self):
        """
        Récupère le bouton "Appliquer" du menu.
        
        Returns:
            Bouton: Instance du bouton "Appliquer"
        """
        return self.bouton

    def setActive(self, name):
        """
        Active un onglet spécifique du menu.
        
        Args:
            name (str): Nom de l'onglet à activer
        """
        self.nav.setActive(name)
        self.activeParam = name


class NavMenu:
    """
    Classe gérant la navigation entre les onglets du menu.
    
    Cette classe s'occupe de l'affichage des boutons d'onglets et de la gestion
    du contenu associé à chaque onglet.
    
    Attributes:
        screen (pygame.Surface): Surface d'affichage pygame
        boutonAppliquer (Bouton): Bouton "Appliquer" du menu principal
        widthtop (int): Position x de la zone de navigation
        heighttop (int): Position y de la zone de navigation
        width (int): Largeur de la zone de navigation
        height (int): Hauteur de la zone de navigation
        optionsNav (list): Liste des noms d'onglets disponibles
        btnWidth (int): Largeur calculée pour chaque bouton d'onglet
        btnHeight (int): Hauteur calculée pour chaque bouton d'onglet
        boutons (dict): Dictionnaire des boutons d'onglets créés
    """
    
    def __init__(
        self, widthtop, heighttop, width, height, options, screen, boutonAppliquer
    ):
        """
        Initialise le système de navigation du menu.
        
        Args:
            widthtop (int): Position x de la zone de navigation
            heighttop (int): Position y de la zone de navigation
            width (int): Largeur de la zone de navigation
            height (int): Hauteur de la zone de navigation
            options (list): Liste des noms d'onglets à créer
            screen (pygame.Surface): Surface d'affichage pygame
            boutonAppliquer (Bouton): Bouton "Appliquer" du menu principal
        """
        self.screen = screen
        self.boutonAppliquer = boutonAppliquer
        self.widthtop = widthtop + 20
        self.heighttop = heighttop + 20
        self.width = int(round(width - 40, 0) - (round(width - 40, 0) % 2))
        self.height = int(round(height - 40, 0) - (round(height - 40, 0) % 2))
        self.optionsNav = options
        self.btnWidth = int(
            round(self.width / len(self.optionsNav), 0)
            - (round(self.width / len(self.optionsNav), 0) % 10)
        )
        self.btnHeight = int(
            round(self.screen.get_height() * 0.055, 0)
            - (round(self.screen.get_height() * 0.055, 0) % 10)
        )
        self.boutons = {}
        self.generateBtn()

    def generateBtn(self):
        """
        Génère tous les boutons d'onglets avec leurs pages associées.
        
        Crée les instances MenuBouton pour chaque onglet et associe les pages
        de paramètres correspondantes (comme ParamsGraph pour l'onglet Graphisme).
        """
        self.boutons = {}
        for loop in range(len(self.optionsNav)):
            page = ""
            if self.optionsNav[loop] == "Graphisme":
                page = ParamsGraph(
                    self.screen,
                    self.widthtop,
                    self.heighttop + self.btnHeight + 10,
                    self.width,
                    self.height - (self.btnHeight + 10),
                    self.boutonAppliquer,
                )
            self.boutons[self.optionsNav[loop]] = MenuBouton(
                self.widthtop + 20 + self.btnWidth * loop,
                self.heighttop,
                self.btnWidth,
                self.btnHeight,
                self.optionsNav[loop],
                loop == 0,
                self.screen,
                page,
                self.boutonAppliquer,
            )

    def Afficher(self, name):
        """
        Affiche tous les boutons d'onglets avec l'onglet actif spécifié.
        
        Args:
            name (str): Nom de l'onglet à afficher comme actif
        """
        for loop in list(self.boutons.keys()):
            self.boutons[loop].Afficher(name)

    def getBoutons(self):
        """
        Récupère la liste de tous les boutons d'onglets.
        
        Returns:
            list: Liste des instances MenuBouton
        """
        res = []
        for loop in list(self.boutons.keys()):
            res.append(self.boutons[loop])
        return res

    def getNameActive(self):
        """
        Récupère le nom de l'onglet actuellement actif.
        
        Returns:
            str|None: Nom de l'onglet actif ou None si aucun n'est actif
        """
        for loop in list(self.boutons.keys()):
            if self.boutons[loop].getActive():
                return self.boutons[loop].getName()
        return None

    def setParams(self, widthtop, heighttop, width, height, screen):
        """
        Met à jour les paramètres de la zone de navigation.
        
        Args:
            widthtop (int): Nouvelle position x
            heighttop (int): Nouvelle position y
            width (int): Nouvelle largeur
            height (int): Nouvelle hauteur
            screen (pygame.Surface): Nouvelle surface d'affichage
        """
        self.screen = screen
        self.widthtop = widthtop + 20
        self.heighttop = heighttop + 20
        self.width = int(round(width - 40, 0) - (round(width - 40, 0) % 2))
        self.height = int(round(height - 40, 0) - (round(height - 40, 0) % 2))
        self.btnWidth = int(
            round(self.width / len(self.optionsNav), 0)
            - (round(self.width / len(self.optionsNav), 0) % 10)
        )
        self.btnHeight = int(
            round(self.screen.get_height() * 0.055, 0)
            - (round(self.screen.get_height() * 0.055, 0) % 10)
        )
        self.generateBtn()

    def getSurfaceLignes(self, text):
        """
        Récupère les surfaces cliquables des lignes d'un onglet spécifique.
        
        Args:
            text (str): Nom de l'onglet dont récupérer les surfaces
            
        Returns:
            dict: Dictionnaire des surfaces cliquables pour chaque ligne
        """
        return self.boutons[text].getSurfaceLignes()

    def setActive(self, name):
        """
        Active un onglet spécifique et désactive tous les autres.
        
        Args:
            name (str): Nom de l'onglet à activer
        """
        for i in list(self.boutons.keys()):
            self.boutons[i].setActive(False)
        self.boutons[name].setActive(True)


class MenuBouton:
    """
    Classe représentant un bouton d'onglet dans le menu de navigation.
    
    Chaque bouton correspond à un onglet et peut avoir une page de contenu associée.
    Le bouton change d'apparence selon son état (actif, survol, normal).
    
    Attributes:
        screen (pygame.Surface): Surface d'affichage pygame
        widthtop (int): Position x du bouton
        heighttop (int): Position y du bouton
        width (int): Largeur du bouton
        height (int): Hauteur du bouton
        text (str): Texte affiché sur le bouton
        active (bool): État actif du bouton
        font (pygame.font.Font): Police utilisée pour le texte
        page: Instance de la page de contenu associée (peut être "")
        boutonAppliquer (Bouton): Référence au bouton "Appliquer"
    """
    
    def __init__(
        self,
        widthtop,
        heighttop,
        width,
        height,
        text,
        active,
        screen,
        page,
        boutonAppliquer,
    ):
        """
        Initialise un bouton d'onglet du menu.
        
        Args:
            widthtop (int): Position x du coin supérieur gauche
            heighttop (int): Position y du coin supérieur gauche
            width (int): Largeur du bouton
            height (int): Hauteur du bouton
            text (str): Texte à afficher sur le bouton
            active (bool): État initial du bouton (actif ou non)
            screen (pygame.Surface): Surface d'affichage pygame
            page: Page de contenu associée à cet onglet
            boutonAppliquer (Bouton): Référence au bouton "Appliquer"
        """
        self.screen = screen
        self.widthtop = widthtop
        self.heighttop = heighttop
        self.width = width
        self.height = height
        self.text = text
        self.active = active
        self.font = pg.font.SysFont("Arial", int(self.height * 0.6))
        self.page = page
        self.boutonAppliquer = boutonAppliquer

    def Afficher(self, name):
        """
        Affiche le bouton d'onglet avec les effets visuels appropriés.
        
        Le bouton change d'apparence selon son état :
        - Actif : fond sombre avec ligne de soulignement claire
        - Survol : fond semi-transparent avec soulignement
        - Normal : fond semi-transparent simple
        
        Args:
            name (str): Nom de l'onglet actuellement sélectionné
        """
        if self.text == name:
            self.active = True
        else:
            self.active = False
        mouse = pg.mouse.get_pos()
        
        # Fond de base du bouton
        center_rect = pg.draw.rect(
            self.screen,
            (180, 180, 180),
            (self.widthtop, self.heighttop, self.width, self.height),
        )
        
        if self.active:
            # Bouton actif : fond sombre avec soulignement
            pg.gfxdraw.box(
                self.screen,
                (self.widthtop, self.heighttop, self.width, self.height),
                (0, 0, 0, 220),
            )
            pg.draw.rect(
                self.screen,
                (180, 180, 180),
                (self.widthtop, self.heighttop + self.height - 5, self.width, 5),
            )
            surf_texte = self.font.render(self.text, 1, (240, 240, 240))
        elif self.isOn(mouse):
            # Bouton en survol : effet de transparence avec soulignement
            pg.gfxdraw.box(
                self.screen,
                (self.widthtop, self.heighttop, self.width, self.height),
                (0, 0, 0, 160),
            )
            pg.gfxdraw.box(
                self.screen,
                (self.widthtop, self.heighttop + self.height - 5, self.width, 5),
                (180, 180, 180, 160),
            )
            surf_texte = self.font.render(self.text, 1, (200, 200, 200))
        else:
            # Bouton normal : fond semi-transparent
            pg.gfxdraw.box(
                self.screen,
                (self.widthtop, self.heighttop, self.width, self.height),
                (0, 0, 0, 160),
            )
            surf_texte = self.font.render(self.text, 1, (180, 180, 180))
        
        # Centrage et affichage du texte
        rect_texte = surf_texte.get_rect()
        rect_texte.center = center_rect.center
        self.screen.blit(surf_texte, rect_texte)
        
        # Affichage du contenu de la page si le bouton est actif
        if self.active and self.page != "":
            self.page.Afficher()

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

    def getWidth(self):
        """
        Récupère les limites horizontales du bouton.
        
        Returns:
            list: [position_gauche, position_droite]
        """
        return [int(self.widthtop), int(self.widthtop + self.width)]

    def getHeight(self):
        """
        Récupère les limites verticales du bouton.
        
        Returns:
            list: [position_haute, position_basse]
        """
        return [int(self.heighttop), int(self.heighttop + self.height)]

    def getActive(self):
        """
        Récupère l'état actif du bouton.
        
        Returns:
            bool: True si le bouton est actif, False sinon
        """
        return self.active

    def getName(self):
        """
        Récupère le nom/texte du bouton.
        
        Returns:
            str: Texte affiché sur le bouton
        """
        return self.text

    def getSurfaceLignes(self):
        """
        Récupère les surfaces cliquables de la page associée.
        
        Returns:
            dict: Surfaces cliquables de la page de contenu
        """
        return self.page.getSurfaceLignes()

    def setActive(self, active):
        """
        Modifie l'état actif du bouton.
        
        Args:
            active (bool): Nouvel état actif du bouton
        """
        self.active = active


class ParamsGraph:
    """
    Classe gérant la page de paramètres graphiques.
    
    Cette classe affiche la liste des résolutions disponibles et gère
    la sélection de la résolution d'écran.
    
    Attributes:
        screen (pygame.Surface): Surface d'affichage pygame
        boutonAppliquer (Bouton): Référence au bouton "Appliquer"
        widthtop (int): Position x de la zone de paramètres
        heighttop (int): Position y de la zone de paramètres
        width (int): Largeur de la zone de paramètres
        height (int): Hauteur de la zone de paramètres
        options (dict): Dictionnaire des résolutions disponibles
        active (str): Résolution actuellement sélectionnée
        blocOptHeight (float): Hauteur de chaque bloc d'option
        optHeight (int): Hauteur des lignes d'options
        lignes (list): Liste des instances LigneGraphisme créées
    """
    
    def __init__(self, screen, widthtop, heighttop, width, height, boutonAppliquer):
        """
        Initialise la page de paramètres graphiques.
        
        Args:
            screen (pygame.Surface): Surface d'affichage pygame
            widthtop (int): Position x de la zone de paramètres
            heighttop (int): Position y de la zone de paramètres
            width (int): Largeur de la zone de paramètres
            height (int): Hauteur de la zone de paramètres
            boutonAppliquer (Bouton): Référence au bouton "Appliquer"
        """
        self.screen = screen
        self.boutonAppliquer = boutonAppliquer
        self.widthtop = widthtop + 20
        self.heighttop = heighttop
        self.width = width - 40
        self.height = height - (
            self.boutonAppliquer.getheight()[1]
            - self.boutonAppliquer.getheight()[0]
            + 10
        )
        self.options = {
            "7680 x 4320 (8k)": [7680, 4320],
            "3840 x 2160 (4k)": [3840, 2160],
            "2560 x 1440 (2k)": [2560, 1440],
            "1920 x 1080 (1080p)": [1920, 1080],
            "1280 x 720 (720p)": [1280, 720],
        }
        temp = config.charger_config()
        self.active = temp["width"] + " x " + temp["height"]
        self.blocOptHeight = self.height / len(self.options)
        self.optHeight = int(
            round(self.screen.get_height() * 0.055, 0)
            + (round(self.screen.get_height() * 0.055, 0) % 2)
        )
        self.lignes = []
        self.generateLines()

    def generateLines(self):
        """
        Génère toutes les lignes d'options de résolution.
        
        Crée une instance LigneGraphisme pour chaque résolution disponible
        avec la position et la taille calculées automatiquement.
        """
        self.lignes = []
        for loop in range(len(self.options.keys())):
            heighttop = self.heighttop + self.blocOptHeight * loop
            self.lignes.append(
                LigneGraphisme(
                    list(self.options.keys())[loop],
                    self.widthtop,
                    heighttop,
                    self.width,
                    self.blocOptHeight,
                    self.optHeight,
                    self.screen,
                )
            )

    def Afficher(self):
        """
        Affiche toutes les lignes d'options de résolution.
        
        Chaque ligne est affichée avec l'indication de la résolution active.
        """
        for loop in self.lignes:
            loop.Afficher(self.active)

    def getSurfaceLignes(self):
        """
        Récupère les surfaces cliquables de toutes les lignes d'options.
        
        Returns:
            dict: Dictionnaire associant chaque nom de résolution à sa surface cliquable
        """
        res = {}
        for loop in self.lignes:
            res[loop.getKey()] = loop.getSurface()
        return res


class LigneGraphisme:
    """
    Classe représentant une ligne d'option de résolution graphique.
    
    Chaque ligne affiche une résolution disponible avec des effets visuels
    selon son état (sélectionnée, survolée, normale).
    
    Attributes:
        screen (pygame.Surface): Surface d'affichage pygame
        key (str): Nom de la résolution (ex: "1920 x 1080 (1080p)")
        widthtop (int): Position x de la ligne
        heighttop (float): Position y du bloc contenant la ligne
        width (int): Largeur de la ligne
        blocOptHeight (float): Hauteur du bloc d'option
        optHeight (int): Hauteur de la ligne d'option
        font (pygame.font.Font): Police utilisée pour le texte
        heighttopligne (int): Position y calculée de la ligne centrée
    """
    
    def __init__(
        self, key, widthtop, heighttop, width, blocOptHeight, optHeight, screen
    ):
        """
        Initialise une ligne d'option de résolution graphique.
        
        Args:
            key (str): Nom de la résolution à afficher
            widthtop (int): Position x de la ligne
            heighttop (float): Position y du bloc contenant la ligne
            width (int): Largeur de la ligne
            blocOptHeight (float): Hauteur du bloc d'option
            optHeight (int): Hauteur de la ligne d'option
            screen (pygame.Surface): Surface d'affichage pygame
        """
        self.screen = screen
        self.key = key
        self.widthtop = int(widthtop)
        self.heighttop = heighttop
        self.width = width
        self.blocOptHeight = blocOptHeight
        self.optHeight = optHeight
        self.font = pg.font.SysFont("Arial", int(self.optHeight * 0.6))
        self.heighttopligne = int(
            self.heighttop + (self.blocOptHeight - self.optHeight) / 2
        )

    def Afficher(self, active):
        """
        Affiche la ligne d'option avec les effets visuels appropriés.
        
        La ligne change d'apparence selon son état :
        - Active : couleurs plus vives, effet de sélection
        - Survol : couleurs intermédiaires
        - Normale : couleurs atténuées
        
        Args:
            active (str): Nom de la résolution actuellement active
        """
        mouse = pg.mouse.get_pos()
        
        # Détermination des couleurs selon l'état
        if active in self.key:
            colorLigne = (0, 0, 0, 180)
            colorText = (200, 200, 200)
            if (
                self.widthtop <= mouse[0] <= self.widthtop + self.width
                and self.heighttopligne
                <= mouse[1]
                <= self.heighttopligne + self.optHeight
            ):
                colorLigne = (0, 0, 0, 220)
        elif (
            self.widthtop <= mouse[0] <= self.widthtop + self.width
            and self.heighttopligne <= mouse[1] <= self.heighttopligne + self.optHeight
        ):
            colorLigne = (0, 0, 0, 160)
            colorText = (160, 160, 160)
        else:
            colorLigne = (0, 0, 0, 120)
            colorText = (120, 120, 120)

        # Fond de la ligne
        center_rect = pg.draw.rect(
            self.screen,
            (80, 80, 80),
            (self.widthtop, self.heighttopligne, self.width, self.optHeight + 1),
        )
        
        # Texte centré
        surf_texte = self.font.render(self.key, 1, colorText)
        rect_texte = surf_texte.get_rect()
        rect_texte.center = center_rect.center
        
        # Effets de bords arrondis avec des arcs
        radius = temp = int(self.optHeight / 2)
        while radius > 0:
            # Arc gauche
            pg.gfxdraw.arc(
                self.screen,
                self.widthtop + temp,
                self.heighttopligne + int(self.optHeight / 2),
                radius,
                90,
                -91,
                colorLigne,
            )
            # Arc droit
            pg.gfxdraw.arc(
                self.screen,
                self.widthtop + self.width - temp,
                self.heighttopligne + int(self.optHeight / 2),
                radius,
                -91,
                90,
                colorLigne,
            )
            radius -= 1
        
        # Fond central avec transparence
        pg.gfxdraw.box(
            self.screen,
            (
                self.widthtop + temp,
                self.heighttopligne,
                self.width - self.optHeight,
                self.optHeight + 1,
            ),
            colorLigne,
        )
        self.screen.blit(surf_texte, rect_texte)

    def getKey(self):
        """
        Récupère le nom de la résolution de cette ligne.
        
        Returns:
            str: Nom de la résolution (ex: "1920 x 1080 (1080p)")
        """
        return self.key

    def getSurface(self):
        """
        Récupère les coordonnées de la surface cliquable de cette ligne.
        
        Returns:
            list: [x_gauche, y_haut, x_droite, y_bas] de la zone cliquable
        """
        return [
            self.widthtop,
            self.heighttopligne,
            self.widthtop + self.width,
            self.heighttopligne + self.optHeight,
        ]
