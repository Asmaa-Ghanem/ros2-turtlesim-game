#!/usr/bin/env python3 
import rclpy
from rclpy.node import Node 
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from turtlesim.srv import Spawn, Kill, TeleportRelative
from functools import partial
import random
import math 
class TurtleCatchSpawn(Node):
    def __init__(self):
        super().__init__("spawn_catch_game")

        self.spX, self.spY, self.spTheta, self.spName = self.new_spawn()

        self.cmd_vel_publisher_ = self.create_publisher(
            Twist, "/turtle1/cmd_vel",10
        )
        self.pose_subscriber_ = self.create_subscription(
            Pose, "/turtle1/pose", self.turtle_attack,10
        )
    
        self.get_logger().info("Catching Spawn game begins")
    
    def turtle_attack(self, pose:Pose):
            cmd = Twist()
            flag = 0
            #calculate hypotenuse to spawn's position
            distance = abs(math.sqrt(((self.spX-pose.x)**2)+((self.spY-pose.y)**2)))
            
            #ensure spawn and turtle aren't at same position
            if distance >0.5:    
                print(self.spX)

                #updating turtle position
                turtle_pos = 2* distance 
                cmd.linear.x = turtle_pos
                angle = math.atan2((self.spY-pose.y),(self.spX-pose.x))
                new_angle = angle - pose.theta
                #adjusting angles in radians according to quadrants
                if new_angle >math.pi:
                     new_angle-=2*math.pi
                elif new_angle<-math.pi:
                     new_angle+=2*math.pi
                #updating according to angle controller factor (worked at 6)
                cmd.angular.z = 6*new_angle
                

            else: 
                flag =1
                self.kill_spawn(self.spName)
                cmd.linear.x = 0.0
                cmd.angular.z=0.0
                self.spX, self.spY, self.spTheta, self.spName = self.new_spawn()
                
                #self.attack_spawn(turtleSpeed,new_angle)

            self.cmd_vel_publisher_.publish(cmd)
                
            

    

            '''
            if pose.x > 9.0 or pose.x <2.0 or pose.y >9.0 or pose.y<2.0:
            cmd.linear.x=1.0
            cmd.angular.z = 0.0
            else:
            cmd.linear.x=5.0
            cmd.angular.z = 0.0
            '''
            
    #generating a spawn at random places 
    def new_spawn(self):
        client = self.create_client(Spawn, "/spawn")
        while not client.wait_for_service(1.0):
            self.get_logger().warn("waiting for service")
        
        self.get_logger().info("spawn on the loose!")
        request = Spawn.Request()

        request.x = random.uniform(2, 9)
        request.y = random.uniform(2, 9)
        request.theta = random.random()
        request.name = "spawn"

        future = client.call_async(request)
        future.add_done_callback(partial(self.callback_spawn))
        return (request.x, request.y, request.theta, str(request.name))
    
    def callback_spawn(self, future):
        try:
            response = future.result()
        except:
            self.get_logger().error("Service call failed: %r" % {e,})

    
   
    def kill_spawn(self,spawn_name):
        client2 = self.create_client(Kill, "/kill")
        while not client2.wait_for_service(1.0):
            self.get_logger().warn("waiting for service2")
        
        self.get_logger().info("killing spawn")
        request2 = Kill.Request()
        request2.name = spawn_name

        future = client2.call_async(request2)
        future.add_done_callback(partial(self.callback_kill))

    def callback_kill(self, future):
        try:
            response2 = future.result()
        except:
            self.get_logger().error("Service call failed: %r" % {e,})
    '''
    def attack_spawn(self,linear_dist, angular_vel):
        client3 = self.create_client(TeleportRelative, "/turtle1/teleport_relative")
        while not client3.wait_for_service(1.0):
            self.get_logger().warn("waiting for service3")
        
        self.get_logger().info("killing spawn")
        request3 = TeleportRelative.Request()
        request3.linear= linear_dist
        request3.angular= angular_vel

        future = client3.call_async(request3)
        future.add_done_callback(partial(self.callback_attack))
    
    def callback_attack(self, future):
        try:
            response3 = future.result()
        except:
            self.get_logger().error("Service call failed: %r" % {e,})
    '''

def main(args = None):
    rclpy.init(args=args)
    node = TurtleCatchSpawn()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()