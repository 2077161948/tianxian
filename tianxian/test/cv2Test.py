import cv2

capture = cv2.VideoCapture(0)

while True:
    ret, frame = capture.read()
    frame2 = cv2.flip(frame,1)
    cv2.imshow("camera",frame2)
    key = cv2.waitKey(1)
    if key!= -1:
        break

capture.release()
