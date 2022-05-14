import cvzone
import cv2
from djitellopy import tello

theta = 0.6
theta_nms = 0.2
cam = cv2.VideoCapture(0)
cam.set(3, 640)
cam.set(4, 480)

classFile = 'coco.names'
with open(classFile, 'rt') as file:
    classNames = file.read().split('\n')

configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
weightsPath = r"frozen_inference_graph.pb"

net = cv2.dnn_DetectionModel(weightsPath, configPath)
net.setInputSize(320, 320)
net.setInputScale(1.0 / 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

while True:
    success, img = cam.read()
    classIds, confs, bbox = net.detect(img, confThreshold=theta, nmsThreshold=theta_nms)

    try:
        for classId, conf, box in zip(classIds.flatten(), confs.flatten(), bbox):
            cvzone.cornerRect(img, box)
            cv2.putText(img, f'{classNames[classId-1].upper()},'
                             f' {round(conf*100, 2)}', (box[0] + 10, box[1] + 30), cv2.FONT_HERSHEY_PLAIN,
                        1, (0, 255, 0), 2)
    except:
        pass

    cv2.imshow("Image", img)
    cv2.waitKey(1)
