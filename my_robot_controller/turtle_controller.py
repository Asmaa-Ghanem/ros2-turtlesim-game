#!/usr/bin/env python3 
from typing import List
import rclpy
from rclpy.node import Node 
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist as twist

class TurtleControllerNode(Node):
    def __init__(self):
        super().__init__("turtle_controller")
        self.cmd_vel_publisher_ = self.create_publisher(
            twist,"/turtle1/cmd_vel",10)
        self.pose_subscriber_ = self.create_subscription(
            Pose, "/turtle1/pose",self.pose_callback,10
        )
        self.get_logger().info("Turtle Controller started!")

    def pose_callback(self, pose: Pose):
        cmd = twist()
        cmd.linear.x=5.0
        cmd.angular.z=0.0
        self.cmd_vel_publisher_.publish(cmd)


def main(args = None):
    rclpy.init(args=args)
    node = TurtleControllerNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()