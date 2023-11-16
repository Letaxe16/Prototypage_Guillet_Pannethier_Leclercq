import rclpy
from rclpy.node import Node
import serial
from std_msgs.msg import Int16


class read_serial(Node):

    def __init__(self):
        super().__init__('read_serial')
        self.pub_tof_received = self.create_publisher(Int16, "tof", 10)
        self.pub_angle_received = self.create_publisher(Int16, "angle_cam", 10)
        self.pub_mode_received = self.create_publisher(Int16, "mode_change", 10)
        self.pub_speed_command = self.create_publisher(Int16, "speed_command", 10)
        self.read_callback()

    def read_callback(self):

        ser = serial.Serial('/dev/ttyUSB0', 9600)  # Assurez-vous de spécifier le bon port et le bon débit en bauds

        while True:

            data = ser.readline().decode('utf-8').strip()  # Utilisation de strip() pour retirer les caractères de contrôle

            if "TOF" in data:
                
                tof_str = data.split(":")[1]

                if tof_str.isnumeric():

                    tof_num = int(tof_str)

                    msg = Int16()
                    msg.data = tof_num

                    self.pub_tof_received.publish(msg)

            elif "Angle_cam" in data:

                angle = data.split(":")[1]

                if angle.isnumeric():

                    angle_num = int(angle)

                    msg = Int16()
                    msg.data = angle_num

                    self.pub_angle_received.publish(msg)


            elif "Mode_status" in data:

                mode = data.split(":")[1]

                if mode.isnumeric():

                    mode_num = int(mode)

                    msg = Int16()
                    msg.data = mode_num

                    self.pub_mode_received.publish(msg)

            elif "Speed_command" in data:

                speed = data.split(":")[1]

                if speed.isnumeric():

                    speed_num = int(speed)

                    msg = Int16()
                    msg.data = speed_num

                    self.pub_speed_command.publish(msg)
            

def main(args=None):

    rclpy.init(args=args)

    node = read_serial()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()