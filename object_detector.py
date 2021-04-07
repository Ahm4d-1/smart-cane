import cv2
classNames= []
classFile = 'coco.names'
with open(classFile,'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

color = (0, 0, 0)
white = (210, 210, 210)
upper = 100
lower = 30

configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
weightsPath = 'frozen_inference_graph.pb'

net = cv2.dnn_DetectionModel(weightsPath,configPath)
net.setInputSize(320,320)
net.setInputScale(1.0/ 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

def getObjects(img,thres,nms,distance,draw=True,objects=[]):
    classIds, confs, bbox = net.detect(img,confThreshold=thres,nmsThreshold=nms)
    #print(classIds,bbox)
    if len(objects) == 0: objects = classNames
    objectInfo =[]
    if len(classIds) != 0:
        for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
            className = classNames[classId - 1]
            if className in objects:
                objectInfo.append([box, className, distance])
                if float(distance) < lower:
                    color = (0,0,255)
                elif (float(distance) < upper) and (float(distance) >= lower):
                    color = (0,255,255)
                else:
                    color = (0,255,0)
                if (draw):
                    cv2.rectangle(img,box,color,thickness=2)
                    cv2.putText(img,className.upper(),(box[0]+10,box[1]+30),
                    cv2.FONT_HERSHEY_COMPLEX,1,white,2)
                    cv2.putText(img,(distance[:5] + ' cm').upper(),(box[0]+10,box[1]+130),
                cv2.FONT_HERSHEY_COMPLEX,1,white,2)
                    cv2.putText(img,(str(round(confidence*100,2)) + ' %'),(box[0]+10,box[1]+80),
                    cv2.FONT_HERSHEY_COMPLEX,1,white,2)
    return img,objectInfo

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    # cap.set(10,70)

    while True:
        success, img = cap.read()
        result,objectInfo = getObjects(img,0.45,0.2,distance,objects=[])
        #print(objectInfo)
        cv2.imshow("Output", img)
        cv2.waitKey(1)

