from pyzbar.pyzbar import decode
import cv2
import numpy as np

def qrcodeReader(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    qrcodes = decode(image)
    for decodedObject in qrcodes:
        points = decodedObject.polygon
        pts = np.array(points, np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(image, [pts], True, (0, 255, 0), 3)
    data = map(lambda bc: bc.data.decode("utf-8"), qrcodes)
    return list(data)

cap = cv2.VideoCapture(2)
while True:
    ret, frame = cap.read()

    # gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # gray_img = cv2.GaussianBlur(gray_img, (5, 5), 0)
    # cv2.threshold(gray_img, 170, 255, cv2.THRESH_BINARY,gray_img)
    qrcode = qrcodeReader(frame)
    print(qrcode)
    cv2.imshow('qrcode reader', frame)
    code = cv2.waitKey(1)
    if code == ord('q'):
        break
