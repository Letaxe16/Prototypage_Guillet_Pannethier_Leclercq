import cv2
from flask import Flask, render_template, Response
import rclpy
from cv_bridge import CvBridge
from rclpy.executors import MultiThreadedExecutor
from multiprocessing import Process, Queue
import numpy as np


from sensor_msgs.msg import Image

app = Flask(__name__)
vs = None  # VideoCapture object
bridge = CvBridge()
image_queue = Queue()

def gen():
    """Video streaming generator function."""
    global vs
    while True:
        frame = image_queue.get()
        if frame is not None:
            # frame_np = np.frombuffer(frame_bytes, dtype=np.uint8)
            # print(frame_np)
            # frame = cv2.imdecode(frame_np, cv2.IMREAD_COLOR)
            scale_percent = 60
            width = int(frame.shape[1] * scale_percent / 100)
            height = int(frame.shape[0] * scale_percent / 100)
            dim = (width, height)

            # resize image
            frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
            ret, jpeg = cv2.imencode('.jpg', frame)
            frame = jpeg.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

def image_callback(msg):
    global vs
    
    vs = bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
    if image_queue.qsize() >= 10:
        image_queue.get()
    image_queue.put(vs)

def flask_process(q):
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)

def main():
    rclpy.init()
    node = rclpy.create_node('image_streamer')
    image_topic = 'image_raw'  # Replace with your actual image topic
    sub = node.create_subscription(Image, image_topic, image_callback, 10)

    executor = MultiThreadedExecutor()
    executor.add_node(node)

    try:
        q = Queue()
        process = Process(target=flask_process, args=(q,))
        process.start()
        executor.spin()
    finally:
        executor.shutdown()
        node.destroy_node()
        process.terminate()

    rclpy.shutdown()

if __name__ == '__main__':
    main()