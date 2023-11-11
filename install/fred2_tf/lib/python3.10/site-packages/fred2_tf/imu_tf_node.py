import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
from geometry_msgs.msg import TransformStamped, Vector3, Quaternion
from tf2_ros.transform_broadcaster import TransformBroadcaster

class IMU_TF_NODE(Node):

    def __init__(self):
        super().__init__('imu_tf_node')
        self.tf_broadcaster = TransformBroadcaster(self)
        self.subscription = self.create_subscription(
            Imu,
            '/sensors/orientation/imu',  # Subscribe to the IMU topic
            self.imu_callback,
            10  # QoS profile
        )
        self.subscription  # Prevent unused variable warning

    def imu_callback(self, imu_msg):
        transform = TransformStamped()
        transform.header.stamp = self.get_clock().now().to_msg()
        transform.header.frame_id = 'base_link'
        transform.child_frame_id = 'imu_link'

        imu_pos = Vector3(x=0.011, y=0.053, z=0.024)  # Replace with actual position
        imu_quat = imu_msg.orientation

        transform.transform.translation = imu_pos
        transform.transform.rotation = imu_quat

        self.tf_broadcaster.sendTransform(transform)

def main():
    rclpy.init()
    node = IMU_TF_NODE()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    rclpy.shutdown()

if __name__ == '__main__':
    main()
