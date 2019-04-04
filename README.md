# Unau
Python3 POO Uno online multiplayer game.

![Graph](http://www.tuks.ovh/github_webpages/Unau-no-rezo/Capture.png)

## Python3 libraries used installed by default with python3
- socket
- time
- random
- pickles
- threading

## Custom libraries
- lib / server

#### unoSaveurVanille.py file:
Basic uno game, without flavors nin as a game nor as a program.

#### UnoPOO.py file:
Local multiplayer Uno game programmed object oriented. (embedded interface).
Note: adding a graphical interface ...

#### File clientUnoReseau.py
Client for multiplayer networked game.

#### MultiPlayer.py file
Server required for mutiplayer games started with clientUnoReseau.py.
  
## Play online multiplayer:
  - Execute multiplayerServer.py

For each party
  - run clientUnoReseau.py (1 per player / post)
  - each customer must enter a different id from 0
  - follow the instructions for each client
  - type 'go' to start the game on the client 0


### note of understanding:

  virtuous circle:

  - a = monjeu(True, 4)

  - j
  
  - paquet = a.pack()
  
  - network.share(pauet)
  
  - network.flow()
  
  - a.receptionPaquet()
  
  - a.ask()
  
  - a.pack()

  - goto j :)
  
  ## Creators
  
  - Joris Placette - joris@placette.fr
  - Matéo Perez
