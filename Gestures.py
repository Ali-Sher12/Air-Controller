import cv2
import math
import time
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from Sprite import SpriteClass
import Globals as gb
import Accessories as ac

#left hand is detected first if both

class GesturesAll:
    def __init__(self):
        self.base_options_gestures = python.BaseOptions(model_asset_path=r'Models/gesture_recognizer.task')
        self.options_gestures = vision.GestureRecognizerOptions(base_options=self.base_options_gestures,running_mode=vision.RunningMode.VIDEO,num_hands=2)
        self.detector_gestures = vision.GestureRecognizer.create_from_options(self.options_gestures)
        self.connections = vision.HandLandmarksConnections.HAND_CONNECTIONS
        self.detected_hand_points = None
        self.detected_hand_points_l = None
        self.detected_hand_points_r = None                
        self.detected_gestures = None
        self.handMissIndex = 0
        self.mp_image = None

    def getImage(self,frame):
        self.mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)

    def _getHandSingle(self):
        if self.detected_gestures.hand_landmarks[0][4].x >= self.detected_gestures.hand_landmarks[0][20].x:
            return "right"        
        return "left"

    def drawSkeleton(self,frame,hand_points):
        for point in hand_points:
            cv2.circle(frame,ac.normalize(point.x,point.y),4,(0, 255, 0),-1)
        ac.drawConnections(hand_points,frame,self.connections)

    def identifyCustomGesture(self,detected_hand_points):
        pass

    def identifyGesture(self,frame):
        self.detected_gestures = self.detector_gestures.recognize_for_video(self.mp_image,gb.time_secs)
        left_name = right_name = "None"
        gb.left_landmarks = gb.right_landmarks = None
        if len(self.detected_gestures.gestures) == 2:
            left = self.detected_gestures.gestures[0]
            right = self.detected_gestures.gestures[1]
            gb.left_landmarks = self.detected_hand_points_l = self.detected_gestures.hand_landmarks[0]
            gb.right_landmarks = self.detected_hand_points_r = self.detected_gestures.hand_landmarks[1]
            if gb.DrawSkeleton:
                self.drawSkeleton(frame,self.detected_hand_points_l)
                self.drawSkeleton(frame,self.detected_hand_points_r)
            left_name = left[0].category_name
            right_name = right[0].category_name
            if gb.printDebug:
                if left_name == "None":
                    print("Custom one starts here left")
                else:
                    print("left : ",left_name)
                if right_name == "None":
                    print("Custom one starts here right")
                else:
                    print("right : ",right_name)

            return left_name,right_name
        elif len(self.detected_gestures.gestures) == 1:
            top_gesture = self.detected_gestures.gestures[0][0]
            self.detected_hand_points = self.detected_gestures.hand_landmarks[0]
            if gb.DrawSkeleton:
                self.drawSkeleton(frame,self.detected_hand_points)
            hand_iden = self._getHandSingle()
            if gb.printDebug:
                if top_gesture.category_name == "None":
                    print("Custom one starts here")
                else:
                    print(hand_iden," , single : ",top_gesture.category_name)
            if hand_iden == "left":
                gb.left_landmarks = self.detected_hand_points
                return top_gesture.category_name,"None"
            elif hand_iden == "right":
                gb.right_landmarks = self.detected_hand_points
                return "None",top_gesture.category_name            
            else:
                return "None","None"
        return "None","None"

