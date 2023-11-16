import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist
from std_msgs.msg import Int16
from time import sleep

class Control(Node):

    def __init__(self):
        super().__init__('turtlebot_control')
        self.subscription_joy = self.create_subscription(
            Joy,
            'joy',
            self.joy_callback,
            10)
        
        self.subscription_tof = self.create_subscription(
            Int16,
            'tof',
            self.tof_callback,
            10
        )
        
        self.subscription_mode_change = self.create_subscription(
            Int16,
            'mode_change',
            self.mode_change_callback,
            10
        )

        self.subscription_speed_command = self.create_subscription(
            Int16,
            'speed_command',
            self.speed_command_callback,
            10
        )

        self.subscription_joy  # prevent unused variable warning
        self.subscription_tof  # prevent unused variable warning
        self.subscription_mode_change  # prevent unused variable warning
        self.subscription_speed_command  # prevent unused variable warning
        self.publisher_turtle = self.create_publisher(Twist, '/commands/velocity',10)
        self.flag_manuel = True
        self.flag_auto = False
        self.commande = Twist()
        self.commande.linear.y = 0.0
        self.commande.linear.z = 0.0
        self.commande.angular.x = 0.0
        self.commande.angular.y = 0.0
        self.facteur_accel = 0.5


    def joy_callback(self, msg):

        if self.flag_manuel:
            avant = msg.axes[2] # Pédale de droite
            volant = msg.axes[0] # Volant
            arriere = msg.axes[1] # Pédale de gauche
            facteur_steer = 3
            avant = avant + 1 # On met la pédale de droite entre 0 et 2 puisque actuellement nous sommes entre -1 et 1 (-1 étant la valeur sans toucher à la pédale)
            arriere = -1 - arriere #On met la pédale de gauche entre -2 et 0 puisque actuellment nous sommes entre -1 et 1 (-1 étant la valeur sans toucher à la pédale)
            acceleration = avant + arriere
            self.commande.linear.x = acceleration * self.facteur_accel
            self.commande.angular.z = volant*facteur_steer
            self.publisher_turtle.publish(self.commande)
        elif not(self.flag_auto):
            self.commande.linear.x = 0.0
            self.commande.angular.z = 0.0
            self.publisher_turtle.publish(self.commande)

    def tof_callback(self,msg):
        distance_max = 600
        if self.flag_auto:
            distance_to_wall = msg.data
            if distance_to_wall <= distance_max:
                self.commande.linear.x = 0.0
                self.commande.angular.z = 0.0
                self.publisher_turtle.publish(self.commande)
                sleep(1)
                self.commande.linear.x = 0.0
                self.commande.angular.z = -3.63
                self.publisher_turtle.publish(self.commande)
                sleep(1)
                self.commande.linear.x = 0.0
                self.commande.angular.z = 0.0
                self.publisher_turtle.publish(self.commande)
                sleep(4)
            else:
                self.commande.linear.x = self.facteur_accel
                self.commande.angular.z = 0.0
                self.publisher_turtle.publish(self.commande)

    def mode_change_callback(self,msg):
        self.flag_auto = not(self.flag_auto)
        self.flag_manuel = not(self.flag_manuel)
        print(f"Mode Manuel: {self.flag_manuel}")
        print(f"Mode Auto: {self.flag_auto}")
    
    def speed_command_callback(self,msg):
        self.facteur_accel = 0.5*float(msg.data)
        print(f"Facteur d'acceleration: {self.facteur_accel}")

def main(args=None):
    rclpy.init(args=args)

    control = Control()

    rclpy.spin(control)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    control.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()