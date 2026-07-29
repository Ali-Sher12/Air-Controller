import cv2
import time
import Globals as gb

def normalize(x,y):
    return int(x*gb.SCREEN_WIDTH),int(y*gb.SCREEN_HEIGHT)

def normalizeY(y):
    return int(y*gb.SCREEN_HEIGHT)

def normalizeX(x):
    return int(x*gb.SCREEN_WIDTH)

def getTimeSeconds():
    return int(time.time()*1000)

def getFlippedFrame(frame):
    return cv2.flip(frame, 1)

def drawConnections(hand,frame,connections):
    for connection in connections:
        start_point = hand[connection.start]
        end_point = hand[connection.end]
        cv2.line(frame,normalize(start_point.x, start_point.y),normalize(end_point.x, end_point.y),(255, 0, 0),2)