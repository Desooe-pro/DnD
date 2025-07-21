import sys, pygame as pg, pygame.gfxdraw, config


class EscapeMenu:
    def __init__(self, widthpos, heightpos, width, height, screen, boutonAppliquer):
        self.screen = screen
        self.config = config.charger_config()
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
        running = True
        while running:
            pg.draw.rect(
                self.screen,
                (0, 0, 0),
                (0, 0, self.screen.get_width(), self.screen.get_height()),
            )
            ongletActif = self.nav.getNameActive()
            self.bouton.setsize(
                (
                    self.widthpos
                    + self.width
                    - 20
                    - (self.bouton.getwidth()[1] - self.bouton.getwidth()[0]) / 2,
                    self.heightpos
                    + self.height
                    - 20
                    - (self.bouton.getheight()[1] - self.bouton.getheight()[0]) / 2,
                ),
                2,
                self.screen.get_width(),
                self.screen.get_height(),
            )
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
                    if (
                        self.bouton.getwidth()[0]
                        <= mouse[0]
                        <= self.bouton.getwidth()[1]
                        and self.bouton.getheight()[0]
                        <= mouse[1]
                        <= self.bouton.getheight()[1]
                        and not self.bouton.getstate() in ["Down", "Dead"]
                    ):
                        config.sauvegarder_config(self.config)
                        return {"end": 1, "config": self.config, "onglet" : self.nav.getNameActive()}
                    btns = self.nav.getBoutons()
                    for loop in range(len(btns)):
                        widthTemp = btns[loop].getWidth()
                        heightTemp = btns[loop].getHeight()
                        if (
                            widthTemp[0] <= mouse[0] <= widthTemp[1]
                            and heightTemp[0] <= mouse[1] <= heightTemp[1]
                        ):
                            self.setActive(btns[loop].getName())
                            ongletActif = self.nav.getNameActive()
                    if ongletActif == "Graphisme":
                        AllCoords = self.nav.getSurfaceLignes("Graphisme")
                        for i in list(AllCoords.keys()) :
                            WL, HL, WR, HR = AllCoords[i]
                            if WL <= mouse[0] <= WR and HL <= mouse[1] <= HR :
                                txt = i.split(" (")
                                x = txt[0].split(" x ")
                                self.config["width"] = x[0]
                                self.config["height"] = x[1]
                                return {"end": 1, "config": self.config, "onglet": self.nav.getNameActive()}

                if ev.type == pg.KEYDOWN:
                    if ev.key == pg.K_ESCAPE:
                        return {"end": 2, "Menu": False}
            pg.display.update()
        return None

    def setParams(self, widthpos, heightpos, width, height, screen):
        self.screen = screen
        self.widthpos = widthpos
        self.heightpos = heightpos
        self.width = width
        self.height = height
        self.nav.setParams(
            self.widthpos, self.heightpos, self.width, self.height, self.screen
        )

    def getBouton(self):
        return self.bouton

    def setActive(self, name) :
        self.nav.setActive(name)
        self.activeParam = name


class NavMenu:
    def __init__(
        self, widthtop, heighttop, width, height, options, screen, boutonAppliquer
    ):
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
        for loop in list(self.boutons.keys()):
            self.boutons[loop].Afficher(name)

    def getBoutons(self):
        res = []
        for loop in list(self.boutons.keys()):
            res.append(self.boutons[loop])
        return res

    def getNameActive(self):
        for loop in list(self.boutons.keys()):
            if self.boutons[loop].getActive():
                return self.boutons[loop].getName()
        return None

    def setParams(self, widthtop, heighttop, width, height, screen):
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
        return self.boutons[text].getSurfaceLignes()

    def setActive(self, name) :
        for i in list(self.boutons.keys()) :
            self.boutons[i].setActive(False)
        self.boutons[name].setActive(True)


class MenuBouton:
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
        if self.text == name :
            self.active = True
        else :
            self.active = False
        mouse = pg.mouse.get_pos()
        center_rect = pg.draw.rect(
            self.screen,
            (180, 180, 180),
            (self.widthtop, self.heighttop, self.width, self.height),
        )
        if self.active:
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
        elif (
            self.widthtop <= mouse[0] <= self.widthtop + self.width
            and self.heighttop <= mouse[1] <= self.heighttop + self.height
        ):
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
            pg.gfxdraw.box(
                self.screen,
                (self.widthtop, self.heighttop, self.width, self.height),
                (0, 0, 0, 160),
            )
            surf_texte = self.font.render(self.text, 1, (180, 180, 180))
        rect_texte = surf_texte.get_rect()
        rect_texte.center = center_rect.center
        self.screen.blit(surf_texte, rect_texte)
        if self.active and self.page != "":
            self.page.Afficher()

    def getWidth(self):
        return [int(self.widthtop), int(self.widthtop + self.width)]

    def getHeight(self):
        return [int(self.heighttop), int(self.heighttop + self.height)]

    def getActive(self):
        return self.active

    def getName(self):
        return self.text

    def getSurfaceLignes(self):
        return self.page.getSurfaceLignes()

    def setActive(self, active):
        self.active = active


class ParamsGraph:
    def __init__(self, screen, widthtop, heighttop, width, height, boutonAppliquer):
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
        for loop in self.lignes:
            loop.Afficher(self.active)

    def getSurfaceLignes(self):
        res = {}
        for loop in self.lignes:
            res[loop.getKey()] =  loop.getSurface()
        return res


class LigneGraphisme:
    def __init__(
        self, key, widthtop, heighttop, width, blocOptHeight, optHeight, screen
    ):
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
        mouse = pg.mouse.get_pos()
        if self.key in active:
            colorLigne = (0, 0, 0, 200)
            colorText = (200, 200, 200)
        elif (
            self.widthtop <= mouse[0] <= self.widthtop + self.width
            and self.heighttopligne <= mouse[1] <= self.heighttopligne + self.optHeight
        ):
            colorLigne = (0, 0, 0, 160)
            colorText = (160, 160, 160)
        else:
            colorLigne = (0, 0, 0, 120)
            colorText = (120, 120, 120)

        center_rect = pg.draw.rect(self.screen, (80, 80, 80), (self.widthtop, self.heighttopligne, self.width, self.optHeight + 1))
        surf_texte = self.font.render(self.key, 1, colorText)
        rect_texte = surf_texte.get_rect()
        rect_texte.center = center_rect.center
        radius = temp = int(self.optHeight / 2)
        while radius > 0:
            pg.gfxdraw.arc(
                self.screen,
                self.widthtop + temp,
                self.heighttopligne + int(self.optHeight / 2),
                radius,
                90,
                -91,
                colorLigne,
            )
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

    def getKey(self) :
        return self.key

    def getSurface(self):
        return [
            self.widthtop,
            self.heighttopligne,
            self.widthtop + self.width,
            self.heighttopligne + self.optHeight,
        ]
