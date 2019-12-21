# returns true if QR code is detected
# o.w. false
from pyzbar.pyzbar import decode
import cv2
import numpy as np
import queue
from HW4.param import *


cap = cv2.VideoCapture(2)

def qrcodeReader():
    data = ""
    cap = cv2.VideoCapture(2)
    for i in range(20):
        ret, frame = cap.read()
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        qrcodes = decode(image)
        for decodedObject in qrcodes:
            points = decodedObject.polygon
            pts = np.array(points, np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(image, [pts], True, (0, 255, 0), 3)
        data = map(lambda bc: bc.data.decode("utf-8"), qrcodes)
        if len(data) != 0:
            SN = data[0]
            return True
    
    return False

# 2 scans
def scan_rotate(s):
    scan_pos = "MOVP 1.3832 293.5219 267.4064 0 0 -90"
    s.sendall(scan_pos.encode('ascii'))
    
    detected= qrcodeReader()
    # Register "SN"
    if detected:
        return True
    return False

# Exit : back to bar code scanning position
# Detecting barcode for 1 object
def detect(i, s):
    SN = ""
    if scan_rotate(s):
        s.sendall(inter_pos[i].encode('ascii'))
    # put it down at man_pose
    # open gripper, rotate 90 deg, close gripper
    if scan_rotate(s):
        # put it to inter_pos[i]
        return
    # put it down at man_pose
    # release
    # move up and back 
    # rotate 90
    # approach with L shape
    # Grab
    scan_rotate(s)
    