#!/usr/bin/env python3
from typing import List
import rclpy
from rclpy.context import Context
from rclpy.node import Node
from rclpy.parameter import Parameter
from geometry_msgs.msg import Twist as twist

class DrawCircleNode(Node):
    def __init__(self):
        super().__init__("draw_circle")
        self.cmd_vel_pub_ = self.create_publisher(twist,"/turtle1/cmd_vel",10) #creating publisher 
        self.timer = self.create_timer(0.5,self.send_velocity_command)
        self.get_logger().info("Draw circle node started")
    
    def send_velocity_command(self):
        msg = twist()
        msg.linear.x = 2.0
        msg.angular.z = 1.0
        self.cmd_vel_pub_.publish(msg)


def main(args =None):
    rclpy.init(args = args)
    node = DrawCircleNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()