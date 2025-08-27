import random, os, sys, pygame_widgets, pygame as pg, pygame.gfxdraw, config as config, Classes.MenuDnD as Menu

from math import floor
from pygame import K_RETURN
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from pygame_widgets.progressbar import ProgressBar

from Classes.Boutons import Bouton, PosBoutons
from Classes.GameState import GameState

os.environ["SDL_VIDEO_CENTERED"] = "1"

dataConfig = config.charger_config()
pg.init()
fonts = {
    "bigfont": pg.font.SysFont("Arial", 40),
    "smallfont": pg.font.SysFont("Arial", 20),
    "vsmallfont": pg.font.SysFont("Arial", 14),
    "atkfont": pg.font.SysFont("Arial", 17),
}
GameState = GameState(dataConfig, fonts)
boutons = {
    "bouton_quit": Bouton(
        (6, 10),
        2,
        GameState.getPhrases()["Bouton"]["Quit"],
        (255, 255, 255),
        "",
        GameState.getPosBoutons(),
    ),
    "bouton_compris": Bouton(
        (6, 9),
        2,
        GameState.getPhrases()["Bouton"]["Rules"],
        (255, 255, 255),
        "",
        GameState.getPosBoutons(),
    ),
    "bouton_1": Bouton(
        (0, 13),
        3,
        GameState.getPhrases()["Bouton"]["BTN1"],
        (255, 255, 255),
        "",
        GameState.getPosBoutons(),
    ),
    "bouton_2": Bouton(
        (1, 13),
        3,
        GameState.getPhrases()["Bouton"]["BTN2"],
        (255, 255, 255),
        "",
        GameState.getPosBoutons(),
    ),
    "bouton_3": Bouton(
        (2, 13),
        3,
        GameState.getPhrases()["Bouton"]["BTN3"],
        (255, 255, 255),
        "",
        GameState.getPosBoutons(),
    ),
    "bouton_4": Bouton(
        (3, 13),
        3,
        GameState.getPhrases()["Bouton"]["BTN4"],
        (255, 255, 255),
        "",
        GameState.getPosBoutons(),
    ),
    "bouton_skip": Bouton(
        (6, 9),
        2,
        GameState.getPhrases()["Bouton"]["Skip"],
        (255, 255, 255),
        "",
        GameState.getPosBoutons(),
    ),
    "bouton_Jouer": Bouton(
        (2, 4),
        1,
        GameState.getPhrases()["Bouton"]["Play"],
        (0, 200, 0),
        "",
        GameState.getPosBoutons(),
    ),
    "bouton_oui": Bouton(
        (2, 6),
        2,
        GameState.getPhrases()["Boucle"]["Possibility"][0],
        (0, 200, 0),
        "",
        GameState.getPosBoutons(),
    ),
    "bouton_non": Bouton(
        (4, 6),
        2,
        GameState.getPhrases()["Boucle"]["Possibility"][1],
        (200, 0, 0),
        "",
        GameState.getPosBoutons(),
    ),
}
GameState.setBoutons(boutons)


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

    def attack(self, adv, lst_joueur):
        """
        Gère l'interface d'attaque du joueur.

        Affiche les options d'attaque disponibles et traite les interactions
        utilisateur pour sélectionner et exécuter une attaque.

        Returns:
            str: Le type d'attaque sélectionné ou None si annulé
        """
        (
            GameState.getBouton("bouton_1").settexte(
                GameState.getPhrases()["J"]["attack"]["attackType"][0]
            ),
            GameState.getBouton("bouton_2").settexte(
                GameState.getPhrases()["J"]["attack"]["attackType"][1]
            ),
            GameState.getBouton("bouton_3").settexte(
                GameState.getPhrases()["J"]["attack"]["attackType"][2]
            ),
        )
        self.boite_info()
        runningJAtt = True
        selecAtta = False
        selecMA = False
        atta_type = ""
        mana_uti = ""

        while runningJAtt:
            GameState.getClock().tick(60)
            pg.draw.rect(
                GameState.getScreen(),
                (0, 0, 0),
                [0, 0, GameState.getScreenWidth(), GameState.getScreenHeight()],
            )
            for ev in pg.event.get():
                if ev.type == pg.QUIT:
                    pg.quit()
                    runningJAtt = False
                    sys.exit()

                elif ev.type == pg.MOUSEBUTTONDOWN:
                    mouse = pg.mouse.get_pos()
                    if GameState.isOn(
                        "bouton_quit", mouse
                    ) and GameState.getBoutonState("bouton_quit") not in [
                        "Down",
                        "Dead",
                    ]:
                        pg.quit()
                        sys.exit()
                    elif GameState.isOn("bouton_1", mouse):
                        if not selecAtta:
                            atta_type = GameState.getPhrases()["J"]["attack"][
                                "attackType"
                            ][0]
                            selecMA = True
                    elif GameState.isOn("bouton_2", mouse):
                        if not selecAtta:
                            atta_type = GameState.getPhrases()["J"]["attack"][
                                "attackType"
                            ][1]
                    elif GameState.isOn("bouton_3", mouse):
                        if not selecAtta:
                            atta_type = GameState.getPhrases()["J"]["attack"][
                                "attackType"
                            ][2]

                elif ev.type == pg.KEYDOWN:
                    if ev.key == pg.K_ESCAPE:
                        if GameState.getMenu() is None:
                            GameState.generateMenu()
                        GameState.setAfficherMenu(True)
                    if ev.key == pg.K_BACKSPACE:
                        mana_uti = mana_uti[:-1]
                    elif ev.key == pg.K_RETURN:
                        selecMA = True

                if ev.type == pg.TEXTINPUT:
                    mana_uti += ev.text  # Ajoute le texte Unicode directement

            GameState.afficherBouton("bouton_quit")
            if GameState.getAfficherMenu():
                res = GameState.AfficherMenu()
                if res["end"] == 1:
                    newConfig = res["config"]
                    GameState.getMenu().setActive(res["onglet"])
                    GameState.updateGeneral(
                        (int(newConfig["width"]), int(newConfig["height"]))
                    )
                elif res["end"] == 2:
                    GameState.setAfficherMenu(res["Menu"])

            if not (selecAtta):
                selecAtta = self.selec_atta(atta_type, selecAtta)
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
                    GameState.getScreen(),
                    (0, 0, 0),
                    [0, 0, GameState.getScreenWidth(), GameState.getScreenHeight()],
                )
                cp_crit = random.randint(1, 100)

                if 100 - (35 - self.prec) < cp_crit <= 100:
                    if mana_uti != 0:
                        self.affiche_texte(
                            GameState.getPhrases()["J"]["attack"]["fail"],
                            lst_joueur,
                            2.5,
                            adv,
                        )
                        self.mana -= int(mana_uti)
                        pg.draw.rect(
                            GameState.getScreen(),
                            (0, 0, 0),
                            [
                                0,
                                0,
                                GameState.getScreenWidth(),
                                GameState.getScreenHeight(),
                            ],
                        )
                        return 0

                    else:
                        self.affiche_texte(
                            GameState.getPhrases()["J"]["attack"]["fail"],
                            lst_joueur,
                            2.5,
                            adv,
                        )
                        pg.draw.rect(
                            GameState.getScreen(),
                            (0, 0, 0),
                            [
                                0,
                                0,
                                GameState.getScreenWidth(),
                                GameState.getScreenHeight(),
                            ],
                        )
                        return 0

                elif 1 <= cp_crit <= self.prec:
                    if (
                        atta_type
                        == GameState.getPhrases()["J"]["attack"]["attackType"][0]
                    ):
                        degats = self.force * 7.5
                        self.affiche_texte(
                            GameState.getPhrases()["J"]["attack"]["crit"]["phy"][0]
                            + str(degats)
                            + GameState.getPhrases()["J"]["attack"]["crit"]["phy"][1],
                            lst_joueur,
                            2.5,
                            adv,
                        )
                        pg.draw.rect(
                            GameState.getScreen(),
                            (0, 0, 0),
                            [
                                0,
                                0,
                                GameState.getScreenWidth(),
                                GameState.getScreenHeight(),
                            ],
                        )
                        return degats

                    elif (
                        atta_type
                        == GameState.getPhrases()["J"]["attack"]["attackType"][1]
                    ):
                        degats = self.force * 2 * 1.5 + int(mana_uti) * 2.5 * 1.5
                        self.affiche_texte(
                            GameState.getPhrases()["J"]["attack"]["crit"]["reinf"][0]
                            + str(degats)
                            + GameState.getPhrases()["J"]["attack"]["crit"]["reinf"][1],
                            lst_joueur,
                            2.5,
                            adv,
                        )
                        self.mana -= int(mana_uti)
                        pg.draw.rect(
                            GameState.getScreen(),
                            (0, 0, 0),
                            [
                                0,
                                0,
                                GameState.getScreenWidth(),
                                GameState.getScreenHeight(),
                            ],
                        )
                        return degats

                    elif (
                        atta_type
                        == GameState.getPhrases()["J"]["attack"]["attackType"][2]
                    ):
                        degats = int(mana_uti) * 1.5
                        self.affiche_texte(
                            GameState.getPhrases()["J"]["attack"]["crit"]["mag"][0]
                            + str(degats)
                            + GameState.getPhrases()["J"]["attack"]["crit"]["mag"][1],
                            lst_joueur,
                            2.5,
                            adv,
                        )
                        self.mana -= int(mana_uti)
                        pg.draw.rect(
                            GameState.getScreen(),
                            (0, 0, 0),
                            [
                                0,
                                0,
                                GameState.getScreenWidth(),
                                GameState.getScreenHeight(),
                            ],
                        )
                        return degats

                else:
                    if (
                        atta_type
                        == GameState.getPhrases()["J"]["attack"]["attackType"][0]
                    ):
                        degats = self.force * 5
                        self.affiche_texte(
                            GameState.getPhrases()["J"]["attack"]["norm"]["phy"][0]
                            + str(degats)
                            + GameState.getPhrases()["J"]["attack"]["norm"]["phy"][1],
                            lst_joueur,
                            2.5,
                            adv,
                        )
                        pg.draw.rect(
                            GameState.getScreen(),
                            (0, 0, 0),
                            [
                                0,
                                0,
                                GameState.getScreenWidth(),
                                GameState.getScreenHeight(),
                            ],
                        )
                        return degats

                    elif (
                        atta_type
                        == GameState.getPhrases()["J"]["attack"]["attackType"][1]
                    ):
                        degats = self.force * 2 + int(mana_uti) * 2.5
                        self.affiche_texte(
                            GameState.getPhrases()["J"]["attack"]["norm"]["reinf"][0]
                            + str(degats)
                            + GameState.getPhrases()["J"]["attack"]["norm"]["reinf"][1],
                            lst_joueur,
                            2.5,
                            adv,
                        )
                        self.mana -= int(mana_uti)
                        pg.draw.rect(
                            GameState.getScreen(),
                            (0, 0, 0),
                            [
                                0,
                                0,
                                GameState.getScreenWidth(),
                                GameState.getScreenHeight(),
                            ],
                        )
                        return degats

                    elif (
                        atta_type
                        == GameState.getPhrases()["J"]["attack"]["attackType"][2]
                    ):
                        degats = int(mana_uti)
                        self.affiche_texte(
                            GameState.getPhrases()["J"]["attack"]["norm"]["mag"][0]
                            + str(degats)
                            + GameState.getPhrases()["J"]["attack"]["norm"]["mag"][1],
                            lst_joueur,
                            2.5,
                            adv,
                        )
                        self.mana -= int(mana_uti)
                        pg.draw.rect(
                            GameState.getScreen(),
                            (0, 0, 0),
                            [
                                0,
                                0,
                                GameState.getScreenWidth(),
                                GameState.getScreenHeight(),
                            ],
                        )
                        return degats

            for joueur in lst_joueur:
                joueur.boite_info()
            adv.boite_info()
            pg.display.flip()
        return None

    def defences(self, degats, adv, lst_joueur):
        """
        Gère l'interface de défense du joueur.

        Affiche les options de défense disponibles et traite les interactions
        utilisateur pour sélectionner une stratégie défensive.

        Returns:
            str: Le type de défense sélectionné ou None si annulé
        """
        (
            GameState.getBouton("bouton_1").settexte(
                GameState.getPhrases()["J"]["defense"]["defenseType"][0]
            ),
            GameState.getBouton("bouton_2").settexte(
                GameState.getPhrases()["J"]["defense"]["defenseType"][1]
            ),
            GameState.getBouton("bouton_3").settexte(
                GameState.getPhrases()["J"]["defense"]["defenseType"][2]
            ),
        )
        runningJDef = True
        selecDef = False
        selecMD = False
        def_type = ""
        mana_uti = ""

        while runningJDef:
            GameState.getClock().tick(60)
            pg.draw.rect(
                GameState.getScreen(),
                (0, 0, 0),
                [0, 0, GameState.getScreenWidth(), GameState.getScreenHeight()],
            )
            for ev in pg.event.get():
                if ev.type == pg.QUIT:
                    pg.quit()
                    runningJDef = False
                    sys.exit()

                elif ev.type == pg.MOUSEBUTTONDOWN:
                    mouse = pg.mouse.get_pos()
                    if GameState.isOn(
                        "bouton_quit", mouse
                    ) and GameState.getBoutonState("bouton_quit") not in [
                        "Down",
                        "Dead",
                    ]:
                        pg.quit()
                        sys.exit()
                    elif GameState.isOn("bouton_1", mouse):
                        if not selecDef:
                            def_type = GameState.getPhrases()["J"]["defense"][
                                "defenseType"
                            ][0]
                            selecMD = True
                    elif GameState.isOn("bouton_2", mouse):
                        if not selecDef:
                            def_type = GameState.getPhrases()["J"]["defense"][
                                "defenseType"
                            ][1]
                    elif GameState.isOn("bouton_3", mouse):
                        if not selecDef:
                            def_type = GameState.getPhrases()["J"]["defense"][
                                "defenseType"
                            ][2]

                elif ev.type == pg.KEYDOWN:
                    if ev.key == pg.K_ESCAPE:
                        if GameState.getMenu() is None:
                            GameState.generateMenu()
                        GameState.setAfficherMenu(True)
                    if ev.key == pg.K_BACKSPACE:
                        mana_uti = mana_uti[:-1]
                    elif ev.key == pg.K_RETURN:
                        selecMD = True

                if ev.type == pg.TEXTINPUT:
                    mana_uti += ev.text  # Ajoute le texte Unicode directement

            GameState.afficherBouton("bouton_quit")
            if GameState.getAfficherMenu():
                res = GameState.AfficherMenu()
                if res["end"] == 1:
                    newConfig = res["config"]
                    GameState.getMenu().setActive(res["onglet"])
                    GameState.updateGeneral(
                        (int(newConfig["width"]), int(newConfig["height"]))
                    )
                elif res["end"] == 2:
                    GameState.setAfficherMenu(res["Menu"])

            if not (selecDef):
                selecDef = self.selec_def(def_type, selecDef)
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
                    GameState.getScreen(),
                    (0, 0, 0),
                    [0, 0, GameState.getScreenWidth(), GameState.getScreenHeight()],
                )
                def_crit = random.randint(1, 100)

                if 100 - (35 - self.prec) < def_crit <= 100:
                    if int(mana_uti) != 0:
                        self.affiche_texte(
                            GameState.getPhrases()["J"]["defense"]["fail"],
                            lst_joueur,
                            2.5,
                            adv,
                        )
                        self.mana -= int(mana_uti)
                        self.pv -= degats

                    else:
                        self.affiche_texte(
                            GameState.getPhrases()["J"]["defense"]["fail"],
                            lst_joueur,
                            2.5,
                            adv,
                        )
                        self.pv -= degats

                elif 1 <= def_crit <= self.prec:
                    if (
                        def_type
                        == GameState.getPhrases()["J"]["defense"]["defenseType"][0]
                    ):
                        degats_def = self.defence * 2.5
                        self.affiche_texte(
                            GameState.getPhrases()["J"]["defense"]["crit"]["phy"][0]
                            + str(degats_def)
                            + GameState.getPhrases()["J"]["defense"]["crit"]["phy"][1],
                            lst_joueur,
                            2.5,
                            adv,
                        )

                        if degats_def <= degats:
                            self.pv -= degats - degats_def

                    elif (
                        def_type
                        == GameState.getPhrases()["J"]["defense"]["defenseType"][1]
                    ):
                        degats_def = self.defence * 2.5 + int(mana_uti) * 3
                        self.affiche_texte(
                            GameState.getPhrases()["J"]["defense"]["crit"]["reinf"][0]
                            + str(degats_def)
                            + GameState.getPhrases()["J"]["defense"]["crit"]["reinf"][
                                1
                            ],
                            lst_joueur,
                            2.5,
                            adv,
                        )
                        self.mana -= int(mana_uti)

                        if degats_def <= degats:
                            self.pv -= degats - degats_def

                    elif (
                        def_type
                        == GameState.getPhrases()["J"]["defense"]["defenseType"][2]
                    ):
                        degats_def = int(mana_uti) * 2.5
                        self.affiche_texte(
                            GameState.getPhrases()["J"]["defense"]["crit"]["mag"][0]
                            + str(degats_def)
                            + GameState.getPhrases()["J"]["defense"]["crit"]["mag"][1],
                            lst_joueur,
                            2.5,
                            adv,
                        )
                        self.mana -= int(mana_uti)

                        if degats_def <= degats:
                            self.pv -= degats - degats_def

                else:
                    if (
                        def_type
                        == GameState.getPhrases()["J"]["defense"]["defenseType"][0]
                    ):
                        degats_def = self.defence * 2.5
                        self.affiche_texte(
                            GameState.getPhrases()["J"]["defense"]["norm"]["phy"][0]
                            + str(degats_def)
                            + GameState.getPhrases()["J"]["defense"]["norm"]["phy"][1],
                            lst_joueur,
                            2.5,
                            adv,
                        )

                        if degats_def <= degats:
                            self.pv -= degats - degats_def

                    elif (
                        def_type
                        == GameState.getPhrases()["J"]["defense"]["defenseType"][1]
                    ):
                        degats_def = self.defence * 1.5 + int(mana_uti) * 2
                        self.affiche_texte(
                            GameState.getPhrases()["J"]["defense"]["norm"]["reinf"][0]
                            + str(degats_def)
                            + GameState.getPhrases()["J"]["defense"]["norm"]["reinf"][
                                1
                            ],
                            lst_joueur,
                            2.5,
                            adv,
                        )
                        self.mana -= int(mana_uti)

                        if degats_def <= degats:
                            self.pv -= degats - degats_def

                    elif (
                        def_type
                        == GameState.getPhrases()["J"]["defense"]["defenseType"][2]
                    ):
                        degats_def = int(mana_uti) * 1.5
                        self.affiche_texte(
                            GameState.getPhrases()["J"]["defense"]["norm"]["mag"][0]
                            + str(degats_def)
                            + GameState.getPhrases()["J"]["defense"]["norm"]["mag"][1],
                            lst_joueur,
                            2.5,
                            adv,
                        )
                        self.mana -= int(mana_uti)

                        if degats_def <= degats:
                            self.pv -= degats - degats_def

                runningJDef = False
                pg.draw.rect(
                    GameState.getScreen(),
                    (0, 0, 0),
                    [0, 0, GameState.getScreenWidth(), GameState.getScreenHeight()],
                )

            for joueur in lst_joueur:
                joueur.boite_info()
            adv.boite_info()
            pg.display.flip()

    def selec_atta(self, atta_type, selecAtta):
        """
        Sélectionne une attaque spécifique par son numéro.

        Args:
            num (int): Numéro de l'attaque à sélectionner (1-3)

        Returns:
            str: Le type d'attaque correspondant au numéro
        """
        (
            GameState.afficherBouton("bouton_1"),
            GameState.afficherBouton("bouton_2"),
            GameState.afficherBouton("bouton_3"),
        )
        if not selecAtta:
            if atta_type == "":
                GameState.getScreen().blit(
                    GameState.getFont("atkfont").render(
                        GameState.getPhrases()["J"]["selection"]["atk"][0],
                        True,
                        (255, 255, 255),
                    ),
                    (int(GameState.getScreenWidth() / 5), 15),
                )
                return None
            else:
                GameState.getScreen().blit(
                    GameState.getFont("atkfont").render(
                        GameState.getPhrases()["J"]["selection"]["atk"][1]
                        + str(atta_type),
                        True,
                        (255, 255, 255),
                    ),
                    (int(GameState.getScreenWidth() / 5), 15),
                )
                selecAtta = True
                return selecAtta
        return None

    def selec_def(self, def_type, selecDef):
        """
        Sélectionne une défense spécifique par son numéro.

        Args:
            num (int): Numéro de la défense à sélectionner (1-3)

        Returns:
            str: Le type de défense correspondant au numéro
        """
        (
            GameState.afficherBouton("bouton_1"),
            GameState.afficherBouton("bouton_2"),
            GameState.afficherBouton("bouton_3"),
        )
        if not selecDef:
            if def_type == "":
                GameState.getScreen().blit(
                    GameState.getFont("atkfont").render(
                        GameState.getPhrases()["J"]["selection"]["def"][0],
                        True,
                        (255, 255, 255),
                    ),
                    (int(GameState.getScreenWidth() / 5), 15),
                )
                return None
            else:
                GameState.getScreen().blit(
                    GameState.getFont("atkfont").render(
                        GameState.getPhrases()["J"]["selection"]["def"][1]
                        + str(def_type),
                        True,
                        (255, 255, 255),
                    ),
                    (int(GameState.getScreenWidth() / 5), 15),
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
            GameState.getScreen().blit(
                GameState.getFont("atkfont").render(
                    GameState.getPhrases()["J"]["selection"]["mana"][0] + str(mana_uti),
                    True,
                    (255, 255, 255),
                ),
                (int(GameState.getScreenWidth() / 5), 15),
            )
            return None
        else:
            GameState.getScreen().blit(
                GameState.getFont("atkfont").render(
                    GameState.getPhrases()["J"]["selection"]["mana"][1][0]
                    + str(mana_uti)
                    + GameState.getPhrases()["J"]["selection"]["mana"][1][1],
                    True,
                    (255, 255, 255),
                ),
                (int(GameState.getScreenWidth() / 5), 15),
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
            Utilise les variables globales screen, vsmallfont et GameState.getPhrases().
            La position est calculée dynamiquement selon self.id.
        """
        # Dessiner la bordure verte si c'est le tour du joueur
        if self.turn:
            pg.draw.rect(
                GameState.getScreen(),
                (0, 255, 0),  # Vert pour indiquer le tour actif
                [13, 13 + (120 * (self.id - 1) + 20 * (self.id - 1)), 229, 119],
            )

        # Dessiner les couches de fond de la boîte (effet de profondeur)
        pg.draw.rect(
            GameState.getScreen(),
            (255, 255, 255),  # Couche blanche externe
            [15, 15 + (120 * (self.id - 1) + 20 * (self.id - 1)), 225, 115],
        )
        pg.draw.rect(
            GameState.getScreen(),
            (200, 200, 200),  # Couche grise claire
            [18, 18 + (120 * (self.id - 1) + 20 * (self.id - 1)), 219, 109],
        )
        pg.draw.rect(
            GameState.getScreen(),
            (170, 170, 170),  # Couche grise moyenne
            [18, 21 + (120 * (self.id - 1) + 20 * (self.id - 1)), 216, 106],
        )
        pg.draw.rect(
            GameState.getScreen(),
            (130, 130, 130),  # Couche grise foncée (fond principal)
            [21, 21 + (120 * (self.id - 1) + 20 * (self.id - 1)), 213, 103],
        )

        # Dessiner les lignes de séparation
        pg.draw.rect(
            GameState.getScreen(),
            (50, 50, 50),  # Ligne horizontale de séparation
            [40, 52 + (120 * (self.id - 1) + 20 * (self.id - 1)), 160, 1],
        )
        pg.draw.rect(
            GameState.getScreen(),
            (50, 50, 50),  # Ligne verticale de séparation pour les stats
            [122, 75 + (120 * (self.id - 1) + 20 * (self.id - 1)), 1, 40],
        )

        # Calculer la largeur du texte des PV pour l'alignement à droite
        retirer = (
            GameState.getFont("vsmallfont")
            .render(
                str(self.pv) + GameState.getPhrases()["J"]["infoBox"]["pv"],
                1,
                (255, 255, 255),
            )
            .get_rect()[2]
        )

        # Définir les positions pour l'alignement du texte
        pos_0 = 165 + retirer  # Position pour les PV (alignement à droite)
        pos_1 = 116  # Position pour les stats de gauche
        pos_2 = 218  # Position pour les stats de droite

        # Afficher le nom du personnage (coin supérieur gauche)
        GameState.getScreen().blit(
            GameState.getFont("vsmallfont").render(self.nom, 1, (255, 255, 255)),
            [25, 30 + (120 * (self.id - 1) + 20 * (self.id - 1)), 50, 25],
        )

        # Afficher les points de vie (coin supérieur droit, aligné à droite)
        GameState.getScreen().blit(
            GameState.getFont("vsmallfont").render(
                str(self.pv) + GameState.getPhrases()["J"]["infoBox"]["pv"],
                1,
                (255, 255, 255),
            ),
            [
                pos_0 - retirer,  # Alignement à droite
                30 + (120 * (self.id - 1) + 20 * (self.id - 1)),
                retirer,
                25,
            ],
        )

        # Afficher le titre "Stats"
        GameState.getScreen().blit(
            GameState.getFont("vsmallfont").render(
                GameState.getPhrases()["J"]["infoBox"]["stats"], 1, (255, 255, 255)
            ),
            [25, 55 + (120 * (self.id - 1) + 20 * (self.id - 1)), 50, 25],
        )

        # Afficher les labels des statistiques (colonne de gauche)
        GameState.getScreen().blit(
            GameState.getFont("vsmallfont").render(
                GameState.getPhrases()["J"]["infoBox"]["strength"], 1, (255, 255, 255)
            ),
            [25, 75 + (120 * (self.id - 1) + 20 * (self.id - 1)), 50, 25],
        )
        GameState.getScreen().blit(
            GameState.getFont("vsmallfont").render(
                GameState.getPhrases()["J"]["infoBox"]["mana"], 1, (255, 255, 255)
            ),
            [25, 95 + (120 * (self.id - 1) + 20 * (self.id - 1)), 50, 25],
        )

        # Afficher les labels des statistiques (colonne de droite)
        GameState.getScreen().blit(
            GameState.getFont("vsmallfont").render(
                GameState.getPhrases()["J"]["infoBox"]["defense"], 1, (255, 255, 255)
            ),
            [127, 75 + (120 * (self.id - 1) + 20 * (self.id - 1)), 50, 25],
        )
        GameState.getScreen().blit(
            GameState.getFont("vsmallfont").render(
                GameState.getPhrases()["J"]["infoBox"]["precision"], 1, (255, 255, 255)
            ),
            [127, 95 + (120 * (self.id - 1) + 20 * (self.id - 1)), 50, 25],
        )

        # Afficher les valeurs des statistiques (alignées à droite dans leurs colonnes)
        # Force (colonne de gauche)
        retirer = (
            GameState.getFont("vsmallfont")
            .render(str(self.force), 1, (255, 255, 255))
            .get_rect()[2]
        )
        GameState.getScreen().blit(
            GameState.getFont("vsmallfont").render(str(self.force), 1, (255, 255, 255)),
            [
                pos_1 - retirer,  # Alignement à droite dans la colonne gauche
                75 + (120 * (self.id - 1) + 20 * (self.id - 1)),
                retirer,
                25,
            ],
        )

        # Défense (colonne de droite)
        GameState.getScreen().blit(
            GameState.getFont("vsmallfont").render(
                str(self.defence), 1, (255, 255, 255)
            ),
            [
                pos_2 - retirer + 10,  # Alignement à droite dans la colonne droite
                75 + (120 * (self.id - 1) + 20 * (self.id - 1)),
                retirer,
                25,
            ],
        )

        # Mana (colonne de gauche)
        retirer = (
            GameState.getFont("vsmallfont")
            .render(str(self.mana), 1, (255, 255, 255))
            .get_rect()[2]
        )
        GameState.getScreen().blit(
            GameState.getFont("vsmallfont").render(str(self.mana), 1, (255, 255, 255)),
            [
                pos_1 - retirer,  # Alignement à droite dans la colonne gauche
                95 + (120 * (self.id - 1) + 20 * (self.id - 1)),
                retirer,
                25,
            ],
        )

        # Précision (colonne de droite, avec symbole %)
        retirer = (
            GameState.getFont("vsmallfont")
            .render(str(self.prec) + "%", 1, (255, 255, 255))
            .get_rect()[2]
        )
        GameState.getScreen().blit(
            GameState.getFont("vsmallfont").render(
                str(self.prec) + "%", 1, (255, 255, 255)
            ),
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
        duree = temps * 60
        while duree > 0:
            GameState.getClock().tick(60)
            pg.draw.rect(
                GameState.getScreen(),
                (0, 0, 0),
                [0, 0, GameState.getScreenWidth(), GameState.getScreenHeight()],
            )
            for ev in pg.event.get():
                if ev.type == pg.QUIT:
                    pg.quit()
                    duree = 0
                    sys.exit()

                elif ev.type == pg.MOUSEBUTTONDOWN:
                    mouse = pg.mouse.get_pos()
                    if GameState.isOn(
                        "bouton_quit", mouse
                    ) and GameState.getBoutonState("bouton_quit") not in [
                        "Down",
                        "Dead",
                    ]:
                        pg.quit()
                        duree = 0
                        sys.exit()

                elif ev.type == pg.KEYDOWN:
                    if ev.key == pg.K_ESCAPE:
                        if GameState.getMenu() is None:
                            GameState.generateMenu()
                        GameState.setAfficherMenu(True)

            GameState.getScreen().blit(
                GameState.getFont("atkfont").render(texte, 1, (255, 255, 255)),
                [int(GameState.getScreenWidth() / 5), 100],
            )
            for joueur in liste_joueur:
                joueur.boite_info()
            adv.boite_info()
            GameState.afficherBouton("bouton_quit")
            if GameState.getAfficherMenu():
                res = GameState.AfficherMenu()
                if res["end"] == 1:
                    newConfig = res["config"]
                    GameState.getMenu().setActive(res["onglet"])
                    GameState.updateGeneral(
                        (int(newConfig["width"]), int(newConfig["height"]))
                    )
                elif res["end"] == 2:
                    GameState.setAfficherMenu(res["Menu"])
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
        self.nom = GameState.getPhrases()["banshee"]["Name"]
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
            print(GameState.getPhrases()["banshee"]["attack"]["noTarget"])
            return None

        target = liste_joueur[0]

        for joueur in liste_joueur:
            if joueur.pv > target.pv:
                target = joueur.nom
        return target

    def attack(self, joueur_att, liste_joueur):
        att_banshee = random.randint(1, 100)
        pg.draw.rect(
            GameState.getScreen(),
            (0, 0, 0),
            [0, 0, GameState.getScreenWidth(), GameState.getScreenHeight()],
        )
        self.affiche_texte(
            GameState.getPhrases()["banshee"]["attack"]["prepare"], liste_joueur, 3
        )
        pg.draw.rect(
            GameState.getScreen(),
            (0, 0, 0),
            [0, 0, GameState.getScreenWidth(), GameState.getScreenHeight()],
        )

        if 0 < att_banshee <= 60:
            degats = 250
            self.affiche_texte(
                GameState.getPhrases()["banshee"]["attack"]["norm"]["bas"][0]
                + str(joueur_att.getnom())
                + GameState.getPhrases()["banshee"]["attack"]["norm"]["bas"][1]
                + str(degats)
                + GameState.getPhrases()["banshee"]["attack"]["norm"]["bas"][2],
                liste_joueur,
                4,
            )
            self.mana -= 150
            return degats, att_banshee

        if 60 < att_banshee <= 95:
            degats = 500
            self.affiche_texte(
                GameState.getPhrases()["banshee"]["attack"]["norm"]["moy"][0]
                + str(joueur_att.getnom())
                + GameState.getPhrases()["banshee"]["attack"]["norm"]["moy"][1]
                + str(degats)
                + GameState.getPhrases()["banshee"]["attack"]["norm"]["moy"][2],
                liste_joueur,
                4,
            )
            self.mana -= 375
            return degats, att_banshee

        if 95 < att_banshee <= 100 and self.pv <= 1500:
            degats = self.pv
            self.affiche_texte(
                GameState.getPhrases()["banshee"]["attack"]["norm"]["haut"][0]
                + str(degats)
                + GameState.getPhrases()["banshee"]["attack"]["norm"]["haut"][1],
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
                GameState.getPhrases()["banshee"]["attack"]["norm"]["noHaut"][0]
                + str(degats)
                + GameState.getPhrases()["banshee"]["attack"]["norm"]["noHaut"][1],
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
                GameState.getPhrases()["banshee"]["defense"]["fail"][0]
                + str(degats + 50)
                + GameState.getPhrases()["banshee"]["defense"]["fail"][1],
                liste_joueur,
                4,
            )
            self.pv -= degats + 50

        elif degats != 0:
            self.affiche_texte(
                GameState.getPhrases()["banshee"]["defense"]["succes"][0]
                + str(degats - 50)
                + GameState.getPhrases()["banshee"]["defense"]["succes"][1],
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
            Utilise les variables globales screen, vsmallfont et GameState.getPhrases().
            Met à jour et affiche la barre de vie à la fin.
        """
        # Calculer la largeur du texte des PV pour l'alignement
        retirer = (
            GameState.getFont("vsmallfont")
            .render(
                str(self.pv) + GameState.getPhrases()["banshee"]["infoBox"]["pv"],
                1,
                (255, 255, 255),
            )
            .get_rect()[2]
        )

        # Définir les positions relatives à la largeur d'écran (côté droit)
        pos_0 = GameState.getScreenWidth() + retirer  # Position de référence pour PV
        pos_1 = GameState.getScreenWidth() - 20  # Position de base côté droit
        pos_2 = GameState.getScreenWidth()  # Bord droit de l'écran

        # Dessiner la bordure verte si c'est le tour de la Banshee
        if self.turn:
            pg.draw.rect(
                GameState.getScreen(), (0, 255, 0), [pos_1 - 13 - 219, 13, 239, 129]
            )

        # Dessiner les couches de fond de la boîte (effet de profondeur)
        pg.draw.rect(
            GameState.getScreen(), (255, 255, 255), [pos_1 - 15 - 215, 15, 235, 125]
        )
        pg.draw.rect(
            GameState.getScreen(), (200, 200, 200), [pos_1 - 18 - 209, 18, 229, 119]
        )
        pg.draw.rect(
            GameState.getScreen(), (170, 170, 170), [pos_1 - 18 - 206, 21, 226, 116]
        )
        pg.draw.rect(
            GameState.getScreen(), (130, 130, 130), [pos_1 - 21 - 203, 21, 223, 113]
        )

        # Dessiner les lignes de séparation
        pg.draw.rect(
            GameState.getScreen(), (50, 50, 50), [pos_1 - 210, 52, 200, 1]
        )  # Horizontale
        pg.draw.rect(
            GameState.getScreen(), (50, 50, 50), [pos_1 - 123, 75, 1, 40]
        )  # Verticale

        # Afficher le nom de la Banshee (coin supérieur gauche de la boîte)
        GameState.getScreen().blit(
            GameState.getFont("vsmallfont").render(self.nom, 1, (255, 255, 255)),
            [pos_1 - 220, 30, 50, 25],
        )

        # Afficher les points de vie (coin supérieur droit, aligné à droite)
        GameState.getScreen().blit(
            GameState.getFont("vsmallfont").render(
                str(self.pv) + GameState.getPhrases()["banshee"]["infoBox"]["pv"],
                1,
                (255, 255, 255),
            ),
            [pos_0 - 79 - retirer, 30, retirer, 25],
        )

        # Afficher le titre "Stats"
        GameState.getScreen().blit(
            GameState.getFont("vsmallfont").render(
                GameState.getPhrases()["banshee"]["infoBox"]["stats"],
                1,
                (255, 255, 255),
            ),
            [pos_1 - 220, 55, 50, 25],
        )

        # Afficher les labels des statistiques (disposition en deux colonnes)
        GameState.getScreen().blit(
            GameState.getFont("vsmallfont").render(
                GameState.getPhrases()["banshee"]["infoBox"]["strength"],
                1,
                (255, 255, 255),
            ),
            [pos_1 - 220, 75, 50, 25],  # Colonne gauche
        )
        GameState.getScreen().blit(
            GameState.getFont("vsmallfont").render(
                GameState.getPhrases()["banshee"]["infoBox"]["defense"],
                1,
                (255, 255, 255),
            ),
            [pos_1 - 118, 75, 50, 25],  # Colonne droite
        )
        GameState.getScreen().blit(
            GameState.getFont("vsmallfont").render(
                GameState.getPhrases()["banshee"]["infoBox"]["mana"], 1, (255, 255, 255)
            ),
            [pos_1 - 220, 95, 50, 25],  # Colonne gauche
        )
        GameState.getScreen().blit(
            GameState.getFont("vsmallfont").render(
                GameState.getPhrases()["banshee"]["infoBox"]["precision"],
                1,
                (255, 255, 255),
            ),
            [pos_1 - 118, 95, 50, 25],  # Colonne droite
        )

        # Afficher les valeurs des statistiques (alignées à droite dans leurs colonnes)
        # Force
        retirer = (
            GameState.getFont("vsmallfont")
            .render(str(self.force), 1, (255, 255, 255))
            .get_rect()[2]
        )
        GameState.getScreen().blit(
            GameState.getFont("vsmallfont").render(str(self.force), 1, (255, 255, 255)),
            [pos_1 - 129 - retirer, 75, retirer, 25],
        )
        # Défense
        GameState.getScreen().blit(
            GameState.getFont("vsmallfont").render(
                str(self.defence), 1, (255, 255, 255)
            ),
            [pos_2 - 27 - retirer, 75, retirer, 25],
        )

        # Mana
        retirer = (
            GameState.getFont("vsmallfont")
            .render(str(self.mana), 1, (255, 255, 255))
            .get_rect()[2]
        )
        GameState.getScreen().blit(
            GameState.getFont("vsmallfont").render(str(self.mana), 1, (255, 255, 255)),
            [pos_1 - 129 - retirer, 95, retirer, 25],
        )

        # Précision (avec symbole %)
        retirer = (
            GameState.getFont("vsmallfont")
            .render(str(self.prec) + "%", 1, (255, 255, 255))
            .get_rect()[2]
        )
        GameState.getScreen().blit(
            GameState.getFont("vsmallfont").render(
                str(self.prec) + "%", 1, (255, 255, 255)
            ),
            [pos_2 - 27 - retirer, 95, retirer, 25],
        )

        # Mettre à jour et afficher la barre de vie
        self.BarreDeVie.setPv(self.pv)
        self.BarreDeVie.Affiche()

    def affiche_texte(self, texte, liste_joueur, temps):
        duree = temps * 60
        while duree > 0:
            GameState.getClock().tick(60)
            pg.draw.rect(
                GameState.getScreen(),
                (0, 0, 0),
                [0, 0, GameState.getScreenWidth(), GameState.getScreenHeight()],
            )
            for ev in pg.event.get():
                if ev.type == pg.QUIT:
                    pg.quit()
                    duree = 0
                    sys.exit()

                elif ev.type == pg.MOUSEBUTTONDOWN:
                    mouse = pg.mouse.get_pos()
                    if GameState.isOn(
                        "bouton_quit", mouse
                    ) and GameState.getBoutonState("bouton_quit") not in [
                        "Down",
                        "Dead",
                    ]:
                        pg.quit()
                        duree = 0
                        sys.exit()

                elif ev.type == pg.KEYDOWN:
                    if ev.key == pg.K_ESCAPE:
                        if GameState.getMenu() is None:
                            GameState.generateMenu()
                        GameState.setAfficherMenu(True)

            GameState.getScreen().blit(
                GameState.getFont("atkfont").render(texte, 1, (255, 255, 255)),
                [int(GameState.getScreenWidth() / 5), 100],
            )
            for joueur in liste_joueur:
                joueur.boite_info()
            self.boite_info()
            GameState.afficherBouton("bouton_quit")
            if GameState.getAfficherMenu():
                res = GameState.AfficherMenu()
                if res["end"] == 1:
                    newConfig = res["config"]
                    GameState.getMenu().setActive(res["onglet"])
                    GameState.updateGeneral(
                        (int(newConfig["width"]), int(newConfig["height"]))
                    )
                elif res["end"] == 2:
                    GameState.setAfficherMenu(res["Menu"])
            pg.display.flip()
            duree -= 1

    def getpv(self):
        return self.pv

    def setturn(self, turn):
        self.turn = turn


class Night_walker:
    def __init__(self, liste_joueur, posBouton):
        self.nom = GameState.getPhrases()["NW"]["Name"]
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
        pg.draw.rect(
            GameState.getScreen(),
            (0, 0, 0),
            [0, 0, GameState.getScreenWidth(), GameState.getScreenHeight()],
        )
        self.affiche_texte(
            GameState.getPhrases()["NW"]["attack"]["prepare"], liste_joueur, 3
        )
        pg.draw.rect(
            GameState.getScreen(),
            (0, 0, 0),
            [0, 0, GameState.getScreenWidth(), GameState.getScreenHeight()],
        )

        if 100 - (35 - self.prec) < crit <= 100:
            self.affiche_texte(
                GameState.getPhrases()["NW"]["attack"]["fail"], liste_joueur, 4
            )

        elif 0 < crit <= self.prec:
            if 0 < attatype <= 60:
                degats = self.force * 7.5
                self.mana += len(liste_joueur) * 100
                self.affiche_texte(
                    GameState.getPhrases()["NW"]["attack"]["crit"]["phy"][0]
                    + str(target.getnom())
                    + GameState.getPhrases()["NW"]["attack"]["crit"]["phy"][1]
                    + str(degats)
                    + GameState.getPhrases()["NW"]["attack"]["crit"]["phy"][2],
                    liste_joueur,
                    4,
                )

            elif 60 < attatype <= 95 and self.objet_lourd > 0:
                degats = self.force * 15
                self.affiche_texte(
                    GameState.getPhrases()["NW"]["attack"]["crit"]["reinf"][0]
                    + str(target.getnom())
                    + GameState.getPhrases()["NW"]["attack"]["crit"]["reinf"][1]
                    + str(degats)
                    + GameState.getPhrases()["NW"]["attack"]["crit"]["reinf"][2],
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
                    GameState.getPhrases()["NW"]["attack"]["crit"]["mag"][0]
                    + str(target.getnom())
                    + GameState.getPhrases()["NW"]["attack"]["crit"]["mag"][1]
                    + str(degats)
                    + GameState.getPhrases()["NW"]["attack"]["crit"]["mag"][2],
                    liste_joueur,
                    4,
                )

        else:
            if 0 < attatype <= 60:
                degats = self.force * 5
                self.mana += len(liste_joueur) * 50
                self.affiche_texte(
                    GameState.getPhrases()["NW"]["attack"]["norm"]["phy"][0]
                    + str(target.getnom())
                    + GameState.getPhrases()["NW"]["attack"]["norm"]["phy"][1]
                    + str(degats)
                    + GameState.getPhrases()["NW"]["attack"]["norm"]["phy"][2],
                    liste_joueur,
                    4,
                )

            elif 60 < attatype <= 95 and self.objet_lourd > 0:
                degats = self.force * 7.5
                self.affiche_texte(
                    GameState.getPhrases()["NW"]["attack"]["norm"]["reinf"][0]
                    + str(target.getnom())
                    + GameState.getPhrases()["NW"]["attack"]["norm"]["reinf"][1]
                    + str(degats)
                    + GameState.getPhrases()["NW"]["attack"]["norm"]["reinf"][2],
                    liste_joueur,
                    4,
                )
                self.objet_lourd -= 1

            elif 95 < attatype <= 100:
                degats = self.force * 5
                self.ombre += len(liste_joueur)
                self.affiche_texte(
                    GameState.getPhrases()["NW"]["attack"]["norm"]["mag"][0]
                    + str(target.getnom())
                    + GameState.getPhrases()["NW"]["attack"]["norm"]["mag"][1]
                    + str(degats)
                    + GameState.getPhrases()["NW"]["attack"]["norm"]["mag"][2],
                    liste_joueur,
                    4,
                )
        return degats

    def defences(self, degats, liste_joueur):
        crit = random.randint(1, 100)
        deftype = random.randint(1, 100)
        pg.draw.rect(
            GameState.getScreen(),
            (0, 0, 0),
            [0, 0, GameState.getScreenWidth(), GameState.getScreenHeight()],
        )
        self.affiche_texte(
            GameState.getPhrases()["NW"]["defense"]["prepare"], liste_joueur, 3
        )
        pg.draw.rect(
            GameState.getScreen(),
            (0, 0, 0),
            [0, 0, GameState.getScreenWidth(), GameState.getScreenHeight()],
        )

        if self.ombre >= 1:
            self.affiche_texte(
                GameState.getPhrases()["NW"]["defense"]["shadowEscape"], liste_joueur, 3
            )
            self.ombre -= 1

        elif 100 - (35 - self.prec) < crit <= 100 and self.ombre == 0:
            self.affiche_texte(
                GameState.getPhrases()["NW"]["defense"]["fail"], liste_joueur, 3
            )

        elif 0 < crit <= self.prec and self.ombre == 0:
            if 0 < deftype <= 60:
                degats_def = self.defence * 10
                self.affiche_texte(
                    GameState.getPhrases()["NW"]["defense"]["crit"]["phy"][0]
                    + str(degats_def)
                    + GameState.getPhrases()["NW"]["defense"]["crit"]["phy"][1],
                    liste_joueur,
                    3,
                )
                self.pv -= degats - degats_def

            elif 60 < deftype <= 95:
                degats_def = self.defence * 7.5 + 100
                self.affiche_texte(
                    GameState.getPhrases()["NW"]["defense"]["crit"]["reinf"][0]
                    + str(degats_def)
                    + GameState.getPhrases()["NW"]["defense"]["crit"]["reinf"][1],
                    liste_joueur,
                    3,
                )
                self.pv -= degats - degats_def
                self.mana -= 100

            elif 95 < deftype <= 100:
                self.affiche_texte(
                    GameState.getPhrases()["NW"]["defense"]["crit"]["mag"],
                    liste_joueur,
                    3,
                )
                self.ombre += len(liste_joueur)
                self.mana -= 250

        elif self.ombre == 0:
            if 0 < deftype <= 60:
                degats_def = self.defence * 5
                self.affiche_texte(
                    GameState.getPhrases()["NW"]["defense"]["norm"]["phy"][0]
                    + str(degats_def)
                    + GameState.getPhrases()["NW"]["defense"]["norm"]["phy"][1],
                    liste_joueur,
                    3,
                )
                self.pv -= degats - degats_def

            elif 60 < deftype <= 95:
                degats_def = self.defence * 4 + 100
                self.affiche_texte(
                    GameState.getPhrases()["NW"]["defense"]["norm"]["reinf"][0]
                    + str(degats_def)
                    + GameState.getPhrases()["NW"]["defense"]["norm"]["reinf"][1],
                    liste_joueur,
                    3,
                )
                self.pv -= degats - degats_def
                self.mana -= 100

            elif 95 < deftype <= 100:
                degats_def = degats * 0.75
                self.affiche_texte(
                    GameState.getPhrases()["NW"]["defense"]["norm"]["mag"][0]
                    + str(degats_def)
                    + GameState.getPhrases()["NW"]["defense"]["norm"]["mag"][1],
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
            Utilise les variables globales screen, vsmallfont et GameState.getPhrases().
            Comportement spécial pour l'affichage des PV selon self.pv / self.pvbase.
        """
        # Calculer la largeur du texte des PV pour l'alignement
        retirer = (
            GameState.getFont("vsmallfont")
            .render(
                str(self.pv) + GameState.getPhrases()["NW"]["infoBox"]["pv"],
                1,
                (255, 255, 255),
            )
            .get_rect()[2]
        )

        # Définir les positions relatives à la largeur d'écran (côté droit)
        pos_0 = GameState.getScreenWidth() + retirer  # Position de référence pour PV
        pos_1 = GameState.getScreenWidth() - 20  # Position de base côté droit
        pos_2 = GameState.getScreenWidth()  # Bord droit de l'écran

        # Dessiner la bordure verte si c'est le tour du Night Walker
        if self.turn:
            pg.draw.rect(
                GameState.getScreen(), (0, 255, 0), [pos_1 - 13 - 219, 13, 239, 129]
            )

        # Dessiner les couches de fond de la boîte (effet de profondeur)
        pg.draw.rect(
            GameState.getScreen(), (255, 255, 255), [pos_1 - 15 - 215, 15, 235, 125]
        )
        pg.draw.rect(
            GameState.getScreen(), (200, 200, 200), [pos_1 - 18 - 209, 18, 229, 119]
        )
        pg.draw.rect(
            GameState.getScreen(), (170, 170, 170), [pos_1 - 18 - 206, 21, 226, 116]
        )
        pg.draw.rect(
            GameState.getScreen(), (130, 130, 130), [pos_1 - 21 - 203, 21, 223, 113]
        )

        # Dessiner les lignes de séparation
        pg.draw.rect(
            GameState.getScreen(), (50, 50, 50), [pos_1 - 210, 52, 200, 1]
        )  # Horizontale
        pg.draw.rect(
            GameState.getScreen(), (50, 50, 50), [pos_1 - 123, 75, 1, 40]
        )  # Verticale

        # Afficher le nom du Night Walker
        GameState.getScreen().blit(
            GameState.getFont("vsmallfont").render(self.nom, 1, (255, 255, 255)),
            [pos_1 - 220, 30, 50, 25],
        )

        # Logique spéciale d'affichage des PV (masquage stratégique)
        if self.pv < self.pvbase / 4:  # Si PV < 25% du maximum
            # Afficher les PV réels (Night Walker affaibli)
            GameState.getScreen().blit(
                GameState.getFont("vsmallfont").render(
                    str(self.pv) + GameState.getPhrases()["NW"]["infoBox"]["pv"],
                    1,
                    (255, 255, 255),
                ),
                [pos_0 - 79 - retirer, 30, retirer, 25],
            )
        else:
            # Masquer les PV réels avec "?" (Night Walker en bonne santé)
            retirer = (
                GameState.getFont("vsmallfont")
                .render(
                    "?" + GameState.getPhrases()["NW"]["infoBox"]["pv"],
                    1,
                    (255, 255, 255),
                )
                .get_rect()[2]
            )
            GameState.getScreen().blit(
                GameState.getFont("vsmallfont").render(
                    "?" + GameState.getPhrases()["NW"]["infoBox"]["pv"],
                    1,
                    (255, 255, 255),
                ),
                [pos_0 - 79 - retirer, 30, retirer, 25],
            )

        # Afficher le titre "Stats"
        GameState.getScreen().blit(
            GameState.getFont("vsmallfont").render(
                GameState.getPhrases()["NW"]["infoBox"]["stats"], 1, (255, 255, 255)
            ),
            [pos_1 - 220, 55, 50, 25],
        )

        # Afficher les labels des statistiques standard (disposition en deux colonnes)
        GameState.getScreen().blit(
            GameState.getFont("vsmallfont").render(
                GameState.getPhrases()["NW"]["infoBox"]["strength"], 1, (255, 255, 255)
            ),
            [pos_1 - 220, 75, 50, 25],  # Force - colonne gauche
        )
        GameState.getScreen().blit(
            GameState.getFont("vsmallfont").render(
                GameState.getPhrases()["NW"]["infoBox"]["defense"], 1, (255, 255, 255)
            ),
            [pos_1 - 118, 75, 50, 25],  # Défense - colonne droite
        )
        GameState.getScreen().blit(
            GameState.getFont("vsmallfont").render(
                GameState.getPhrases()["NW"]["infoBox"]["mana"], 1, (255, 255, 255)
            ),
            [pos_1 - 220, 95, 50, 25],  # Mana - colonne gauche
        )
        GameState.getScreen().blit(
            GameState.getFont("vsmallfont").render(
                GameState.getPhrases()["NW"]["infoBox"]["precision"], 1, (255, 255, 255)
            ),
            [pos_1 - 118, 95, 50, 25],  # Précision - colonne droite
        )

        # Afficher le label "ombre" (statistique spéciale du Night Walker)
        GameState.getScreen().blit(
            GameState.getFont("vsmallfont").render(
                GameState.getPhrases()["NW"]["infoBox"]["ombre"], 1, (255, 255, 255)
            ),
            [pos_1 - 220, 115, 50, 25],  # Ombre - ligne supplémentaire
        )

        # Afficher les valeurs des statistiques (alignées à droite dans leurs colonnes)
        # Force
        retirer = (
            GameState.getFont("vsmallfont")
            .render(str(self.force), 1, (255, 255, 255))
            .get_rect()[2]
        )
        GameState.getScreen().blit(
            GameState.getFont("vsmallfont").render(str(self.force), 1, (255, 255, 255)),
            [pos_1 - 129 - retirer, 75, retirer, 25],
        )
        # Défense
        GameState.getScreen().blit(
            GameState.getFont("vsmallfont").render(
                str(self.defence), 1, (255, 255, 255)
            ),
            [pos_2 - 27 - retirer, 75, retirer, 25],
        )

        # Mana
        retirer = (
            GameState.getFont("vsmallfont")
            .render(str(self.mana), 1, (255, 255, 255))
            .get_rect()[2]
        )
        GameState.getScreen().blit(
            GameState.getFont("vsmallfont").render(str(self.mana), 1, (255, 255, 255)),
            [pos_1 - 129 - retirer, 95, retirer, 25],
        )

        # Précision (avec symbole %)
        retirer = (
            GameState.getFont("vsmallfont")
            .render(str(self.prec) + "%", 1, (255, 255, 255))
            .get_rect()[2]
        )
        GameState.getScreen().blit(
            GameState.getFont("vsmallfont").render(
                str(self.prec) + "%", 1, (255, 255, 255)
            ),
            [pos_2 - 27 - retirer, 95, retirer, 25],
        )

        # Valeur de la statistique "ombre" (capacité spéciale)
        retirer = (
            GameState.getFont("vsmallfont")
            .render(str(self.ombre), 1, (255, 255, 255))
            .get_rect()[2]
        )
        GameState.getScreen().blit(
            GameState.getFont("vsmallfont").render(str(self.ombre), 1, (255, 255, 255)),
            [pos_2 - 27 - retirer, 115, retirer, 25],
        )

        # Mettre à jour et afficher la barre de vie
        self.BarreDeVie.setPv(self.pv)
        self.BarreDeVie.Affiche()

    def affiche_texte(self, texte, liste_joueur, temps):
        duree = temps * 60
        while duree > 0:
            GameState.getClock().tick(60)
            pg.draw.rect(
                GameState.getScreen(),
                (0, 0, 0),
                [0, 0, GameState.getScreenWidth(), GameState.getScreenHeight()],
            )
            for ev in pg.event.get():
                if ev.type == pg.QUIT:
                    pg.quit()
                    duree = 0
                    sys.exit()

                elif ev.type == pg.MOUSEBUTTONDOWN:
                    mouse = pg.mouse.get_pos()
                    if GameState.isOn(
                        "bouton_quit", mouse
                    ) and GameState.getBoutonState("bouton_quit") not in [
                        "Down",
                        "Dead",
                    ]:
                        pg.quit()
                        duree = 0
                        sys.exit()
                elif ev.type == pg.KEYDOWN:
                    if ev.key == pg.K_ESCAPE:
                        if GameState.getMenu() is None:
                            GameState.generateMenu()
                        GameState.setAfficherMenu(True)

            GameState.getScreen().blit(
                GameState.getFont("atkfont").render(texte, 1, (255, 255, 255)),
                [int(GameState.getScreenWidth() / 5), 100],
            )
            for joueur in liste_joueur:
                joueur.boite_info()
            self.boite_info()
            GameState.afficherBouton("bouton_quit")
            if GameState.getAfficherMenu():
                res = GameState.AfficherMenu()
                if res["end"] == 1:
                    newConfig = res["config"]
                    GameState.getMenu().setActive(res["onglet"])
                    GameState.updateGeneral(
                        (int(newConfig["width"]), int(newConfig["height"]))
                    )
                elif res["end"] == 2:
                    GameState.setAfficherMenu(res["Menu"])
            pg.display.flip()
            duree -= 1

    def getpv(self):
        return self.pv

    def setpv(self, pv):
        self.pv = pv

    def setturn(self, turn):
        self.turn = turn


class Texte_Histoire:
    def __init__(self, heighttop, texte, font):
        self.widthtop = GameState.getScreenWidth() / 2
        self.heighttop = heighttop
        self.texte = texte
        self.font = font
        self.color = (255, 255, 255)
        self.state = 2

    def afficher(self):
        if self.state == 1 or self.state == 3:
            self.widthtop = GameState.getScreenWidth() / 2
            text = GameState.getFont("atkfont").render(self.texte, True, self.color)
            text_rect = text.get_rect(center=(self.widthtop, self.heighttop))
            GameState.getScreen().blit(text, text_rect)
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
        self.bouton_quit = GameState.getBouton("bouton_quit")
        self.bouton_skip = GameState.getBouton("bouton_skip")
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
            GameState.getClock().tick(30)
            pg.draw.rect(
                GameState.getScreen(),
                (0, 0, 0),
                [0, 0, GameState.getScreenWidth(), GameState.getScreenHeight()],
            )
            self.bouton_quit.setsize((6, 10), self.posBouton)
            self.bouton_skip.setsize((6, 9), self.posBouton)
            coordsSkip = self.bouton_skip.getpose()
            for ev in pg.event.get():
                if ev.type == pg.QUIT:
                    pg.quit()
                    game_over = False
                    sys.exit()

                elif ev.type == pg.MOUSEBUTTONDOWN:
                    mouse = pg.mouse.get_pos()
                    if self.bouton_quit.isOn(
                        mouse
                    ) and self.bouton_quit.getstate() not in ["Down", "Dead"]:
                        pg.quit()
                        game_over = False
                        sys.exit()

                    elif self.bouton_skip.isOn(
                        mouse
                    ) and self.bouton_skip.getstate() not in ["Down", "Dead"]:
                        game_over = False
                elif ev.type == pg.KEYDOWN:
                    if ev.key == pg.K_ESCAPE:
                        if GameState.getMenu() is None:
                            GameState.generateMenu()
                        GameState.setAfficherMenu(True)
                    if ev.key == pg.K_RETURN:
                        down = True
                elif ev.type == pg.KEYUP:
                    if ev.key == pg.K_RETURN:
                        down = False

            pg.gfxdraw.arc(
                GameState.getScreen(),
                coordsSkip["coord"][0],
                coordsSkip["coord"][1] - coordsSkip["height"],
                floor((coordsSkip["height"] - 10) / 2),
                0,
                180,
                (90, 90, 90),
            )
            pg.gfxdraw.arc(
                GameState.getScreen(),
                coordsSkip["coord"][0],
                coordsSkip["coord"][1] - coordsSkip["height"],
                floor((coordsSkip["height"] - 10) / 2),
                180,
                360,
                (90, 90, 90),
            )
            if down:
                if skip >= 45:
                    game_over = False
                skip += 1
            elif skip >= 0:
                skip -= 1
            for loop in self.texte:
                loop.afficher()

            if game_over and skip > 0:
                pg.gfxdraw.arc(
                    GameState.getScreen(),
                    coordsSkip["coord"][0],
                    coordsSkip["coord"][1] - coordsSkip["height"],
                    floor((coordsSkip["height"] - 9) / 2),
                    -90,
                    -90 + floor(180 / 45 * skip),
                    (255, 255, 255),
                )
                pg.gfxdraw.arc(
                    GameState.getScreen(),
                    coordsSkip["coord"][0],
                    coordsSkip["coord"][1] - coordsSkip["height"],
                    floor((coordsSkip["height"] - 10) / 2),
                    -90,
                    -90 + floor(180 / 45 * skip),
                    (255, 255, 255),
                )
                pg.gfxdraw.arc(
                    GameState.getScreen(),
                    coordsSkip["coord"][0],
                    coordsSkip["coord"][1] - coordsSkip["height"],
                    floor((coordsSkip["height"] - 11) / 2),
                    -90,
                    -90 + floor(180 / 45 * skip),
                    (255, 255, 255),
                )

                pg.gfxdraw.arc(
                    GameState.getScreen(),
                    coordsSkip["coord"][0],
                    coordsSkip["coord"][1] - coordsSkip["height"],
                    floor((coordsSkip["height"] - 9) / 2),
                    90,
                    90 + floor(180 / 45 * skip),
                    (255, 255, 255),
                )
                pg.gfxdraw.arc(
                    GameState.getScreen(),
                    coordsSkip["coord"][0],
                    coordsSkip["coord"][1] - coordsSkip["height"],
                    floor((coordsSkip["height"] - 10) / 2),
                    90,
                    90 + floor(180 / 45 * skip),
                    (255, 255, 255),
                )
                pg.gfxdraw.arc(
                    GameState.getScreen(),
                    coordsSkip["coord"][0],
                    coordsSkip["coord"][1] - coordsSkip["height"],
                    floor((coordsSkip["height"] - 11) / 2),
                    90,
                    90 + floor(180 / 45 * skip),
                    (255, 255, 255),
                )

            self.bouton_skip.affiche_bouton()
            self.bouton_quit.affiche_bouton()
            if GameState.getAfficherMenu():
                res = GameState.AfficherMenu()
                if res["end"] == 1:
                    newConfig = res["config"]
                    GameState.getMenu().setActive(res["onglet"])
                    GameState.updateGeneral(
                        (int(newConfig["width"]), int(newConfig["height"]))
                    )
                elif res["end"] == 2:
                    GameState.setAfficherMenu(res["Menu"])

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
            GameState.getScreen(),
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
            GameState.getScreen(),
            900,
            y - 16,
            100,
            100,
            fontSize=30,
            textColour=(240, 240, 240),
            colour=(0, 0, 0),
        )
        self.textMax = TextBox(
            GameState.getScreen(),
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
            GameState.getScreen(),
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
                GameState.getScreen(),
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
                GameState.getScreen(),
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
            GameState.getScreen(),
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
            GameState.getScreen(),
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
                GameState.getScreen(),
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
                GameState.getScreen(),
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
        width = GameState.getScreenWidth()
        if (
            self.name == GameState.getPhrases()["NW"]["Name"]
            and self.pv > self.pvAffiche
        ):
            completedColour = (100, 100, 100)
        else:
            completedColour = (200, 0, 0)
        progressBar = ProgressBar(
            GameState.getScreen(),
            width / 4,
            50,
            width / 2,
            18,
            lambda: (self.pv / self.pvbase),
            curved=True,
            completedColour=completedColour,
        )
        pg.draw.polygon(
            GameState.getScreen(),
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
            GameState.getScreen(),
            (255, 215, 0),
            [
                (width / 16 * 4 - 3, 59),
                (width / 16 * 4 - 16, 59),
                (width / 16 * 4 - 4, 68),
                (width / 16 * 4 + 2, 68),
            ],
        )

        pg.draw.polygon(
            GameState.getScreen(),
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
            GameState.getScreen(),
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
        width = GameState.getScreenWidth()
        pg.draw.rect(
            GameState.getScreen(),
            (218, 165, 32),
            [width / 2 - self.width / 2, 40, self.width, 8],
        )
        pg.draw.rect(
            GameState.getScreen(),
            (255, 210, 0),
            [width / 2 - self.width / 2, 44, self.width, 4],
        )
        pg.draw.rect(
            GameState.getScreen(),
            (218, 165, 32),
            [width / 2 - self.width / 2 - 8, 40 - 8, 8, 8],
        )
        pg.draw.rect(
            GameState.getScreen(),
            (218, 165, 32),
            [width / 2 + self.width / 2, 40 - 8, 8, 8],
        )
        pg.draw.polygon(
            GameState.getScreen(),
            (255, 215, 0),
            [
                (width / 2 - self.width / 2 - 8, 33),
                (width / 2 - self.width / 2, 40),
                (width / 2 - self.width / 2 - 8, 40),
            ],
        )
        pg.draw.polygon(
            GameState.getScreen(),
            (255, 215, 0),
            [
                (width / 2 + self.width / 2 + 7, 33),
                (width / 2 + self.width / 2 + 7, 40),
                (width / 2 + self.width / 2, 40),
            ],
        )
        nom = GameState.getFont("bigfont").render(self.name, True, (200, 200, 200))
        nom_rect = nom.get_rect(center=(width / 2, 20))
        GameState.getScreen().blit(nom, nom_rect)

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


def banshee_fight(liste_joueur, nb_joueur):
    banshee = Banshee(liste_joueur, GameState.getPosBoutons())
    for joueur in liste_joueur:
        joueur.boite_info()
    banshee.boite_info()
    pg.display.flip()

    while GameState.getGameOverFight() == 0:
        joueur_att = banshee.choose_target(liste_joueur)
        degats_infliges = banshee.attack(joueur_att, liste_joueur)

        if not 95 < degats_infliges[1] <= 100:
            banshee.setturn(False)
            joueur_att.setturn(True)
            joueur_att.defences(
                degats_infliges[0],
                banshee,
                liste_joueur,
            )
            joueur_att.setturn(False)

        for joueur in liste_joueur:
            joueur.setturn(True)
            dgt_joueur = joueur.attack(banshee, liste_joueur)
            joueur.setturn(False)
            banshee.setturn(True)
            banshee.defences(dgt_joueur, liste_joueur)
            banshee.setturn(False)

            for joueur in liste_joueur[:]:  # éviter bug de suppression
                if joueur.getpv() <= 0:
                    del liste_joueur[joueur.getid() - 1]

            if len(liste_joueur) == 0:
                pg.draw.rect(
                    GameState.getScreen(),
                    (0, 0, 0),
                    [0, 0, GameState.getScreenWidth(), GameState.getScreenHeight()],
                )
                GameState.getScreen().blit(
                    GameState.getFont("atkfont").render(
                        GameState.getPhrases()["banshee"]["attack"]["defense"]["fail"][
                            0
                        ],
                        1,
                        (255, 255, 255),
                    ),
                    [int(GameState.getScreenWidth() / 5), 100],
                )
                GameState.getScreen().blit(
                    GameState.getFont("atkfont").render(
                        GameState.getPhrases()["banshee"]["attack"]["defense"]["fail"][
                            1
                        ],
                        1,
                        (255, 255, 255),
                    ),
                    [int(GameState.getScreenWidth() / 5), 130],
                )
                pg.display.flip()
                pg.time.delay(1500)
                GameState.setGameOverFight(1)
                break

            if banshee.getpv() <= 0:
                pg.draw.rect(
                    GameState.getScreen(),
                    (0, 0, 0),
                    [0, 0, GameState.getScreenWidth(), GameState.getScreenHeight()],
                )
                if len(liste_joueur) < nb_joueur:
                    GameState.getScreen().blit(
                        GameState.getFont("atkfont").render(
                            GameState.getPhrases()["banshee"]["Fight"]["HalfWin"],
                            1,
                            (255, 255, 255),
                        ),
                        [int(GameState.getScreenWidth() / 5), 100],
                    )
                else:
                    GameState.getScreen().blit(
                        GameState.getFont("atkfont").render(
                            GameState.getPhrases()["banshee"]["Fight"]["Win"],
                            1,
                            (255, 255, 255),
                        ),
                        [int(GameState.getScreenWidth() / 5), 100],
                    )
                pg.display.flip()
                pg.time.delay(1500)
                GameState.setGameOverFight(1)
                break


def NW_fight(liste_joueur, nb_joueur):
    NW = Night_walker(liste_joueur, GameState.getPosBoutons())
    for joueur in liste_joueur:
        joueur.boite_info()
    NW.boite_info()
    pg.display.flip()

    while GameState.getGameOverFight() == 0:
        joueur_att = NW.choose_target(liste_joueur)
        degats_infliges = NW.attack(joueur_att, liste_joueur)
        joueur_att.setturn(True)
        NW.setturn(False)
        joueur_att.defences(degats_infliges, NW, liste_joueur)
        joueur_att.setturn(False)
        NW.setturn(True)

        joueur_att = NW.choose_target(liste_joueur)
        degats_infliges = NW.attack(joueur_att, liste_joueur)
        joueur_att.setturn(True)
        NW.setturn(False)
        joueur_att.defences(degats_infliges, NW, liste_joueur)
        joueur_att.setturn(False)
        NW.setturn(False)

        for joueur in liste_joueur:
            joueur.setturn(True)
            dgt_joueur = joueur.attack(NW, liste_joueur)
            joueur.setturn(False)
            NW.setturn(True)
            NW.defences(dgt_joueur, liste_joueur)
            NW.setturn(False)

        for joueur in liste_joueur[:]:  # éviter bug de suppression en itération
            if joueur.getpv() <= 0:
                del liste_joueur[joueur.getid() - 1]

        if len(liste_joueur) == 0:
            pg.draw.rect(
                GameState.getScreen(),
                (0, 0, 0),
                [0, 0, GameState.getScreenWidth(), GameState.getScreenHeight()],
            )
            GameState.getScreen().blit(
                GameState.getFont("atkfont").render(
                    GameState.getPhrases()["NW"]["Fight"]["Lose"][0], 1, (255, 255, 255)
                ),
                [int(GameState.getScreenWidth() / 5), 100],
            )
            GameState.getScreen().blit(
                GameState.getFont("atkfont").render(
                    GameState.getPhrases()["NW"]["Fight"]["Lose"][1], 1, (255, 255, 255)
                ),
                [int(GameState.getScreenWidth() / 5), 130],
            )
            pg.display.flip()
            pg.time.delay(1500)
            GameState.setGameOverFight(1)
            break

        if NW.getpv() <= 0:
            pg.draw.rect(
                GameState.getScreen(),
                (0, 0, 0),
                [0, 0, GameState.getScreenWidth(), GameState.getScreenHeight()],
            )
            if len(liste_joueur) < nb_joueur:
                GameState.getScreen().blit(
                    GameState.getFont("atkfont").render(
                        GameState.getPhrases()["NW"]["Fight"]["HalfWin"],
                        1,
                        (255, 255, 255),
                    ),
                    [int(GameState.getScreenWidth() / 5), 100],
                )
            else:
                GameState.getScreen().blit(
                    GameState.getFont("atkfont").render(
                        GameState.getPhrases()["NW"]["Fight"]["Win"], 1, (255, 255, 255)
                    ),
                    [int(GameState.getScreenWidth() / 5), 100],
                )
            pg.display.flip()
            pg.time.delay(1500)
            GameState.setGameOverFight(1)
            break


def nbperso(perso, selecPerso):
    (
        GameState.afficherBouton("bouton_1"),
        GameState.afficherBouton("bouton_2"),
        GameState.afficherBouton("bouton_3"),
        GameState.afficherBouton("bouton_4"),
    )
    if not selecPerso:
        if perso == 0:
            GameState.getScreen().blit(
                GameState.getFont("atkfont").render(
                    GameState.getPhrases()["Creation"]["NbPerso"][0],
                    True,
                    (255, 255, 255),
                ),
                (15, 15),
            )
            return None
        else:
            GameState.getScreen().blit(
                GameState.getFont("atkfont").render(
                    GameState.getPhrases()["Creation"]["NbPerso"][1] + str(perso),
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
        GameState.getScreen().blit(
            GameState.getFont("atkfont").render(
                GameState.getPhrases()["Creation"]["Name"][0] + str(nom),
                True,
                (255, 255, 255),
            ),
            (15, 15),
        )
        return None
    else:
        GameState.getScreen().blit(
            GameState.getFont("atkfont").render(
                GameState.getPhrases()["Creation"]["Name"][1] + str(nom),
                True,
                (255, 255, 255),
            ),
            (15, 15),
        )
        selecNOM = True
        return selecNOM


def nbpv(pv, selecPV):
    (
        GameState.afficherBouton("bouton_1"),
        GameState.afficherBouton("bouton_2"),
        GameState.afficherBouton("bouton_3"),
        GameState.afficherBouton("bouton_4"),
    )
    if not selecPV:
        if pv == 0:
            GameState.getScreen().blit(
                GameState.getFont("atkfont").render(
                    GameState.getPhrases()["Creation"]["PV"][0], True, (255, 255, 255)
                ),
                (15, 15),
            )
            return None
        else:
            GameState.getScreen().blit(
                GameState.getFont("atkfont").render(
                    GameState.getPhrases()["Creation"]["PV"][1][0]
                    + str(pv)
                    + GameState.getPhrases()["Creation"]["PV"][1][1],
                    True,
                    (255, 255, 255),
                ),
                (15, 15),
            )
            selecPV = True
            return selecPV
    return None


def nbmana(mana, selecMana):
    (
        GameState.afficherBouton("bouton_1"),
        GameState.afficherBouton("bouton_2"),
        GameState.afficherBouton("bouton_3"),
        GameState.afficherBouton("bouton_4"),
    )
    if not selecMana:
        if mana == 0:
            GameState.getScreen().blit(
                GameState.getFont("atkfont").render(
                    GameState.getPhrases()["Creation"]["Mana"][0], True, (255, 255, 255)
                ),
                (15, 15),
            )
            return None
        else:
            GameState.getScreen().blit(
                GameState.getFont("atkfont").render(
                    GameState.getPhrases()["Creation"]["Mana"][1][0]
                    + str(mana)
                    + GameState.getPhrases()["Creation"]["Mana"][1][1],
                    True,
                    (255, 255, 255),
                ),
                (15, 15),
            )
            selecMana = True
            return selecMana
    return None


def nbstats(stats, force, Def, prec, selecStats, sliders):
    GameState.afficherBouton("bouton_1")
    if sliders.getTot() > 100:
        GameState.setBoutonState("bouton_1", "Down")
    else:
        GameState.setBoutonState("bouton_1", "")
    if not selecStats:
        if stats == 0:
            GameState.getScreen().blit(
                GameState.getFont("atkfont").render(
                    GameState.getPhrases()["Creation"]["Stats"]["Question"],
                    True,
                    (255, 255, 255),
                ),
                (15, 15),
            )
            sliders.afficheSlider()
            return None
        else:
            GameState.getScreen().blit(
                GameState.getFont("atkfont").render(
                    GameState.getPhrases()["Creation"]["Stats"]["Response"]["Str"][0]
                    + str(force)
                    + GameState.getPhrases()["Creation"]["Stats"]["Response"]["Str"][1],
                    True,
                    (255, 255, 255),
                ),
                (15, 15),
            )
            GameState.getScreen().blit(
                GameState.getFont("atkfont").render(
                    GameState.getPhrases()["Creation"]["Stats"]["Response"]["Def"][0]
                    + str(Def)
                    + GameState.getPhrases()["Creation"]["Stats"]["Response"]["Def"][1],
                    True,
                    (255, 255, 255),
                ),
                (15, 45),
            )
            GameState.getScreen().blit(
                GameState.getFont("atkfont").render(
                    GameState.getPhrases()["Creation"]["Stats"]["Response"]["Prec"][0]
                    + str(prec)
                    + GameState.getPhrases()["Creation"]["Stats"]["Response"]["Prec"][
                        1
                    ],
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
    msg = GameState.getFont("smallfont").render(
        GameState.getPhrases()["J"]["info"]["attack"][0], 1, (255, 255, 255)
    )
    text_rect = msg.get_rect(
        center=(GameState.getScreenWidth() / 2, GameState.getScreenHeight() / 2 - 50)
    )
    GameState.getScreen().blit(msg, text_rect)


def info_defence():
    msg = GameState.getFont("smallfont").render(
        GameState.getPhrases()["J"]["info"]["defense"][0], 1, (255, 255, 255)
    )
    text_rect = msg.get_rect(
        center=(GameState.getScreenWidth() / 2, GameState.getScreenHeight() / 2 + 50)
    )
    GameState.getScreen().blit(msg, text_rect)


def Jouer():
    """
    La fonction Jouer permet de lancer le jeu (créer les personnages entre 1 et 4, de donner les informations essentielles au jeu et de lancer la partie)
    Aucune entrée et sortie
    Pour le moment ne fait que combattre le / les joueur(s) contre la banshee ou Le marcheur de la nuit
    """
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
    loop = 0
    regles = False
    hist = 1
    sliders = GestionSlider(
        SliderS(100, 200, 600, 20, 90),
        SliderS(100, 300, 600, 20, 90),
        SliderS(100, 400, 600, 20, 25),
    )

    while GameState.getGameOverJouer() == 0:
        GameState.getClock().tick(60)
        pg.draw.rect(
            GameState.getScreen(),
            (0, 0, 0),
            [0, 0, GameState.getScreenWidth(), GameState.getScreenHeight()],
        )

        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                pg.quit()
                GameState.setGameOverJouer(3)
                sys.exit()

            elif ev.type == pg.MOUSEBUTTONDOWN:
                mouse = pg.mouse.get_pos()
                if not GameState.getAfficherMenu():
                    if GameState.isOn(
                        "bouton_quit", mouse
                    ) and GameState.getBoutonState("bouton_quit") not in [
                        "Down",
                        "Dead",
                    ]:
                        pg.quit()
                        GameState.setGameOverJouer(3)
                        sys.exit()

                    elif (
                        GameState.isOn("bouton_1", mouse)
                        and GameState.getBoutonState("bouton_1") == ""
                    ):
                        if not selecPerso:
                            perso = 1

                        elif not selecPV:
                            pv = 2500
                            (
                                GameState.setBoutonState("bouton_2", "Down"),
                                GameState.setBoutonState("bouton_3", "Down"),
                                GameState.setBoutonState("bouton_4", "Down"),
                            )

                        elif not selecMana and 3000 - pv == 500:
                            mana = 500

                        elif not selecStat:
                            force = sliders.getStr()
                            Def = sliders.getDef()
                            prec = sliders.getPrec()
                            stats = 1

                    elif (
                        GameState.isOn("bouton_2", mouse)
                        and GameState.getBoutonState("bouton_2") == ""
                    ):
                        if not selecPerso:
                            perso = 2

                        elif not selecPV:
                            pv = 2000
                            (
                                GameState.setBoutonState("bouton_1", "Down"),
                                GameState.setBoutonState("bouton_3", "Down"),
                                GameState.setBoutonState("bouton_4", "Down"),
                            )

                        elif not selecMana and 3000 - pv == 1000:
                            mana = 1000

                    elif (
                        GameState.isOn("bouton_3", mouse)
                        and GameState.getBoutonState("bouton_3") == ""
                    ):
                        if not selecPerso:
                            perso = 3

                        elif not selecPV:
                            pv = 1500
                            (
                                GameState.setBoutonState("bouton_1", "Down"),
                                GameState.setBoutonState("bouton_2", "Down"),
                                GameState.setBoutonState("bouton_4", "Down"),
                            )

                        elif not selecMana and 3000 - pv == 1500:
                            mana = 1500

                    elif (
                        GameState.isOn("bouton_4", mouse)
                        and GameState.getBoutonState("bouton_4") == ""
                    ):
                        if not selecPerso:
                            perso = 4

                        elif not selecPV:
                            pv = 1000
                            (
                                GameState.setBoutonState("bouton_1", "Down"),
                                GameState.setBoutonState("bouton_2", "Down"),
                                GameState.setBoutonState("bouton_3", "Down"),
                            )

                        elif not selecMana and 3000 - pv == 2000:
                            mana = 2000

            if ev.type == pg.KEYDOWN:
                if ev.key == pg.K_ESCAPE:
                    if GameState.getMenu() is None:
                        GameState.generateMenu()
                    GameState.setAfficherMenu(True)
                elif ev.key == pg.K_BACKSPACE:
                    name = name[:-1]
                elif ev.key == pg.K_RETURN:
                    selecNOM = True
                    (
                        GameState.getBouton("bouton_1").settexte("2500"),
                        GameState.getBouton("bouton_2").settexte("2000"),
                        GameState.getBouton("bouton_3").settexte("1500"),
                        GameState.getBouton("bouton_4").settexte("1000"),
                    )

            if ev.type == pg.TEXTINPUT:
                name += ev.text  # Ajoute le texte Unicode directement

        GameState.afficherBouton("bouton_quit")
        if GameState.getAfficherMenu():
            res = GameState.AfficherMenu()
            if res["end"] == 1:
                newConfig = res["config"]
                GameState.getMenu().setActive(res["onglet"])
                GameState.updateGeneral(
                    (int(newConfig["width"]), int(newConfig["height"]))
                )
            elif res["end"] == 2:
                GameState.setAfficherMenu(res["Menu"])

        while not regles:
            for ev in pg.event.get():
                if ev.type == pg.QUIT:
                    pg.quit()
                    GameState.setGameOverJouer(3)
                    sys.exit()
                elif ev.type == pg.MOUSEBUTTONDOWN:
                    mouse = pg.mouse.get_pos()
                    if GameState.isOn(
                        "bouton_quit", mouse
                    ) and GameState.getBoutonState("bouton_quit") not in [
                        "Down",
                        "Dead",
                    ]:
                        pg.quit()
                        GameState.setGameOverJouer(3)
                        sys.exit()
                    elif GameState.isOn(
                        "bouton_compris", mouse
                    ) and GameState.getBoutonState("bouton_compris") not in [
                        "Down",
                        "Dead",
                    ]:
                        regles = True

                elif ev.type == pg.KEYDOWN:
                    if ev.key == pg.K_ESCAPE:
                        if GameState.getMenu() is None:
                            GameState.generateMenu()
                        GameState.setAfficherMenu(True)
                    if ev.key == K_RETURN:
                        regles = True
            pg.draw.rect(
                GameState.getScreen(),
                (0, 0, 0),
                [0, 0, GameState.getScreenWidth(), GameState.getScreenHeight()],
            )
            info_attaque()
            info_defence()
            GameState.afficherBouton("bouton_quit")
            GameState.afficherBouton("bouton_compris")
            if GameState.getAfficherMenu():
                res = GameState.AfficherMenu()
                if res["end"] == 1:
                    newConfig = res["config"]
                    GameState.getMenu().setActive(res["onglet"])
                    GameState.updateGeneral(
                        (int(newConfig["width"]), int(newConfig["height"]))
                    )
                elif res["end"] == 2:
                    GameState.setAfficherMenu(res["Menu"])
            pg.display.flip()

        if not selecPerso:
            selecPerso = nbperso(perso, selecPerso)
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
                    selecPV = nbpv(pv, selecPV)
                    if selecPV:
                        (
                            GameState.getBouton("bouton_1").settexte("500"),
                            GameState.getBouton("bouton_2").settexte("1000"),
                            GameState.getBouton("bouton_3").settexte("1500"),
                            GameState.getBouton("bouton_4").settexte("2000"),
                        )
                        pg.display.flip()
                        pg.time.delay(1000)
                    pg.display.flip()

                if (not selecMana) and selecPV:
                    selecMana = nbmana(mana, selecMana)
                    if selecMana:
                        GameState.getBouton("bouton_1").settexte(
                            GameState.getPhrases()["Bouton"]["Validate"]
                        )
                        (
                            GameState.setBoutonState("bouton_1", ""),
                            GameState.setBoutonState("bouton_2", ""),
                            GameState.setBoutonState("bouton_3", ""),
                            GameState.setBoutonState("bouton_4", ""),
                        )
                        pg.display.flip()
                        pg.time.delay(1000)
                    pg.display.flip()

                if (not selecStat) and selecMana:
                    selecStat = nbstats(stats, force, Def, prec, selecStat, sliders)
                    if selecStat:
                        pg.display.flip()
                        pg.time.delay(1000)
                    pg.display.flip()

                if selecStat and loop == 0:
                    J1 = creation_perso(
                        name,
                        pv,
                        mana,
                        force,
                        Def,
                        prec,
                        1,
                        GameState.getPosBoutons(),
                        False,
                    )
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
                    J2 = creation_perso(
                        name,
                        pv,
                        mana,
                        force,
                        Def,
                        prec,
                        2,
                        GameState.getPosBoutons(),
                        False,
                    )
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
                    J3 = creation_perso(
                        name,
                        pv,
                        mana,
                        force,
                        Def,
                        prec,
                        3,
                        GameState.getPosBoutons(),
                        False,
                    )
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
                    J4 = creation_perso(
                        name,
                        pv,
                        mana,
                        force,
                        Def,
                        prec,
                        4,
                        GameState.getPosBoutons(),
                        False,
                    )
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
                        NW = Night_walker(liste_joueur, GameState.getPosBoutons())
                        histo = Histoire(
                            GameState.getPhrases()["NW"]["Hist"],
                            GameState.getFont("atkfont"),
                            GameState.getPosBoutons(),
                            GameState.getScreen(),
                        )
                        histo.affiche_histoire()
                        hist = 0

                    for joueur in liste_joueur:
                        joueur.boite_info()
                    NW.boite_info()
                    pg.display.flip()
                    GameState.setGameOverJouer(1)
                    NW_fight(liste_joueur, len(liste_joueur))

                if adversaire_selec == 2:
                    if hist == 1:
                        banshee = Banshee(liste_joueur, GameState.getPosBoutons())
                        histo = Histoire(
                            GameState.getPhrases()["banshee"]["Hist"],
                            GameState.getFont("atkfont"),
                            GameState.getPosBoutons(),
                            GameState.getScreen(),
                        )
                        histo.affiche_histoire()
                        hist = 0
                    for joueur in liste_joueur:
                        joueur.boite_info()
                    banshee.boite_info()
                    pg.display.flip()
                    GameState.setGameOverJouer(1)
                    banshee_fight(liste_joueur, len(liste_joueur))


def JouerBoucle():
    bouton_oui = Bouton((2, 6), "Oui", (0, 200, 0), "", GameState.getPosBoutons())
    bouton_non = Bouton((4, 6), "Non", (200, 0, 0), "", GameState.getPosBoutons())
    while GameState.getRunningBoucle():
        pg.draw.rect(
            GameState.getScreen(),
            (0, 0, 0),
            [0, 0, GameState.getScreenWidth(), GameState.getScreenHeight()],
        )

        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                pg.quit()
                sys.exit()

            elif ev.type == pg.MOUSEBUTTONDOWN:
                mouse = pg.mouse.get_pos()
                if bouton_non.isOn(mouse):
                    pg.quit()
                    GameState.setRunningBoucle(False)
                    sys.exit()

                elif bouton_oui.isOn(mouse):
                    GameState.setReplay(True)
                    GameState.setRunningBoucle(False)

                elif bouton_non.isOn(mouse):
                    GameState.setRunningBoucle(False)

            elif ev.type == pg.KEYDOWN:
                if ev.key == pg.K_ESCAPE:
                    if GameState.getMenu() is None:
                        GameState.generateMenu()
                    GameState.setAfficherMenu(True)

        text = GameState.getFont("smallfont").render(
            GameState.getPhrases()["Boucle"]["Question"], True, (255, 255, 255)
        )
        text_rect = text.get_rect(
            center=(
                GameState.getScreenWidth() / 2,
                GameState.getScreenHeight() / 2 - 20,
            )
        )
        GameState.getScreen().blit(text, text_rect)
        GameState.afficherBouton("bouton_oui")
        GameState.afficherBouton("bouton_oui")
        if GameState.getAfficherMenu():
            res = GameState.AfficherMenu()
            if res["end"] == 1:
                newConfig = res["config"]
                GameState.setNewConfig(newConfig)
                GameState.getMenu().setActive(res["onglet"])
                GameState.updateGeneral(
                    (int(newConfig["width"]), int(newConfig["height"]))
                )
                if res["save"]:
                    config.sauvegarder_config(newConfig)
                    GameState.setConfig(config.charger_config())
                    GameState.setNewConfig(None)
            elif res["end"] == 2:
                GameState.setAfficherMenu(res["Menu"])
        pg.display.flip()

    return GameState.getReplay()


def afficher_nom_jeu():
    screen_w_2_10 = GameState.getScreenWidth() / 2 - GameState.getScreenWidth() / 10
    screen_w_5 = GameState.getScreenWidth() / 5
    screen_h_10 = GameState.getScreenHeight() / 10
    pg.draw.rect(
        GameState.getScreen(),
        (120, 120, 120),
        [screen_w_2_10 - 10, 40, screen_w_5 + 20, screen_h_10 + 20],
    )
    for loop in range(10):
        pg.draw.rect(
            GameState.getScreen(),
            (180, 180, 180),
            [screen_w_2_10 - 10, 40 + loop, screen_w_5 + 20 - loop, 1],
        )

    for loop in range(10):
        pg.draw.rect(
            GameState.getScreen(),
            (180, 180, 180),
            [screen_w_2_10 - 10 + loop, 50, 1, screen_h_10 + 10 - loop],
        )
    center_rect = pg.draw.rect(
        GameState.getScreen(),
        (150, 150, 150),
        [
            GameState.getScreenWidth() / 2 - GameState.getScreenWidth() / 10,
            50,
            GameState.getScreenWidth() / 5,
            GameState.getScreenHeight() / 10,
        ],
    )
    surf_texte = GameState.getFont("bigfont").render("D&D?", 1, (255, 255, 255))
    rect_texte = surf_texte.get_rect()
    rect_texte.center = center_rect.center
    GameState.getScreen().blit(surf_texte, rect_texte)


def jouer_bloc():
    screen_w_2_10 = GameState.getScreenWidth() / 2 - GameState.getScreenWidth() / 10
    screen_w_5 = GameState.getScreenWidth() / 5
    screen_h_2_8 = GameState.getScreenHeight() / 2 - GameState.getScreenHeight() / 8
    screen_h_4 = GameState.getScreenHeight() / 4
    pg.draw.rect(
        GameState.getScreen(),
        (120, 120, 120),
        [screen_w_2_10 - 10, screen_h_2_8 - 10, screen_w_5 + 20, screen_h_4 + 20],
    )
    pg.draw.rect(
        GameState.getScreen(),
        (150, 150, 150),
        [screen_w_2_10, screen_h_2_8, screen_w_5, screen_h_4],
    )
    for loop in range(10):
        pg.draw.rect(
            GameState.getScreen(),
            (180, 180, 180),
            [screen_w_2_10 - 10, screen_h_2_8 - 10 + loop, screen_w_5 + 20 - loop, 1],
        )
    for loop in range(10):
        pg.draw.rect(
            GameState.getScreen(),
            (180, 180, 180),
            [screen_w_2_10 - 10 + loop, screen_h_2_8 - 5, 1, screen_h_4 + 15 - loop],
        )
    GameState.afficherBouton("bouton_Jouer")
    GameState.afficherBouton("bouton_quit")


while GameState.getRunning():
    GameState.getClock().tick(60)
    pg.draw.rect(
        GameState.getScreen(),
        (0, 0, 0),
        [0, 0, GameState.getScreenWidth(), GameState.getScreenHeight()],
    )
    for ev in pg.event.get():
        if ev.type == pg.QUIT:
            pg.quit()
            GameState.setRunning(False)
            sys.exit()

        elif ev.type == pg.MOUSEBUTTONDOWN:
            mouse = pg.mouse.get_pos()
            if not GameState.getAfficherMenu():
                if GameState.isOn("bouton_quit", mouse) and GameState.getBoutonState(
                    "bouton_quit"
                ) not in [
                    "Down",
                    "Dead",
                ]:
                    pg.quit()
                    running = False
                    sys.exit()
                elif GameState.isOn("bouton_Jouer", mouse):
                    Jouer()
                    ask = True

        elif ev.type == pg.KEYDOWN:
            if ev.key == pg.K_ESCAPE:
                if GameState.getMenu() is None:
                    GameState.generateMenu()
                GameState.setAfficherMenu(True)

    if GameState.getAsk():
        GameState.setRunning(JouerBoucle())
        GameState.setReplay(GameState.getRunning())

    if GameState.getReplay():
        Jouer()

    if not GameState.getReplay():
        afficher_nom_jeu()
        jouer_bloc()

    if GameState.getAfficherMenu():
        res = GameState.AfficherMenu()
        if res["end"] == 1:
            newConfig = res["config"]
            GameState.getMenu().setActive(res["onglet"])
            GameState.updateGeneral((int(newConfig["width"]), int(newConfig["height"])))
        elif res["end"] == 2:
            GameState.setAfficherMenu(res["Menu"])

    pg.display.flip()
