"""
1. This app is contoller for Kitchen Master2
2. Change the project name to Robot-in-the-Kitchen

Written by Junho Shin, since 09-2021
"""
#coding: utf-8


from flask import Flask, render_template, request, stream_with_context, Response
from flask import stream_with_context
import cv2
from queue import Queue
import socket, threading
import time
from datetime import datetime
# from flask_socketio import SocketIO, emit


#initialize the Flask app
app = Flask(__name__) # Flask object instance 
app.secret_key = "secret"
# socketio = SocketIO(app)

# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
# server_socket.bind()
# server_socket.listen()
# client_socket, addr=server_socket.accept()
# print('Connected by', addr)

# k=0

# # infinity loop per 2s
# while True:
#     msg="test" + str(k)
#     client_socket.sendall(msg.encode())
#     print('done'+str(k))
#     k+=1
#     time.sleep(2)

#     client_socket.close()
#     server_socket.close()

user_no = 1

camera = cv2.VideoCapture(0)
'''
for ip camera use - rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp'
for local webcam use cv2.VideoCapture(0)
'''

def gen_frames():
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.png', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


#Define main template. If you enter the controller app, you will be watched this page first
@app.route('/') #url routing
def index(): # View function call
    return render_template('index.html') # template, seem to user


#Receive Unity streaming data. export to index page and yolo 
@app.route('/video_feed') 
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/yolo')
def yolo():
    '''
        It can be real-time object capture 
    '''
    import cv2
    import matplotlib.pyplot as plt
    import numpy as np
    import time
    import os
    
    # Load Unity Realsense
    sim_cam=cv2.imread(video_feed)
    
    weights_path = './models/yolov3-tiny.weights'
    config_path = './models/yolov3-tiny.cfg'
    
    load_yolo_tiny=cv2.dnn.readNet(config_path, weights_path)
    
    conf_threshold = 1
    nms_threshold = 2
    
    # detected_obj 
    detected_obj = get_detected_obj(load_yolo_tiny, sim_cam, conf_threshold=conf_threshold, nms_threshold=nms_threshold, is_print=True)

    img_rgb = cv2.cvtColor(detected_obj, cv2.COLOR_BGR2RGB)

    # plt.figure(figsize=(12, 12))
    # plt.imshow(img_rgb)
    return Response(img_rgb)

#Coordinate Whole Environment 
@app.route('/mapping')
def mapping():
    '''
        measure the object's 3D coordination using Unity sim and YOLO data
        1. Print 3D point cloud environment using mapping function
        2. Compute coordination among YOLO captured objects 
        3. send object coordination to /send_to_jetson  
    '''
    pass

# send to jetson
@app.route('/send_to_jetson')
def send_to_jetson():
    '''
        object coordinate send function
        1. receive data from /mapping
        2. send 3d coordinaion data to jetson nano in this route
    '''
    pass
    
if __name__ == '__main__':
    app.run(port = 5000, debug=True)



