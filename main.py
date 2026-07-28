import cv2
import math
import time
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from Sprite import SpriteClass

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
waitKeyDelayMs = 1
MAXGHOSTFRAMES = 10
LastHand = None
enableGHOSTFRAMEFIX = False
enableHandLandmarkDetection = True
enableGestureRecognition = True

def normalize(x,y):
    return int(x*SCREEN_WIDTH),int(y*SCREEN_HEIGHT)

def getTimeSeconds():
    return int(time.time()*1000)

def getFlippedFrame(frame):
    return cv2.flip(frame, 1)

def drawConnections(hand,frame):
    for connection in connections:
        start_point = hand[connection.start]
        end_point = hand[connection.end]
        cv2.line(frame,normalize(start_point.x, start_point.y),normalize(end_point.x, end_point.y),(255, 0, 0),2)


if __name__ == "__main__":

    sampleSprite = SpriteClass("Assets/Images/sample.png")
    sampleSprite.setPosition(0, 0)
    sampleSprite.scale(0.5, 0.5)
    sampleSprite.setOpacity(1)
 
    cap = cv2.VideoCapture(0)    
    if not cap.isOpened():
        print("Webcam error!!")
        exit()
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, SCREEN_WIDTH )
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,SCREEN_HEIGHT)

    if enableHandLandmarkDetection:
        base_options_landmarks = python.BaseOptions(model_asset_path=r'Models/hand_landmarker.task')
        options_landmarks = vision.HandLandmarkerOptions(base_options=base_options_landmarks,running_mode = vision.RunningMode.VIDEO, num_hands=2)
        detector_landmarks = vision.HandLandmarker.create_from_options(options_landmarks)
        connections = vision.HandLandmarksConnections.HAND_CONNECTIONS

    if enableGestureRecognition:
        base_options_gestures = python.BaseOptions(model_asset_path=r'Models/gesture_recognizer.task')
        options_gestures = vision.GestureRecognizerOptions(base_options=base_options_gestures,running_mode=vision.RunningMode.VIDEO,num_hands=2)
        detector_gestures = vision.GestureRecognizer.create_from_options(options_gestures)

    handMissIndex = 0
    while True:
        time_secs = getTimeSeconds()
        ret, frame = cap.read()
        if not ret:
            continue
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        if enableHandLandmarkDetection:
            detected_hand_points = detector_landmarks.detect_for_video(mp_image,time_secs)
        if enableGestureRecognition:
            detected_gestures = detector_gestures.recognize_for_video(mp_image, time_secs)

        if enableHandLandmarkDetection:
            if enableGHOSTFRAMEFIX:
                if detected_hand_points.hand_landmarks:
                    LastHand = detected_hand_points.hand_landmarks
                    handMissIndex = 0
                else:
                    handMissIndex += 1
                if handMissIndex >= MAXGHOSTFRAMES:
                    LastHand = None
            else:
                LastHand = detected_hand_points.hand_landmarks
            if LastHand:
                for hand in LastHand:
                    for point in hand:
                        cv2.circle(frame,normalize(point.x,point.y),4,(0, 255, 0),-1)
                    drawConnections(hand,frame)


        if enableGestureRecognition:
            for hand in detected_gestures.gestures:
                top_gesture = hand[0]
                gesture_name = top_gesture.category_name
                confidence = top_gesture.score
                print(gesture_name, confidence)
        

        frame = sampleSprite.draw(frame)
        frame = getFlippedFrame(frame)
        cv2.imshow("Webcam", frame)

        if cv2.waitKey(waitKeyDelayMs) == 27:
            break

cap.release()
cv2.destroyAllWindows()