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

### Récapitulatif des communications Hardware : 

![alt text](https://github.com/Letaxe16/Prototypage_Guillet_Pannethier_Leclercq/blob/main/hardware_graph.png)

### Achitechture ROS : 

![alt text](https://github.com/Letaxe16/Prototypage_Guillet_Pannethier_Leclercq/blob/main/graph.png)

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

- Clonez ce repo
- Dans un terminal, placez vous avant le src
- source /opt/ros/ROSDISTRIBUTION/setup.bash
- export ROS_DOMAIN_ID=2
- export ROS_LOCALHOST_ONLY=0
- colcon build --packages-select turtlebot_control
- source install/setup.bash
- ros2 launch turtlebot_control triton_launch.py

### Sur la turtlebot kobuki 4 avec une distribution foxy

- Clonez ce repo
- Dans un terminal, placez vous avant le src
- source /opt/ros/foxy/setup.bash
- export ROS_DOMAIN_ID=2
- export ROS_LOCALHOST_ONLY=0
- colcon build
- source install/setup.bash
- Ouvrez 6 autres terminaux, pensez à exporter le ROS_DOMAIN_ID, le LOCALHOST_ONLY et à sourcer install/setup.bash après vous être rendu avant le dossier src
- Dans le terminal 1: ros2 launch kobuki_node kobuki_node-launch.py
- Dans le terminal 2: ros2 run camera_send camera_send
- Dans le terminal 3: ros2 run camera_control camera_control
- Dans le terminal 4: ros2 run dynamixel dynamixelControl
- Dans le terminal 5: ros2 run dynamixel_sdk_examples read_write_node 
- Dans le terminal 6: ros2 run esp_command read_serial

Nous avons ici créée trop de package par rapport à ce que l'on avait, une bonne pratique aurait été de créé un seul package avec plusieurs nodes.

### Lancer l'application

Pour lancer l'app sur MIT Inventor app, il faut d'abord télécharger l'application "MIT AI2 Companion" sur téléphone. Sur l'ordinateur, cliquez sur "Projects", puis sur "Import project from my computer" et sélectionner l'application "BLE_controller_app2" sur ce repo git. Allez ensuite dans "Connect" puis cliquez "AI Companion". Sur l'application associée sur le téléphone, scannez le QR code qui s'affiche pour charger l'application. Sur l'app, vous pouvez voir:

- Un retour caméra connecter via une connexion wifi
- Un bouton de connexion / déconnexion au BLE
- Une commande d'angle envoyée à la caméra
- Un switch permettant de changer de mode (automatique / manuel)
- Une commande de vitesse

[Pour le poster, c'est par ici ;)](https://docs.google.com/presentation/d/1WS9vpEQbbWqnNprn5wOiG1peDnAIBaEEbh5glAAThIg/edit#slide=id.p)

[Cliquez ici pour voir le robot fonctionner](https://www.youtube.com/watch?v=-LsRl1qgzCM)

:+1:


