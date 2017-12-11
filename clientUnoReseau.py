# -∗- coding: utf-8 -∗-
global debug
debug = False

import pickle
import socket
import threading
import time

import UnoPOO


# ---------------------UNO Local---------------------------

def getNetworkInfos():
    '''Fct de démonstration et de test.
    Par Joris Placette
    '''
    host = input('''Saisir l' adresse du serveur (laisser vide pour une 127.0.0.1)  : ''')
    if host == '': host = "127.0.0.1"
    port = 8082
    if debug: print("Saisir 'q' pour obtenir un terminal de commande")

    nickname = ''
    while nickname == '':
        nickname = str(input("saisir un pseudo (inferieur à 10 caractères):  "))

    password = "azertyuiop mdr en vrai ignorez pmoi je sers à rien  "  # prévu juste au cas où un jour l'envie nous prends de sécuriser un peu les échanges

    return (host, port, nickname, password)


def getLocalID():
    id = int(input('saisir id client local :  '))
    if id == 0:
        roomPlayers = int(input('saisir le nombre de joueurs dans la partie :  '))
    else:
        roomPlayers = 2  # la valeur ser écrasée si le joueur n'est pas le premier à jouer
    return id, roomPlayers


# ------------------------client.py---------------------





class NetThread(threading.Thread):
    '''Classe-Thread chargé de l'envoi & récéption de donnée via le socket une fois le client identifié.
    Elle s'occupe de la partie "veille" de la classe Net.

    N'est pas concue pour être manipulée par Mes camarades.

    Voir l' help(Net())

    Par Joris Placette
    '''

    def __init__(self):
        threading.Thread.__init__(self)  # séquence init du thread
        self.Message = []
        self.thereIsSomeNewData = False  # désolé pour la longueur du nom de cette variable je nickname'ai pas trouvé mieux

    def __RequestTreatment(self, Request):

        receptionPaquet(Request)
        # flow(Request)
        # #extractiona =  des données pour qu'elles soient récupérées par Arthur

    def run(self):

        while 1:
            if len(self.Message) >= 1:  # si un message a été ajouté depuis la dernière fois
                data = self.Message.pop()
                dataP = pickle.dumps(data)
                if debug: print('pickled!')
                Sock.sendall(dataP)  # envoi du message ss forme de bytecode
                if debug: print('data sent!')
                # conn, addr = s.accept()

            try:
                data = Sock.recv(9000)

                if debug: print('received!')
                dataP = pickle.loads(data)
                if debug: print('unpickled!')
                if debug: print(type(dataP))

                data = dataP  # attente d'une reponse pdt 2sec en cas de timeout retourne une erreur, d'ou le try & except

                self.thereIsSomeNewData = True

            except:
                pass
                # print("y'a un pb bb") #en cas de time-out on passe simplement à la suite
            if self.thereIsSomeNewData:
                self.__RequestTreatment(data)  # J'ai sorti la fonction du try; pour rendre le débuggage possible
            self.thereIsSomeNewData = False


class Net():
    '''Classe interactive (API) pour mes camarades, se charge de mettre en forme les interactions client-serveurr pour une utilisation simplifiée des fonctionnallités socket.

    Par Joris Placette
    '''

    def __init__(self, Host, Port, Nickname, Pass):

        global Sock  # devra être accessible dans toutes les classes
        Sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # on cree notre socket
        Sock.settimeout(
            1.0)  # timeout crucial pour que le serv abandonne l'écoute toute les 2 secondes pour transmettre le(s) message(s)

        self.host = socket.gethostbyname(
            Host)  # récupération de l'adresse auprès des DNS par défaut si nom de domaine fourni
        self.port = Port
        self.nickname = Nickname  # La Gui indique Pseudo au lieu de nickname, doit mesurer 10 charactères ou moins
        self.nickLen = str(len(self.nickname))  # calcul de la longueur du Pseudonyme
        self.password = Pass  # le pas ne sert pas durant la phase d'identification du client, j'ai cependant implanté cette variable si mes camarades en ont besoin
        self.connected = False
        self.__NetThread = NetThread()
        self.__NetThread.start()  # Démarrage du thread chargé d'éccouter et de shipper les messages

    def identify(self):
        '''Envoie une requette d'identification.
        Necessaire coté serveur c'est la première chose à faire après avoir initialisé Net.

        Par Joris Placette
        '''
        data = bytes("IDTF" + self.nickLen + self.nickname,
                     'utf8')  # on crée la chaine d'info d'identification comme "IDTF7exemple"

        try:
            Sock.connect((self.host, self.port))  # on se connecte sur le serveur avec les informations données
            print("Connection avec le serveur...")
            Sock.sendall(data)
            print("Identification auprès du serveur...")
            time.sleep(1)  # afin de donner le temps au serv d'être en écoute
            print("Connection établie :) ")
            self.connected = True  # la connexion a été établie, MAJ du status

        except:
            print("Impossible de se connecter au serveur !")
            self.connected = False

    def connected(self):
        '''Affiche le statut du client vis à vis du serveur

        Par Joris Placette
        '''
        return self.connected

    def disconnect(self):
        '''Force la fermeture de la connexion, rends impossible l'entrée et la sortie de données.

        Par Joris Placette
        '''
        Sock.close()  # rends impossible l'entrée et la sortie de données.
        print("Déconnection")

    def share(self, typed):
        '''Permet de transmettre une chaine de caractères brute au serveur.

        /!\ : Pour le moment les messages sont transmis toute les 2sec et non empillés, donc en cas de spam des messages seront perdus :/

        /!\ : Version DEV :
            Svp pay attention :) !
            Si la Chaine est reconnue comme une ligne de code python alors elle est EXECUTEE.

        Par Joris Placette
        '''
        self.__NetThread.Message.append(
            typed)  # transmett la chaine au thread, on nickname'execute pas de fonction sinon il faut attentdre la fin de celle-ci , on se contente donc de transmettre la donnée.

    def whoAmI(self):
        '''Renvoie le Pseudonyme déclaré au serveur lors de l'__init__()

        Par Joris Placette
        '''
        return self.nickname


global flow


def flow(request):
    '''Cette fonction est appelée à chaque fois que des données sont recues.
    Le traitement de ces données est une simple démonstration.
    Cette fonction permettra à Arthur de recevoir et traiter les données émises par les clients.

    Par Joris Placette
    '''


def receptionPaquet(paquetIn):
    global a
    del a
    a = UnoPOO.Jeu(False, paquetIn)
    a.player[localID].nom = localNickname

    if localID == a.active:
        print('''! ! !  A TOI DE JOUER ! ! !''')
        a.ask()
        paquetOut = a.pack()
        network.share(paquetOut)

    else:
        print('en attente de joueur {}:  {} '.format(a.player[a.active].num, a.player[a.active].nom))


if __name__ == '__main__':
    # création de l'objet jeu
    global localID, localNickname
    localID, roomPlayers = getLocalID()

    global a

    a = UnoPOO.Jeu(True, 'False', roomPlayers)

    paquet = a.pack()

    # obtension des infos de networking
    host, port, localNickname, password = getNetworkInfos()

    # création de l'objet de networking client
    network = Net(host, port, localNickname, password)
    # identification auprès du serveur
    network.identify()

    ## en attente de la suite ...
    startAnswer = ''
    if localID == 0:
        print("Vous êtes joueur 0 donc l'hôte de cette partie.")
        print('Pour interagir avec le terminal python interactif tapez "term".')
        while startAnswer != 'go':
            startAnswer = input(
                'Quand {} joueurs au total sont connectés au serveur tapez "go" :  '.format(roomPlayers))
            if startAnswer == 'term':
                break
        network.share(paquet)
    else:
        print("En attente de l'hote. Veuillez patienter ...")
