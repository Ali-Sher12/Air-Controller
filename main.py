import cv2
import copy
import time
from Sprite import SpriteClass
import Globals as gb
import Accessories as ac
from Gestures import GesturesAll
import pydirectinput
import sys
from PyQt5.QtWidgets import QApplication
import FrontEnd as QTFront
import FaceGestures as FaceGes

if __name__ == "__main__":
    app = None
    window = None
    out = None
    if gb.enableFrontEnd:
        app = QApplication(sys.argv)
        window = QTFront.ColorTextWindow()


    url = 0
    pydirectinput.PAUSE = 0
    pydirectinput.FAILSAFE = False
    if gb.doVideoStream:
        url = "http://192.168.18.10:8080/video"

    #soulSprite = SpriteClass("Assets/Images/sample.png",["Pointing_Up","Index_Up","Left_Lean","Right_Lean"])
    #soulSprite.setPosition(0, 0)
    #soulSprite.scale(1, 1)
    #soulSprite.setOpacity(1)
    #tennaSprite = SpriteClass("Assets/Images/tenna.png",["Pointing_Up","Index_Up","Left_Lean","Right_Lean"])
    #tennaSprite.setPosition(0, 90)
    #tennaSprite.scale(1, 1)
    #tennaSprite.setOpacity(1)    

    cap = cv2.VideoCapture(url)
    if not cap.isOpened():
        print("Webcam error!!")
        exit()
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, gb.SCREEN_WIDTH )
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,gb.SCREEN_HEIGHT)

    cap.set(cv2.CAP_PROP_FPS, 60)
    fps = cap.get(cv2.CAP_PROP_FPS)
    if gb.Record:
        out = cv2.VideoWriter("output.mp4",cv2.VideoWriter_fourcc(*'mp4v'),fps,(gb.SCREEN_WIDTH, gb.SCREEN_HEIGHT))
    #setup

    bg_frame = cv2.imread("Assets/Images/haha.png")
    bg_frame = cv2.resize(bg_frame, (gb.SCREEN_WIDTH,gb.SCREEN_HEIGHT))

    GestureObj = GesturesAll()
    FaceGestureObj = FaceGes.FaceGestures()    
    prev_time = time.time()
    while True:
        gb.time_secs = ac.getTimeSeconds()        
        ret, frame = cap.read()
        gb.frame = copy.deepcopy(frame)
        frame = copy.deepcopy(gb.frame)

        if not ret:
            continue
        #send frame

        im = GestureObj.getImage()
        left_ges,right_ges = GestureObj.identifyGesture(frame)
        FaceGestureObj.getImage(im)
        FaceGestureObj.identifyGesture(frame)
        if left_ges == "ILoveYou" or right_ges == "ILoveYou":
            gb.enableMouse = not gb.enableMouse

        if gb.enableMouse:
            FaceGestureObj.move_mouse_mode_3()

#        print(left_ges ," , ",right_ges)
        if gb.pressKeys:
            #causes youtube to freak out
            if left_ges == "Left_Lean" or right_ges == "Left_Lean":
                pydirectinput.keyDown('left')
            else:
                pydirectinput.keyUp('left')

            if left_ges == "Right_Lean" or right_ges == "Right_Lean":
                pydirectinput.keyDown('right')
            else:
                pydirectinput.keyUp('right')

            if left_ges == "Open_Palm" or right_ges == "Open_Palm":
                pydirectinput.keyDown('up')
            else:
                pydirectinput.keyUp('up')

            if left_ges == "Closed_Fist" or right_ges == "Closed_Fist":
                pydirectinput.keyDown('f')
            else:
                pydirectinput.keyUp('f')


        if gb.RenderVideo:
#            if not soulSprite.MoveL(left_ges):
#                soulSprite.MoveR(right_ges)
#            if not tennaSprite.MoveR(right_ges):
#                tennaSprite.MoveL(left_ges)
#
#
#            frame = tennaSprite.draw(frame)            
#            frame = soulSprite.draw(frame)
            frame = ac.getFlippedFrame(frame)
            cv2.imshow("Webcam", frame)

        if cv2.waitKey(gb.waitKeyDelayMs) == 27:
            break
        if gb.Record:
            out.write(frame)
        if gb.enableFrontEnd:
            window.Update(left_ges,right_ges)
            window.show()
            #important
            gb.rightMissing = True
            gb.leftMissing = True        

        current_time = time.time()
        delta_time = current_time - prev_time        
        if delta_time > 0:
            fps = 1 / delta_time
            print(f"FPS: {fps:.2f}", end="\r")            
        prev_time = current_time

if gb.enableFrontEnd:
    sys.exit(app.exec())
cap.release()
cv2.destroyAllWindows()