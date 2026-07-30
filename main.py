import cv2
from Sprite import SpriteClass
import Globals as gb
import Accessories as ac
from Gestures import GesturesAll
import pydirectinput


if __name__ == "__main__":
    url = 0
    pydirectinput.PAUSE = 0
    pydirectinput.FAILSAFE = False
    if gb.doVideoStream:
        url = "http://192.168.18.10:8080/video"
    sampleSprite = SpriteClass("Assets/Images/sample.png","Index_Up")
    sampleSprite.setPosition(0, 0)
    sampleSprite.scale(1.5, 1.5)
    sampleSprite.setOpacity(1)

    cap = cv2.VideoCapture(url)
    if not cap.isOpened():
        print("Webcam error!!")
        exit()
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, gb.SCREEN_WIDTH )
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,gb.SCREEN_HEIGHT)

    fps = cap.get(cv2.CAP_PROP_FPS)
    out = cv2.VideoWriter("output.mp4",cv2.VideoWriter_fourcc(*'mp4v'),fps,(gb.SCREEN_WIDTH, gb.SCREEN_HEIGHT))
    #setup
    GestureObj = GesturesAll()
    while True:
        gb.time_secs = ac.getTimeSeconds()        
        ret, frame = cap.read()
        if not ret:
            continue
        #send frame

        GestureObj.getImage(frame)
        left_ges,right_ges = GestureObj.identifyGesture(frame)

        if gb.pressKeys:
            #causes youtube to freak out
            if left_ges == "Pointing_Up" or right_ges == "Pointing_Up":
                pydirectinput.keyDown('space')
            else:
                pydirectinput.keyUp('space')


            if left_ges == "ILoveYou":
                pydirectinput.keyDown('ctrl')
            else:
                pydirectinput.keyUp('ctrl')

            if right_ges == "ILoveYou":
                pydirectinput.mouseDown(button='left')
            else:
                pydirectinput.mouseUp(button='left')                

            if left_ges == "Closed_Fist" or right_ges == "Closed_Fist":
                pydirectinput.keyDown('f')
            else:
                pydirectinput.keyUp('f')

            if right_ges == "Victory":
                pydirectinput.keyDown('d')
            else:
                pydirectinput.keyUp('d')

            if left_ges == "Victory":
                pydirectinput.keyDown('a')
            else:
                pydirectinput.keyUp('a')            

            if left_ges == "Open_Palm" or right_ges == "Open_Palm":
                pydirectinput.keyDown('w')
            else:
                pydirectinput.keyUp('w')            

            if left_ges == "Thumb_Up" or right_ges == "Thumb_Up":
                pydirectinput.keyDown('s')
            else:
                pydirectinput.keyUp('s')


        if gb.RenderVideo:

            if not sampleSprite.MoveL(left_ges):
                sampleSprite.MoveR(right_ges)

            frame = sampleSprite.draw(frame)
            frame = ac.getFlippedFrame(frame)
            cv2.imshow("Webcam", frame)

        if cv2.waitKey(gb.waitKeyDelayMs) == 27:
            break


        if gb.Record:
            out.write(frame)

cap.release()
cv2.destroyAllWindows()