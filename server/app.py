# """
# 1. This app is contoller for Kitchen Master2
# 2. Change the project name to Robot-in-the-Kitchen

# Written by Junho Shin, since 09-2021
# """
#coding: utf-8

from __future__ import absolute_import, division, print_function, nested_scopes, generators, with_statement, unicode_literals
from flask import Flask, render_template, request, stream_with_context, Response
from flask import stream_with_context
import cv2
import yolo_detection
import numpy as np
# import argparse
import time
# import os

#initialize the Flask app
app = Flask(__name__) # Flask object instance
app.secret_key = "secret"
sub = cv2.createBackgroundSubtractorMOG2()  # create background subtractor

user_no = 1

'''
for ip camera use - rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp'
for local webcam use cv2.Videocamerature(0)
'''
config_path='cfg/tiny.cfg'
weights_path='yolov3.weights'
cv_net = cv2.dnn.readNetFromDarknet(config_path, weights_path)
conf_threshold = 0.2
nms_threshold = 0.4
camera = cv2.VideoCapture(0)


def get_detected_img(cv_net, camera, conf_threshold=conf_threshold, nms_threshold=nms_threshold):
    # while True:
    #     success, frame = camera.read()  # read the camera frame
    #     if not success:
    #         break
    #     else:
    #         ret, buffer = cv2.imencode('.png', frame)
    #         frame = buffer.tobytes()
    #         yield (b'--frame\r\n'
    #                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


    # Read until video is completed
    while(camera.isOpened()):
        success, frame = camera.read()  # import image
        if not success: #if vid finish repeat
            frame = cv2.VideoCapture(0)
            continue
        if success:  # if there is a frame continue with code
            rows = camera.shape[0]
            cols = camera.shape[1]
            draw_img = camera.copy()

            layer_names = cv_net.getLayerNames()
            outlayer_names = [layer_names[i[0] - 1] for i in cv_net.getUnconnectedOutLayers()]

            cv_net.setInput(cv2.dnn.blobFromImage(camera, scalefactor=1/255.0, size=(416, 416), swapRB=True, crop=False))
            start = time.time()
            # Object Detection 수행하여 결과를 cvOut으로 반환
            cv_outs = cv_net.forward(outlayer_names)
            layerOutputs = cv_net.forward(outlayer_names)
            # bounding box의 테두리와 caption 글자색 지정
            green_color=(0, 255, 0)
            red_color=(0, 0, 255)

            class_ids = []
            confidences = []
            boxes = []

            # 3개의 개별 output layer별로 Detect된 Object들에 대해서 Detection 정보 추출 및 시각화 
            for ix, output in enumerate(cv_outs):
                # Detected된 Object별 iteration
                for jx, detection in enumerate(output):
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]
                    # confidence가 지정된 conf_threshold보다 작은 값은 제외
                    if confidence > conf_threshold:

                        center_x = int(detection[0] * cols)
                        center_y = int(detection[1] * rows)
                        width = int(detection[2] * cols)
                        height = int(detection[3] * rows)
                        left = int(center_x - width / 2)
                        top = int(center_y - height / 2)
                        # 3개의 개별 output layer별로 Detect된 Object들에 대한 class id, confidence, 좌표정보를 모두 수집
                        class_ids.append(class_id)
                        confidences.append(float(confidence))
                        boxes.append([left, top, width, height])
            # NMS로 최종 filtering된 idxs를 이용하여 boxes, classes, confidences에서 해당하는 Object정보를 추출하고 시각화.
            idxs = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)
            if len(idxs) > 0:
                for i in idxs.flatten():
                    box = boxes[i]
                    left = box[0]
                    top = box[1]
                    width = box[2]
                    height = box[3]
                    # # labels_to_names 딕셔너리로 class_id값을 클래스명으로 변경. opencv에서는 class_id + 1로 매핑해야함.
                    # caption = "{}: {:.4f}".format(labels_to_names_seq[class_ids[i]], confidences[i])
                    #cv2.rectangle()은 인자로 들어온 draw_img에 사각형을 그림. 위치 인자는 반드시 정수형.
                    cv2.rectangle(draw_img, (int(left), int(top)), (int(left+width), int(top+height)), color=green_color, thickness=2)
                    cv2.putText(draw_img, (int(left), int(top - 5)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, red_color, 1)
        # cv2.imshow("countours", image)
        frame = cv2.imencode('.jpg', draw_img)[1].tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        #time.sleep(0.1)
        key = cv2.waitKey(20)
        if key == 27:
            break



#Define main template. If you enter the controller app, you will be watched this page first
@app.route('/') #url routing
def index(): # View function call
    return render_template('index.html') # template, seem to user

#Receive webcam streaming data. export to index page
@app.route('/video_feed')
def video_feed():
    return Response(get_detected_img(), mimetype='multipart/x-mixed-replace; boundary=frame')

#Coordinate Whole Environment
@app.route('/mapping', methods=['GET', 'POST'])
def mapping():
    '''
        measure the object's 3D coordination using Unity sim and YOLO data
        1. Print 3D point cloud environment using mapping function
        2. Compute coordination among YOLO cameratured objects
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

