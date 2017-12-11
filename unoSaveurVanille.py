# coding : utf-8

from random import *


def initialisation():
    # sauf si tu trouves une autre méthode, je suis obligé de passer le deck en global pour qu'il soit utilisable par les joueurs
    print("Bienvenue !")
    global deck
    deck = [["+4", 0], ["+4", 0], ["+4", 0], ["+4", 0], ["change", 0], ["change", 0], ["change", 0], ["change", 0]]
    val = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, "+2", 1, 2, 3, 4, 5, 6, 7, 8, 9, "+2", "sens", "sens", "no", "no"]
    # jeu alternantif :   val=[0,1,2]#,3,4,5,6,7,8,9,"+2"]#,1,2,3,4,5,6,7,8,9,"+2","sens","sens","no","no"]

    colors = ["j", "v", "b", "r"]
    for i in range(len(val)):
        for j in range(len(colors)):
            deck.append([val[i], colors[j]])
    shuffle(deck)
    routine()


class Mj():
    ''' maitre du jeu , objet manipulant les 'cartes' & les permissions
    '''

    def __init__(self, nombreJoueurs=2):
        self.player = []
        self.alivePlayers = [i for i in range(nombreJoueurs)]
        self.sens = True
        self.lastPlayer = nombreJoueurs - 1  # dernier joueur ayant joué

        self.chainMemory = 0
        self.battle = False
        for i in range(nombreJoueurs):
            self.player.append(Player(i))

        self.table = deck.pop(0)

        self.bin = []

        while type(self.table[0]) != type(1):  # si la 1ere carte est "spéciale"
            self.bin.append(self.table)  # on repioche jusqu'à l'obtention d'un nbr
            self.table = deck.pop(0)

    def whosNext(self):
        if self.table[0] == "no":
            if self.sens:
                return self.alivePlayers[(self.lastPlayer + 2 * 1) % (len(self.alivePlayers))]
            else:
                return self.alivePlayers[(self.lastPlayer - 2 * 1 + len(self.alivePlayers)) % (len(self.alivePlayers))]

        else:
            if self.sens:
                return (self.lastPlayer + 1) % (len(self.alivePlayers))
            else:
                return (self.lastPlayer - 1) % (len(self.alivePlayers))

    def call(self):
        called = self.whosNext()
        print("\nC'est le tour du joueur {} !".format(called + 1))
        print(self.table)
        input("Appuyer sur une touche...")
        action = self.player[called].play()
        return called, action

    def validation(self, act):
        if (self.table[0] != "+2" and self.table[0] != "+4") or self.battle == False:  # si on a pas de surenchère,
            if act == "pioche":  # le joueur peut effectuer un tour "normal" (jouer/piocher)
                return True

            elif self.table[0] == act[0] or self.table[1] == act[1]:
                return True

            elif act[1] == 0:
                return True

            else:  # carte interdite
                return False



        else:  # +4 ou +2
            if act == "pioche":
                return True

            elif act[0] == self.table[0]:  # surenchère
                return True

            else:  # mauvaise carte
                return False

    def ParentDeJeu(self):
        '''
        fct qui appelle jeu et le rapelle après une pioche
        '''

        replay = False
        endTurn, called = self.jeu(replay)
        if endTurn == False:
            replay = True
            self.jeu(replay)
        self.lastPlayer = called

    def jeu(self, replay):
        called, action = self.call()
        test = self.validation(action)
        while test != True:
            print("\nAction Impossible")
            called, action = self.call()
            test = self.validation(action)
        if action != "pioche":
            del self.player[called].main[self.player[called].indice]
        endTurn = False

        if action == "pioche" and replay == False:
            if self.table[0] != "+2" and self.table[0] != "+4":  # si on a pas de surenchère
                self.player[called].pioche()
                endTurn = False
            elif self.table[0] == "+2" and self.battle == True:

                endTurn = True
                for i in range(int(self.chainMemory)):
                    self.player[called].pioche()
                self.chainMemory = 0

            elif self.table[0] == "+4" and self.battle == True:

                endTurn = True
                for i in range(int(self.chainMemory)):
                    self.player[called].pioche()
                self.chainMemory = 0
            self.battle = False

        elif action == "pioche" and replay == True:
            endTurn = True
            self.battle = False

        else:
            self.bin.append(self.table)
            self.table = action

            if self.table[0] == "sens":
                self.sens = not (self.sens)
                endTurn = True

            if self.table[0] == "change":
                self.table[1] = self.player[called].askColor()
                endTurn = True

            if self.table[0] == "+2":
                self.chainMemory += 2
                endTurn = True
                self.battle = True
            if self.table[0] == "+4":
                self.table[1] = self.player[called].askColor()
                self.chainMemory += 4
                endTurn = True
                self.battle = True
            else:
                endTurn = True

        return endTurn, called


class Player():
    '''Classe joueur, qui permet à un ultilisateur physique de donner des instructions
    '''

    def __init__(self, number):
        self.playerNumber = number
        self.main = [deck.pop(0) for i in range(7)]
        self.gagne = False

    def play(self):
        print(self.main)
        self.indice = input("indice de la carte à jouer  (-1 pour piocher/passer) :")
        ActionCorrecte = False
        while ActionCorrecte == False:
            try:
                self.indice = int(self.indice)
                ActionCorrecte = True
            except:
                self.indice = input("merci d'entrer un entier :")
        if self.indice < 0:
            return "pioche"
        else:
            if self.indice >= len(self.main):
                self.indice = len(self.main) - 1
            carte = self.main[self.indice]
            if len(self.main) == 1:
                print("Uno !")

            elif len(self.main) == 0:
                self.victoire()
            return carte

    def pioche(self):
        print("Joueur {} pioche !".format(self.playerNumber + True))
        if len(deck) == 0:
            recyclage()
            print("Reconstruction du deck...")
        self.main.append(deck.pop())

    def askColor(self):
        color = 'satan'
        colors = ["v", "b", "j", "r"]
        while colors.count(color) == 0:
            color = input("r/v/j/b")
        return color

    def victoire(self):
        self.gagne = True


def routine():
    global Sensei
    Sensei = Mj(2)  # nombre de joueurs

    while len(Sensei.alivePlayers) != 1:
        Sensei.ParentDeJeu()

        for i in range(len(Sensei.alivePlayers)):
            if Sensei.player[Sensei.alivePlayers[i]].gagne == True:  # enlève le joueur qui a gagné
                print(str(Sensei.alivePlayers[i] + 1) + " a gagné !")
                del Sensei.alivePlayers[i]
    print("La partie est terminée, le perdant est le joueur " + str(Sensei.alivePlayers[0] + 1))


def recyclage():
    global deck
    deck = list(Sensei.bin)
    # print("len bin {}".format(len(Sensei.bin)))
    # print("deck : {}".format(deck))
    shuffle(deck)
    Sensei.bin = []
    # print("deck apres: {}".format(deck))
    for i in range(len(deck)):  # on redonne aux cartes qui ont changé de couleur le noir d'origine
        if deck[i][0] == "change" or deck[i][0] == "+4":
            deck[i][1] = 0


if __name__ == '__main__':
    initialisation()
