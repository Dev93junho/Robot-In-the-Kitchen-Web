"""
This app is contoller for Kitchen Master2
Written by Junho Shin, 09-2021
"""
#coding: utf-8


from flask import Flask, render_template, request, stream_with_context, Response
import cv2
from threading import Thread
from queue import Queue
from flask_socketio import SocketIO, emit


#initialize the Flask app
app = Flask(__name__) # Flask object instance 
app.secret_key = "secret"
socketio = SocketIO(app)
streamer = Streamer()

user_no = 1

camera = cv2.VideoCapture(0)
'''
for ip camera use - rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp'
for local webcam use cv2.VideoCapture(0)
'''

def gen_frames():  
    while True:
        capture = cv2.VideoCapture(0)
        capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        while cv2.waitKey(33) < 0:
            ret, frame = capture.read()
            cv2.imshow("Test", frame)


@app.route('/') #url routing
def index(): # View function call 
    return render_template('index.html') # template, seem to user

@app.route('/stream')
def stream():
    src = requests.args.get('src', default = 0, type = int)
    
    try:
        return Response(
            stream_with_context( stream_gen( src )),
            mimetype='multipart/x''multipart/x-mixed-replace; boundary=frame')
    except Exception as e:
        print('[wandlab] ', 'stream error : ',str(e))

def stream_gen( src ):
    try:
        streamer.run( src )
        while True:
            frame = streamer.bytescode()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                    
    except GeneratorExit :
        #print( '[wandlab]', 'disconnected stream' )
        streamer.stop()            

if __name__ == '__main__':
    app.run(port = 5000, debug=True)



