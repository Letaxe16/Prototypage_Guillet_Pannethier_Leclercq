# Prototypage d'un robot de surveillance

## Présentation de l'équipe:

Nous avons réalisé ce projet de prototypage en trinôme, les membres de l'équipe sont: <br>

- Clément Leclercq
- Théo Pannethier 
- Axel Guillet

## Objectifs:

Le but de ce projet de 20h était de prototyper un robot de surveillance en utilisant un TurtleBot comme base. Au cours de ce projet nous devions aussi utiliser le matériel suivant:

- Servomoteur dynamixel AX-12
- 1 capteur de proximité (sharp, ToF…)
- ESP32 T-Display
  
Ainsi que les technologies suivantes:

- ROS (en Python)
- Langage Arduino
- BLE (Bluetooth Low Energy)
- Application smartphone (MIT App Inventor)
- Impression 3D

Nous avons créé un robot de surveillance avec deux modes de fonctionnement: 

- un mode de pilotage manuel (avec un volant Logitech G29 et les pédales permettant d'avancer / reculer)
- un mode automatique (Le robot tourne automatiquement à droite lorsqu'il détecte un obstacle)

Nous avons créé une application mobile avec le retour caméra du robot, permettant à l'utilisateur de pouvoir manier le robot plus facilement. L'application peut aussi se connecter en BLE à l'ESP 32 du robot afin que l'utilisateur puisse lui communiquer diverses paramètres:

- Commande de l'angle de rotation de la caméra du robot (ente 0 et 360°), la rotation de la caméra est commandé par un moteur dyanmixel AX-12

- Changer le mode de fonctionnement du robot (manuel / automatique)
  
- Modifier la vitesse de fonctionnement du robot

Un capteur de distance ToF, avec une sensibilité d'environ 1 mètre est aussi connecté à l'ESP 32, ce capteur est crucial dans le mode automatique puisqu'il permet au robot de tourner automatiquement à droite lorsqu'il détecte un obstacle.














[Cliquez ici pour voir le robot fonctionné](U)


