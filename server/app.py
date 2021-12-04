# """
# 1. This app is contoller for Kitchen Master2
# 2. Change the project name to Robot-in-the-Kitchen

# Written by Junho Shin, since 09-2021
# """
#coding: utf-8

from __future__ import absolute_import, division, print_function, nested_scopes, generators, with_statement, unicode_literals
from flask import Flask, render_template, request, stream_with_context, Response
from flask import stream_with_context
from flask_socketio import SocketIO
import cv2

#initialize the Flask app
app = Flask(__name__) # Flask object instance
app.config['SECRET_KEY'] = 'SET THE PW' 
app.secret_key = "secret"

socketio = SocketIO(app) # Casulize Web server

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


#open Session
@app.route('/session')
def sessions():
    return render_template('index.html')

def messageReceived(methods=['GET','POST']):
    print("received!")
    
@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)

#Receive webcam streaming data. export to index page
@app.route('/video_feed') 
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/yolo', methods=['GET', 'POST'])
def predict(Response):
    '''
        It can be real-time object capture 
    '''
    # Load Unity Realsense
    sim_cam=cv2.imread(Response)
    
    weights_path =  './models/tiny.weights'
    cfg_path = './models/yolov3-tiny.cfg'
    
    load_yolo_tiny=cv2.dnn.readNet(cfg_path, weights_path)
    
    conf_threshold = 1
    nms_threshold = 2
    
    # detected_obj 
    detected_obj = get_detected_obj(load_yolo_tiny, sim_cam, conf_threshold=conf_threshold, nms_threshold=nms_threshold, is_print=True)

    img_rgb = cv2.cvtColor(detected_obj, cv2.COLOR_BGR2RGB)

    # plt.figure(figsize=(12, 12))
    # plt.imshow(img_rgb)
    return Response(img_rgb)

#Coordinate Whole Environment 
@app.route('/mapping', methods=['GET', 'POST'])
def mapping():
    '''
        measure the object's 3D coordination using Unity sim and YOLO data
        1. Print 3D point cloud environment using mapping function
        2. Compute coordination among YOLO captured objects 
        3. send object coordination to /send_to_jetson  
    '''

    pass

# send to jetson
@app.route('/send_to_jetson', methods=['GET', 'POST'])
def send_to_jetson():
    '''
        object coordinate send function
        1. receive data from /mapping
        2. send 3d coordinaion data to jetson nano in this route
    '''
    pass
    
if __name__ == '__main__':
    app.run(port = 5000, debug=True)

