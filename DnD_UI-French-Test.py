import random, os, sys, pygame_widgets, pygame as pg, pygame.gfxdraw, config as config
from math import floor

from pygame import K_RETURN
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from pygame_widgets.progressbar import ProgressBar

os.environ["SDL_VIDEO_CENTERED"] = "1"

dataConfig = config.charger_config()
pg.init()
screen = pg.display.set_mode(
    (int(dataConfig["width"]), int(dataConfig["height"])), pg.RESIZABLE
)
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
global afficheMenu

volume = dataConfig["volume"]
phrasesClass = config.load_phrases(dataConfig["langue"])


class J:
    """
    Classe représentant un joueur dans le jeu de rôle.

    Cette classe gère les caractéristiques, les actions et l'interface utilisateur
    d'un personnage joueur, incluant les attaques, défenses et interactions.
    """

    def __init__(self, nom, pv, mana, precision, force, defence, id, posBouton, turn):
        """
                Initialise un nouveau joueur.

                Args:
                    nom (str): Le nom du personnage
                    pc (int): Points de compétence (Un jour ?)
                    pv (int): Points de vie
                    mana (int): Points de mana
                    force (int): Valeur de force
                    precision (int): Valeur de précision
                    defence (int): Valeur de défense
                    id (int): Identifiant unique du joueur
                    turn (int): Numéro du tour
                    posBouton (PosBoutons): Gestionnaire de positions des boutons
                """
        self.nom = nom
        self.posBouton = posBouton

        if self.nom == "N°0":
            self.nom = "GODMOD"
            self.pv = 10000
            self.mana = 5000
            self.force = 999
            self.prec = 100
            self.defence = 999
            self.id = id
            self.turn = False

        elif (
            force + precision + defence <= 100
            and 0 < precision <= 25
            and pv + mana <= 3000
        ):
            self.pv = pv
            self.pc = 1
            self.mana = mana
            self.force = force
            self.prec = precision
            self.defence = defence
            self.id = id
            self.turn = False

    def attack(self, bouton_quit, bouton_1, bouton_2, bouton_3, adv, lst_joueur):
        """
                Gère l'interface d'attaque du joueur.

                Affiche les options d'attaque disponibles et traite les interactions
                utilisateur pour sélectionner et exécuter une attaque.

                Returns:
                    str: Le type d'attaque sélectionné ou None si annulé
                """
        (
            bouton_1.settexte(phrasesClass["J"]["attack"]["attackType"][0]),
            bouton_2.settexte(phrasesClass["J"]["attack"]["attackType"][1]),
            bouton_3.settexte(phrasesClass["J"]["attack"]["attackType"][2]),
        )
        self.boite_info()
        running = True
        selecAtta = False
        selecMA = False
        atta_type = ""
        mana_uti = ""

        while running:
            clock.tick(60)
            pg.draw.rect(
                screen, (0, 0, 0), [0, 0, screen.get_width(), screen.get_height()]
            )
            bouton_quit.setsize((6, 10), self.posBouton)
            bouton_1.setsize((0, 13), self.posBouton)
            bouton_2.setsize((1, 13), self.posBouton)
            bouton_3.setsize((2, 13), self.posBouton)
            for ev in pg.event.get():
                if ev.type == pg.QUIT:
                    pg.quit()
                    running = False
                    sys.exit()

                if ev.type == pg.MOUSEBUTTONDOWN:
                    mouse = pg.mouse.get_pos()
                    if (
                        bouton_quit.isOn(mouse)
                        and bouton_quit.getstate() not in ["Down", "Dead"]
                    ):
                        pg.quit()
                        sys.exit()
                    elif (
                        bouton_1.isOn(mouse)
                    ):
                        if not selecAtta:
                            atta_type = phrasesClass["J"]["attack"]["attackType"][0]
                            selecMA = True
                    elif (
                        bouton_2.isOn(mouse)
                    ):
                        if not selecAtta:
                            atta_type = phrasesClass["J"]["attack"]["attackType"][1]
                    elif (
                        bouton_3.isOn(mouse)
                    ):
                        if not selecAtta:
                            atta_type = phrasesClass["J"]["attack"]["attackType"][2]

                if ev.type == pg.KEYDOWN:
                    if ev.key == pg.K_BACKSPACE:
                        mana_uti = mana_uti[:-1]
                    elif ev.key == pg.K_RETURN:
                        selecMA = True

                if ev.type == pg.TEXTINPUT:
                    mana_uti += ev.text  # Ajoute le texte Unicode directement

            bouton_quit.affiche_bouton()

            if not (selecAtta):
                selecAtta = self.selec_atta(
                    atta_type, selecAtta, bouton_1, bouton_2, bouton_3
                )
                if selecAtta:
                    for joueur in lst_joueur:
                        joueur.boite_info()
                    adv.boite_info()
                    pg.display.flip()
                    pg.time.delay(1500)

            if not (selecMA) and selecAtta:
                selecMA = self.mana_atta(mana_uti, selecMA)
                if selecMA:
                    for joueur in lst_joueur:
                        joueur.boite_info()
                    adv.boite_info()
                    pg.display.flip()
                    pg.time.delay(1500)

            if selecMA:
                pg.draw.rect(
                    screen, (0, 0, 0), [0, 0, screen.get_width(), screen.get_height()]
                )
                cp_crit = random.randint(1, 100)

                if 100 - (35 - self.prec) < cp_crit <= 100:
                    if mana_uti != 0:
                        self.affiche_texte(
                            phrasesClass["J"]["attack"]["fail"], lst_joueur, 2.5, adv
                        )
                        self.mana -= int(mana_uti)
                        pg.draw.rect(
                            screen,
                            (0, 0, 0),
                            [0, 0, screen.get_width(), screen.get_height()],
                        )
                        return 0

                    else:
                        self.affiche_texte(
                            phrasesClass["J"]["attack"]["fail"], lst_joueur, 2.5, adv
                        )
                        pg.draw.rect(
                            screen,
                            (0, 0, 0),
                            [0, 0, screen.get_width(), screen.get_height()],
                        )
                        return 0

                elif 1 <= cp_crit <= self.prec:
                    if atta_type == phrasesClass["J"]["attack"]["attackType"][0]:
                        degats = self.force * 7.5
                        self.affiche_texte(
                            phrasesClass["J"]["attack"]["crit"]["phy"][0]
                            + str(degats)
                            + phrasesClass["J"]["attack"]["crit"]["phy"][1],
                            lst_joueur,
                            2.5,
                            adv,
                        )
                        pg.draw.rect(
                            screen,
                            (0, 0, 0),
                            [0, 0, screen.get_width(), screen.get_height()],
                        )
                        return degats

                    elif atta_type == phrasesClass["J"]["attack"]["attackType"][1]:
                        degats = self.force * 2 * 1.5 + int(mana_uti) * 2.5 * 1.5
                        self.affiche_texte(
                            phrasesClass["J"]["attack"]["crit"]["reinf"][0]
                            + str(degats)
                            + phrasesClass["J"]["attack"]["crit"]["reinf"][1],
                            lst_joueur,
                            2.5,
                            adv,
                        )
                        self.mana -= int(mana_uti)
                        pg.draw.rect(
                            screen,
                            (0, 0, 0),
                            [0, 0, screen.get_width(), screen.get_height()],
                        )
                        return degats

                    elif atta_type == phrasesClass["J"]["attack"]["attackType"][2]:
                        degats = int(mana_uti) * 1.5
                        self.affiche_texte(
                            phrasesClass["J"]["attack"]["crit"]["mag"][0]
                            + str(degats)
                            + phrasesClass["J"]["attack"]["crit"]["mag"][1],
                            lst_joueur,
                            2.5,
                            adv,
                        )
                        self.mana -= int(mana_uti)
                        pg.draw.rect(
                            screen,
                            (0, 0, 0),
                            [0, 0, screen.get_width(), screen.get_height()],
                        )
                        return degats

                else:
                    if atta_type == phrasesClass["J"]["attack"]["attackType"][0]:
                        degats = self.force * 5
                        self.affiche_texte(
                            phrasesClass["J"]["attack"]["norm"]["phy"][0]
                            + str(degats)
                            + phrasesClass["J"]["attack"]["norm"]["phy"][1],
                            lst_joueur,
                            2.5,
                            adv,
                        )
                        pg.draw.rect(
                            screen,
                            (0, 0, 0),
                            [0, 0, screen.get_width(), screen.get_height()],
                        )
                        return degats

                    elif atta_type == phrasesClass["J"]["attack"]["attackType"][1]:
                        degats = self.force * 2 + int(mana_uti) * 2.5
                        self.affiche_texte(
                            phrasesClass["J"]["attack"]["norm"]["reinf"][0]
                            + str(degats)
                            + phrasesClass["J"]["attack"]["norm"]["reinf"][1],
                            lst_joueur,
                            2.5,
                            adv,
                        )
                        self.mana -= int(mana_uti)
                        pg.draw.rect(
                            screen,
                            (0, 0, 0),
                            [0, 0, screen.get_width(), screen.get_height()],
                        )
                        return degats

                    elif atta_type == phrasesClass["J"]["attack"]["attackType"][2]:
                        degats = int(mana_uti)
                        self.affiche_texte(
                            phrasesClass["J"]["attack"]["norm"]["mag"][0]
                            + str(degats)
                            + phrasesClass["J"]["attack"]["norm"]["mag"][1],
                            lst_joueur,
                            2.5,
                            adv,
                        )
                        self.mana -= int(mana_uti)
                        pg.draw.rect(
                            screen,
                            (0, 0, 0),
                            [0, 0, screen.get_width(), screen.get_height()],
                        )
                        return degats

            for joueur in lst_joueur:
                joueur.boite_info()
            adv.boite_info()
            pg.display.flip()
        return None

    def defences(
        self, degats, bouton_quit, bouton_1, bouton_2, bouton_3, adv, lst_joueur
    ):
        """
                Gère l'interface de défense du joueur.

                Affiche les options de défense disponibles et traite les interactions
                utilisateur pour sélectionner une stratégie défensive.

                Returns:
                    str: Le type de défense sélectionné ou None si annulé
                """
        (
            bouton_1.settexte(phrasesClass["J"]["defense"]["defenseType"][0]),
            bouton_2.settexte(phrasesClass["J"]["defense"]["defenseType"][1]),
            bouton_3.settexte(phrasesClass["J"]["defense"]["defenseType"][2]),
        )
        running = True
        selecDef = False
        selecMD = False
        def_type = ""
        mana_uti = ""

        while running:
            clock.tick(60)
            pg.draw.rect(
                screen, (0, 0, 0), [0, 0, screen.get_width(), screen.get_height()]
            )
            bouton_quit.setsize((6, 10), self.posBouton)
            bouton_1.setsize((0, 13), self.posBouton)
            bouton_2.setsize((1, 13), self.posBouton)
            bouton_3.setsize((2, 13), self.posBouton)
            for ev in pg.event.get():
                if ev.type == pg.QUIT:
                    pg.quit()
                    running = False
                    sys.exit()

                if ev.type == pg.MOUSEBUTTONDOWN:
                    mouse = pg.mouse.get_pos()
                    if (
                        bouton_quit.isOn(mouse)
                        and bouton_quit.getstate() not in ["Down", "Dead"]
                    ):
                        pg.quit()
                        sys.exit()
                    elif (
                        bouton_1.isOn(mouse)
                    ):
                        if not selecDef:
                            def_type = phrasesClass["J"]["defense"]["defenseType"][0]
                            selecMD = True
                    elif (
                        bouton_2.isOn(mouse)
                    ):
                        if not selecDef:
                            def_type = phrasesClass["J"]["defense"]["defenseType"][1]
                    elif (
                        bouton_3.isOn(mouse)
                    ):
                        if not selecDef:
                            def_type = phrasesClass["J"]["defense"]["defenseType"][2]

                if ev.type == pg.KEYDOWN:
                    if ev.key == pg.K_BACKSPACE:
                        mana_uti = mana_uti[:-1]
                    elif ev.key == pg.K_RETURN:
                        selecMD = True

                if ev.type == pg.TEXTINPUT:
                    mana_uti += ev.text  # Ajoute le texte Unicode directement

            bouton_quit.affiche_bouton()

            if not (selecDef):
                selecDef = self.selec_def(
                    def_type, selecDef, bouton_1, bouton_2, bouton_3
                )
                if selecDef:
                    for joueur in lst_joueur:
                        joueur.boite_info()
                    adv.boite_info()
                    pg.display.flip()
                    pg.time.delay(1500)

            if not (selecMD) and selecDef:
                selecMD = self.mana_atta(mana_uti, selecMD)
                if selecMD:
                    for joueur in lst_joueur:
                        joueur.boite_info()
                    adv.boite_info()
                    pg.display.flip()
                    pg.time.delay(1500)

            if selecMD:
                pg.draw.rect(
                    screen, (0, 0, 0), [0, 0, screen.get_width(), screen.get_height()]
                )
                def_crit = random.randint(1, 100)

                if 100 - (35 - self.prec) < def_crit <= 100:
                    if int(mana_uti) != 0:
                        self.affiche_texte(
                            phrasesClass["J"]["defense"]["fail"], lst_joueur, 2.5, adv
                        )
                        self.mana -= int(mana_uti)
                        self.pv -= degats

                    else:
                        self.affiche_texte(
                            phrasesClass["J"]["defense"]["fail"], lst_joueur, 2.5, adv
                        )
                        self.pv -= degats

                elif 1 <= def_crit <= self.prec:
                    if def_type == phrasesClass["J"]["defense"]["defenseType"][0]:
                        degats_def = self.defence * 2.5
                        self.affiche_texte(
                            phrasesClass["J"]["defense"]["crit"]["phy"][0]
                            + str(degats_def)
                            + phrasesClass["J"]["defense"]["crit"]["phy"][1],
                            lst_joueur,
                            2.5,
                            adv,
                        )

                        if degats_def <= degats:
                            self.pv -= degats - degats_def

                    elif def_type == phrasesClass["J"]["defense"]["defenseType"][1]:
                        degats_def = self.defence * 2.5 + int(mana_uti) * 3
                        self.affiche_texte(
                            phrasesClass["J"]["defense"]["crit"]["reinf"][0]
                            + str(degats_def)
                            + phrasesClass["J"]["defense"]["crit"]["reinf"][1],
                            lst_joueur,
                            2.5,
                            adv,
                        )
                        self.mana -= int(mana_uti)

                        if degats_def <= degats:
                            self.pv -= degats - degats_def

                    elif def_type == phrasesClass["J"]["defense"]["defenseType"][2]:
                        degats_def = int(mana_uti) * 2.5
                        self.affiche_texte(
                            phrasesClass["J"]["defense"]["crit"]["mag"][0]
                            + str(degats_def)
                            + phrasesClass["J"]["defense"]["crit"]["mag"][1],
                            lst_joueur,
                            2.5,
                            adv,
                        )
                        self.mana -= int(mana_uti)

                        if degats_def <= degats:
                            self.pv -= degats - degats_def

                else:
                    if def_type == phrasesClass["J"]["defense"]["defenseType"][0]:
                        degats_def = self.defence * 2.5
                        self.affiche_texte(
                            phrasesClass["J"]["defense"]["norm"]["phy"][0]
                            + str(degats_def)
                            + phrasesClass["J"]["defense"]["norm"]["phy"][1],
                            lst_joueur,
                            2.5,
                            adv,
                        )

                        if degats_def <= degats:
                            self.pv -= degats - degats_def

                    elif def_type == phrasesClass["J"]["defense"]["defenseType"][1]:
                        degats_def = self.defence * 1.5 + int(mana_uti) * 2
                        self.affiche_texte(
                            phrasesClass["J"]["defense"]["norm"]["reinf"][0]
                            + str(degats_def)
                            + phrasesClass["J"]["defense"]["norm"]["reinf"][1],
                            lst_joueur,
                            2.5,
                            adv,
                        )
                        self.mana -= int(mana_uti)

                        if degats_def <= degats:
                            self.pv -= degats - degats_def

                    elif def_type == phrasesClass["J"]["defense"]["defenseType"][2]:
                        degats_def = int(mana_uti) * 1.5
                        self.affiche_texte(
                            phrasesClass["J"]["defense"]["norm"]["mag"][0]
                            + str(degats_def)
                            + phrasesClass["J"]["defense"]["norm"]["mag"][1],
                            lst_joueur,
                            2.5,
                            adv,
                        )
                        self.mana -= int(mana_uti)

                        if degats_def <= degats:
                            self.pv -= degats - degats_def

                running = False
                pg.draw.rect(
                    screen, (0, 0, 0), [0, 0, screen.get_width(), screen.get_height()]
                )

            for joueur in lst_joueur:
                joueur.boite_info()
            adv.boite_info()
            pg.display.flip()

    def selec_atta(self, atta_type, selecAtta, bouton_1, bouton_2, bouton_3):
        """
                Sélectionne une attaque spécifique par son numéro.

                Args:
                    num (int): Numéro de l'attaque à sélectionner (1-3)

                Returns:
                    str: Le type d'attaque correspondant au numéro
                """
        bouton_1.affiche_bouton(), bouton_2.affiche_bouton(), bouton_3.affiche_bouton()
        if not selecAtta:
            if atta_type == "":
                screen.blit(
                    atkfont.render(
                        phrasesClass["J"]["selection"]["atk"][0], True, (255, 255, 255)
                    ),
                    (int(screen.get_width() / 5), 15),
                )
                return None
            else:
                screen.blit(
                    atkfont.render(
                        phrasesClass["J"]["selection"]["atk"][1] + str(atta_type),
                        True,
                        (255, 255, 255),
                    ),
                    (int(screen.get_width() / 5), 15),
                )
                selecAtta = True
                return selecAtta
        return None

    def selec_def(self, def_type, selecDef, bouton_1, bouton_2, bouton_3):
        """
                Sélectionne une défense spécifique par son numéro.

                Args:
                    num (int): Numéro de la défense à sélectionner (1-3)

                Returns:
                    str: Le type de défense correspondant au numéro
                """
        bouton_1.affiche_bouton(), bouton_2.affiche_bouton(), bouton_3.affiche_bouton()
        if not selecDef:
            if def_type == "":
                screen.blit(
                    atkfont.render(
                        phrasesClass["J"]["selection"]["def"][0], True, (255, 255, 255)
                    ),
                    (int(screen.get_width() / 5), 15),
                )
                return None
            else:
                screen.blit(
                    atkfont.render(
                        phrasesClass["J"]["selection"]["def"][1] + str(def_type),
                        True,
                        (255, 255, 255),
                    ),
                    (int(screen.get_width() / 5), 15),
                )
                selecDef = True
                return selecDef
        return None

    def mana_atta(self, mana_uti, selecMD):
        """
                Calcule et déduit le coût en mana d'une attaque.

                Args:
                    type_atta (str): Type d'attaque effectuée

                Returns:
                    bool: True si le joueur a suffisamment de mana, False sinon
                """
        if not selecMD:
            screen.blit(
                atkfont.render(
                    phrasesClass["J"]["selection"]["mana"][0] + str(mana_uti),
                    True,
                    (255, 255, 255),
                ),
                (int(screen.get_width() / 5), 15),
            )
            return None
        else:
            screen.blit(
                atkfont.render(
                    phrasesClass["J"]["selection"]["mana"][1][0]
                    + str(mana_uti)
                    + phrasesClass["J"]["selection"]["mana"][1][1],
                    True,
                    (255, 255, 255),
                ),
                (int(screen.get_width() / 5), 15),
            )
            selecMD = True
            return selecMD

    def boite_info(self):
        """
        Affiche la boîte d'informations du joueur sur le côté gauche de l'écran.

        Cette méthode dessine une interface graphique complète montrant :
        - Le nom du personnage
        - Les points de vie actuels
        - Toutes les statistiques (Force, Défense, Mana, Précision)
        - Un indicateur visuel si c'est le tour du joueur (bordure verte)

        La boîte est positionnée verticalement en fonction de l'ID du joueur
        pour permettre l'affichage de plusieurs joueurs simultanément.

        Note:
            Utilise les variables globales screen, vsmallfont et phrasesClass.
            La position est calculée dynamiquement selon self.id.
        """
        # Dessiner la bordure verte si c'est le tour du joueur
        if self.turn:
            pg.draw.rect(
                screen,
                (0, 255, 0),  # Vert pour indiquer le tour actif
                [13, 13 + (120 * (self.id - 1) + 20 * (self.id - 1)), 229, 119],
            )

        # Dessiner les couches de fond de la boîte (effet de profondeur)
        pg.draw.rect(
            screen,
            (255, 255, 255),  # Couche blanche externe
            [15, 15 + (120 * (self.id - 1) + 20 * (self.id - 1)), 225, 115],
        )
        pg.draw.rect(
            screen,
            (200, 200, 200),  # Couche grise claire
            [18, 18 + (120 * (self.id - 1) + 20 * (self.id - 1)), 219, 109],
        )
        pg.draw.rect(
            screen,
            (170, 170, 170),  # Couche grise moyenne
            [18, 21 + (120 * (self.id - 1) + 20 * (self.id - 1)), 216, 106],
        )
        pg.draw.rect(
            screen,
            (130, 130, 130),  # Couche grise foncée (fond principal)
            [21, 21 + (120 * (self.id - 1) + 20 * (self.id - 1)), 213, 103],
        )

        # Dessiner les lignes de séparation
        pg.draw.rect(
            screen,
            (50, 50, 50),  # Ligne horizontale de séparation
            [40, 52 + (120 * (self.id - 1) + 20 * (self.id - 1)), 160, 1],
        )
        pg.draw.rect(
            screen,
            (50, 50, 50),  # Ligne verticale de séparation pour les stats
            [122, 75 + (120 * (self.id - 1) + 20 * (self.id - 1)), 1, 40],
        )

        # Calculer la largeur du texte des PV pour l'alignement à droite
        retirer = vsmallfont.render(
            str(self.pv) + phrasesClass["J"]["infoBox"]["pv"], 1, (255, 255, 255)
        ).get_rect()[2]

        # Définir les positions pour l'alignement du texte
        pos_0 = 165 + retirer  # Position pour les PV (alignement à droite)
        pos_1 = 116  # Position pour les stats de gauche
        pos_2 = 218  # Position pour les stats de droite

        # Afficher le nom du personnage (coin supérieur gauche)
        screen.blit(
            vsmallfont.render(self.nom, 1, (255, 255, 255)),
            [25, 30 + (120 * (self.id - 1) + 20 * (self.id - 1)), 50, 25],
        )

        # Afficher les points de vie (coin supérieur droit, aligné à droite)
        screen.blit(
            vsmallfont.render(
                str(self.pv) + phrasesClass["J"]["infoBox"]["pv"], 1, (255, 255, 255)
            ),
            [
                pos_0 - retirer,  # Alignement à droite
                30 + (120 * (self.id - 1) + 20 * (self.id - 1)),
                retirer,
                25,
            ],
        )

        # Afficher le titre "Stats"
        screen.blit(
            vsmallfont.render(
                phrasesClass["J"]["infoBox"]["stats"], 1, (255, 255, 255)
            ),
            [25, 55 + (120 * (self.id - 1) + 20 * (self.id - 1)), 50, 25],
        )

        # Afficher les labels des statistiques (colonne de gauche)
        screen.blit(
            vsmallfont.render(
                phrasesClass["J"]["infoBox"]["strength"], 1, (255, 255, 255)
            ),
            [25, 75 + (120 * (self.id - 1) + 20 * (self.id - 1)), 50, 25],
        )
        screen.blit(
            vsmallfont.render(
                phrasesClass["J"]["infoBox"]["mana"], 1, (255, 255, 255)
            ),
            [25, 95 + (120 * (self.id - 1) + 20 * (self.id - 1)), 50, 25],
        )

        # Afficher les labels des statistiques (colonne de droite)
        screen.blit(
            vsmallfont.render(
                phrasesClass["J"]["infoBox"]["defense"], 1, (255, 255, 255)
            ),
            [127, 75 + (120 * (self.id - 1) + 20 * (self.id - 1)), 50, 25],
        )
        screen.blit(
            vsmallfont.render(
                phrasesClass["J"]["infoBox"]["precision"], 1, (255, 255, 255)
            ),
            [127, 95 + (120 * (self.id - 1) + 20 * (self.id - 1)), 50, 25],
        )

        # Afficher les valeurs des statistiques (alignées à droite dans leurs colonnes)
        # Force (colonne de gauche)
        retirer = vsmallfont.render(str(self.force), 1, (255, 255, 255)).get_rect()[2]
        screen.blit(
            vsmallfont.render(str(self.force), 1, (255, 255, 255)),
            [
                pos_1 - retirer,  # Alignement à droite dans la colonne gauche
                75 + (120 * (self.id - 1) + 20 * (self.id - 1)),
                retirer,
                25,
            ],
        )

        # Défense (colonne de droite)
        screen.blit(
            vsmallfont.render(str(self.defence), 1, (255, 255, 255)),
            [
                pos_2 - retirer + 10,  # Alignement à droite dans la colonne droite
                75 + (120 * (self.id - 1) + 20 * (self.id - 1)),
                retirer,
                25,
            ],
        )

        # Mana (colonne de gauche)
        retirer = vsmallfont.render(str(self.mana), 1, (255, 255, 255)).get_rect()[2]
        screen.blit(
            vsmallfont.render(str(self.mana), 1, (255, 255, 255)),
            [
                pos_1 - retirer,  # Alignement à droite dans la colonne gauche
                95 + (120 * (self.id - 1) + 20 * (self.id - 1)),
                retirer,
                25,
            ],
        )

        # Précision (colonne de droite, avec symbole %)
        retirer = vsmallfont.render(
            str(self.prec) + "%", 1, (255, 255, 255)
        ).get_rect()[2]
        screen.blit(
            vsmallfont.render(str(self.prec) + "%", 1, (255, 255, 255)),
            [
                pos_2 - retirer + 10,  # Alignement à droite dans la colonne droite
                95 + (120 * (self.id - 1) + 20 * (self.id - 1)),
                retirer,
                25,
            ],
        )


    def affiche_texte(self, texte, liste_joueur, temps, adv):
        """
                Affiche un texte à l'écran avec une couleur spécifiée.

                Args:
                    texte (str): Le texte à afficher
                    color (tuple): Couleur RGB du texte
        """
        bouton_quit = Bouton(
            (6, 10),
            2,
            "Quit",
            (255, 255, 255),
            "",
            self.posBouton
        )
        duree = temps * 60
        while duree > 0:
            clock.tick(60)
            pg.draw.rect(
                screen, (0, 0, 0), [0, 0, screen.get_width(), screen.get_height()]
            )
            bouton_quit.setsize((6, 10), self.posBouton)
            for ev in pg.event.get():
                if ev.type == pg.QUIT:
                    pg.quit()
                    duree = 0
                    sys.exit()

                if ev.type == pg.MOUSEBUTTONDOWN:
                    mouse = pg.mouse.get_pos()
                    if (
                        bouton_quit.isOn(mouse)
                        and bouton_quit.getstate() not in ["Down", "Dead"]
                    ):
                        pg.quit()
                        duree = 0
                        sys.exit()

            screen.blit(
                atkfont.render(texte, 1, (255, 255, 255)),
                [int(screen.get_width() / 5), 100],
            )
            for joueur in liste_joueur:
                joueur.boite_info()
            adv.boite_info()
            bouton_quit.affiche_bouton()
            pg.display.flip()
            duree -= 1

    def getforce(self):
        return self.force

    def getmana(self):
        return self.mana

    def getpv(self):
        return self.pv

    def getnom(self):
        return self.nom

    def getid(self):
        return self.id

    def setpv(self, pv):
        self.pv = pv

    def setpc(self, pc):
        self.pc = pc

    def setmana(self, mana):
        self.mana = mana

    def setforce(self, force):
        self.force = force

    def setturn(self, turn):
        self.turn = turn


class Banshee:
    """
        Classe représentant un ennemi de type Banshee.

        Ennemi avec des capacités spéciales et une IA pour combattre
        automatiquement contre les joueurs.
    """
    def __init__(self, liste_joueur, posBouton):
        """
                Initialise une nouvelle Banshee.

                Attributs:
                    nom (str): Nom de la Banshee
                    pv (int): Points de vie
                    force (int): Valeur de force
                    mana (int): Points de mana
                    defence (int): Valeur de défense
                    prec (int): Valeur de précision
                    turn (int): Numéro du tour
                    posBouton (PosBoutons): Gestionnaire de positions des boutons
        """
        self.nom = phrasesClass["banshee"]["Name"]
        self.posBouton = posBouton

        if len(liste_joueur) > 1:
            self.pv = self.pvbase = int(
                2500 * (len(liste_joueur) * (1 + (len(liste_joueur) - 1) * 0.25))
            )

        else:
            self.pv = self.pvbase = 2500

        self.force = 0
        self.mana = 10000
        self.defence = 0
        self.prec = 10
        self.turn = True
        self.BarreDeVie = BarreDeVie(300, self.nom, self.pv, self.pvbase)

    def choose_target(self, liste_joueur):
        """
                Choisit automatiquement une cible parmi les joueurs.

                Args:
                    liste_joueur (list): Liste des joueurs disponibles

                Returns:
                    J: Le joueur ciblé
        """
        if not liste_joueur:
            print(phrasesClass["banshee"]["attack"]["noTarget"])
            return None

        target = liste_joueur[0]

        for joueur in liste_joueur:
            if joueur.pv > target.pv:
                target = joueur.nom
        return target

    def attack(self, joueur_att, liste_joueur):
        att_banshee = random.randint(1, 100)
        pg.draw.rect(screen, (0, 0, 0), [0, 0, screen.get_width(), screen.get_height()])
        self.affiche_texte(
            phrasesClass["banshee"]["attack"]["prepare"], liste_joueur, 3
        )
        pg.draw.rect(screen, (0, 0, 0), [0, 0, screen.get_width(), screen.get_height()])

        if 0 < att_banshee <= 60:
            degats = 250
            self.affiche_texte(
                phrasesClass["banshee"]["attack"]["norm"]["bas"][0]
                + str(joueur_att.getnom())
                + phrasesClass["banshee"]["attack"]["norm"]["bas"][1]
                + str(degats)
                + phrasesClass["banshee"]["attack"]["norm"]["bas"][2],
                liste_joueur,
                4,
            )
            self.mana -= 150
            return degats, att_banshee

        if 60 < att_banshee <= 95:
            degats = 500
            self.affiche_texte(
                phrasesClass["banshee"]["attack"]["norm"]["moy"][0]
                + str(joueur_att.getnom())
                + phrasesClass["banshee"]["attack"]["norm"]["moy"][1]
                + str(degats)
                + phrasesClass["banshee"]["attack"]["norm"]["moy"][2],
                liste_joueur,
                4,
            )
            self.mana -= 375
            return degats, att_banshee

        if 95 < att_banshee <= 100 and self.pv <= 1500:
            degats = self.pv
            self.affiche_texte(
                phrasesClass["banshee"]["attack"]["norm"]["haut"][0]
                + str(degats)
                + phrasesClass["banshee"]["attack"]["norm"]["haut"][1],
                liste_joueur,
                4,
            )
            self.pv = 0
            self.mana -= 500

            for joueur in liste_joueur:
                joueur.pv -= degats

            return 0, att_banshee

        if 95 < att_banshee <= 100:
            degats = 750
            self.affiche_texte(
                phrasesClass["banshee"]["attack"]["norm"]["noHaut"][0]
                + str(degats)
                + phrasesClass["banshee"]["attack"]["norm"]["noHaut"][1],
                liste_joueur,
                4,
            )
            self.pv -= 125
            self.mana -= 375

            for joueur in liste_joueur:
                joueur.pv -= degats

            return 0, att_banshee
        return None

    def defences(self, degats, liste_joueur):
        def_crit = random.randint(1, 100)
        if 100 - (35 - self.prec) < def_crit <= 100:
            self.affiche_texte(
                phrasesClass["banshee"]["defense"]["fail"][0]
                + str(degats + 50)
                + phrasesClass["banshee"]["defense"]["fail"][1],
                liste_joueur,
                4,
            )
            self.pv -= degats + 50

        elif degats != 0:
            self.affiche_texte(
                phrasesClass["banshee"]["defense"]["succes"][0]
                + str(degats - 50)
                + phrasesClass["banshee"]["defense"]["succes"][1],
                liste_joueur,
                4,
            )
            self.pv -= degats - 50

        for joueur in liste_joueur:
            joueur.boite_info()
        self.boite_info()
        pg.display.flip()
        pg.time.delay(3000)

    def boite_info(self):
        """
        Affiche la boîte d'informations de la Banshee sur le côté droit de l'écran.

        Cette méthode dessine une interface graphique complète montrant :
        - Le nom de la Banshee
        - Les points de vie actuels
        - Toutes les statistiques (Force, Défense, Mana, Précision)
        - Un indicateur visuel si c'est le tour de la Banshee (bordure verte)
        - Une barre de vie graphique via self.BarreDeVie

        La boîte est positionnée à droite de l'écran avec un alignement
        calculé dynamiquement selon la largeur de l'écran.

        Note:
            Utilise les variables globales screen, vsmallfont et phrasesClass.
            Met à jour et affiche la barre de vie à la fin.
        """
        # Calculer la largeur du texte des PV pour l'alignement
        retirer = vsmallfont.render(
            str(self.pv) + phrasesClass["banshee"]["infoBox"]["pv"], 1, (255, 255, 255)
        ).get_rect()[2]

        # Définir les positions relatives à la largeur d'écran (côté droit)
        pos_0 = screen.get_width() + retirer  # Position de référence pour PV
        pos_1 = screen.get_width() - 20  # Position de base côté droit
        pos_2 = screen.get_width()  # Bord droit de l'écran

        # Dessiner la bordure verte si c'est le tour de la Banshee
        if self.turn:
            pg.draw.rect(screen, (0, 255, 0), [pos_1 - 13 - 219, 13, 239, 129])

        # Dessiner les couches de fond de la boîte (effet de profondeur)
        pg.draw.rect(screen, (255, 255, 255), [pos_1 - 15 - 215, 15, 235, 125])
        pg.draw.rect(screen, (200, 200, 200), [pos_1 - 18 - 209, 18, 229, 119])
        pg.draw.rect(screen, (170, 170, 170), [pos_1 - 18 - 206, 21, 226, 116])
        pg.draw.rect(screen, (130, 130, 130), [pos_1 - 21 - 203, 21, 223, 113])

        # Dessiner les lignes de séparation
        pg.draw.rect(screen, (50, 50, 50), [pos_1 - 210, 52, 200, 1])  # Horizontale
        pg.draw.rect(screen, (50, 50, 50), [pos_1 - 123, 75, 1, 40])  # Verticale

        # Afficher le nom de la Banshee (coin supérieur gauche de la boîte)
        screen.blit(
            vsmallfont.render(self.nom, 1, (255, 255, 255)), [pos_1 - 220, 30, 50, 25]
        )

        # Afficher les points de vie (coin supérieur droit, aligné à droite)
        screen.blit(
            vsmallfont.render(
                str(self.pv) + phrasesClass["banshee"]["infoBox"]["pv"],
                1,
                (255, 255, 255),
            ),
            [pos_0 - 79 - retirer, 30, retirer, 25],
        )

        # Afficher le titre "Stats"
        screen.blit(
            vsmallfont.render(
                phrasesClass["banshee"]["infoBox"]["stats"], 1, (255, 255, 255)
            ),
            [pos_1 - 220, 55, 50, 25],
        )

        # Afficher les labels des statistiques (disposition en deux colonnes)
        screen.blit(
            vsmallfont.render(
                phrasesClass["banshee"]["infoBox"]["strength"], 1, (255, 255, 255)
            ),
            [pos_1 - 220, 75, 50, 25],  # Colonne gauche
        )
        screen.blit(
            vsmallfont.render(
                phrasesClass["banshee"]["infoBox"]["defense"], 1, (255, 255, 255)
            ),
            [pos_1 - 118, 75, 50, 25],  # Colonne droite
        )
        screen.blit(
            vsmallfont.render(
                phrasesClass["banshee"]["infoBox"]["mana"], 1, (255, 255, 255)
            ),
            [pos_1 - 220, 95, 50, 25],  # Colonne gauche
        )
        screen.blit(
            vsmallfont.render(
                phrasesClass["banshee"]["infoBox"]["precision"], 1, (255, 255, 255)
            ),
            [pos_1 - 118, 95, 50, 25],  # Colonne droite
        )

        # Afficher les valeurs des statistiques (alignées à droite dans leurs colonnes)
        # Force
        retirer = vsmallfont.render(str(self.force), 1, (255, 255, 255)).get_rect()[2]
        screen.blit(
            vsmallfont.render(str(self.force), 1, (255, 255, 255)),
            [pos_1 - 129 - retirer, 75, retirer, 25],
        )
        # Défense
        screen.blit(
            vsmallfont.render(str(self.defence), 1, (255, 255, 255)),
            [pos_2 - 27 - retirer, 75, retirer, 25],
        )

        # Mana
        retirer = vsmallfont.render(str(self.mana), 1, (255, 255, 255)).get_rect()[2]
        screen.blit(
            vsmallfont.render(str(self.mana), 1, (255, 255, 255)),
            [pos_1 - 129 - retirer, 95, retirer, 25],
        )

        # Précision (avec symbole %)
        retirer = vsmallfont.render(
            str(self.prec) + "%", 1, (255, 255, 255)
        ).get_rect()[2]
        screen.blit(
            vsmallfont.render(str(self.prec) + "%", 1, (255, 255, 255)),
            [pos_2 - 27 - retirer, 95, retirer, 25],
        )

        # Mettre à jour et afficher la barre de vie
        self.BarreDeVie.setPv(self.pv)
        self.BarreDeVie.Affiche()


    def affiche_texte(self, texte, liste_joueur, temps):
        bouton_quit = Bouton(
            (6, 10),
            2,
            "Quit",
            (255, 255, 255),
            "",
            self.posBouton
        )
        duree = temps * 60
        while duree > 0:
            clock.tick(60)
            pg.draw.rect(
                screen, (0, 0, 0), [0, 0, screen.get_width(), screen.get_height()]
            )
            bouton_quit.setsize((6, 10), self.posBouton)
            for ev in pg.event.get():
                if ev.type == pg.QUIT:
                    pg.quit()
                    duree = 0
                    sys.exit()

                if ev.type == pg.MOUSEBUTTONDOWN:
                    mouse = pg.mouse.get_pos()
                    if (
                        bouton_quit.isOn(mouse)
                        and bouton_quit.getstate() not in ["Down", "Dead"]
                    ):
                        pg.quit()
                        duree = 0
                        sys.exit()

            screen.blit(
                atkfont.render(texte, 1, (255, 255, 255)),
                [int(screen.get_width() / 5), 100],
            )
            for joueur in liste_joueur:
                joueur.boite_info()
            self.boite_info()
            bouton_quit.affiche_bouton()
            pg.display.flip()
            duree -= 1

    def getpv(self):
        return self.pv

    def setturn(self, turn):
        self.turn = turn


class Night_walker:
    def __init__(self, liste_joueur, posBouton):
        self.nom = phrasesClass["NW"]["Name"]
        self.posBouton = posBouton

        if len(liste_joueur) > 1:
            self.pv = int(
                1500 * (len(liste_joueur) * (1 + (len(liste_joueur) - 1) * 0.25))
            )
            self.pvbase = int(
                1500 * (len(liste_joueur) * (1 + (len(liste_joueur) - 1) * 0.25))
            )

        else:
            self.pv = 1500
            self.pvbase = 1500

        self.force = 25
        self.mana = 1000
        self.defence = 25
        self.prec = 37.5
        self.objet_lourd = 3 * len(liste_joueur)
        self.ombre = 0
        self.turn = True
        self.BarreDeVie = BarreDeVie(
            400, self.nom, self.pv, self.pvbase, self.pvbase / 4
        )

    def choose_target(self, liste_joueur):
        if not liste_joueur:
            print("Il n'y a aucun joueur à attaquer.")

        target = liste_joueur[0]

        for joueur in liste_joueur:
            if joueur.pv > target.pv:
                target = joueur.nom
        return target

    def attack(self, target, liste_joueur):
        crit = random.randint(1, 100)
        attatype = random.randint(1, 100)
        degats = 0
        pg.draw.rect(screen, (0, 0, 0), [0, 0, screen.get_width(), screen.get_height()])
        self.affiche_texte(phrasesClass["NW"]["attack"]["prepare"], liste_joueur, 3)
        pg.draw.rect(screen, (0, 0, 0), [0, 0, screen.get_width(), screen.get_height()])

        if 100 - (35 - self.prec) < crit <= 100:
            self.affiche_texte(phrasesClass["NW"]["attack"]["fail"], liste_joueur, 4)

        elif 0 < crit <= self.prec:
            if 0 < attatype <= 60:
                degats = self.force * 7.5
                self.mana += len(liste_joueur) * 100
                self.affiche_texte(
                    phrasesClass["NW"]["attack"]["crit"]["phy"][0]
                    + str(target.getnom())
                    + phrasesClass["NW"]["attack"]["crit"]["phy"][1]
                    + str(degats)
                    + phrasesClass["NW"]["attack"]["crit"]["phy"][2],
                    liste_joueur,
                    4,
                )

            elif 60 < attatype <= 95 and self.objet_lourd > 0:
                degats = self.force * 15
                self.affiche_texte(
                    phrasesClass["NW"]["attack"]["crit"]["reinf"][0]
                    + str(target.getnom())
                    + phrasesClass["NW"]["attack"]["crit"]["reinf"][1]
                    + str(degats)
                    + phrasesClass["NW"]["attack"]["crit"]["reinf"][2],
                    liste_joueur,
                    4,
                )
                self.objet_lourd -= 1
                for joueur in liste_joueur:
                    joueur.boite_info()
                self.boite_info()
                pg.display.flip()
                pg.time.delay(4000)

            elif 95 < attatype <= 100:
                degats = self.force * 7.5
                self.ombre += len(liste_joueur)
                self.affiche_texte(
                    phrasesClass["NW"]["attack"]["crit"]["mag"][0]
                    + str(target.getnom())
                    + phrasesClass["NW"]["attack"]["crit"]["mag"][1]
                    + str(degats)
                    + phrasesClass["NW"]["attack"]["crit"]["mag"][2],
                    liste_joueur,
                    4,
                )

        else:
            if 0 < attatype <= 60:
                degats = self.force * 5
                self.mana += len(liste_joueur) * 50
                self.affiche_texte(
                    phrasesClass["NW"]["attack"]["norm"]["phy"][0]
                    + str(target.getnom())
                    + phrasesClass["NW"]["attack"]["norm"]["phy"][1]
                    + str(degats)
                    + phrasesClass["NW"]["attack"]["norm"]["phy"][2],
                    liste_joueur,
                    4,
                )

            elif 60 < attatype <= 95 and self.objet_lourd > 0:
                degats = self.force * 7.5
                self.affiche_texte(
                    phrasesClass["NW"]["attack"]["norm"]["reinf"][0]
                    + str(target.getnom())
                    + phrasesClass["NW"]["attack"]["norm"]["reinf"][1]
                    + str(degats)
                    + phrasesClass["NW"]["attack"]["norm"]["reinf"][2],
                    liste_joueur,
                    4,
                )
                self.objet_lourd -= 1

            elif 95 < attatype <= 100:
                degats = self.force * 5
                self.ombre += len(liste_joueur)
                self.affiche_texte(
                    phrasesClass["NW"]["attack"]["norm"]["mag"][0]
                    + str(target.getnom())
                    + phrasesClass["NW"]["attack"]["norm"]["mag"][1]
                    + str(degats)
                    + phrasesClass["NW"]["attack"]["norm"]["mag"][2],
                    liste_joueur,
                    4,
                )
        return degats

    def defences(self, degats, liste_joueur):
        crit = random.randint(1, 100)
        deftype = random.randint(1, 100)
        pg.draw.rect(screen, (0, 0, 0), [0, 0, screen.get_width(), screen.get_height()])
        self.affiche_texte(phrasesClass["NW"]["defense"]["prepare"], liste_joueur, 3)
        pg.draw.rect(screen, (0, 0, 0), [0, 0, screen.get_width(), screen.get_height()])

        if self.ombre >= 1:
            self.affiche_texte(
                phrasesClass["NW"]["defense"]["shadowEscape"], liste_joueur, 3
            )
            self.ombre -= 1

        elif 100 - (35 - self.prec) < crit <= 100 and self.ombre == 0:
            self.affiche_texte(phrasesClass["NW"]["defense"]["fail"], liste_joueur, 3)

        elif 0 < crit <= self.prec and self.ombre == 0:
            if 0 < deftype <= 60:
                degats_def = self.defence * 10
                self.affiche_texte(
                    phrasesClass["NW"]["defense"]["crit"]["phy"][0]
                    + str(degats_def)
                    + phrasesClass["NW"]["defense"]["crit"]["phy"][1],
                    liste_joueur,
                    3,
                )
                self.pv -= degats - degats_def

            elif 60 < deftype <= 95:
                degats_def = self.defence * 7.5 + 100
                self.affiche_texte(
                    phrasesClass["NW"]["defense"]["crit"]["reinf"][0]
                    + str(degats_def)
                    + phrasesClass["NW"]["defense"]["crit"]["reinf"][1],
                    liste_joueur,
                    3,
                )
                self.pv -= degats - degats_def
                self.mana -= 100

            elif 95 < deftype <= 100:
                self.affiche_texte(
                    phrasesClass["NW"]["defense"]["crit"]["mag"], liste_joueur, 3
                )
                self.ombre += len(liste_joueur)
                self.mana -= 250

        elif self.ombre == 0:
            if 0 < deftype <= 60:
                degats_def = self.defence * 5
                self.affiche_texte(
                    phrasesClass["NW"]["defense"]["norm"]["phy"][0]
                    + str(degats_def)
                    + phrasesClass["NW"]["defense"]["norm"]["phy"][1],
                    liste_joueur,
                    3,
                )
                self.pv -= degats - degats_def

            elif 60 < deftype <= 95:
                degats_def = self.defence * 4 + 100
                self.affiche_texte(
                    phrasesClass["NW"]["defense"]["norm"]["reinf"][0]
                    + str(degats_def)
                    + phrasesClass["NW"]["defense"]["norm"]["reinf"][1],
                    liste_joueur,
                    3,
                )
                self.pv -= degats - degats_def
                self.mana -= 100

            elif 95 < deftype <= 100:
                degats_def = degats * 0.75
                self.affiche_texte(
                    phrasesClass["NW"]["defense"]["norm"]["mag"][0]
                    + str(degats_def)
                    + phrasesClass["NW"]["defense"]["norm"]["mag"][1],
                    liste_joueur,
                    3,
                )
                self.pv -= degats - degats_def
                self.mana -= 250

    def boite_info(self):
        """
        Affiche la boîte d'informations du Night Walker sur le côté droit de l'écran.

        Cette méthode dessine une interface graphique complète avec une particularité :
        - Masque les PV réels par "?" si les PV sont supérieurs à 25% du maximum
        - Affiche une statistique supplémentaire "ombre" unique au Night Walker
        - Montre toutes les autres statistiques standard
        - Inclut un indicateur visuel pour le tour actif
        - Affiche une barre de vie graphique

        La logique de masquage des PV ajoute un élément stratégique au combat,
        ne révélant les PV exacts que lorsque le Night Walker est affaibli.

        Note:
            Utilise les variables globales screen, vsmallfont et phrasesClass.
            Comportement spécial pour l'affichage des PV selon self.pv / self.pvbase.
        """
        # Calculer la largeur du texte des PV pour l'alignement
        retirer = vsmallfont.render(
            str(self.pv) + phrasesClass["NW"]["infoBox"]["pv"], 1, (255, 255, 255)
        ).get_rect()[2]

        # Définir les positions relatives à la largeur d'écran (côté droit)
        pos_0 = screen.get_width() + retirer  # Position de référence pour PV
        pos_1 = screen.get_width() - 20  # Position de base côté droit
        pos_2 = screen.get_width()  # Bord droit de l'écran

        # Dessiner la bordure verte si c'est le tour du Night Walker
        if self.turn:
            pg.draw.rect(screen, (0, 255, 0), [pos_1 - 13 - 219, 13, 239, 129])

        # Dessiner les couches de fond de la boîte (effet de profondeur)
        pg.draw.rect(screen, (255, 255, 255), [pos_1 - 15 - 215, 15, 235, 125])
        pg.draw.rect(screen, (200, 200, 200), [pos_1 - 18 - 209, 18, 229, 119])
        pg.draw.rect(screen, (170, 170, 170), [pos_1 - 18 - 206, 21, 226, 116])
        pg.draw.rect(screen, (130, 130, 130), [pos_1 - 21 - 203, 21, 223, 113])

        # Dessiner les lignes de séparation
        pg.draw.rect(screen, (50, 50, 50), [pos_1 - 210, 52, 200, 1])  # Horizontale
        pg.draw.rect(screen, (50, 50, 50), [pos_1 - 123, 75, 1, 40])  # Verticale

        # Afficher le nom du Night Walker
        screen.blit(
            vsmallfont.render(self.nom, 1, (255, 255, 255)), [pos_1 - 220, 30, 50, 25]
        )

        # Logique spéciale d'affichage des PV (masquage stratégique)
        if self.pv < self.pvbase / 4:  # Si PV < 25% du maximum
            # Afficher les PV réels (Night Walker affaibli)
            screen.blit(
                vsmallfont.render(
                    str(self.pv) + phrasesClass["NW"]["infoBox"]["pv"],
                    1,
                    (255, 255, 255),
                ),
                [pos_0 - 79 - retirer, 30, retirer, 25],
            )
        else:
            # Masquer les PV réels avec "?" (Night Walker en bonne santé)
            retirer = vsmallfont.render(
                "?" + phrasesClass["NW"]["infoBox"]["pv"], 1, (255, 255, 255)
            ).get_rect()[2]
            screen.blit(
                vsmallfont.render(
                    "?" + phrasesClass["NW"]["infoBox"]["pv"], 1, (255, 255, 255)
                ),
                [pos_0 - 79 - retirer, 30, retirer, 25],
            )

        # Afficher le titre "Stats"
        screen.blit(
            vsmallfont.render(
                phrasesClass["NW"]["infoBox"]["stats"], 1, (255, 255, 255)
            ),
            [pos_1 - 220, 55, 50, 25],
        )

        # Afficher les labels des statistiques standard (disposition en deux colonnes)
        screen.blit(
            vsmallfont.render(
                phrasesClass["NW"]["infoBox"]["strength"], 1, (255, 255, 255)
            ),
            [pos_1 - 220, 75, 50, 25],  # Force - colonne gauche
        )
        screen.blit(
            vsmallfont.render(
                phrasesClass["NW"]["infoBox"]["defense"], 1, (255, 255, 255)
            ),
            [pos_1 - 118, 75, 50, 25],  # Défense - colonne droite
        )
        screen.blit(
            vsmallfont.render(
                phrasesClass["NW"]["infoBox"]["mana"], 1, (255, 255, 255)
            ),
            [pos_1 - 220, 95, 50, 25],  # Mana - colonne gauche
        )
        screen.blit(
            vsmallfont.render(
                phrasesClass["NW"]["infoBox"]["precision"], 1, (255, 255, 255)
            ),
            [pos_1 - 118, 95, 50, 25],  # Précision - colonne droite
        )

        # Afficher le label "ombre" (statistique spéciale du Night Walker)
        screen.blit(
            vsmallfont.render(
                phrasesClass["NW"]["infoBox"]["ombre"], 1, (255, 255, 255)
            ),
            [pos_1 - 220, 115, 50, 25],  # Ombre - ligne supplémentaire
        )

        # Afficher les valeurs des statistiques (alignées à droite dans leurs colonnes)
        # Force
        retirer = vsmallfont.render(str(self.force), 1, (255, 255, 255)).get_rect()[2]
        screen.blit(
            vsmallfont.render(str(self.force), 1, (255, 255, 255)),
            [pos_1 - 129 - retirer, 75, retirer, 25],
        )
        # Défense
        screen.blit(
            vsmallfont.render(str(self.defence), 1, (255, 255, 255)),
            [pos_2 - 27 - retirer, 75, retirer, 25],
        )

        # Mana
        retirer = vsmallfont.render(str(self.mana), 1, (255, 255, 255)).get_rect()[2]
        screen.blit(
            vsmallfont.render(str(self.mana), 1, (255, 255, 255)),
            [pos_1 - 129 - retirer, 95, retirer, 25],
        )

        # Précision (avec symbole %)
        retirer = vsmallfont.render(
            str(self.prec) + "%", 1, (255, 255, 255)
        ).get_rect()[2]
        screen.blit(
            vsmallfont.render(str(self.prec) + "%", 1, (255, 255, 255)),
            [pos_2 - 27 - retirer, 95, retirer, 25],
        )

        # Valeur de la statistique "ombre" (capacité spéciale)
        retirer = vsmallfont.render(str(self.ombre), 1, (255, 255, 255)).get_rect()[2]
        screen.blit(
            vsmallfont.render(str(self.ombre), 1, (255, 255, 255)),
            [pos_2 - 27 - retirer, 115, retirer, 25],
        )

        # Mettre à jour et afficher la barre de vie
        self.BarreDeVie.setPv(self.pv)
        self.BarreDeVie.Affiche()

    def affiche_texte(self, texte, liste_joueur, temps):
        bouton_quit = Bouton(
            (6, 10),
            2,
            "Quit",
            (255, 255, 255),
            "",
            self.posBouton
        )
        duree = temps * 60
        while duree > 0:
            clock.tick(60)
            pg.draw.rect(
                screen, (0, 0, 0), [0, 0, screen.get_width(), screen.get_height()]
            )
            bouton_quit.setsize((6, 10), self.posBouton)
            for ev in pg.event.get():
                if ev.type == pg.QUIT:
                    pg.quit()
                    duree = 0
                    sys.exit()

                if ev.type == pg.MOUSEBUTTONDOWN:
                    mouse = pg.mouse.get_pos()
                    if (
                        bouton_quit.isOn(mouse)
                        and bouton_quit.getstate() not in ["Down", "Dead"]
                    ):
                        pg.quit()
                        duree = 0
                        sys.exit()

            screen.blit(
                atkfont.render(texte, 1, (255, 255, 255)),
                [int(screen.get_width() / 5), 100],
            )
            for joueur in liste_joueur:
                joueur.boite_info()
            self.boite_info()
            bouton_quit.affiche_bouton()
            pg.display.flip()
            duree -= 1

    def getpv(self):
        return self.pv

    def setpv(self, pv):
        self.pv = pv

    def setturn(self, turn):
        self.turn = turn


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
        btnSize['btnSizeW'] = int(
            floor((self.width - 24 - (btnSize['nbCol'] * btnSize['sep'] - btnSize['sep'])) / btnSize['nbCol']) - (
                    floor((self.width - 24 - (btnSize['nbCol'] * btnSize['sep'] - btnSize['sep'])) / btnSize[
                        'nbCol']) % 2))
        btnSize['btnSizeH'] = int(
            floor(((self.height - 24 - (btnSize['nbLigne'] * btnSize['sep'] - btnSize['sep'])) / btnSize['nbLigne']) - (
                floor(((self.height - 24 - (btnSize['nbLigne'] * btnSize['sep'] - btnSize['sep'])) / btnSize[
                    'nbLigne']) % 2))))
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
            '1': {'nbCol': 5, 'nbLigne': 7, 'sep': 30},
            '2': {'nbCol': 5, 'nbLigne': 9, 'sep': 20},
            '3': {'nbCol': 7, 'nbLigne': 12, 'sep': 10}
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
            coordinates (tuple): Coordonnées (colonne, ligne) dans la grille (type 1 : 0-4 - 0-8, type 2 : 0-6 - 0-10, type 3 : 0-8 - 0-13)
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

    def getpose(self):
        return {'coord': self.coordinates, 'width': self.width, 'height': self.height}

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
            coordinates (tuple): Nouvelles coordonnées (colonne, ligne) (type 1 : 0-4 - 0-8, type 2 : 0-6 - 0-10, type 3 : 0-8 - 0-13)
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


class Texte_Histoire:
    def __init__(self, heighttop, texte, font):
        self.widthtop = screen.get_width() / 2
        self.heighttop = heighttop
        self.texte = texte
        self.font = font
        self.color = (255, 255, 255)
        self.state = 2

    def afficher(self):
        if self.state == 1 or self.state == 3:
            self.widthtop = screen.get_width() / 2
            text = atkfont.render(self.texte, True, self.color)
            text_rect = text.get_rect(center=(self.widthtop, self.heighttop))
            screen.blit(text, text_rect)
        self.next_turn()

    def next_turn(self):
        if self.heighttop == 150:
            self.state = 3
            self.color = (15, 15, 15)
        if self.heighttop <= 120:
            self.state = 1
        if self.heighttop < 0:
            self.state = 0
        if self.state == 1:
            self.color = (self.color[0] - 2, self.color[1] - 2, self.color[2] - 2)
        if self.state == 3:
            self.color = (self.color[0] + 8, self.color[1] + 8, self.color[2] + 8)
        self.heighttop -= 1

    def get_state(self):
        return self.state

    def get_heighttop(self):
        return self.heighttop

    def get_texte(self):
        return self.texte

    def get_color(self):
        return self.color

    def get_font(self):
        return self.font


class Histoire:
    def __init__(self, texte, font2, posBouton, screen):
        self.screen = screen
        self.posBouton = posBouton
        self.bouton_quit = Bouton(
            (6, 10),
            2,
            "Quit",
            (255, 255, 255),
            "",
            self.posBouton
        )
        self.bouton_skip = Bouton(
            (6, 9),
            2,
            "Passer",
            (255, 255, 255),
            "",
            self.posBouton
        )
        self.font = font2
        self.texte = self.creer_lst_texte(texte)

    def creer_lst_texte(self, texte):
        lst_texte = []
        for loop in range(len(texte)):
            lst_texte.append(Texte_Histoire(151 + 30 * loop, texte[loop], self.font))
        return lst_texte

    def affiche_histoire(self):
        game_over = True
        skip = 0
        down = False
        while game_over:
            clock.tick(30)
            pg.draw.rect(
                screen, (0, 0, 0), [0, 0, screen.get_width(), screen.get_height()]
            )
            self.bouton_quit.setsize((6, 10), self.posBouton)
            self.bouton_skip.setsize((6, 9), self.posBouton)
            coordsSkip = self.bouton_skip.getpose()
            for ev in pg.event.get():
                if ev.type == pg.QUIT:
                    pg.quit()
                    game_over = False
                    sys.exit()

                if ev.type == pg.MOUSEBUTTONDOWN:
                    mouse = pg.mouse.get_pos()
                    if (
                        self.bouton_quit.isOn(mouse)
                        and self.bouton_quit.getstate() not in ["Down", "Dead"]
                    ):
                        pg.quit()
                        game_over = False
                        sys.exit()

                    elif (self.bouton_skip.isOn(mouse)
                        and self.bouton_skip.getstate() not in ["Down", "Dead"]):
                        game_over = False
                elif ev.type == pg.KEYDOWN :
                    if ev.key == pg.K_RETURN:
                        down = True
                elif ev.type == pg.KEYUP :
                    if ev.key == pg.K_RETURN:
                        down = False

            pg.gfxdraw.arc(self.screen, coordsSkip['coord'][0], coordsSkip['coord'][1] - coordsSkip['height'],
                           floor((coordsSkip['height'] - 10) / 2), 0, 180, (90, 90, 90))
            pg.gfxdraw.arc(self.screen, coordsSkip['coord'][0], coordsSkip['coord'][1] - coordsSkip['height'],
                           floor((coordsSkip['height'] - 10) / 2), 180, 360, (90, 90, 90))
            if down :
                if skip >= 45:
                    game_over = False
                skip += 1
            elif skip >= 0:
                skip -= 1
            for loop in self.texte:
                loop.afficher()

            if game_over and skip > 0:
                pg.gfxdraw.arc(self.screen, coordsSkip['coord'][0], coordsSkip['coord'][1] - coordsSkip['height'],
                               floor((coordsSkip['height'] - 9) / 2), -90, -90 + floor(180 / 45 * skip),
                               (255, 255, 255))
                pg.gfxdraw.arc(self.screen, coordsSkip['coord'][0], coordsSkip['coord'][1] - coordsSkip['height'],
                               floor((coordsSkip['height'] - 10) / 2), -90, -90 + floor(180 / 45 * skip),
                               (255, 255, 255))
                pg.gfxdraw.arc(self.screen, coordsSkip['coord'][0], coordsSkip['coord'][1] - coordsSkip['height'],
                               floor((coordsSkip['height'] - 11) / 2), -90, -90 + floor(180 / 45 * skip),
                               (255, 255, 255))

                pg.gfxdraw.arc(self.screen, coordsSkip['coord'][0], coordsSkip['coord'][1] - coordsSkip['height'],
                               floor((coordsSkip['height'] - 9) / 2), 90, 90 + floor(180 / 45 * skip), (255, 255, 255))
                pg.gfxdraw.arc(self.screen, coordsSkip['coord'][0], coordsSkip['coord'][1] - coordsSkip['height'],
                               floor((coordsSkip['height'] - 10) / 2), 90, 90 + floor(180 / 45 * skip), (255, 255, 255))
                pg.gfxdraw.arc(self.screen, coordsSkip['coord'][0], coordsSkip['coord'][1] - coordsSkip['height'],
                               floor((coordsSkip['height'] - 11) / 2), 90, 90 + floor(180 / 45 * skip), (255, 255, 255))

            self.bouton_skip.affiche_bouton()
            self.bouton_quit.affiche_bouton()

            pg.display.flip()
            pg.time.delay(50)
            if game_over:
                game_over = not (self.texte[-1].get_state() == 0)

    def state_up(self):
        self.state += 1

    def state_restart(self):
        self.state = 1

    def getwidth(self):
        return [self.widthtop, self.widthbot]

    def getheight(self):
        return [self.heighttop, self.heightbot]

    def getstate(self):
        return self.state

    def settexte(self, texte):
        if type(texte) is str:
            self.texte = texte

    def setwidthtop(self, widthtop):
        self.widthtop = widthtop

    def setheighttop(self, heighttop):
        self.heighttop = heighttop


class SliderS:
    def __init__(self, x, y, length, height, max):
        self.x = x
        self.y = y
        self.length = length
        self.height = height
        self.basemax = max
        self.max = max
        self.current = 1
        self.slider = Slider(
            screen,
            x,
            y,
            length,
            height,
            min=1,
            max=max,
            step=1,
            initial=1,
            colour=(150, 20, 200),
        )
        self.output = TextBox(
            screen,
            900,
            y - 16,
            100,
            100,
            fontSize=30,
            textColour=(240, 240, 240),
            colour=(0, 0, 0),
        )
        self.textMax = TextBox(
            screen,
            750,
            y - 16,
            150,
            100,
            fontSize=30,
            textColour=(240, 240, 240),
            colour=(0, 0, 0),
        )
        self.output.disable()
        self.textMax.disable()

    def __del__(self):
        return

    def update(self):
        self.current = self.getValue()
        self.slider = Slider(
            screen,
            self.x,
            self.y,
            self.length,
            self.height,
            min=1,
            max=self.max,
            step=1,
            initial=int(self.current),
        )

    def ChangeColor(self, color):
        if color == "Red":
            self.current = self.getValue()
            self.slider = Slider(
                screen,
                self.x,
                self.y,
                self.length,
                self.height,
                min=1,
                max=self.max,
                step=1,
                initial=int(self.current),
                colour=(150, 0, 0),
            )
        else:
            self.current = self.getValue()
            self.slider = Slider(
                screen,
                self.x,
                self.y,
                self.length,
                self.height,
                min=1,
                max=self.max,
                step=1,
                initial=int(self.current),
                colour=(150, 20, 200),
            )

    def reset(self):
        self.slider = Slider(
            screen,
            self.x,
            self.y,
            self.length,
            self.height,
            min=1,
            max=self.basemax,
            step=1,
            initial=1,
            colour=(150, 20, 200),
        )

    def setMax(self, max):
        if type(max) is int:
            self.max = max

    def getMax(self):
        return self.max

    def getValue(self):
        return str(self.slider.getValue())

    def setText(self, text):
        self.output.setText(str(text))

    def setTextMax(self):
        self.textMax.setText("max : " + str(self.max))


class GestionSlider:
    def __init__(self, sliderStr, sliderDef, sliderPrec):
        self.Str = sliderStr
        self.Def = sliderDef
        self.prec = sliderPrec
        self.CurColor = "White"
        self.tot = TextBox(
            screen,
            950,
            100,
            200,
            60,
            fontSize=30,
            textColour=(240, 240, 240),
            colour=(0, 0, 0),
        )

    def __del__(self):
        del self.Str
        del self.Def
        del self.prec
        return

    def afficheSlider(self):
        self.update()
        self.tot.disable()
        pygame_widgets.update(ev)

    def update(self):
        tot = (
            int(self.Str.getValue())
            + int(self.Def.getValue())
            + int(self.prec.getValue())
        )
        if tot > 100 and self.CurColor != "Red":
            self.ChangeColor("Red")
            self.CurColor = "Red"
        elif self.CurColor == "Red" and tot <= 100:
            self.ChangeColor("White")
            self.CurColor = "White"
        self.tot.setText(str(tot) + "/100")
        self.Str.setText(self.Str.getValue())
        self.Def.setText(self.Def.getValue())
        self.prec.setText(self.prec.getValue())
        self.Str.setTextMax()
        self.Def.setTextMax()
        self.prec.setTextMax()

    def ChangeColor(self, color):
        if color == "Red":
            self.tot = TextBox(
                screen,
                950,
                100,
                200,
                60,
                fontSize=30,
                textColour=(200, 0, 0),
                colour=(0, 0, 0),
            )
            self.Str.ChangeColor(color)
            self.Def.ChangeColor(color)
            self.prec.ChangeColor(color)
        else:
            self.tot = TextBox(
                screen,
                950,
                100,
                200,
                60,
                fontSize=30,
                textColour=(240, 240, 240),
                colour=(0, 0, 0),
            )
            self.Str.ChangeColor(color)
            self.Def.ChangeColor(color)
            self.prec.ChangeColor(color)

        self.tot.disable()

    def reset(self):
        self.Str.reset()
        self.Def.reset()
        self.prec.reset()

    def getTot(self):
        return (
            int(self.Str.getValue())
            + int(self.Def.getValue())
            + int(self.prec.getValue())
        )

    def getStr(self):
        return int(self.Str.getValue())

    def getDef(self):
        return int(self.Def.getValue())

    def getPrec(self):
        return int(self.prec.getValue())


class BarreDeVie:
    def __init__(self, width, name, pv, pvbase, pvAffiche=False):
        self.width = width
        self.name = name
        self.pv = pv
        self.pvbase = pvbase
        self.pvAffiche = pvAffiche

    def Affiche(self):
        self.AfficheBar()
        self.AfficheNom()

    def AfficheBar(self):
        width = screen.get_width()
        if self.name == phrasesClass["NW"]["Name"] and self.pv > self.pvAffiche:
            completedColour = (100, 100, 100)
        else:
            completedColour = (200, 0, 0)
        progressBar = ProgressBar(
            screen,
            width / 4,
            50,
            width / 2,
            18,
            lambda: (self.pv / self.pvbase),
            curved=True,
            completedColour=completedColour,
        )
        pg.draw.polygon(
            screen,
            (218, 165, 32),
            [
                (width / 16 * 4 + 2, 49),
                (width / 16 * 4 - 4, 49),
                (width / 16 * 4 - 16, 59),
                (width / 16 * 4 - 4, 68),
                (width / 16 * 4 + 2, 68),
                (width / 16 * 4 - 3, 59),
            ],
        )
        pg.draw.polygon(
            screen,
            (255, 215, 0),
            [
                (width / 16 * 4 - 3, 59),
                (width / 16 * 4 - 16, 59),
                (width / 16 * 4 - 4, 68),
                (width / 16 * 4 + 2, 68),
            ],
        )

        pg.draw.polygon(
            screen,
            (218, 165, 32),
            [
                (width / 16 * 12 - 2, 49),
                (width / 16 * 12 + 4, 49),
                (width / 16 * 12 + 16, 59),
                (width / 16 * 12 + 4, 68),
                (width / 16 * 12 - 2, 68),
                (width / 16 * 12 + 3, 59),
            ],
        )
        pg.draw.polygon(
            screen,
            (255, 215, 0),
            [
                (width / 16 * 12 + 3, 59),
                (width / 16 * 12 + 16, 59),
                (width / 16 * 12 + 4, 68),
                (width / 16 * 12 - 2, 68),
            ],
        )
        pygame_widgets.update(ev)

    def AfficheNom(self):
        width = screen.get_width()
        pg.draw.rect(
            screen, (218, 165, 32), [width / 2 - self.width / 2, 40, self.width, 8]
        )
        pg.draw.rect(
            screen, (255, 210, 0), [width / 2 - self.width / 2, 44, self.width, 4]
        )
        pg.draw.rect(
            screen, (218, 165, 32), [width / 2 - self.width / 2 - 8, 40 - 8, 8, 8]
        )
        pg.draw.rect(screen, (218, 165, 32), [width / 2 + self.width / 2, 40 - 8, 8, 8])
        pg.draw.polygon(
            screen,
            (255, 215, 0),
            [
                (width / 2 - self.width / 2 - 8, 33),
                (width / 2 - self.width / 2, 40),
                (width / 2 - self.width / 2 - 8, 40),
            ],
        )
        pg.draw.polygon(
            screen,
            (255, 215, 0),
            [
                (width / 2 + self.width / 2 + 7, 33),
                (width / 2 + self.width / 2 + 7, 40),
                (width / 2 + self.width / 2, 40),
            ],
        )
        nom = bigfont.render(self.name, True, (200, 200, 200))
        nom_rect = nom.get_rect(center=(width / 2, 20))
        screen.blit(nom, nom_rect)

    def setPv(self, pv):
        self.pv = pv


def creation_perso(nom, pv, mana, force, defence, precision, id, posBouton, turn):
    """
    Outils de création de personnage.
    creation_perso est automatiquement lancé avec la fonction Jouer, il n'est pas utile de l'appeler diréctement.
    id est un entier associé directement despuis la fonction Jouer.
    Sortie : instance de la classe J
    """
    if nom == "N°0":
        Joueur = J(nom, 0, 0, 0, 0, 0, id, posBouton, True)
        return Joueur

    if force + precision + defence <= 100 and precision <= 25 and pv + mana <= 3000:
        Joueur = J(nom, pv, mana, precision, force, defence, id, posBouton, turn)
        return Joueur
    return None


def banshee_fight(liste_joueur, nb_joueur, bouton_quit, bouton_1, bouton_2, bouton_3, posBouton):
    banshee = Banshee(liste_joueur, posBouton)
    for joueur in liste_joueur:
        joueur.boite_info()
    banshee.boite_info()
    pg.display.flip()
    game_over = 0

    while game_over == 0:
        joueur_att = banshee.choose_target(liste_joueur)
        degats_infliges = banshee.attack(joueur_att, liste_joueur)

        if not 95 < degats_infliges[1] <= 100:
            banshee.setturn(False)
            joueur_att.setturn(True)
            joueur_att.defences(
                degats_infliges[0],
                bouton_quit,
                bouton_1,
                bouton_2,
                bouton_3,
                banshee,
                liste_joueur,
            )
            joueur_att.setturn(False)

        for joueur in liste_joueur:
            joueur.setturn(True)
            dgt_joueur = joueur.attack(
                bouton_quit, bouton_1, bouton_2, bouton_3, banshee, liste_joueur
            )
            joueur.setturn(False)
            banshee.setturn(True)
            banshee.defences(dgt_joueur, liste_joueur)
            banshee.setturn(False)

            for joueur in liste_joueur[:]:  # éviter bug de suppression
                if joueur.getpv() <= 0:
                    del liste_joueur[joueur.getid() - 1]

            if len(liste_joueur) == 0:
                pg.draw.rect(
                    screen, (0, 0, 0), [0, 0, screen.get_width(), screen.get_height()]
                )
                screen.blit(
                    atkfont.render(
                        phrasesClass["banshee"]["attack"]["defense"]["fail"][0],
                        1,
                        (255, 255, 255),
                    ),
                    [int(screen.get_width() / 5), 100],
                )
                screen.blit(
                    atkfont.render(
                        phrasesClass["banshee"]["attack"]["defense"]["fail"][1],
                        1,
                        (255, 255, 255),
                    ),
                    [int(screen.get_width() / 5), 130],
                )
                pg.display.flip()
                pg.time.delay(1500)
                game_over = 1
                break

            if banshee.getpv() <= 0:
                pg.draw.rect(
                    screen, (0, 0, 0), [0, 0, screen.get_width(), screen.get_height()]
                )
                if len(liste_joueur) < nb_joueur:
                    screen.blit(
                        atkfont.render(
                            phrasesClass["banshee"]["Fight"]["HalfWin"],
                            1,
                            (255, 255, 255),
                        ),
                        [int(screen.get_width() / 5), 100],
                    )
                else:
                    screen.blit(
                        atkfont.render(
                            phrasesClass["banshee"]["Fight"]["Win"],
                            1,
                            (255, 255, 255),
                        ),
                        [int(screen.get_width() / 5), 100],
                    )
                pg.display.flip()
                pg.time.delay(1500)
                game_over = 2
                break


def NW_fight(liste_joueur, nb_joueur, bouton_quit, bouton_1, bouton_2, bouton_3, posBouton):
    NW = Night_walker(liste_joueur, posBouton)
    for joueur in liste_joueur:
        joueur.boite_info()
    NW.boite_info()
    pg.display.flip()
    game_over = 0

    while game_over == 0:
        joueur_att = NW.choose_target(liste_joueur)
        degats_infliges = NW.attack(joueur_att, liste_joueur)
        joueur_att.setturn(True)
        NW.setturn(False)
        joueur_att.defences(
            degats_infliges, bouton_quit, bouton_1, bouton_2, bouton_3, NW, liste_joueur
        )
        joueur_att.setturn(False)
        NW.setturn(True)

        joueur_att = NW.choose_target(liste_joueur)
        degats_infliges = NW.attack(joueur_att, liste_joueur)
        joueur_att.setturn(True)
        NW.setturn(False)
        joueur_att.defences(
            degats_infliges, bouton_quit, bouton_1, bouton_2, bouton_3, NW, liste_joueur
        )
        joueur_att.setturn(False)
        NW.setturn(False)

        for joueur in liste_joueur:
            joueur.setturn(True)
            dgt_joueur = joueur.attack(
                bouton_quit, bouton_1, bouton_2, bouton_3, NW, liste_joueur
            )
            joueur.setturn(False)
            NW.setturn(True)
            NW.defences(dgt_joueur, liste_joueur)
            NW.setturn(False)

        for joueur in liste_joueur[:]:  # éviter bug de suppression en itération
            if joueur.getpv() <= 0:
                del liste_joueur[joueur.getid() - 1]

        if len(liste_joueur) == 0:
            pg.draw.rect(
                screen, (0, 0, 0), [0, 0, screen.get_width(), screen.get_height()]
            )
            screen.blit(
                atkfont.render(
                    phrasesClass["NW"]["Fight"]["Lose"][0], 1, (255, 255, 255)
                ),
                [int(screen.get_width() / 5), 100],
            )
            screen.blit(
                atkfont.render(
                    phrasesClass["NW"]["Fight"]["Lose"][1], 1, (255, 255, 255)
                ),
                [int(screen.get_width() / 5), 130],
            )
            pg.display.flip()
            pg.time.delay(1500)
            game_over = 1
            break

        if NW.getpv() <= 0:
            pg.draw.rect(
                screen, (0, 0, 0), [0, 0, screen.get_width(), screen.get_height()]
            )
            if len(liste_joueur) < nb_joueur:
                screen.blit(
                    atkfont.render(
                        phrasesClass["NW"]["Fight"]["HalfWin"], 1, (255, 255, 255)
                    ),
                    [int(screen.get_width() / 5), 100],
                )
            else:
                screen.blit(
                    atkfont.render(
                        phrasesClass["NW"]["Fight"]["Win"], 1, (255, 255, 255)
                    ),
                    [int(screen.get_width() / 5), 100],
                )
            pg.display.flip()
            pg.time.delay(1500)
            game_over = 2
            break


def nbperso(perso, selecPerso, bouton_1, bouton_2, bouton_3, bouton_4):
    (
        bouton_1.affiche_bouton(),
        bouton_2.affiche_bouton(),
        bouton_3.affiche_bouton(),
        bouton_4.affiche_bouton(),
    )
    if not selecPerso:
        if perso == 0:
            screen.blit(
                atkfont.render(
                    phrasesClass["Creation"]["NbPerso"][0], True, (255, 255, 255)
                ),
                (15, 15),
            )
            return None
        else:
            screen.blit(
                atkfont.render(
                    phrasesClass["Creation"]["NbPerso"][1] + str(perso),
                    True,
                    (255, 255, 255),
                ),
                (15, 15),
            )
            selecPerso = True
            return selecPerso
    return None


def nom(nom, selecNOM):
    if not selecNOM:
        screen.blit(
            atkfont.render(
                phrasesClass["Creation"]["Name"][0] + str(nom), True, (255, 255, 255)
            ),
            (15, 15),
        )
        return None
    else:
        screen.blit(
            atkfont.render(
                phrasesClass["Creation"]["Name"][1] + str(nom), True, (255, 255, 255)
            ),
            (15, 15),
        )
        selecNOM = True
        return selecNOM


def nbpv(pv, selecPV, bouton_1, bouton_2, bouton_3, bouton_4):
    (
        bouton_1.affiche_bouton(),
        bouton_2.affiche_bouton(),
        bouton_3.affiche_bouton(),
        bouton_4.affiche_bouton(),
    )
    if not selecPV:
        if pv == 0:
            screen.blit(
                atkfont.render(
                    phrasesClass["Creation"]["PV"][0], True, (255, 255, 255)
                ),
                (15, 15),
            )
            return None
        else:
            screen.blit(
                atkfont.render(
                    phrasesClass["Creation"]["PV"][1][0]
                    + str(pv)
                    + phrasesClass["Creation"]["PV"][1][1],
                    True,
                    (255, 255, 255),
                ),
                (15, 15),
            )
            selecPV = True
            return selecPV
    return None


def nbmana(mana, selecMana, bouton_1, bouton_2, bouton_3, bouton_4):
    (
        bouton_1.affiche_bouton(),
        bouton_2.affiche_bouton(),
        bouton_3.affiche_bouton(),
        bouton_4.affiche_bouton(),
    )
    if not selecMana:
        if mana == 0:
            screen.blit(
                atkfont.render(
                    phrasesClass["Creation"]["Mana"][0], True, (255, 255, 255)
                ),
                (15, 15),
            )
            return None
        else:
            screen.blit(
                atkfont.render(
                    phrasesClass["Creation"]["Mana"][1][0]
                    + str(mana)
                    + phrasesClass["Creation"]["Mana"][1][1],
                    True,
                    (255, 255, 255),
                ),
                (15, 15),
            )
            selecMana = True
            return selecMana
    return None


def nbstats(stats, force, Def, prec, selecStats, bouton_1, sliders):
    bouton_1.affiche_bouton()
    if sliders.getTot() > 100:
        bouton_1.setstate("Down")
    else:
        bouton_1.setstate("")
    if not selecStats:
        if stats == 0:
            screen.blit(
                atkfont.render(
                    phrasesClass["Creation"]["Stats"]["Question"], True, (255, 255, 255)
                ),
                (15, 15),
            )
            sliders.afficheSlider()
            return None
        else:
            screen.blit(
                atkfont.render(
                    phrasesClass["Creation"]["Stats"]["Response"]["Str"][0]
                    + str(force)
                    + phrasesClass["Creation"]["Stats"]["Response"]["Str"][1],
                    True,
                    (255, 255, 255),
                ),
                (15, 15),
            )
            screen.blit(
                atkfont.render(
                    phrasesClass["Creation"]["Stats"]["Response"]["Def"][0]
                    + str(Def)
                    + phrasesClass["Creation"]["Stats"]["Response"]["Def"][1],
                    True,
                    (255, 255, 255),
                ),
                (15, 45),
            )
            screen.blit(
                atkfont.render(
                    phrasesClass["Creation"]["Stats"]["Response"]["Prec"][0]
                    + str(prec)
                    + phrasesClass["Creation"]["Stats"]["Response"]["Prec"][1],
                    True,
                    (255, 255, 255),
                ),
                (15, 75),
            )
            selecStats = True
            sliders.reset()
            return selecStats
    return None

def info_attaque():
    msg = smallfont.render(phrasesClass["J"]["info"]["attack"][0], 1, (255, 255, 255))
    text_rect = msg.get_rect(
        center=(screen.get_width() / 2, screen.get_height() / 2 - 50)
    )
    screen.blit(msg, text_rect)

def info_defence():
    msg = smallfont.render(phrasesClass["J"]["info"]["defense"][0], 1, (255, 255, 255))
    text_rect = msg.get_rect(
        center=(screen.get_width() / 2, screen.get_height() / 2 + 50)
    )
    screen.blit(msg, text_rect)

def Jouer():
    """
    La fonction Jouer permet de lancer le jeu (créer les personnages entre 1 et 4, de donner les informations essentielles au jeu et de lancer la partie)
    Aucune entrée et sortie
    Pour le moment ne fait que combattre le / les joueur(s) contre la banshee ou Le marcheur de la nuit
    """
    global afficheMenu
    perso = 0
    liste_joueur = []
    selecPerso = False
    selecNOM = False
    selecPV = False
    selecMana = False
    selecStat = False
    name = ""
    pv = 0
    mana = 0
    stats = 0
    force = 0
    Def = 0
    prec = 0
    game_over = 0
    loop = 0
    regles = False
    hist = 1

    posBouton = PosBoutons(screen)

    bouton_quit = Bouton(
        (6, 10),
        2,
        "Quit",
        (255, 255, 255),
        "",
        posBouton
    )
    bouton_compris = Bouton(
        (6, 9),
        2,
        phrasesClass["Bouton"]["Rules"],
        (255, 255, 255),
        "",
        posBouton
    )
    bouton_1 = Bouton(
        (0, 13),
        3,
        phrasesClass["Bouton"]["BTN1"],
        (255, 255, 255),
        "",
        posBouton
    )
    bouton_2 = Bouton(
        (1, 13),
        3,
        phrasesClass["Bouton"]["BTN2"],
        (255, 255, 255),
        "",
        posBouton
    )
    bouton_3 = Bouton(
        (2, 13),
        3,
        phrasesClass["Bouton"]["BTN3"],
        (255, 255, 255),
        "",
        posBouton
    )
    bouton_4 = Bouton(
        (3, 13),
        3,
        phrasesClass["Bouton"]["BTN4"],
        (255, 255, 255),
        "",
        posBouton
    )
    sliders = GestionSlider(
        SliderS(100, 200, 600, 20, 90),
        SliderS(100, 300, 600, 20, 90),
        SliderS(100, 400, 600, 20, 25),
    )

    while game_over == 0:
        clock.tick(60)
        width = screen.get_width()
        height = screen.get_height()
        pg.draw.rect(screen, (0, 0, 0), [0, 0, width, height])
        bouton_quit.setsize((6, 10), posBouton)
        bouton_compris.setsize((6, 9), posBouton)
        bouton_1.setsize((0, 13), posBouton)
        bouton_2.setsize((1, 13), posBouton)
        bouton_3.setsize((2, 13), posBouton)
        bouton_4.setsize((3, 13), posBouton)

        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                pg.quit()
                game_over = 3
                sys.exit()

            if ev.type == pg.MOUSEBUTTONDOWN:
                mouse = pg.mouse.get_pos()
                if not afficheMenu:
                    if (
                        bouton_quit.isOn(mouse)
                        and bouton_quit.getstate() not in ["Down", "Dead"]
                    ):
                        pg.quit()
                        game_over = 3
                        sys.exit()

                    elif (
                        bouton_1.isOn(mouse)
                        and bouton_1.getstate() == ""
                    ):
                        if not selecPerso:
                            perso = 1

                        elif not selecPV:
                            pv = 2500
                            (
                                bouton_2.setstate("Down"),
                                bouton_3.setstate("Down"),
                                bouton_4.setstate("Down"),
                            )

                        elif not selecMana and 3000 - pv == 500:
                            mana = 500

                        elif not selecStat:
                            force = sliders.getStr()
                            Def = sliders.getDef()
                            prec = sliders.getPrec()
                            stats = 1

                    elif (
                        bouton_2.isOn(mouse)
                    ):
                        if not selecPerso:
                            perso = 2

                        elif not selecPV:
                            pv = 2000
                            (
                                bouton_1.setstate("Down"),
                                bouton_3.setstate("Down"),
                                bouton_4.setstate("Down"),
                            )

                        elif not selecMana and 3000 - pv == 1000:
                            mana = 1000

                    elif (
                        bouton_3.isOn(mouse)
                    ):
                        if not selecPerso:
                            perso = 3

                        elif not selecPV:
                            pv = 1500
                            (
                                bouton_1.setstate("Down"),
                                bouton_2.setstate("Down"),
                                bouton_4.setstate("Down"),
                            )

                        elif not selecMana and 3000 - pv == 1500:
                            mana = 1500

                    elif (
                        bouton_4.isOn(mouse)
                    ):
                        if not selecPerso:
                            perso = 4

                        elif not selecPV:
                            pv = 1000
                            (
                                bouton_1.setstate("Down"),
                                bouton_2.setstate("Down"),
                                bouton_3.setstate("Down"),
                            )

                        elif not selecMana and 3000 - pv == 2000:
                            mana = 2000

            if ev.type == pg.KEYDOWN:
                if ev.key == pg.K_ESCAPE:
                    afficheMenu = not afficheMenu
                elif ev.key == pg.K_BACKSPACE:
                    name = name[:-1]
                elif ev.key == pg.K_RETURN:
                    selecNOM = True
                    (
                        bouton_1.settexte("2500"),
                        bouton_2.settexte("2000"),
                        bouton_3.settexte("1500"),
                        bouton_4.settexte("1000"),
                    )

            if ev.type == pg.TEXTINPUT:
                name += ev.text  # Ajoute le texte Unicode directement

        bouton_quit.affiche_bouton()

        while not regles:
            bouton_quit.setsize((6, 10), posBouton)
            bouton_compris.setsize((6, 9), posBouton)
            for ev in pg.event.get():
                if ev.type == pg.QUIT:
                    pg.quit()
                    game_over = 3
                    sys.exit()
                if ev.type == pg.MOUSEBUTTONDOWN:
                    mouse = pg.mouse.get_pos()
                    if (
                            bouton_quit.isOn(mouse)
                            and bouton_quit.getstate()
                            not in ["Down", "Dead"]
                    ):
                        pg.quit()
                        game_over = 3
                        sys.exit()
                    elif (
                            bouton_compris.isOn(mouse)
                            and bouton_compris.getstate()
                            not in ["Down", "Dead"]
                    ):
                        regles = True
                elif ev.type == pg.KEYDOWN:
                    if ev.key == K_RETURN:
                        regles = True
            pg.draw.rect(
                screen,
                (0, 0, 0),
                [0, 0, screen.get_width(), screen.get_height()],
            )
            info_attaque()
            info_defence()
            bouton_quit.affiche_bouton()
            bouton_compris.affiche_bouton()
            pg.display.flip()

        if not selecPerso:
            selecPerso = nbperso(
                perso, selecPerso, bouton_1, bouton_2, bouton_3, bouton_4
            )
            if selecPerso:
                pg.display.flip()
                pg.time.delay(500)
            pg.display.flip()

        else:
            if perso > 0:
                if not selecNOM:
                    selecNOM = nom(name, selecNOM)
                    if selecPV:
                        pg.display.flip()
                        pg.time.delay(1000)
                    pg.display.flip()

                if name == "N°0" and selecNOM:
                    selecPV = True
                    selecMana = True
                    selecStat = True

                if (not selecPV) and selecNOM:
                    selecPV = nbpv(pv, selecPV, bouton_1, bouton_2, bouton_3, bouton_4)
                    if selecPV:
                        (
                            bouton_1.settexte("500"),
                            bouton_2.settexte("1000"),
                            bouton_3.settexte("1500"),
                            bouton_4.settexte("2000"),
                        )
                        pg.display.flip()
                        pg.time.delay(1000)
                    pg.display.flip()

                if (not selecMana) and selecPV:
                    selecMana = nbmana(
                        mana, selecMana, bouton_1, bouton_2, bouton_3, bouton_4
                    )
                    if selecMana:
                        bouton_1.settexte(phrasesClass["Bouton"]["Validate"])
                        (
                            bouton_1.setstate(""),
                            bouton_2.setstate(""),
                            bouton_3.setstate(""),
                            bouton_4.setstate(""),
                        )
                        pg.display.flip()
                        pg.time.delay(1000)
                    pg.display.flip()

                if (not selecStat) and selecMana:
                    selecStat = nbstats(
                        stats, force, Def, prec, selecStat, bouton_1, sliders
                    )
                    if selecStat:
                        pg.display.flip()
                        pg.time.delay(1000)
                    pg.display.flip()

                if selecStat and loop == 0:
                    J1 = creation_perso(name, pv, mana, force, Def, prec, 1, posBouton, False)
                    liste_joueur.append(J1)
                    perso -= 1
                    if perso > 0:
                        name = ""
                        pv = 0
                        mana = 0
                        force = 0
                        Def = 0
                        prec = 0
                        stats = 0
                        loop += 1
                        selecNOM = False
                        selecPV = False
                        selecMana = False
                        selecStat = False

                if selecStat and loop == 1:
                    J2 = creation_perso(name, pv, mana, force, Def, prec, 2, posBouton, False)
                    liste_joueur.append(J2)
                    perso -= 1
                    if perso > 0:
                        name = ""
                        pv = 0
                        mana = 0
                        force = 0
                        Def = 0
                        prec = 0
                        stats = 0
                        loop += 1
                        selecNOM = False
                        selecPV = False
                        selecMana = False
                        selecStat = False

                if selecStat and loop == 2:
                    J3 = creation_perso(name, pv, mana, force, Def, prec, 3, posBouton, False)
                    liste_joueur.append(J3)
                    perso -= 1
                    if perso > 0:
                        name = ""
                        pv = 0
                        mana = 0
                        force = 0
                        Def = 0
                        prec = 0
                        stats = 0
                        loop += 1
                        selecNOM = False
                        selecPV = False
                        selecMana = False
                        selecStat = False

                if selecStat and loop == 3:
                    J4 = creation_perso(name, pv, mana, force, Def, prec, 4, posBouton, False)
                    liste_joueur.append(J4)
                    perso -= 1
                    if perso > 0:
                        name = ""
                        pv = 0
                        mana = 0
                        force = 0
                        Def = 0
                        prec = 0
                        stats = 0
                        loop += 1
                        selecNOM = False
                        selecPV = False
                        selecMana = False
                        selecStat = False

            else:
                del sliders
                adversaire_selec = random.randint(1, 2)

                if adversaire_selec == 1:
                    if hist == 1:
                        NW = Night_walker(liste_joueur, posBouton)
                        histo = Histoire(phrasesClass["NW"]["Hist"], atkfont, posBouton, screen)
                        histo.affiche_histoire()
                        hist = 0

                    for joueur in liste_joueur:
                        joueur.boite_info()
                    NW.boite_info()
                    pg.display.flip()
                    game_over = 1
                    NW_fight(
                        liste_joueur,
                        len(liste_joueur),
                        bouton_quit,
                        bouton_1,
                        bouton_2,
                        bouton_3,
                        posBouton
                    )

                if adversaire_selec == 2:
                    if hist == 1:
                        banshee = Banshee(liste_joueur, posBouton)
                        histo = Histoire(phrasesClass["banshee"]["Hist"], atkfont, posBouton, screen)
                        histo.affiche_histoire()
                        hist = 0
                    for joueur in liste_joueur:
                        joueur.boite_info()
                    banshee.boite_info()
                    pg.display.flip()
                    game_over = 1
                    banshee_fight(
                        liste_joueur,
                        len(liste_joueur),
                        bouton_quit,
                        bouton_1,
                        bouton_2,
                        bouton_3,
                        posBouton
                    )


def JouerBoucle():
    running = True
    posBouton = PosBoutons(screen)
    bouton_oui = Bouton(
        (2, 6),
        "Oui",
        (0, 200, 0),
        "",
        posBouton
    )
    bouton_non = Bouton(
        (4, 6),
        "Non",
        (200, 0, 0),
        "",
        posBouton
    )
    replay = False
    while running:
        width = screen.get_width()
        height = screen.get_height()
        pg.draw.rect(screen, (0, 0, 0), [0, 0, width, height])
        bouton_oui.setsize((2, 6), posBouton)
        bouton_non.setsize((4, 6), posBouton)

        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if ev.type == pg.MOUSEBUTTONDOWN:
                mouse = pg.mouse.get_pos()
                if (
                    bouton_non.isOn(mouse)
                ):
                    pg.quit()
                    running = False
                    sys.exit()

                elif (
                    bouton_oui.isOn(mouse)
                ):
                    replay = True
                    running = False

                elif (
                    bouton_non.isOn(mouse)
                ):
                    running = False

        text = smallfont.render(
            phrasesClass["Boucle"]["Question"], True, (255, 255, 255)
        )
        text_rect = text.get_rect(
            center=(screen.get_width() / 2, screen.get_height() / 2 - 20)
        )
        screen.blit(text, text_rect)
        bouton_oui.affiche_bouton()
        bouton_non.affiche_bouton()
        pg.display.flip()

    return replay


def afficher_nom_jeu():
    screen_w_2_10 = screen.get_width() / 2 - screen.get_width() / 10
    screen_w_5 = screen.get_width() / 5
    screen_h_10 = screen.get_height() / 10
    pg.draw.rect(
        screen,
        (120, 120, 120),
        [screen_w_2_10 - 10, 40, screen_w_5 + 20, screen_h_10 + 20],
    )
    for loop in range(10):
        pg.draw.rect(
            screen,
            (180, 180, 180),
            [screen_w_2_10 - 10, 40 + loop, screen_w_5 + 20 - loop, 1],
        )

    for loop in range(10):
        pg.draw.rect(
            screen,
            (180, 180, 180),
            [screen_w_2_10 - 10 + loop, 50, 1, screen_h_10 + 10 - loop],
        )
    center_rect = pg.draw.rect(
        screen,
        (150, 150, 150),
        [
            screen.get_width() / 2 - screen.get_width() / 10,
            50,
            screen.get_width() / 5,
            screen.get_height() / 10,
        ],
    )
    surf_texte = bigfont.render("D&D?", 1, (255, 255, 255))
    rect_texte = surf_texte.get_rect()
    rect_texte.center = center_rect.center
    screen.blit(surf_texte, rect_texte)


def jouer_bloc(bouton_Jouer, bouton_quit):
    screen_w_2_10 = screen.get_width() / 2 - screen.get_width() / 10
    screen_w_5 = screen.get_width() / 5
    screen_h_2_8 = screen.get_height() / 2 - screen.get_height() / 8
    screen_h_4 = screen.get_height() / 4
    pg.draw.rect(
        screen,
        (120, 120, 120),
        [screen_w_2_10 - 10, screen_h_2_8 - 10, screen_w_5 + 20, screen_h_4 + 20],
    )
    pg.draw.rect(
        screen, (150, 150, 150), [screen_w_2_10, screen_h_2_8, screen_w_5, screen_h_4]
    )
    for loop in range(10):
        pg.draw.rect(
            screen,
            (180, 180, 180),
            [screen_w_2_10 - 10, screen_h_2_8 - 10 + loop, screen_w_5 + 20 - loop, 1],
        )
    for loop in range(10):
        pg.draw.rect(
            screen,
            (180, 180, 180),
            [screen_w_2_10 - 10 + loop, screen_h_2_8 - 5, 1, screen_h_4 + 15 - loop],
        )
    bouton_Jouer.affiche_bouton()
    bouton_quit.affiche_bouton()


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
afficheMenu = False

while running:
    clock.tick(60)
    width = screen.get_width()
    height = screen.get_height()
    pg.draw.rect(screen, (0, 0, 0), [0, 0, width, height])
    bouton_Jouer.setsize((2, 4), posBouton)
    bouton_quit.setsize((6, 10), posBouton)
    for ev in pg.event.get():
        if ev.type == pg.QUIT:
            pg.quit()
            running = False
            sys.exit()

        if ev.type == pg.MOUSEBUTTONDOWN:
            mouse = pg.mouse.get_pos()
            if not afficheMenu:
                if (
                    bouton_quit.isOn(mouse)
                    and bouton_quit.getstate() not in ["Down", "Dead"]
                ):
                    pg.quit()
                    running = False
                    sys.exit()
                elif (
                    bouton_Jouer.isOn(mouse)
                ):
                    Jouer()
                    ask = True

        if ev.type == pg.KEYDOWN:
            if ev.key == pg.K_ESCAPE:
                afficheMenu = not afficheMenu

    if ask:
        running = JouerBoucle()
        replay = running

    if replay:
        Jouer()

    if not replay:
        afficher_nom_jeu()
        jouer_bloc(bouton_Jouer, bouton_quit)

    pg.display.flip()
