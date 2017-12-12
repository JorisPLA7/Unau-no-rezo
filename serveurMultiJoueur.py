from lib.serveur import *

global broadcast
broadcast = True  # ATTENTION DEF LE BROADCAST à VRAI OU FAUX EST INDISPENSABLE POUR LE MOMENT


def SimpleHost():
    '''Fct de démonstration et de test.


    Par Joris Placette
    '''
    MyServ = ServerNet()
    MyServ.Listen(True)

    print("Note : Vous pouvez effectuer plusieurs parties conséqutives sans redémarer le serveur.")
    print("Note : Ce serveur peut accueillir une partie à la fois.")
    print("Note : Pour Lancer une partie référez-vous au ReadMe joint avec les fichiers.")

    print("Serveur Démarré avec succès.")
    print("En attente de clients...")


if __name__ == '__main__':
    SimpleHost()  # ce fichier sera peut-être une librairie, il faut donc empêcher l'inclusion du login si appelée par un autre fichier.
