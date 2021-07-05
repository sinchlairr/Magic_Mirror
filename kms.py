from flask import Flask, render_template, Response
import cv2
from vcam import vcam,meshGen
import numpy as np
import math
import os

app = Flask(__name__)
vid=cv2.VideoCapture(0)

def generate():
    # while True:
    #     success,frame=camera.read()
    #     if not success:
    #         break
    #     else:
    #         ret,buffer= cv2.imencode('.jpg',frame)
    #         frame=buffer.tobytes()
    #     yield(b'--frame\r\n'
    #                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    while(True):



        ret, frame = vid.read()
        H,W = frame.shape[:2]

        c1 = vcam(H=H,W=W)

    #     # Creating the surface object
        plane = meshGen(H,W)
        plane.Z += 20*np.sin(2*np.pi*((plane.X-plane.W/4.0)/plane.W)) + 20*np.sin(2*np.pi*((plane.Y-plane.H/4.0)/plane.H))
        
        pts3d = plane.getPlane()

        pts2d = c1.project(pts3d)
        map_x,map_y = c1.getMaps(pts2d)

        output = cv2.remap(frame,map_x,map_y,interpolation=cv2.INTER_LINEAR)
        ret,buffer= cv2.imencode('.jpg',output)
        output=buffer.tobytes()

    #     # cv2.imshow("Funny Mirror",output)
        yield(b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + output + b'\r\n')
#     cv2.waitKey(0)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video')
def video():
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__=="__main__":
    
    app.run()