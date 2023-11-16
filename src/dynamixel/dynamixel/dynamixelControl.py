import rclpy
from rclpy.node import Node
from functools import partial

from dynamixel_sdk_custom_interfaces.msg import SetPosition
from dynamixel_sdk_custom_interfaces.srv import GetPosition
from sensor_msgs.msg import Joy
from std_msgs.msg import Int16


class dynamixelControl(Node):

    def __init__(self):
        super().__init__('dynamixel_Control')
        self.publisher_ = self.create_publisher(SetPosition, 'set_position', 10)


        self.subscription = self.create_subscription(
            Joy,
            'joy',
            self.joy_calback,
            10)
        self.subscription  # prevent unused variable warning


        self.app_subscription = self.create_subscription(
            Int16,
            'angle_cam',
            self.app_callback,
            10)
        self.app_subscription  # prevent unused variable warning

        self.cli = self.create_client(GetPosition, 'get_position')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        
        self.req1 = GetPosition.Request()
        self.req1.id = 1
        self.req2 = GetPosition.Request()
        self.req2.id = 2

        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.posRecieved)

        self.position = {}
        self.sendCMD(id=1,cmd=512)
        self.sendCMD(id=2,cmd=512)
        self.position[1] = 512
        self.position[2] = 512



    def sendCMD(self,id,cmd= 512):
        msg = SetPosition()
        msg.id = id
        msg.position = cmd
        self.publisher_.publish(msg)
    
    def app_callback(self,msg):
        angle = msg.data
        if angle < 22 :
            angle = 22 
        if angle > 338 :
            angle = 338
        a = 1023/316
        b = -a*22
	
        angle = int(a*angle+b)
	
        self.sendCMD(id=1,cmd=angle)

    def joy_calback(self, msg):

        left_right = msg.axes[4]

        
        up_down = msg.axes[5]
        speed = 5
        if left_right == 1.0 :
            position = min(self.position[1] + speed,1023-5)
            self.sendCMD(id=1,cmd=position)
            self.position[1]  =  position

        if left_right == -1.0 :
            position = max(self.position[1] - speed,0+5)
            self.sendCMD(id=1,cmd=position)
            self.position[1]  = position
        
        if up_down == 1.0 :
            position = max(self.position[2] - speed,145+5)

            self.sendCMD(id=2,cmd=position)
            self.position[2]  = position

        if up_down == -1.0 :
            position = min(self.position[2] + speed,860-5)
            self.sendCMD(id=2,cmd=position)
            self.position[2]  =  position
        
        
        try:
            self.get_logger().info(str(self.position[2]))
        except :
            pass

            


    def posRecieved(self):
        self.future1 = self.cli.call_async(self.req1)
        self.future2 = self.cli.call_async(self.req2)
        self.future1.add_done_callback(partial(self.readPos,1))
        self.future2.add_done_callback(partial(self.readPos,2))
    def readPos(self,ids,future) :
        if future.result().position <= 1023 :
            pass
            

    





def main(args=None):
    rclpy.init(args=args)

    control = dynamixelControl()

    rclpy.spin(control)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    control.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
