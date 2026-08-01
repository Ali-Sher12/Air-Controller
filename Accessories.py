import math
import cv2
import time
import Globals as gb
#import win32gui
#import win32con
#import win32process

def normalize2D(x,y):
    return int(x*gb.SCREEN_WIDTH),int(y*gb.SCREEN_HEIGHT)

def normalizeY(y):
    return int(y*gb.SCREEN_HEIGHT)

def normalizeX(x):
    return int(x*gb.SCREEN_WIDTH)

def normalizeZ(z):#yes, using screen_width is recommended
    return int(z*gb.SCREEN_WIDTH)

def getTimeSeconds():
    return int(time.time()*1000)

def getFlippedFrame(frame):
    return cv2.flip(frame, 1)

def get_finger_index(point1, point2):
    for finger_idx, points in gb.FINGER_POINTS.items():
        if point1 in points and point2 in points:
            return finger_idx
    return None

def get_line_color(point1, point2, raised):
    finger_idx = get_finger_index(point1, point2)
    if finger_idx is None:
        return (255, 0, 0)  # blue for palm/wrist connections

    if raised[finger_idx]:
        return (0, 0, 255)  # red — raised
    return (255, 0, 0)      # blue — not raised

def drawConnections(hand, frame, connections, hand_iden):
    for connection in connections:
        start_point = hand[connection.start]
        end_point = hand[connection.end]
        color = None
        if hand_iden == "left":
            color = get_line_color(connection.start, connection.end, gb.leftRaised)
        else:
            color = get_line_color(connection.start, connection.end, gb.rightRaised)
        cv2.line(frame,normalize2D(start_point.x, start_point.y),normalize2D(end_point.x, end_point.y),color, 2)

def getVector(p1, p2):
    return (p2.x - p1.x, p2.y - p1.y, p2.z - p1.z)

def getDot_product(v1, v2):
    return v1[0]*v2[0] + v1[1]*v2[1] + v1[2]*v2[2]

def getMagnitude(v):
    return math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)

def getAngle(p1, p2, p3,horizaontal_base):
    # p3 is the base point. Can or cannot be collinear iwth p2 (toggle)
    if horizaontal_base:
        p3.y = p2.y
    v1 = getVector(p2, p1)
    v2 = getVector(p2, p3)
    dot = getDot_product(v1, v2)
    mag = getMagnitude(v1) * getMagnitude(v2)
    cos_angle = dot / mag
    cos_angle = max(-1.0, min(1.0, cos_angle))   # clamp to avoid math errors
    angle_radians = math.acos(cos_angle)
    return math.degrees(angle_radians)



"""
def list_open_windows():
    #{hwnd, pid, title}
    windows = []
    def enum_handler(hwnd, results):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if title.strip():
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                results.append({"hwnd": hwnd, "pid": pid, "title": title})
    win32gui.EnumWindows(enum_handler, windows)
    return windows


def print_open_windows():
    for i, w in enumerate(list_open_windows()):
        print(f"{i}: PID={w['pid']:<6} TITLE={w['title']}")


def _restore_and_focus(hwnd):
    if win32gui.IsIconic(hwnd):
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)

    fg_hwnd = win32gui.GetForegroundWindow()
    fg_thread = win32process.GetWindowThreadProcessId(fg_hwnd)[0]
    target_thread = win32process.GetWindowThreadProcessId(hwnd)[0]

    win32process.AttachThreadInput(target_thread, fg_thread, True)
    win32gui.SetForegroundWindow(hwnd)
    win32process.AttachThreadInput(target_thread, fg_thread, False)


def focus_window_by_pid(pid):
    for w in list_open_windows():
        if w["pid"] == pid:
            _restore_and_focus(w["hwnd"])
            return True
    print(f"No window found for PID {pid}")
    return False


def focus_window_by_title(partial_title):
    partial_title = partial_title.lower()
    for w in list_open_windows():
        if partial_title in w["title"].lower():
            _restore_and_focus(w["hwnd"])
            return True
    print(f"No window found matching '{partial_title}'")
    return False


def get_pid_by_title(partial_title):
    #helper
    partial_title = partial_title.lower()
    for w in list_open_windows():
        if partial_title in w["title"].lower():
            return w["pid"]
    return None
"""