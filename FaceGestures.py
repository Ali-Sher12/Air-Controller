import sys
import numpy as np
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import Globals as gb
import Accessories as ac
import FaceMeshCustom as fc

"""
0 _neutral

1  browDownLeft

2  browDownRight

3  browInnerUp

4  browOuterUpLeft

5  browOuterUpRight

6  cheekPuff
7  cheekSquintLeft
8  cheekSquintRight
  
9  eyeBlinkLeft

10 eyeBlinkRight

11 eyeLookDownLeft

12 eyeLookDownRight

13 eyeLookInLeft

14 eyeLookInRight

15 eyeLookOutLeft

16 eyeLookOutRight

17 eyeLookUpLeft

18 eyeLookUpRight

19 eyeSquintLeft

20 eyeSquintRight

21 eyeWideLeft

22 eyeWideRight
 
23  jawForward
24  jawLeft
25  jawOpen
26  jawRight
 
27  mouthClose
28  mouthDimpleLeft
29  mouthDimpleRight
30  mouthFrownLeft
31  mouthFrownRight
32  mouthFunnel
33  mouthLeft
34  mouthLowerDownLeft
35  mouthLowerDownRight
36  mouthPressLeft
37  mouthPressRight
38  mouthPucker
39  mouthRight
40  mouthRollLower
41  mouthRollUpper
42  mouthShrugLower
43  mouthShrugUpper
44  mouthSmileLeft
45  mouthSmileRight
46  mouthStretchLeft
47  mouthStretchRight
48  mouthUpperUpLeft
49  mouthUpperUpRight
  
50  noseSneerLeft
51  noseSneerRight
"""

class FaceGestures:
    def __init__(self):
        self.base_options = python.BaseOptions(model_asset_path=r'Models/face_landmarker.task')
        self.options = vision.FaceLandmarkerOptions(
            base_options=self.base_options,
            output_face_blendshapes=True,
            output_facial_transformation_matrixes=True,
            num_faces=1,
            running_mode=vision.RunningMode.VIDEO # See into the livestream stuff. Why the FUCK is it different from video?
        )
        self.face_landmarker = vision.FaceLandmarker.create_from_options(self.options) 
        self.connections = fc.FACEMESH_CONTOURS
        self.mp_image = None
        self.face_landmarks = None
        self.face_points = None

        self.L_eyebrows = "None"
        self.L_eyes = "None"
        self.R_eyebrows = "None"
        self.R_eyes = "None"
        self.jaw = "None"
        self.mouth = "None"

        self.yaw = 0
        self.pitch = 0
        self.roll = 0

    def getImage(self,done_frame):
        # get the image from hand gestures 
        self.mp_image = done_frame

    def drawSkeleton(self, frame):
        ac.drawConnections(self.face_points, frame, self.connections, "face")
        for point in self.face_points:
            cv2.circle(frame, ac.normalize2D(point.x, point.y), 1, (0, 105, 0), -1)

    def calc_yaw_pitch_roll(self):
        matrix = self.face_landmarks.facial_transformation_matrixes[0]
        matrix = np.array(matrix)
        r = matrix[:3, :3]
        self.pitch = np.degrees(np.arcsin(-r[2, 0]))
        self.yaw = np.degrees(np.arctan2(r[1, 0], r[0, 0]))
        self.roll = np.degrees(np.arctan2(r[2, 1], r[2, 2]))

    def getRegionGestures(self):
        results = []
        for region_name, indices in fc.REGION_INDICES.items():
            best_name = "None"
            best_score = 0.0

            for i in indices:
                shape = self.face_landmarks.face_blendshapes[0][i]
                if shape.score > best_score:
                    best_score = shape.score
                    best_name = shape.category_name
            if best_score < gb.facialThresh:
                results.append(("None", 0))
            else:
                results.append((best_name, best_score))
        return results

    def identifyGesture(self,frame):
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=gb.frame)
        self.face_landmarks = self.face_landmarker.detect_for_video(mp_image, gb.time_secs)
        if len(self.face_landmarks.face_landmarks) == 1:
            self.face_points = self.face_landmarks.face_landmarks[0]
            self.drawSkeleton(frame)
            self.L_eyebrows,self.L_eyes,self.R_eyebrows,self.R_eyes,self.jaw,self.mouth = self.getRegionGestures()
            self.calc_yaw_pitch_roll()
            # get yaw pitch and roll here
            print("Yaw   : ",self.yaw)
            print("Pitch : ",self.pitch)
            print("Roll  : ",self.roll)
            print(" ")
            print(" ")
            print(" ")
            print(" ")
            print(" ")
            print(" ")

            return self.L_eyebrows,self.L_eyes,self.R_eyebrows,self.R_eyes,self.jaw,self.mouth        
        return "None","None","None","None","None","None"
    