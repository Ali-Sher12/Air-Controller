import Globals as gb
import ctypes

centerYaw = [-4,4]
centerPitch = [-4,4]
centerRoll = [-4,4]

yawRange = [-25,25]
pitchRange = [-20,15]
rollRange = [-25,25]

def inNormalRange(y,p,r):
    # yaw,pitch,roll : 1,2,3
    a = b = c = 0
    if centerYaw[0]<y<centerYaw[1]:
        a = 1
    if centerPitch[0]<p<centerPitch[1]:
        b = 1
    if centerRoll[0]<r<centerRoll[1]:
        c = 1
    return a,b,c

def getDeltas(y,p,r):
    a = y
    b = p
    c = r
    a,b,c = inNormalRange(y,p,r)    
    if not a:
        if y<0:
            a = -y + centerYaw[0]
        else:
            a = -y + centerYaw[1]
    if not b:
        if p<0:
            b = p - centerPitch[0]
        else:
            b = p - centerPitch[1]
    if not c:
        if r<0:
            c = r - centerRoll[0]
        else:
            c = r - centerRoll[1]

    return a,b,c

def remap(y,p,r):
    y = max(yawRange[0]  , min(yawRange[1]  , y))
    p = max(pitchRange[0], min(pitchRange[1], p))
    r = max(rollRange[0] , min(rollRange[1] , r))    
    retY = (y - yawRange[0]  ) / (yawRange[1]   - yawRange[0]  )
    retP = (p - pitchRange[0]) / (pitchRange[1] - pitchRange[0])
    retR = (r - rollRange[0] ) / (rollRange[1]  - rollRange[0] )        
    retY = retY * (gb.ACTIVE_SCREEN_WIDTH)
    retP = retP * (gb.ACTIVE_SCREEN_HEIGHT)
    retR = retR * (gb.ACTIVE_SCREEN_WIDTH) #placeholder
    return retY,retP,retR

def send_relative_mouse_move(dx, dy):
    extra = ctypes.c_ulong(0)
    ii_ = ctypes.c_ulong(0)

    class MOUSEINPUT(ctypes.Structure):
        _fields_ = [
            ("dx", ctypes.c_long),
            ("dy", ctypes.c_long),
            ("mouseData", ctypes.c_ulong),
            ("dwFlags", ctypes.c_ulong),
            ("time", ctypes.c_ulong),
            ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))
        ]

    class INPUT(ctypes.Structure):
        _fields_ = [
            ("type", ctypes.c_ulong),
            ("mi", MOUSEINPUT)
        ]

    MOUSEEVENTF_MOVE = 0x0001
    mi = MOUSEINPUT(dx, dy, 0, MOUSEEVENTF_MOVE, 0, ctypes.pointer(extra))
    inp = INPUT(0, mi)  # type=0 means INPUT_MOUSE
    ctypes.windll.user32.SendInput(1, ctypes.pointer(inp), ctypes.sizeof(inp))
