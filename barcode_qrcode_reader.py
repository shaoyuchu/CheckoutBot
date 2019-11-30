from pyzbar.pyzbar import decode
import cv2
import numpy as np

def qrcodeReader(image):
    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    qrcodes = decode(gray_img)
    for decodedObject in qrcodes:
        points = decodedObject.polygon
        pts = np.array(points, np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(image, [pts], True, (0, 255, 0), 3)
    data = map(lambda bc: bc.data.decode("utf-8"), qrcodes)
    return list(data)

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    qrcode = qrcodeReader(frame)
    print(qrcode)
    cv2.imshow('qrcode reader', frame)
    code = cv2.waitKey(5)
    if code == ord('q'):
        break
