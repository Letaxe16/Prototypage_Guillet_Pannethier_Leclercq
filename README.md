Test
# Prototypage d'un robot de surveillance

## Présentation de l'équipe:

Nous avons réalisé ce projet de prototypage en trinôme, les membres de l'équipe sont: <br>

- Clément Leclercq
- Théo Pannethier 
- Axel Guillet

## Objectifs:

Notre projet de 20h était de prototyper un robot de surveillance en utilisant un Kobuki TurtleBot comme base. Au cours de ce projet nous devions aussi utiliser le matériel suivant:

- Servomoteur dynamixel AX-12
- 1 capteur de proximité (sharp, ToF…)
- ESP32 T-Display
  
Ainsi que les technologies suivantes:

- ROS2 (en Python)
- Langage Arduino
- BLE (Bluetooth Low Energy)
- Application smartphone (MIT App Inventor)
- Impression 3D

## Ce que nous avons fait:

### En résumé

Nous avons créé un robot de surveillance avec deux modes de fonctionnement: 

- un mode de pilotage manuel (avec un volant Logitech G29 et les pédales permettant d'avancer / reculer)
- un mode automatique (Le robot tourne automatiquement à droite lorsqu'il détecte un obstacle)

Nous avons créé une application mobile avec le retour caméra du robot, permettant à l'utilisateur de pouvoir manier le robot plus facilement. L'application peut aussi se connecter en BLE à l'ESP 32 du robot afin que l'utilisateur puisse lui communiquer diverses paramètres:

- Commande de l'angle de rotation de la caméra du robot (ente 0 et 360°), la rotation de la caméra est commandé par un moteur dyanmixel AX-12

- Changer le mode de fonctionnement du robot (manuel / automatique)
  
- Modifier la vitesse de fonctionnement du robot

Un capteur de distance ToF, avec une sensibilité d'environ 1 mètre est aussi connecté à l'ESP 32, ce capteur est crucial dans le mode automatique puisqu'il permet au robot de tourner automatiquement à droite lorsqu'il détecte un obstacle.

### Le mode manuel

Mode lancé par défaut.
Le mode manuel permet de contrôler le robot à l'aide d'un volant Logitech G29 et de son pédalier.
La pédale de droite permet d'avancer tandis que celle de gauche permet de reculer (appuyer sur les deux pédales en même temps ne fait rien car l'action des deux pédales se compense).
La pédale du centre ne sert à rien.

### Le mode automatique

En déclenchant le mode automatique via l'application, le robot suit un schéma basique: à chaque détection par le tof d'un obstacle à 60 cm ou moins, le robot s'arrête, tourne d'environ 90° sur la droite, puis reprend sa course après une légère pause.

Ce mode est pour l'instant très limité puisque l'on tourne à droite et pas forcément précisément à 90°. Il pourrait être améliorer en implémentant une centrale inertielle qui nous permettrait de mesurer très précisément l'angle de notre robot.  

### Commande de l'axe de la caméra

Nous avons mappé le contrôle de nos 2 dynamixels sur la croix directionnelle de notre volant logitech G29, ainsi nous pouvons en plus de l'application, régler manuellement l'orientation droite gauche et haut bas de notre caméra.

## Procédure de lancement du projet

Nous allons vous expliquer comment lancer le projet

### Sur un ordinateur avec ros2 humble ou foxy

### Sur la turtlebot kobuki 4 avec une distribution foxy

### Lancer l'application
TODO Axel









[Cliquez ici pour voir le robot fonctionner](U)


