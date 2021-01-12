# Jhima Mohamed
# 12/01/2021
#To do : relancer le jeu en cas de victoire ou défaites
# https://github.com/Mohajhima/TPPythonSpace-Invaders.git

import tkinter as tk  # On a travaillé sur python 3 mais ça ne devrait rien changer à part la majuscule sur Tkinter.
import random as rd

class Ennemi: # gère le type des ennemis, leurs déplacements
    def __init__(self, canvas, jeu, Horde, positionx=6, positiony=1, direction = 1, vitesse = 2, frequence = 16, kind=2):
        self.kind = kind
        self.canvas = canvas
        self.positionx = positionx
        self.setimage = [tk.PhotoImage(file='mechant1.png'),tk.PhotoImage(file='mechant2.png'),tk.PhotoImage(file='mechant12.png'),tk.PhotoImage(file='mechant22.png')] #50px*50px
        self.positiony= positiony # Pourrait être utile. Position dans la grille de la horde
        self.sprite= canvas.create_image(50*positionx,50*positiony+50,image=self.setimage[kind-1], anchor='nw')
        self.direction = direction # utile pour les solitaires hors hordes qui donnent des bonus
        self.image=self.setimage[kind-1]
        self.Horde = Horde        
        self.jeu = jeu
        self.vitesse = vitesse
        self.frequence = frequence
        self.score = 50*kind**2
        self.pv = kind
        if self.pv == 3:
            self.pv = 1
            # C'est le boss

    def deplacementboss(self): # si on ajoute un boss dans le jeu
        if self.jeu.GameOver:
            return
        # Deplacement pour les solitaires persistant sur une ligne et qui n'avancent pas (boss ?). Se manipule en dehors des hordes. Pas implémenté (suffit de créer l'objet de type Ennemi et lancer cette fonction apres un certain nombre de manche)
        if self.canvas.coords(self.sprite)[0] + self.direction*self.vitesse > 0 and self.canvas.coords(self.sprite)[0] + self.direction*self.vitesse + 50 < 600:
            self.canvas.move(self.sprite, self.direction*self.vitesse, 0)
        else:
            self.direction = (self.direction == -1) - (self.direction == 1)
            self.canvas.move(self.sprite, self.direction*self.vitesse, 0)
        self.canvas.after(self.frequence,self.deplacementboss)

    def deplacementsurprise(self):
        if self.jeu.GameOver:
            return
        # Deplacement pour les solitaires surprises qui apparaitrait à intervalle regulier mais pas toujours. Se manipule en dehors des hordes. Pas implémenté (suffit de créer l'objet de type Ennemi et lancer cette fonction apres un after)
        if self.canvas.coords(self.sprite)[0] + self.direction*self.vitesse > 0 and self.canvas.coords(self.sprite)[0] + self.direction*self.vitesse + 50 < 650:
            self.canvas.move(self.sprite, self.direction*self.vitesse, 0)
        else:
            self.canvas.destroy(self.sprite)
        self.canvas.after(self.frequence,self.deplacementsurprise)

class Horde:  # gère les ennemis en tant que groupe
    def __init__(self,canvas, jeu, length, height, vitesse = 1, proba = 5000,frequence = 16, direction = 1):
        self.listeEnnemis = []
        self.length = length
        self.height = height
        self.canvas = canvas
        self.jeu = jeu
        self.vitesse = vitesse
        self.direction = direction
        self.frequence = frequence
        self.proba = proba
        
        
        for i in range(length):
            for j in range(height-1):
                self.listeEnnemis.append(Ennemi(canvas, jeu, self, i+(12-length)//2, j, self.direction, self.vitesse, self.frequence, 2))
            self.listeEnnemis.append(Ennemi(canvas, jeu, self, i+(12-length)//2, height-1, self.direction, self.vitesse, self.frequence, 1))
    def deplacements(self):
        if self.jeu.GameOver or self.jeu.transition:
            return
        deplacementOK=True
        for Ennemi in self.listeEnnemis:
            if self.canvas.coords(Ennemi.sprite)[0] + self.direction*self.vitesse < 0 or self.canvas.coords(Ennemi.sprite)[0] + self.direction*self.vitesse + 50 > 600:
                deplacementOK = False
        if deplacementOK:
            for Ennemi in self.listeEnnemis:
                self.canvas.move(Ennemi.sprite, self.direction*self.vitesse, 0)
        else:
            for Ennemi in self.listeEnnemis:
                if self.canvas.coords(Ennemi.sprite)[1] + 50 + 25 > 490:
                    self.jeu.GameOver = True
            if self.jeu.GameOver:
                self.canvas.after(16, self.jeu.endGame)
                return

            for Ennemi in self.listeEnnemis:
                self.canvas.move(Ennemi.sprite, 0, 25)
                Ennemi.direction = (Ennemi.direction == -1) - (Ennemi.direction == 1) # Pas utilisé dans horde mais fait par rigueur
            self.direction = (self.direction == -1) - (self.direction == 1)
        self.canvas.after(self.frequence,self.deplacements)
    
    def NouveauTir(self):
        if self.jeu.GameOver or self.jeu.transition:
            return
        for Ennemi in self.listeEnnemis:
            probatir = rd.randint(0,self.proba)
            if probatir <= 1:
                self.jeu.Tirsactuels.append(Tir(self.canvas, self.jeu, self.canvas.coords(Ennemi.sprite)[0], self.canvas.coords(Ennemi.sprite)[1], 1))
        self.canvas.after(16, self.NouveauTir)
                
                
            
class Tir: # gère les tirs du joueur et des ennemis
    def __init__(self, canvas, jeu, positionx, positiony, direction):
        self.image = [tk.PhotoImage(file='laser.png'), tk.PhotoImage(file='laser2.png')]
        self.canvas= canvas
        self.jeu = jeu
        self.direction = direction
        self.sprite = canvas.create_image(positionx,positiony+direction*30,image=self.image[(self.direction == -1)], anchor='nw')



class Player:
    def __init__(self, canvas, jeu, positionx=275, positiony=550): # on initie tous les attributs du vaisseau
        
        self.canvas = canvas
        self.image = tk.PhotoImage(file='player.png').subsample(10,10) #50px*50px
        self.sprite= canvas.create_image(positionx,positiony,image=self.image, anchor='nw')
        self.direction = 0
        self.jeu = jeu
        self.TimerTir = 1000
        self.tir = False

    def moveleft(self, event):
        if self.jeu.GameOver:
            return
        self.direction=-1

    def moveright(self, event):
        if self.jeu.GameOver:
            return
        self.direction=1

    def stopmove(self, event):
        if self.jeu.GameOver:
            return
        if (event.keysym == "q" and self.direction == -1) or (event.keysym == "d" and self.direction == 1):
            self.direction = 0
        if (event.keysym == "space" and self.tir == 1):
            self.tir = False

    def deplacementplayer(self):  # déplacement du sprite 
        if self.jeu.GameOver:
            return
            
        if (self.canvas.coords(self.sprite)[0] <= 4 and self.direction==-1) or (self.canvas.coords(self.sprite)[0] >= 550 and self.direction==1) :
            self.direction=0 # On fait attention à ne pas dépasser les bordures
        else:
            self.canvas.move(self.sprite, self.direction*5,0)
        self.canvas.after(16,self.deplacementplayer)
        
        if self.tir == True and self.TimerTir >= 25 and not(self.jeu.transition): 
            self.jeu.Tirsactuels.append(Tir(self.canvas, self.jeu, self.canvas.coords(self.sprite)[0], self.canvas.coords(self.sprite)[1], -1))
            self.TimerTir = 0 # remise à zéro du timer après un tir du vaisseau

    def NouveauTirP(self, event):
        if self.jeu.GameOver:
            return
        if self.TimerTir >= 25:   # on ne peut pas tirer si le timer n'est pas terminé
            self.tir = True  
    
    def PasdeTir(self):   #incrémentation du timer entre deux tirs
        if self.jeu.GameOver:
            return
        self.TimerTir += 1

        self.canvas.after(16, self.PasdeTir) # à modifier si on veut changer la fréquence des tirs


class Menu:  # crée un objet qui a comme attributs tous les éléments du menu.
    def __init__(self):        
        self.background = tk.PhotoImage(file = 'backgroundMenu.png')
        self.logo =  tk.PhotoImage(file = 'logo.png')
        self.boutonPlay = tk.Button( text = 'PLAY !',height = 4, width = 20,activebackground='#ffbd33',background='#FFE213')
        self.boutonExit = tk.Button( text = 'EXIT',height = 2, width = 10,activebackground='#ffbd33',background='#FFE213')



class Jeu: # Classe principale : objet gérant la fenêtre de jeu, le canvas, et a pour attributs les autres objets du programme.
    def __init__(self, fenetre, length, height, vitesse = 1,proba = 4000):

        self.fenetre = fenetre # fenetre est une fenêtre Tk()
        self.fenetre.title('Space Invaders')
        self.fenetre.geometry("600x600")
        self.fenetre.resizable(width=False, height=False)

        self.canvas = tk.Canvas(self.fenetre, bg = 'black', bd= 0, highlightthickness=0, height = 600, width = 600)

        self.player = Player(self.canvas, self)

        self.length = length
        self.height = height
        self.vitesse = vitesse
        self.proba = proba  # proba n'est pas vraiment une probabilité, plus il baisse plus les ennemis tirent fréquemment.
         # Ces 3 pour manches suivantes, incrémentés


        self.manche = 1
        self.mancheSv = tk.StringVar()
        self.mancheSv.set(str(self.manche))

        self.horde = Horde(self.canvas, self, self.length, self.height, self.vitesse,self.proba)
        self.murs = Murs(self.canvas,self)
        self.GameOver = False
        self.Tirsactuels = []

        self.menu = Menu()        

        self.transition = False

        self.score = 0
        self.highScoreSv = tk.StringVar()   # on utilise une stringvariable pour pouvoir changer sa valeur ensuite 
        self.temp = open("highscore.txt", "rt")
        self.highScore = int(self.temp.readline())  # Entier qui stocke le highscore, pas le même type de variable que HighScoreSv
        self.temp.close()        
        self.temp = open("highscore.txt", "rt")  # on ouvre deux fois le fichiers au lieu d'une car cela génère une erreur de faire les deux manipulations en une fois
        self.highScoreSv.set('HIGHSCORE : '+self.temp.readline())      
        self.temp.close()
       
        

    def lancerMenu(self): # première méthode appelée quand le jeu est lancé
        self.canvas.pack(anchor='nw')
        self.affBackground = self.canvas.create_image(300,300,image=self.menu.background)
        self.affLogo = self.canvas.create_image(300,133,image=self.menu.logo)        
        self.affBoutonPLay =self.canvas.create_window(300,350,window = self.menu.boutonPlay)
        self.menu.boutonPlay.config( command=self.Debut)      
        self.affBoutonExit = self.canvas.create_window(300,450,window = self.menu.boutonExit)
        self.menu.boutonExit.config( command=self.fenetre.destroy)
        self.labelHighScore = tk.Label(self.canvas, textvariable=self.highScoreSv, fg='white', bg='black', font='Helvetica 16 bold')
        self.affHighScore = self.canvas.create_window(490,15,window = self.labelHighScore)
        self.canvas.after(16, self.affichageHighScore)
        self.sv = tk.StringVar()
        self.sv.set('SCORE : '+str(self.score))
        self.labelScore = tk.Label(self.canvas, textvariable=self.sv, fg='white', bg='black', font='Helvetica 16 bold')
    
    def Debut(self): #est appelée pour commencer à jouer, supprime les éléments du menu et lancer les methodes qui permettent le bon déroulement du jeu
        self.canvas.delete(self.affBoutonPLay,self.affBoutonExit,self.affBackground,self.affLogo)
        self.canvas.pack(anchor='nw')
        
        self.affScore = self.canvas.create_window(90,15,window = self.labelScore)
        
        self.canvas.after(16, self.horde.deplacements)
        self.canvas.after(16, self.player.deplacementplayer)
        self.canvas.after(16, self.GestionTirs)
        self.canvas.after(16, self.gestionScore)
        self.canvas.after(16, self.horde.NouveauTir)       
        self.canvas.after(16, self.player.PasdeTir)
        self.fenetre.bind('<q>', self.player.moveleft)
        self.fenetre.bind('<Q>', self.player.moveleft)
        self.fenetre.bind('<d>', self.player.moveright)
        self.fenetre.bind('<D>', self.player.moveright)
        self.fenetre.bind('<KeyRelease>', self.player.stopmove)
        self.fenetre.bind('<space>', self.player.NouveauTirP)
    
    def gestionScore(self): # affichage du score pendant la partie
        self.canvas.delete(self.affScore)
        self.sv.set('SCORE : '+str(self.score))        
        self.affScore = self.canvas.create_window(90,15,window = self.labelScore)
        self.canvas.after(16, self.gestionScore)
        
    def affichageHighScore(self): # gère la modification en direct de la valeur du highscore après une partie 
        self.canvas.delete(self.affHighScore)
        self.temp = open("highscore.txt", "rt")
        self.highScoreSv.set('HIGHSCORE : '+self.temp.readline())    
        self.temp.close()
        self.affHighScore = self.canvas.create_window(490,15,window = self.labelHighScore)

    def ecranManche(self): # Ecran de transition entre deux manches
        self.manche += 1
        self.mancheSv.set('MANCHE '+ str(self.manche))
        self.labelManche = tk.Label(self.canvas, textvariable=self.mancheSv, fg='#FFE213', bg='black', font='Helvetica 60 bold')
        self.affManche = self.canvas.create_window(300,250,window = self.labelManche)
        self.canvas.after(1000,self.newmanche)  #lancement de la prochaine manche

    def newmanche(self):  
        self.canvas.delete(self.affManche)        
        
        if self.vitesse < 3 :  # augmentation de la vitesse jusqu'à un certain seuil
            self.vitesse += 0.5 
        if self.proba > 2100 : # pareil pour la fréquence de tir
            self.proba -= 900
        if self.proba > 500 and self.proba < 2100:
            self.proba -= 300        
        self.horde = Horde(self.canvas, self, self.length, self.height, self.vitesse,self.proba)
        self.transition = False
        self.canvas.after(16, self.horde.deplacements)
        self.canvas.after(16, self.horde.NouveauTir)
        self.canvas.after(16, self.GestionTirs)

    def endGame(self): # Ecran de game over
        self.canvas.delete('all')
        label = tk.Label(self.canvas, text='GAME OVER', fg='white', bg='black')
        label.config(font=("Liberation", 30))
        self.canvas.create_window(300, 300, window=label)
        self.affBackground = self.canvas.create_image(300,300,image=self.menu.background)
        
        if self.score > self.highScore: # sauvegarde du meilleur score si on bat le record
            temp = open("highscore.txt", "wt")
            temp.write(str(self.score))
            temp.close()
        
        self.canvas.after(500, self.relaunch)
        
    def relaunch(self): # réinitialisation du jeu pour ré-afficher le menu et relancer une partie.
        self.canvas.delete('all')
        self.vitesse = 1
        self.proba = 4000
        self.manche = 1
        self.player = Player(self.canvas, self)
        self.horde = Horde(self.canvas, self, self.length, self.height, self.vitesse)
        self.murs = Murs(self.canvas,self)
        self.GameOver = False
        self.Tirsactuels = []
        self.score = 0
        
        self.menu = Menu()
        self.boutonPlay = tk.Button(self.fenetre, text = 'PLAY !',height = 4, width = 20,command=self.Debut,activebackground='#ffbd33',background='#FFE213')
        self.boutonExit = tk.Button(self.fenetre, text = 'EXIT',height = 2, width = 10,command=self.fenetre.destroy,activebackground='#ffbd33',background='#FFE213')
        
        jeu.lancerMenu()

    def GestionTirs(self): # gestion du mouvement des lasers et de la collision, ainsi que de l'augmentation de la variable score
        if self.GameOver:
            return
        for tir in self.Tirsactuels:
            touche = False  # True si l'entité est touchée
            indexEnnemiasuppr = None 
            indexblocasuppr = None
            indexEnnemiatoucher = None

            self.canvas.move(tir.sprite, 0,tir.direction*4)
            if abs(self.canvas.coords(tir.sprite)[0] - self.canvas.coords(self.player.sprite)[0]) < 20 and abs(self.canvas.coords(tir.sprite)[1] - self.canvas.coords(self.player.sprite)[1]) < 33 and tir.direction == 1:
                
                touche = True
                self.GameOver = True
                
            for Ennemi in self.horde.listeEnnemis:
                if abs(self.canvas.coords(tir.sprite)[0] - self.canvas.coords(Ennemi.sprite)[0]) < 23 and abs(self.canvas.coords(tir.sprite)[1] - self.canvas.coords(Ennemi.sprite)[1]) < 33 and tir.direction == -1:
                    
                    touche = True                    
                    if Ennemi.pv == 1:
                        indexEnnemiasuppr = self.horde.listeEnnemis.index(Ennemi)  # suppression de l'ennemi mort              
                        self.score += Ennemi.score  #augmentation du score quand on tue un ennemi                        
                    else:
                        Ennemi.pv -= 1  # on baisse la vie de l'ennemi touché
                        indexEnnemiatoucher = self.horde.listeEnnemis.index(Ennemi)
               

            for bloc in self.murs.listeBlocs: # gestion de la destruction des blocs
                if self.canvas.coords(bloc.sprite)[0] - self.canvas.coords(tir.sprite)[0] < 29 and self.canvas.coords(bloc.sprite)[0] - self.canvas.coords(tir.sprite)[0] > 0 and self.canvas.coords(tir.sprite)[1] - self.canvas.coords(bloc.sprite)[1] < 9 and self.canvas.coords(bloc.sprite)[1] - self.canvas.coords(tir.sprite)[1] < 29:
                    touche = True
                    indexblocasuppr = self.murs.listeBlocs.index(bloc)
            
            if indexEnnemiatoucher != None:
                temp = self.horde.listeEnnemis[indexEnnemiatoucher]
                self.canvas.itemconfig(temp.sprite, image=temp.setimage[temp.kind-1+len(temp.setimage)//2]) # La liste est pensée telle que la 2e moitié puisse servir à representer la premiere moitié blessée
            if indexEnnemiasuppr != None:
                self.canvas.delete(self.horde.listeEnnemis[indexEnnemiasuppr].sprite)
                self.horde.listeEnnemis.remove(self.horde.listeEnnemis[indexEnnemiasuppr])
            if indexblocasuppr != None:
                self.canvas.delete(self.murs.listeBlocs[indexblocasuppr].sprite)
                self.murs.listeBlocs.remove(self.murs.listeBlocs[indexblocasuppr])
            
            if self.canvas.coords(tir.sprite)[1] >= 560 or self.canvas.coords(tir.sprite)[1] < 0 or touche == True:
                self.canvas.delete(tir.sprite)
                self.Tirsactuels.remove(tir)
            
            if self.GameOver == True:
                self.canvas.delete(self.player.sprite)
                self.canvas.after(1000, self.endGame)
                return

            if len(self.horde.listeEnnemis) == 0:
                self.transition = True
            if len(self.horde.listeEnnemis) == 0 and len(self.Tirsactuels) == 0:
                self.canvas.after(1000, self.ecranManche) # on lance la prochaine manche
                return
                
        self.canvas.after(16, self.GestionTirs)

class Bloc: #Objet qui compose les murs : carré blanc 
    def __init__(self, canvas, jeu,positionx, positiony):
        self.image = tk.PhotoImage(file='bloc.png').subsample(25,25)
        self.jeu = jeu
        self.canvas = canvas
        self.sprite = self.canvas.create_image(positionx,positiony,image=self.image, anchor='nw')
        
class Murs: #composé des blocs
    def __init__(self, canvas, jeu):
        self.jeu = jeu
        self.canvas = canvas
        self.listeBlocs=[] 
        for i in range(5):  # 5 blocs par ligne
            for j in range(3):  # 3 blocs par colonne 
                self.listeBlocs.append(Bloc(canvas, jeu, 60+20*i, j*20+485)) # trois murs
                self.listeBlocs.append(Bloc(canvas, jeu, 260+20*i, j*20+485))
                self.listeBlocs.append(Bloc(canvas, jeu, 460+20*i, j*20+485))
                
        


if __name__ == '__main__':  # utile si on travaille sur plusieurs fichiers .py dans le répertoire 
    fenetre = tk.Tk() # initialisation de la variable qui gère la fenêtre de jeu 
    jeu = Jeu(fenetre, 8, 3) # nombre de lignes et de colonnes qui composent la horde d'ennemis.
    jeu.lancerMenu()
    jeu.fenetre.mainloop()