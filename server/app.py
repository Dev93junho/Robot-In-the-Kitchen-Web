"""
This app is contoller for Kitchen Master2
Written by Junho Shin, 09-2021
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

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
server_socket.bind()
server_socket.listen()
client_socket, addr=server_socket.accept()
print('Connected by', addr)

k=0

# infinity loop per 2s
while True:
    msg="test" + str(k)
    client_socket.sendall(msg.encode())
    print('done'+str(k))
    k+=1
    time.sleep(2)

    client_socket.close()
    server_socket.close()

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



@app.route('/') #url routing
def index(): # View function call
    return render_template('index.html') # template, seem to user

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# @app.route()
# def dist():
#     pass

# @app.route()
# def unity_to_flask():
#     pass

# @app.route()
# def bot_to_flask():
#     pass

# @app.route()
# def sidebar():
#     pass


if __name__ == '__main__':
    app.run(port = 5000, debug=True)



