# returns true if QR code is detected
# o.w. false
from pyzbar.pyzbar import decode
import cv2
import numpy as np
import queue
from param import *


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
        data = list(data)
        print("i = %d" % i)
        if len(data) != 0:
            SN = data[0]
            print("serial number = {}".format(data[0]))
            return True
    
    return False

# 2 scans
def scan_rotate(s):
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

    # First 2 scans
    if scan_rotate(s):
        input()
        s.sendall(inter_pos[i].encode('ascii'))
        input()
        s.sendall(open_grip.encode('ascii')) # open gripper
        input()
        s.sendall(scan_pos.encode('ascii')) # go to scan pos
        return
    input()
    # If no QR code detected, grip the next 2 sides of the object
    s.sendall(man_pose(0, 0).encode('ascii'))   # go to man_pose
    s.sendall(open_grip.encode('ascii'))        # open gripper
    input()
    s.sendall(man_pose(50, 0).encode('ascii'))  # rise 50mm
    s.sendall(man_pose(50, 90).encode('ascii')) # rotate 90deg
    input()
    s.sendall(man_pose(0, 90).encode('ascii'))  # lower 50mm
    s.sendall(close_grip.encode('ascii'))       # close gripper
    input()
    if scan_rotate(s):
        input()
        s.sendall(inter_pos[i].encode('ascii'))
        input()
        s.sendall(open_grip.encode('ascii')) # open gripper
        input()
        s.sendall(scan_pos.encode('ascii')) # go to scan pos
        return

    # If no QR code detected, do the roll manoeuver
    input()
    s.sendall(man_pose(0, 0).encode('ascii'))   # go to man_pose
    s.sendall(open_grip.encode('ascii'))        # open gripper
    input()
    s.sendall(man_pose(120, 0).encode('ascii')) # rise 1200mm
    s.sendall(temp_pose.encode('ascii'))        # go to temp pose (L shape)
    input()
    s.sendall(woman_pose.encode('ascii'))       # go to woman pose
    s.sendall(open_grip.encode('ascii'))        # close gripper

    scan_rotate(s)
    