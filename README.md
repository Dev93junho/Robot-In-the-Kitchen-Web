# Robot in the Kitchen Web controller

## Description
- This project is Upgrade version of [KitchenMaster](https://github.com/MinTpie30/KitchenMaster)
- In Progress since Sep.2021
- Transer to PUBLIC Repo according to the "[AI Robotics Hackerthon in MAGOK](https://m-hackathon.tistory.com/)" Policy, since Oct.2021

- --------------------- Specs --------------------------
- Receive Unity simulator depth camera data
- can Visualize Space Mapping
- Compute Object Detection & Trajectory Planning
- ------------------------------------------------------
## Configuration___flask Remote Controller 
### 01. Front-End
- FLASK static html 
### 02. Back-End
- Camera & Mapping Module
> Generate 3D map data merging image data and distance data
> read the image from Fixed CAM system on real-time
> command communicate among modules by socketIO

- Control System
> - Load Map data from Mapping Module
> - Operate world coordinate data 
### 03. Utils
#### KinematicSim
Verification of the kinematical principle of the robotics model
## Contributors : Team SHINRobotics
- Junho Shin : S/W Design, PM
- EngHo Shin : H/W Design
