# Unau
Jeu de Uno.

## Librairies python3 utilisées installées par défaut avec python3 
- socket
- time
- random
- pickles
- threading

## Librairies personnalisées 
- lib/serveur

Fichier uno.py : 
  Jeu de uno basique, sans saveurs nin en tant que jeu ni en tant que programme.
  
## Lancement d'une partie de Jeu de Uno en multijoueur en ligne:
  - executer serveurMultiJoueur.py

Pour chaque partie  
  - executer clientUnoReseau.py (1 par joueur/poste)
  - chaque client doit saisir un id différent à partir de 0
  - suivre les instructions pour chaque client
  - saisir 'go' pour lancer la partie sur le client 0



### remarque de compréhension : 

  cercle vertueux:

  - a = monjeu(True, 4)

  - j
  
  - a.pack()
  
  - myNet.Transmit()
  
  - myNet.flow()
  
  - a.receptionPaquet()
  
  - a.ask()
  
  - a.pack()

  - goto j :)
