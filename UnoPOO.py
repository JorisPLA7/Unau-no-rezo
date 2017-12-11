from random import *
from tkinter import *


##Jeu
class Jeu:
    """ Jeu : Instance supérieure qui fait tout tourner seule.
    
    Taper :
    
    MonJeu=Jeu(True, "False", Nombre de joueur, Nombre de cartes au début)
         pour générer une nouvelle partie de Uno (qui reste en attente pour l'instant)
         
    MonJeu=Jeu(False, données)
         pour générer une partie à partir de données d'un autre jeu
         
    
    données = MonJeu.pack() pour récupérer les données de la partie en cours
    
    MonJeu.unpack(données) pour mettre à jour les données d'un jeu (en écrasant les précédentes)
    
    MonJeu.launch() lance une partie en local, défilement automatique
    """

    def __init__(self, main=False, packet="False", nombreJoueurs=2, nombreCartes=7):

        self.autoAsk = False
        if main: self.gameInit(nombreJoueurs, nombreCartes)
        if packet != "False":
            self.unpack(packet)

    def gameInit(self, nombreJoueurs, nombreCartes):
        """ Fonction qui initialise tout le jeu, le programme peut tourner sans mais il faut alors créer les instances à la main et certaines méthodes ne sont pas disponibles"""

        self.active = 0  # Id du joueur actif
        self.nextPlayer = 1
        self.bin = []  # défausse
        self.deck = Deck  # le deck est un objet aussi
        self.deck.__init__(
            self.deck)  # pas nécessaire mais il y avait des bugs (je retirerai quand tout sera bien fini)
        self.table = self.pioche()  # carte retournée
        self.nb_joueurs = nombreJoueurs
        self.sens = 1
        self.modificateurs_de_jeu = []
        self.extensions = {}
        while type(self.table) != Carte:  # on retourne des cartes jusqu'à obtenir une carte "normale"
            self.pose(self.pioche())

        self.player = []  # liste des joueurs
        for i in range(nombreJoueurs):
            self.player.append(Joueur(i))
            paquet = self.player[i].main_depart(self)
            self.unpack(paquet)

    def pioche(self):
        """renvoie une carte du deck"""
        carte, status = self.deck.pioche(self.deck, self.bin)  # status : nb de carte restantes dans le deck
        if status == 0:
            self.bin = []
        return carte

    def setNextPlayer(self, nb=1):
        '''nb = 0 le joueur rejoue
        =1 joueur suivant
        =2 passe le tour
        =-1 joueur précédent sans changement de sens

        '''
        next = (self.active + self.sens * nb) % self.nb_joueurs
        self.nextPlayer = next
        return next

    def setActive(self):
        """Changement de tour"""
        act = self.nextPlayer
        self.active = act
        return act

    def pose(self, carte):
        """Pose la carte sur la table"""
        self.bin.append(self.table)
        self.table = carte

    def autorisation(self, carte):
        """Fonction en prévivion de futures modifications (cartes pouvant éventuellement influer sur la partie à long terme)"""
        can_play = True
        for i in self.modificateurs_de_jeu:
            can_play = can_play and i[0](carte)
        return can_play

    def applyModifs(self):
        """Fonction en prévivion de futures modifications (cartes pouvant éventuellement influer sur la partie à long terme)"""
        for i in self.modificateurs_de_jeu:
            i[1]()
        self.modificateurs_de_jeu = []

    def unpack(self, data):  # pour récupérer les données, écrire MonJeu.unpack(data)
        """ Ecrase les données avec les nouvelles reçues"""
        [self.deck,
         self.active,
         self.nextPlayer,
         self.bin,
         self.table,
         self.player,
         self.nb_joueurs,
         self.sens,
         self.modificateurs_de_jeu,
         self.autoAsk,
         self.extensions] = list(data)

    def getActive(self):  # fonction pas nécessaire mais utile au déboguage
        """ Renvoie le joueur en train de jouer """
        try:
            return self.active
        except:
            return -1

    def enregistrer(self):
        """créée une copie des données"""
        data = [self.deck,
                self.active,
                self.nextPlayer,
                self.bin,
                self.table,
                self.player,
                self.nb_joueurs,
                self.sens,
                self.modificateurs_de_jeu,
                self.autoAsk,
                self.extensions
                ]
        return data

    def pack(self):
        self.data = list(self.enregistrer())

        return self.data

    def describe(self):  # si quelqu'un est perdu
        dico = self.caracteristics()

        print(self.caracteristics())
        return dico

    def launch(self):
        self.autoAsk = True
        self.routine()

    def launchGUI(self):
        while True:
            self.askGUI()

    def routine(self):
        while self.autoAsk == True:

            request = ""  # input("Appuyez sur Entrée ou entrez une commande :")
            if request == "stop":
                self.autoAsk = False
            elif len(request) != 0:
                try:
                    exec(request)
                except:
                    print("Erreur.")
            else:
                if self.player[self.active].nom == 'en attente de ':
                    self.player[self.active].nom = input("Veuillez saisir un pseudonyme pour jouer :  ")
                self.ask()

    def askGUI(self):
        if len(self.player) == 1:
            kill()
        else:
            self.setNextPlayer(1)

            TourDeJeu(self.player[self.active], self)

            self.setActive()

    def ask(self):
        if len(self.player) == 1:
            print("La partie est finie !")
        else:
            self.setNextPlayer(1)

            paquet = self.player[self.active].answer(self)

            self.unpack(paquet)

            self.setActive()


class Deck(Jeu):
    def __init__(self):
        deckInit = [["Cataclysme", "Pouvoir"], ["Cataclysme", "Pouvoir"], ["Cataclysme", "Pouvoir"],
                    ["Cataclysme", "Pouvoir"], ["Tempete", "Pouvoir"], ["Tempete", "Pouvoir"], ["Tempete", "Pouvoir"],
                    ["Tempete", "Pouvoir"]]
        val = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, "Salamandre", 1, 2, 3, 4, 5, 6, 7, 8, 9, "Salamandre", "Dragon", "Dragon",
               "Esprit", "Esprit"]
        colors = ["Bambous", "Cascade", "Braises", "Lumière"]
        for i in range(len(val)):
            for j in range(len(colors)):
                deckInit.append([val[i], colors[j]])

        self.deckActive = []

        for i in deckInit:
            self.deckActive.append(self.createCard(i))

        shuffle(self.deckActive)

    def createCard(liste):

        if type(liste[0]) == int:
            return Carte(liste)

        if liste[0] == "Salamandre":
            return Salamandre(liste)

        if liste[0] == "Dragon":
            return Dragon(liste)

        if liste[0] == "Esprit":
            return Esprit(liste)

        if liste[0] == "Cataclysme":
            return Cataclysme(liste)

        if liste[0] == "Benediction":
            return Benediction(liste)

        if liste[0] == "Tempete":
            return Tempete(liste)

    def reset(self, bin):
        cartes = list(bin)

        for i in range(len(cartes)):
            cartes[i] = createCard(cartes[i].id)  # on régénère un deck neuf, sans modification
        shuffle(cartes)
        self.deckActive = cartes

    def pioche(self, bin):

        carte = self.deckActive.pop()
        status = len(self.deckActive)
        if status == 0:
            self.reset(bin)

        return carte, status

    def caracteristics(self):
        dico = {"nombre de cartes": len(self.deckActive), "cartes": self.deckActive}
        return dico


class Joueur(Jeu):
    hand = []

    def __init__(self, playNumb, Username='en attente de '):
        self.num = playNumb
        self.nom = Username

        self.StartMethodList = []

        self.restrictions = []

    def main_depart(self, jeu):
        self.hand = [jeu.pioche() for i in range(7)]
        return jeu.pack()

    def answer(self, jeu):
        input("C'est à {} {} de jouer !".format(self.nom, self.num))

        for i in self.StartMethodList:  # effets de début de tour
            paquet, jeu = i(self, jeu)

        print("La carte posée est | ~ {} de {} ~ |".format(jeu.table.val, jeu.table.typ))
        print("Voici vos cartes : ")
        for i in range(len(self.hand)):
            print("| {} : ~ {} de {} ~ |".format(i, self.hand[i].val, self.hand[i].typ))
        print()
        if not self.peutJouer(jeu):
            jeu = self.pioche(jeu)
            print("Vous piochez : | {} : ~ {} de {} ~ |".format(len(self.hand) - 1, self.hand[len(self.hand) - 1].val,
                                                                self.hand[len(self.hand) - 1].typ))

        if not self.peutJouer(jeu):
            print("Vous ne pouvez pas jouer.")

        else:
            indice = input("Quelle carte poser ? ")
            try:
                indice = int(indice)
            except:
                while type(indice) != int:
                    indice = input("Il faudrait songer à entrer le numéro correspondant : ")
                    try:
                        indice = int(indice)
                    except:
                        pass

            while self.playable(indice, jeu) == False:
                indice = input("Vous ne pouvez pas jouer ça. Essayez encore : ")
                try:
                    indice = int(indice)
                except:
                    while type(indice) != int:
                        indice = input("Il faudrait songer à entrer le numéro correspondant : ")
                        try:
                            indice = int(indice)
                        except:
                            pass
            jeu = self.pose(indice, jeu)

        paquet = self.endTurn(jeu)
        return paquet

    def endTurn(self, jeu):
        # modifie le jeu
        if len(self.hand) == 0:
            jeu = self.setVictory(jeu)
        if jeu.nextPlayer != self.num:
            print("C'est la fin de votre tour.")
        print()
        self.clearLists()
        paquet = jeu.pack()
        return paquet

    def setVictory(self):
        print("Vous avez gagné, Bravo !")
        jeu.player.pop[jeu.getActive()]
        jeu.nb_joueurs -= 1
        return jeu

    def pioche(self, jeu):
        # modifie le jeu
        self.hand.append(jeu.pioche())
        return jeu

    def clearLists(self):
        self.StartMethodList = []

        self.restrictions = []

    def peutJouer(self, jeu):  # renvoie vraie si la main du joueur contient au moins une carte jouable
        Canplay = False
        for i in self.hand:
            Canplay = (Canplay or self.verify(i, jeu))
        return Canplay

    def verify(self, carte,
               jeu):  # détermine si une carte est jouable en prenant en compte les restricions imposées par...

        canPlay = True
        # canPlay=(canPlay and jeu.autorisation(carte) )#les modificateurs de jeu en cours
        canPlay = (canPlay and carte.compatibTest(jeu.table))  # la carte elle-même
        for i in self.restrictions:  # les diverses restrictions supplémentaires du joueur
            if i(self, carte, jeu) == "ByPass":  # "code spécial" pour éviter toutes les restricions
                canPlay = True
                return canPlay

            else:
                canPlay = canPlay and i(self, carte, jeu)

        return canPlay

    def playable(self, cardId, jeu):

        if cardId < 0:
            cardId = 0
        if cardId >= len(self.hand):
            cardId = len(self.hand) - 1
        return self.verify(self.hand[cardId], jeu)

    def enregistrer(self):

        data = [
            self.num,
            self.nom,
            self.hand,
            self.StartMethodList,

            self.restrictions
        ]
        return data

    def unpack(self, data):

        [self.num,
         self.nom,
         self.hand,
         self.StartMethodList,

         self.restrictions] = list(data)

    def pack(self):
        self.data = self.enregistrer()
        return self.data

    def pose(self, cardId, jeu):
        # modifie le jeu
        carte = self.hand.pop(cardId)
        jeu, paquet = carte.pose(jeu, self)
        self.unpack(paquet)

        return jeu

    def caracteristics(self):
        dico = {"Joueur": [self.num, self.nom], "nombre de carte": len(self.hand)}
        return dico


class Restriction:
    def __init__(self, condition, carte):
        self.comparaisonVal = list(condition)
        self.creator = carte

    def __call__(self, joueur, carte, jeu):
        """vérifie si la carte est conforme à la restriction (si sa valeur correspond à une de celles de la liste)"""
        if len(self.comparaisonVal) == 0:
            return True

        if len(self.comparaisonVal) >= 1:
            flag = False
            for i in self.comparaisonVal:
                flag = flag or carte[0] == self.comparaisonVal[i]
                flag = flag or carte[1] == self.comparaisonVal[i]

            return flag

        return True


class Carte(Jeu):
    def __init__(self, liste):
        self.id = liste  # pour la régénération du deck
        self.val = liste[0]
        self.typ = liste[1]
        self.owner = None  # pour des effets spéciaux

    def pose(self, jeu, joueur):
        # modifie le jeu
        # mofifie le joueur
        jeu.pose(self)
        self.setOwner(joueur.num)
        paquet = joueur.pack()
        return jeu, paquet

    def setOwner(self, parent):
        self.owner = parent

    def coveredEffect(self):
        def noEffect(joueur, jeu):
            return joueur.pack(), jeu

        return noEffect

    def compatibTest(self, carte):
        return self.val == carte.val or self.typ == carte.typ

    def caracteristics(self):
        dico = {"carte": self.id, "owner": self.owner}
        return dico


class Special(Carte):
    '''carte de nous
    '''

    def __init__(self, liste):
        Carte.__init__(self, liste)

    def pose(self, jeu, joueur):
        # modifie le jeu
        # mofifie le joueur
        jeu.pose(self)
        self.setOwner(joueur.num)

        paquet, jeu = self.poseEffect(jeu, joueur)

        return jeu, paquet

    def poseEffect(self, jeu, joueur):
        """Effet vierge"""
        return joueur.pack(), jeu


class Salamandre(Special):
    ''' equivalent carte +2
    '''

    def __init__(self, liste):
        Carte.__init__(self, liste)

    def poseEffect(self, jeu, joueur):

        nextPlayer = (jeu.active + jeu.sens) % jeu.nb_joueurs

        if "counter" in jeu.extensions:
            jeu.extensions["counter"] += 2
        else:
            jeu.extensions["counter"] = 2

        can_play = False
        for i in jeu.player[nextPlayer].hand:
            can_play = (can_play or i.val == "Salamandre" or i.val == "Cataclysme")

        if not can_play:
            print("C'est parti pour piocher !")
            for i in range(jeu.extensions["counter"]):
                jeu = jeu.player[nextPlayer].pioche(jeu)
                print(
                    "{} {} pioche !".format(jeu.player[nextPlayer].nom, jeu.player[nextPlayer].num))
            jeu.extensions["counter"] = 0
            jeu.setNextPlayer(2)

        else:
            rest = restriction(["Salamandre", "Cataclysme"], self)
            jeu.player[nextPlayer].restrictions.append(rest)

        return joueur.pack(), jeu


class Dragon(Special):
    ''' equivalent carte 'No' '''

    def __init__(self, liste):
        Carte.__init__(self, liste)

    def poseEffect(self, jeu, joueur):
        jeu.setNextPlayer(2)
        return joueur.pack(), jeu


class Esprit(Special):
    ''' equivalent changement de sens'''

    def __init__(self, liste):
        Carte.__init__(self, liste)

    def poseEffect(self, jeu, joueur):
        jeu.sens = jeu.sens * (-1)
        jeu.setNextPlayer(1)
        return joueur.pack(), jeu


class Cataclysme(Special):
    """ equivalent +4 """

    def __init__(self, liste):
        Carte.__init__(self, liste)

    def poseEffect(self, jeu, joueur):

        nextPlayer = (jeu.active + jeu.sens) % jeu.nb_joueurs

        if "counter" in jeu.extensions:
            jeu.extensions["counter"] += 4
        else:
            jeu.extensions["counter"] = 4

        can_play = False
        for i in jeu.player[nextPlayer].hand:
            can_play = (can_play or i.val == "Cataclysme")

        if not can_play:
            print("C'est parti pour piocher !")
            for i in range(jeu.extensions["counter"]):
                jeu = jeu.player[nextPlayer].pioche(jeu)
                print(
                    "{} {} pioche !".format(jeu.player[nextPlayer].nom, jeu.player[nextPlayer].num))
            jeu.extensions["counter"] = 0
            jeu.setNextPlayer(1)

        else:
            rest = restriction(["Cataclysme"], self)
            jeu.player[nextPlayer].restrictions.append(rest)

        colors = ["Braises", "Cascade", "Bambous", "Lumière"]
        color = int(input("0 : Braises | 1 : Cascade | 2 : Bambous | 3 : Lumière"))

        if abs(color) >= 4:
            color = 0

        self.typ = colors[color]

        return joueur.pack(), jeu

    def compatibTest(self, carte):
        return True


class Tempete(Special):
    """ equivalent joker"""

    def __init__(self, liste):
        liste[0] = "Tempête"
        Carte.__init__(self, liste)

    def poseEffect(self, jeu, joueur):
        colors = ["Braises", "Cascade", "Bambous", "Lumière"]
        color = int(input("0 : Braises | 1 : Cascade | 2 : Bambous | 3 : Lumière"))
        if abs(color) >= 4:
            color = 0

        self.typ = colors[color]

        return joueur.pack(), jeu

    def compatibTest(self, carte):
        return True


"""
class Benediction(Special):
    def __init__(self, liste):
        liste[0] = "Bénédiction"
        Carte.__init__(self, liste)

    def compatibTest(self, carte):
        if type(carte.val) == str:
            return False
        elif carte.val > 7:
            return True
        return False
"""


##Interface Graphique

def kill():
    print("fin")


def startGame():
    nbj = int(starterNbj.get())
    nbc = int(starterNbc.get())
    global a
    a = Jeu(True, "False", nbj, nbc)

    starter.destroy()
    root.destroy()
    a.launchGUI()


def TourDeJeu(joueur, jeu):
    for i in joueur.StartMethodList:  # effets de début de tour
        paquet, jeu = i(joueur, jeu)
    global copyjo, copyje
    copyjo = joueur;
    copyje = jeu
    global root
    root = Tk()
    global stat, played
    stat = False
    played = False
    ##Barre de Menu supérieur

    menubar = Menu(root)

    filemenu = Menu(menubar, tearoff=0)  # sous menu
    filemenu.add_command(label="Quitter", command=root.destroy)
    menubar.add_cascade(label="Fichier", menu=filemenu)

    root.config(menu=menubar)

    ##Titre
    """
    header = Label(root, text="C'est à {} {} de jouer !".format(joueur.nom, joueur.num))
    header.pack(fill="both", expand="no")"""

    ##panneau  informatif
    # indicatif = LabelFrame(root, text="Module indicatif")
    # indicatif.pack(fill="both", expand="yes", side=TOP)
    """
    deckCard = Button(root, text ="La carte posée est | ~ {} de {} ~ |".format(a.table.val, a.table.typ))
    deckCard.pack()"""

    """
    interactif = LabelFrame(root, text="Module interactif")
    interactif.pack(fill="both", expand="yes", side=TOP)

    subinteractif1 = Frame(interactif)
    subinteractif1.pack(fill="both", expand="yes", side=TOP)
    """
    cartetable = genCanvas(jeu.table, root)
    cartetable.grid(row=0, column=int(len(joueur.hand) // 2))

    jouer = Button(root, text="Jouer cette carte", command=Play)
    jouer.grid(row=1, column=int(len(joueur.hand) // 2), pady=100)
    etiquettes = [" "] * len(joueur.hand)
    values = [i for i in range(len(joueur.hand))]
    global var
    var = IntVar()
    var.set(values[0])
    for i in range(len(joueur.hand)):
        but = Radiobutton(root, variable=var, text=etiquettes[i], value=values[i])
        can = genCanvas(joueur.hand[i], root)
        can.grid(row=2 + i // 7, column=i, padx=40, pady=40)
        but.grid(row=3 + i // 7, column=i)

    root.mainloop()


def Play():
    print("ok")
    global selected, stat
    stat = True
    selected = var.get()
    appel()


def appel():
    global copyjo, copyje
    if stat:
        copyjo, copyje = TheRest(copyjo, copyje)
    if played:
        root.destroy()
        jeu = copyje.pack()

        a.unpack(jeu)
        a.player[a.active] = copyjo


def TheRest(joueur, jeu):
    print("bruh")
    for i in joueur.StartMethodList:  # effets de début de tour
        paquet, jeu = i(joueur, jeu)
    played = False
    if not joueur.peutJouer(jeu):
        jeu = joueur.pioche(jeu)
        printSomething(root, "Vous piochez : ", joueur.hand[-1])

    if not joueur.peutJouer(jeu):
        printSomething(root, "Vous ne pouvez pas jouer. ")

    else:
        indice = selected

        if joueur.playable(indice, jeu) == False:
            printSomething(root, "Vous ne pouvez pas jouer cela.")
        else:
            jeu = joueur.pose(indice, jeu)
            played = True

    if len(joueur.hand) == 0:
        jeu = joueur.setVictory(jeu)
    if jeu.nextPlayer != joueur.num:
        printSomething(root, "Fin du tour")

    joueur.clearLists()
    stat = False
    return joueur, jeu


def starterTk():
    global starter, starterNbc, starterNbj

    starter = LabelFrame(root, text="Configuration : initiale")
    starter.pack(fill="both", expand="yes", side=TOP)

    left1 = Label(starter, text="nombre de joueurs")
    left1.pack()  # on intègre le module déclaré à sa fenêtre (pack(sans paramètre) donc simplement à la suite du reste)

    starterNbj = Spinbox(starter, from_=2, to=6, )
    starterNbj.pack()  # on intègre le module déclaré à sa fenêtre (pack(sans paramètre) donc simplement à la suite du reste)

    left1 = Label(starter, text="nombre de cartes par main")
    left1.pack()  # on intègre le module déclaré à sa fenêtre (pack(sans paramètre) donc simplement à la suite du reste)

    starterNbc = Spinbox(starter, from_=7, to=20, )
    starterNbc.pack()  # on intègre le module déclaré à sa fenêtre (pack(sans paramètre) donc simplement à la suite du reste)

    creatbutton = Button(starter, text="Jouer !", command=startGame)
    creatbutton.pack()


def printSomething(fen, texte, carte="rien"):
    message = Toplevel()

    t = Label(message, text=texte)
    t.pack()
    if carte != "rien":
        c = genCanvas(carte, message)
        c.pack()
    ok = Button(fen, text="ok", command=self.destroy)
    message.mainloop()


def genCanvas(carte, fen):
    colors = {"Bambous": "green", "Cascade": "blue", "Braises": "red", "Lumière": "yellow", "Pouvoir": "black"}
    s = 2 / 3
    if type(carte.val) == int:
        texte = str(carte.val)
    elif carte.val == "Salamandre":
        texte = "+2"

    elif carte.val == "Cataclysme":
        texte = "+4"

    elif carte.val == "Tempête":
        texte = "J"

    elif carte.val == "Esprit":
        texte = "~"

    elif carte.val == "Dragon":
        texte = "¤"
    else:
        texte = "?"

    dessin = Canvas(fen, bd=15, bg=colors[carte.typ], height=int(300 * s), width=int(200 * s))
    dessin.create_oval(int(30 * s), int(30 * s), int(200 * s), int(300 * s), fill="white", width=0)
    dessin.create_text(int(120 * s), int(70 * s), anchor="n", state="disabled", font=('Times', int(-165 * s), 'bold'),
                       justify="center", text=texte)

    return dessin

goGui = 0

if goGui :

    global gui
    gui = False
    askGui = input("saisir 'gui' pour obtenire une interface graphique :  ")
    if askGui == 'gui':
        global root
        gui = True
        root = Tk()  # création de la fenêtre tkinter racine
        root.wm_title('Uno Client')
        starterTk()
        root.mainloop()


if __name__ == '__main__':
   nombreJoueurs = int(input("Veuillez saisir un nombre de joueurs :  "))
   a = Jeu(True, "False", nombreJoueurs)
   a.launch()
