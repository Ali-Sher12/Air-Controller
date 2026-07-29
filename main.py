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
#    sampleSprite = SpriteClass("Assets/Images/sample.png","Pointing_Up")
#    sampleSprite.setPosition(0, 0)
#    sampleSprite.scale(1.5, 1.5)
#    sampleSprite.setOpacity(1)

    cap = cv2.VideoCapture(url)
    if not cap.isOpened():
        print("Webcam error!!")
        exit()
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, gb.SCREEN_WIDTH )
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,gb.SCREEN_HEIGHT)

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

        if left_ges == "Pointing_Up" or right_ges == "Pointing_Up":
            pydirectinput.keyDown('a')
        else:
            pydirectinput.keyUp('a')

        if left_ges == "ILoveYou" or right_ges == "ILoveYou":
            pydirectinput.keyDown('enter')
        else:
            pydirectinput.keyUp('enter')

        if left_ges == "Victory" or right_ges == "Victory":
            pydirectinput.keyDown('left')
        else:
            pydirectinput.keyUp('left')            

        if left_ges == "Open_Palm" or right_ges == "Open_Palm":
            pydirectinput.keyDown('right')
        else:
            pydirectinput.keyUp('right')            

        if left_ges == "Thumb_Down" or right_ges == "Thumb_Down":
            pydirectinput.keyDown('down')
        else:
            pydirectinput.keyUp('down')                        

#        if left_ges == "None" and right_ges == "None":
#            pydirectinput.keyDown('enter')

        if gb.RenderVideo:
            frame = ac.getFlippedFrame(frame)
            cv2.imshow("Webcam", frame)

        if cv2.waitKey(gb.waitKeyDelayMs) == 27:
            break


cap.release()
cv2.destroyAllWindows()