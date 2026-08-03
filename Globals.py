left_landmarks = None
right_landmarks = None

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
waitKeyDelayMs = 1
time_secs = 0
doVideoStream = False
printDebug = False

DrawSkeleton = True
RenderVideo = True

Record = False
pressKeys = False

giveCustomGesturesPriority = True
isAngleBaseHorizontal = True
enableFrontEnd = False

leftMissing = True
rightMissing = True

leftRaised = [False,True,False,False,False]
rightRaised = [False,False,False,True,False] # do we reset these in main? Lets see.


FINGER_POINTS = {
    0: (1, 2, 3, 4),      # thumb
    1: (5, 6, 7, 8),      # index
    2: (9, 10, 11, 12),   # middle
    3: (13, 14, 15, 16),  # ring
    4: (17, 18, 19, 20),  # pinky
}

facialThresh = 0.35
frame = None