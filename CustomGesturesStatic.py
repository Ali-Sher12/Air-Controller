import math
import Globals as gb
import Accessories as ac

scale = 100
def distance3D(p1, p2):
    return math.hypot(p1.x - p2.x ,p1.y - p2.y, p1.z - p2.z)


def hand_scale(hand):
    return distance3D(hand[0], hand[9])

def normalized_distance3D(p1, p2, hand):
    return (distance3D(p1, p2) / hand_scale(hand))*scale


def indexFingerPointedANY(detected_hand_points,hand_iden):
    #Index & middle
    ind_mid = normalized_distance3D(detected_hand_points[8],detected_hand_points[12],detected_hand_points)

    #Index & weird
    ind_wrd = normalized_distance3D(detected_hand_points[8],detected_hand_points[16],detected_hand_points)

    #Index & pinky
    ind_pnky = normalized_distance3D(detected_hand_points[8],detected_hand_points[20],detected_hand_points)

    #thumb & middle
    thmb_mid = normalized_distance3D(detected_hand_points[2],detected_hand_points[12],detected_hand_points)

    if 150>=ind_mid>=90 and 160>=ind_wrd>=100 and 175>=ind_pnky>=100 and 60>=thmb_mid>=0:
        ac.getAngle(detected_hand_points[8],detected_hand_points[5],detected_hand_points[13])
        return "Index_Up"
    return "None"

