'''
Kinematic Simulation Library for Robot 
Determine the value of each joint to place the arm at a desired position and orientation

Created by Junho Shin in Sep.2021
'''

import numpy as np
from numpy import sin, cos, arcsin, tan, pi

class KinematicSim:
    def __init__(self, *args, **kwargs): # initialize to manipulator
        pass

    ## These modules defined movement method
    def prismatic(self):
        pass

    def revolute(self):
        pass


    def forward_kinematics(self): # fk_module will be return target point coordination
        
        target = -1
        return target

    def inverse_kinematics(self): # ik_module will be return joint theta from fk_solution
        
        sol = -1
        return sol
