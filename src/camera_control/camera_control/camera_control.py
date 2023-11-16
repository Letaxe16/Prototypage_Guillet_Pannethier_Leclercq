import cv2
from cv_bridge import CvBridge

import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image


class Camera(Node):

    def __init__(self):
        super().__init__('camera')
        self.publisher_ = self.create_publisher(Image, 'image_raw', 10)
        self.vs = cv2.VideoCapture('/dev/video0')
        timer_period = 1/40  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        # For example, read an image from file
        ret,image=self.vs.read()

        # Convert the OpenCV image to a ROS Image message
        bridge = CvBridge()
        ros_image = bridge.cv2_to_imgmsg(image, encoding='bgr8')
        self.publisher_.publish(ros_image)


def main(args=None):
    

    rclpy.init(args=args)

    control = Camera()

    rclpy.spin(control)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    control.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()


