#!/usr/bin/env python3
from typing import List
import rclpy
from rclpy.context import Context
from rclpy.node import Node
from rclpy.parameter import Parameter

#class inherits from Node class to have functionalities from it
class MyNode(Node):

    def __init__(self):
        super().__init__("first_node")
        self.counter_ = 0
        self.create_timer(1.0, self.timer_callback)

    def timer_callback(self):
        self.get_logger().info("hello "+ str(self.counter_))
        self.counter_+=1

def main(args = None):
    rclpy.init(args = args)
    #code in between here 

    node = MyNode()
    rclpy.spin(node) #spinning a node is keeping it alive until it's killed and all callbacks are made 
    rclpy.shutdown() #shuts down ros communications


if __name__ == '__main__':
    main()


