'''
Kinematic Simulation Library for Robot 
Determine the value of each joint to place the arm at a desired position and orientation

Created by Junho Shin in Sep.2021
'''

import numpy as np
from numpy import sin, cos, arcsin, tan, pi
import sys

class KinematicSim:
    def __init__(self, *args, **kwargs): # initialize to manipulator
        pass

    '''
    Below two modules defined movement method
    prismatic defined linear motion 
    revolute defined rotation motion
    '''
    def prismatic(self):
        pass

    def revolute(self):
        pass


    '''
    Below two modules about 
    '''
    def DH_table(self):
        pass

    def transform_Mat(self):
        pass


    '''
    Below two modules defined for solving kinematics solution from Kinematics Theory
    forward_kinematics is solved for End-Effector's target coordination
    inverse_kinematics module is solved for joint theata from End-Effector's target
    '''
    def forward_kinematics(self): # fk_module will be return target point coordination
        
        target = -1
        return target

    def inverse_kinematics(self): # ik_module will be return joint theta from fk_solution
        try:
            sol = -1
            return sol

        except:
            print("should not solved invers kinematics solution")
            sys.exit
            

