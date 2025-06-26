import random, sys, pygame_widgets, pygame as pg, config as config

from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from pygame_widgets.progressbar import ProgressBar

dataConfig = config.charger_config()
pg.init()
screen = pg.display.set_mode((int(dataConfig["width"]), int(dataConfig["height"])))
clock = pg.time.Clock()
running = True
running2 = True
hugeassfont = pg.font.SysFont('Arial', 150, 1, 0)
hugeassfontplus = pg.font.SysFont('Arial', 160, 1, 0)
bigfont = pg.font.SysFont('Arial', 40)
font = pg.font.SysFont('Arial', 30)
smallfont = pg.font.SysFont('Arial', 20)
vsmallfont = pg.font.SysFont('Arial', 14)
atkfont = pg.font.SysFont('Arial', 17)
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

class Bouton :
  def __init__(self,widthtop,heighttop,width,height,texte,font,color,state) :
    self.widthtop = widthtop
    self.width = width
    self.heighttop = heighttop
    self.height = height
    self.texte = texte
    self.font = font
    self.color = color
    self.state = state
  
  def affiche_bouton(self):
    center_rect = pg.draw.rect(screen, (179, 179, 179), [self.widthtop + 5, self.heighttop + 5, self.width - 10, self.height - 10])
    print(center_rect)
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
      pg.draw.rect(screen, (0, 0, 0), [self.widthtop, self.heighttop, self.width, self.height])

    else :
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
              and not afficheMenu
            ) :
        colorMid = (120, 120, 120)
        colorTop = (70, 70, 70)
        colorRight = (150, 150, 150)
        colorBot = (180, 180, 180)
        colorLeft = (90, 90, 90)

      pg.draw.polygon(screen, colorTop,
                      [(self.widthtop, self.heighttop), (self.widthtop + self.width, self.heighttop),
                       (self.widthtop + self.width - 5, self.heighttop + 5), (self.widthtop + 5, self.heighttop + 5)])
      pg.draw.polygon(screen, colorRight, [(self.widthtop + self.width - 5, self.heighttop + 5),
                                                (self.widthtop + self.width, self.heighttop),
                                                (self.widthtop + self.width, self.heighttop + self.height),
                                                (self.widthtop + self.width - 5, self.heighttop + self.height - 5)])
      pg.draw.polygon(screen, colorBot, [(self.widthtop + 5, self.heighttop + self.height - 5),
                                                (self.widthtop + self.width - 5, self.heighttop + self.height - 5),
                                                (self.widthtop + self.width, self.heighttop + self.height),
                                                (self.widthtop, self.heighttop + self.height)])
      pg.draw.polygon(screen, colorLeft,
                      [(self.widthtop, self.heighttop), (self.widthtop + 5, self.heighttop + 5),
                       (self.widthtop + 5, self.heighttop + self.height - 6),
                       (self.widthtop, self.heighttop + self.height - 1)])
      
      pg.draw.rect(screen, colorMid, [self.widthtop + 5, self.heighttop + 5, self.width - 10, self.height - 10])
      screen.blit(surf_texte, rect_texte)
  
  def getwidth(self) : 
    return([self.widthtop,self.widthtop + self.width])
  
  def getheight(self) : 
    return([self.heighttop,self.heighttop + self.height])
  
  def getstate(self) : 
    return(self.state)
  
  def setstate(self, state) : 
    if state in ["", "Down", "Dead"]:
      self.state = state
  
  def settexte(self, texte) : 
    if type(texte) == str : 
      self.texte = texte
  
  def setwidth(self, widthtop, width) :
    self.widthtop = widthtop
    self.width = width
  
  def setheight(self, heighttop, height) :
    self.heighttop = heighttop
    self.height = height

class BarreDeVie : 
  def __init__(self, width, name, pv) : 
    self.width = width
    self.name = name
    self.pv = pv
  
  def Affiche(self) : 
    self.AfficheBar()
    self.AfficheNom()
  
  def AfficheBar(self) : 
    width = screen.get_width()
    progressBar = ProgressBar(screen, width/4, 50, width/2, 18, lambda: self.pv, curved=True, completedColour=(200, 0, 0))
    pg.draw.polygon(screen, (218, 165, 32), [(width/16*4+2, 49), (width/16*4-4, 49), (width/16*4-16, 59), (width/16*4-4, 68), (width/16*4+2, 68), (width/16*4-3, 59)])
    pg.draw.polygon(screen, (255, 215, 0), [(width/16*4-3, 59), (width/16*4-16, 59), (width/16*4-4, 68), (width/16*4+2, 68)])
    
    pg.draw.polygon(screen, (218, 165, 32), [(width/16*12-2, 49), (width/16*12+4, 49), (width/16*12+16, 59), (width/16*12+4, 68), (width/16*12-2, 68), (width/16*12+3, 59)])
    pg.draw.polygon(screen, (255, 215, 0), [(width/16*12+3, 59), (width/16*12+16, 59), (width/16*12+4, 68), (width/16*12-2, 68)])
    pygame_widgets.update(ev)
  
  def AfficheNom(self) : 
    width = screen.get_width()
    pg.draw.rect(screen, (218, 165, 32), [width/2-self.width/2, 40, self.width, 8])
    pg.draw.rect(screen, (255, 210, 0), [width/2-self.width/2, 44, self.width, 4])
    pg.draw.rect(screen, (218, 165, 32), [width/2-self.width/2-8, 40-8, 8, 8])
    pg.draw.rect(screen, (218, 165, 32), [width/2+self.width/2, 40-8, 8, 8])
    pg.draw.polygon(screen, (255, 215, 0), [(width/2-self.width/2-8,33), (width/2-self.width/2, 40), (width/2-self.width/2-8, 40)])
    pg.draw.polygon(screen, (255, 215, 0), [(width/2+self.width/2+7, 33), (width/2+self.width/2+7, 40), (width/2+self.width/2, 40)])
    nom = bigfont.render(self.name, True, (200, 200, 200))
    nom_rect = nom.get_rect(center = (width/2, 20))
    screen.blit(nom, nom_rect)
  
  def setPv(self, pv) : 
    self.pv = pv

class BTNLangue : 
  def __init__(self, widthpos, heighttop, width, height, img) :
    self.widthpos = widthpos
    self.heighttop = heighttop
    self.width = width
    self.height = height
    self.img = img # Gérer la récupération de l'image

  def Afficher(self) :
    pg.draw.rect(screen, (120, 120, 120), [self.widthpos, self.heighttop, self.width, self.height])
    pg.draw.rect(screen, (140, 140, 140), [self.widthpos + 5, self.heighttop + 5, self.width - 10, self.height - 10])
    pg.draw.polygon(screen, (200, 200, 200), [(self.widthpos, self.heighttop), (self.widthpos + self.width - 1, self.heighttop), (self.widthpos + self.width - 6, self.heighttop + 5), (self.widthpos + 5, self.heighttop + 5)])
    pg.draw.polygon(screen, (180, 180, 180), [(self.widthpos, self.heighttop), (self.widthpos + 5, self.heighttop + 5), (self.widthpos + 5, self.heighttop + self.height - 5), (self.widthpos, self.heighttop + self.height)])
    pg.draw.polygon(screen, (100, 100, 100), [(self.widthpos + 5, self.heighttop + self.height - 5), (self.widthpos + self.width - 5, self.heighttop + self.height - 5), (self.widthpos + self.width, self.heighttop + self.height), (self.widthpos, self.heighttop + self.height)])

class EscapeMenu :
  def __init__(self, widthpos, heightpos, width, height) :
    self.widthpos = widthpos
    self.heightpos = heightpos
    self.width = width
    self.height = height

  def Afficher(self):
    pg.draw.rect(screen, (80, 80, 80), [self.widthpos, self.heightpos, self.width, self.height], border_radius=20)

  def setParams(self, widthpos, heightpos, width, height):
    self.widthpos = widthpos
    self.heightpos = heightpos
    self.width = width
    self.height = height

  def getArea(self):
    return (self.widthpos, self.heightpos, self.width, self.height)

bouton_Jouer = Bouton(screen.get_width() / 2 - 100, screen.get_height() / 2 - 25, 220, 50, 'Jouer', font, (0, 200, 0), "")
bouton_quit = Bouton(screen.get_width() / 2 - 100, screen.get_height() / 2 - 25, 220, 50, 'Quit', font, (255, 255, 255), "")
bouton_resize = Bouton(screen.get_width() / 2 - 100, screen.get_height() / 2 - 25, 220, 50, '500x400', font, (255, 255, 255), "")
histo = 1
barreDeVie = BarreDeVie(300, "Banshee", 200)
BTNFR = BTNLangue(150, 150, 200, 50, "img")
Menu = EscapeMenu(screen.get_width() / 3, screen.get_height() / 3, screen.get_width() / 3, screen.get_height() / 3)

while running :
    width = screen.get_width()
    height = screen.get_height()
    pg.draw.rect(screen, (0, 0, 0), [0, 0, width, height])
    bouton_Jouer.setwidth(width / 2 - 100, 220)
    bouton_Jouer.setheight(height / 2 - 25, 50)
    bouton_quit.setwidth(width / 2 - 100, 220)
    bouton_quit.setheight(height / 2 - 25, 50)
    bouton_resize.setwidth(width / 2 - 100, 220)
    bouton_resize.setheight(height / 4 * 3 - 25, 50)
    Menu.setParams(width / 3, height / 3, width / 3, height / 3)
    for ev in pg.event.get():

      if ev.type == pg.QUIT:
        pg.quit()
        running = False
        sys.exit()
      
      if ev.type == pg.MOUSEBUTTONDOWN:
        mouse = pg.mouse.get_pos()
        if bouton_quit.getwidth()[0] <= mouse[0] <= bouton_quit.getwidth()[1] and bouton_quit.getheight()[0] <= mouse[1] <= bouton_quit.getheight()[1] and not bouton_quit.getstate() in ["Down", "Dead"] and not afficheMenu :
          pg.quit()
          running = False
          sys.exit()
        if bouton_resize.getwidth()[0] <= mouse[0] <= bouton_resize.getwidth()[1] and bouton_resize.getheight()[0] <= mouse[1] <= bouton_resize.getheight()[1] and not bouton_resize.getstate() in ["Down", "Dead"] and not afficheMenu :
          if width != 800 :
            screen = pg.display.set_mode((800, 600))
          else :
            screen = pg.display.set_mode((1440, 1080))
      
      if ev.type == pg.KEYDOWN :
        if ev.key == pg.K_ESCAPE :
          afficheMenu = not afficheMenu
        if ev.key == pg.K_BACKSPACE :
          mana_uti = mana_uti[:-1]
        elif ev.key == pg.K_RETURN : 
          selecMD = True
        
      if ev.type == pg.TEXTINPUT:
        mana_uti += ev.text  # Ajoute le texte Unicode directement

    bouton_quit.affiche_bouton()
    bouton_resize.affiche_bouton()
    barreDeVie.Affiche()
    if afficheMenu :
      Menu.Afficher()
      # Afficher le menu
    
    pg.display.update()