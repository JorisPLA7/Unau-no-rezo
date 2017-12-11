# -∗- coding: utf-8 -∗-
# toute l'initiallisation des lib est en try except pour pouvoir dépister instantanément d'éventuels dépendances non satisfaites

import pickle
import socket
import threading

global Host, Port, broadcast
broadcast = True
Host = '127.0.0.1'  # l'ip locale de l'ordinateur
Port = 8082  # choix d'un port

Sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Sock.bind((Host, Port))

# Fonction intéragissant avec la base de donnée


global Flow


class ServerNet():
    '''Classe Serveur, sert d'interface entre certains threads et mes collègues


    '''

    def __init__(self):  # initiallisation du thread de reception des nouveaux clients
        global Timeout
        Timeout = 1.0  # timeout crucial pour que le serv abandonne l'écoute toute les 2 secondes pour transmettre le(s) message(s)
        global verbose
        verbose = 0  # en cas de besoin il est possible de demander au serveur plus d'informations.

        global NicknameList
        NicknameList = {}
        '''
        La NicknameList est un historique des utilisateurs connectés depuis le lancement.
        Elle permet de savoir à quel thread s'adresser pour envoyer des informations.

        Par exemple pour envoyer un message à 'joris' :
        MyClient[NicknameList['joris']].Transmit('Message!')

        Quand deux clients s'identifient avec le même pseudonyme alors seul le dernier client connecté aura son ID associé avec le pseudonyme

          
        '''

        global MyClient
        MyClient = []

        self.ReceptionistThread = Receptionist(1, "ReceptionistThread")

    def Listen(self, Toogler):
        if Toogler == True:
            self.ReceptionistThread.start()


class Guest(threading.Thread):
    '''Classe de gestion de Client individuellement.


    '''

    def __init__(self, GuestID, Client, Address):  # initiallisation des variables de l'objet nouvellement crée
        threading.Thread.__init__(self)
        self.__GuestID = GuestID
        self.Client = Client
        self.Client.settimeout(
            Timeout)  # timeout crucial pour que le serv abandonne l'écoute toute les 2 secondes pour transmettre le(s) message(s)
        self.Address = Address
        self.Identificated = False
        self.Nickname = None
        self.NickLen = None
        self.IdentificationThread = 0
        self.DoComm = 0
        self.Message = []

    def SetNickname(self, NewNick):
        self.Nickname = NewNick
        self.NickLen = len(self.Nickname)

    def GetIdentified(self):
        while not self.Identificated:
            data = self.Client.recv(32)  # on recoit x caracteres grand max
            RequeteDuClient = data.decode()  # qu'on décode
            RequeteDuClient = str(object=RequeteDuClient)
            if verbose: print("RequeteDuClient : '{}'".format(RequeteDuClient))

            if RequeteDuClient[0:4] == 'IDTF':
                ReceivedNickLen = int(RequeteDuClient[4])  # lecture de la longueur du pseudo (doit être <= à 9 char! )
                if verbose: print("ReceivedNicklen = {}".format(ReceivedNickLen))
                self.Nickname = RequeteDuClient[5:5 + ReceivedNickLen]

                self.Identificated = True  # Le client est désormais identifié
                me = (self.Client)
                NicknameList[
                    self.Nickname] = self.__GuestID  # permet à samuel de savoir à quel thread s'adresser en donnant un pseudo
                if verbose:  print("Historique des clients : {}".format(NicknameList))
                print("Client {} Identifié !".format(self.Nickname))

    def __RequestTreatment(self, Request):
        Flow(self.__GuestID, self.Address, self.Nickname, Request)  # sinon on la soumet à la fonction flow pour Samuel

    def Transmit(self, msg):
        '''Cette fonction permet d'envoyer du contenu tel qu'une chaine de caractères (un tuple, une image, etc...) au client.


        '''
        self.Message.append(msg)

    def __Comm(self, value):
        ''' Classe chargée de l'envoi & récéption de donnée via le socket une fois le client Identifié.
        Elle s'occupe de la partie "veille" de la classe Net.




        '''
        self.DoComm = value  # variable permettant de stopper les échanges
        while self.DoComm == 1:
            if len(self.Message) >= 1:  # si un message a été ajouté depuis la dernière fois
                data = self.Message.pop()
                dataP = pickle.dumps(data)
                if verbose: print('pickled!')

                self.Client.sendall(dataP)  # envoi du message ss forme de bytecode
                if verbose: print('data sent!')
                # conn, addr = s.accept()

            try:
                data = self.Client.recv(9000)
                if verbose: print('received!')
                dataP = pickle.loads(data)
                if verbose: print('unpickled!')
                # print(type(dataP), "-------------------- serv")
                # print(type(dataP['test']), "-------------------- test")

                self.__RequestTreatment(
                    dataP)  # on sous-traite les données pour reserver cette fonction aux seuls communications
            except:
                pass

    def WhoIsIt(self):
        '''Fonction retournant le Pseudonyme rensigné par l'utilisateur lors de la phase d'Identification.

        '''
        return self.Nickname

    def run(self):
        '''Se lance automatiquement en thread.



        '''
        try:
            self.GetIdentified()
        except:
            print("impossible d'Identififier le client {}".format(self.Address))

        if self.Identificated: self.__Comm(1)


class Receptionist(threading.Thread):
    ''' Classe de threading chargée de récéptionner les conncetions des clients.
    concue pour être invoquée en 1 exemplaire par la classe ServerNet.




    '''

    def __init__(self, threadID, name):  # initiallisation des variables de l'objet nouvellement crée
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        i = 0  # i : thread counter
        while 1:  # On est a l'ecoute d'une seule et unique connexion à la fois :
            Sock.listen(5)
            # Le script se stoppe ici jusqu'a ce qu'il y ait connexion :
            Client, Address = Sock.accept()  # accepte les connexions de l'exterieur
            t = Guest(i, Client, Address)
            MyClient.insert(i, t)  # c'est moche mais onn y touche plus
            MyClient[i].start()
            i += 1


def Flow(clientID, clientAddress, clientNick, data):
    '''Cette fonction est appelée à chaque fois que des données sont recues.
    Le traitement de ces données est une simple démonstration.
    Cette fonction permettra à Samuel de recevoir et traiter les données émises par les clients.

    pour envoyer un message à un client précis: MyClient[NicknameList['joris']].Transmit('Message!')


    '''
    global cache
    cache = data
    result = "-- {} -- {} {} :  {}".format(clientID, clientNick, clientAddress, data)
    if verbose: print(result)

    if broadcast == True:
        for i in range(0, len(MyClient) + 1):
            MyClient[i].Transmit(data)

    if isinstance(data, str) == True:
        a = verificationPseudo(data)
        if verbose: print(a)
        if a == False:
            userAdd(data)

    elif isinstance(data, int) == True:
        requestMessage(data, clientNick)

    elif isinstance(data, list) == True:
        writeMessage(data[1], data[0])


def SimpleHost():
    '''Fct de démonstration et de test.
    c'est un cadeau pour toi Samuel <3 ^^


    '''
    MyServ = ServerNet()
    MyServ.Listen(True)
    print("En attente de clients...")


if __name__ == '__main__':
    SimpleHost()  # ce fichier sera peut-être une librairie, il faut donc empêcher l'inclusion du login si appelée par un autre fichier.
