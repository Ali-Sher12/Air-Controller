import math
import cv2
import time
import Globals as gb

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

def drawConnections(hand,frame,connections):
    for connection in connections:
        start_point = hand[connection.start]
        end_point = hand[connection.end]
        cv2.line(frame,normalize2D(start_point.x, start_point.y),normalize2D(end_point.x, end_point.y),(255, 0, 0),2)


def getVector(p1, p2):
    return (p2.x - p1.x, p2.y - p1.y, p2.z - p1.z)

def dot_product(v1, v2):
    return v1[0]*v2[0] + v1[1]*v2[1] + v1[2]*v2[2]

def magnitude(v):
    return math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)

def angle_between(p1, p2, p3):
    # p2 is the joint (the "hinge" point)
    v1 = getVector(p2, p1)   # vector from joint to first point
    v2 = getVector(p2, p3)   # vector from joint to second point

    dot = dot_product(v1, v2)
    mag = magnitude(v1) * magnitude(v2)

    cos_angle = dot / mag
    cos_angle = max(-1.0, min(1.0, cos_angle))   # clamp to avoid math errors

    angle_radians = math.acos(cos_angle)
    return math.degrees(angle_radians)