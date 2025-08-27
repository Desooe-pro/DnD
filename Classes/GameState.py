import pygame as pg, config

from math import floor
from Classes.Boutons import Bouton, PosBoutons
from Classes.MenuDnD import EscapeMenu


class GameState:
    def __init__(self, dataConfig, fonts: dict):
        self.dataConfig = dataConfig
        self.newConfig = None
        self.screen = pg.display.set_mode(
            (int(self.dataConfig["width"]), int(self.dataConfig["height"]))
        )
        self.screenSize = (self.screen.get_width(), self.screen.get_height())
        self.posBoutons = PosBoutons(self.screen)
        self.afficherMenu = False
        self.replay = False
        self.ask = False
        self.players = {}
        self.monsters = {}
        self.stats = {"pv": 0, "mana": 0, "force": 0, "defense": 0, "precision": 0}
        self.selectedStats = {
            "pv": 0,
            "mana": 0,
            "force": 0,
            "defense": 0,
            "precision": 0,
        }
        self.menu = None
        self.boutons = {}
        self.BarDeVie = None
        self.clock = pg.time.Clock()
        self.fonts = fonts
        self.volume = self.dataConfig["volume"]
        self.phrasesClass = config.load_phrases(dataConfig["langue"])
        self.running = True
        self.runningBoucle = True
        self.gameOverJouer = 0
        self.gameOverFight = 0

    def setSizeBouton(self, coord, nom):
        self.boutons[nom].setsize(coord)

    def isOn(self, nom: str, mouse: tuple[int, int]):
        if nom in self.boutons.keys():
            return self.boutons[nom].isOn(mouse)
        else:
            return False

    def updateGeneral(self, screen: tuple[int, int]):
        self.screen = pg.display.set_mode((screen[0], screen[1]))
        self.screenSize = (self.screen.get_width(), self.screen.get_height())
        self.posBoutons.setScreen(self.screen)
        for bouton in self.boutons:
            self.boutons[bouton].setsize(self.boutons[bouton].getCoords(), self.posBoutons)
        self.menu.setParams(
            floor(self.getScreenWidth() / 6),
            floor(self.getScreenHeight() / 6),
            floor(self.getScreenWidth() / 3 * 2),
            floor(self.getScreenHeight() / 3 * 2),
            self.screen,
        )

    def afficherBouton(self, nom: str):
        if nom in self.boutons.keys():
            self.boutons[nom].affiche_bouton()

    def generateMenu(self):
        print("pass")
        self.menu = EscapeMenu(
            floor(self.getScreenWidth() / 6),
            floor(self.getScreenHeight() / 6),
            floor(self.getScreenWidth() / 3 * 2),
            floor(self.getScreenHeight() / 3 * 2),
            self.screen,
        )

    def AfficherMenu(self):
        return self.menu.Afficher()

    # --- --- Getters --- ---

    def getFont(self, name=None):
        if name in self.fonts.keys():
            return self.fonts[name]
        else:
            return self.fonts

    def getScreen(self):
        return self.screen

    def getScreenWidth(self):
        return self.screenSize[0]

    def getScreenHeight(self):
        return self.screenSize[1]

    def getClock(self):
        return self.clock

    def getPhrases(self):
        return self.phrasesClass

    def getAsk(self):
        return self.ask

    def getReplay(self):
        return self.replay

    def getPosBoutons(self):
        return self.posBoutons

    def getMenu(self):
        return self.menu

    def getBoutons(self):
        return self.boutons

    def getBouton(self, name: str):
        if name in self.boutons.keys():
            return self.boutons[name]
        else:
            return None

    def getBoutonState(self, nom: str):
        if nom in self.boutons.keys():
            return self.boutons[nom].getstate()
        else:
            return "Dead"

    def getBarDeVie(self):
        return self.BarDeVie

    def getRunning(self):
        return self.running

    def getRunningBoucle(self):
        return self.runningBoucle

    def getAfficherMenu(self):
        return self.afficherMenu

    def getGameOverJouer(self):
        return self.gameOverJouer

    def getGameOverFight(self):
        return self.gameOverFight

    def getNewConfig(self):
        return self.newConfig

    # --- --- Setters --- ---

    def setAsk(self, ask):
        if type(ask) is bool:
            self.ask = ask

    def setReplay(self, replay):
        if type(replay) is bool:
            self.replay = replay

    def setMenu(self, menu: EscapeMenu):
        self.menu = menu

    def setBoutons(self, boutons: dict[str, Bouton]):
        for bouton in boutons:
            if bouton not in self.boutons.keys():
                self.boutons[bouton] = boutons[bouton]

    def setBoutonPos(self, nom, coords: tuple[int, int]):
        self.boutons[nom].setsize(coords, self.posBoutons)

    def setRunning(self, running):
        if type(running) is bool:
            self.running = running

    def setRunningBoucle(self, running):
        if type(running) is bool:
            self.runningBoucle = running

    def setBoutonState(self, nom: str, state: str):
        if nom in self.boutons.keys() and state in ["", "Down", "Dead"]:
            self.boutons[nom].setState(state)

    def setAfficherMenu(self, afficherMenu):
        if type(afficherMenu) is bool:
            self.afficherMenu = afficherMenu

    def setGameOverJouer(self, gameOverJouer: int):
        self.gameOverJouer = gameOverJouer

    def setGameOverFight(self, gameOverFight: int):
        self.gameOverFight = gameOverFight

    def setConfig(self, configuration):
        self.dataConfig = configuration
        self.menu.setConfig(configuration)

    def setNewConfig(self, newConfig):
        self.newConfig = newConfig