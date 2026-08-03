import math
import Globals as gb
import Accessories as ac

scale = 100
angle_max = 96
angle_min = 81

def distance3D(p1, p2):
    return math.hypot(p1.x - p2.x ,p1.y - p2.y, p1.z - p2.z)

def hand_scale(hand):
    return distance3D(hand[0], hand[9])

def normalized_distance3D(p1, p2, hand):
    return (distance3D(p1, p2) / hand_scale(hand))*scale


straight_threshold_min = 0
straight_threshold_max = 8

# insane lmao
def getExtendedFingers(detected_hand_points, hand_iden):
    raised = [False, False, False, False, False]
    i = 0
    for finger in gb.FINGER_POINTS:
        if i==0:
            angle1 = ac.getAngle(detected_hand_points[gb.FINGER_POINTS[finger][1]],detected_hand_points[gb.FINGER_POINTS[finger][3]],detected_hand_points[gb.FINGER_POINTS[finger][2]],False)
            if straight_threshold_max >= angle1 >= straight_threshold_min:
                raised[i] = True
        else:
            angle1 = ac.getAngle(detected_hand_points[gb.FINGER_POINTS[finger][0]],detected_hand_points[gb.FINGER_POINTS[finger][2]],detected_hand_points[gb.FINGER_POINTS[finger][1]],False)
            angle2 = ac.getAngle(detected_hand_points[gb.FINGER_POINTS[finger][1]],detected_hand_points[gb.FINGER_POINTS[finger][3]],detected_hand_points[gb.FINGER_POINTS[finger][2]],False)
            if straight_threshold_max >= angle1 >= straight_threshold_min and straight_threshold_max >= angle2 >= straight_threshold_min:
                raised[i] = True
        i+=1

        
    if hand_iden == "left":
        gb.leftRaised = raised
    else:
        gb.rightRaised = raised

def indexFingerPointedANY(detected_hand_points,hand_iden,built_in_closest):
    if not ((hand_iden == "left" and gb.leftRaised[0] == False) or ((hand_iden == "right" and gb.rightRaised[0] == False))):
        return "None"
    #Index & middle
    ind_mid = normalized_distance3D(detected_hand_points[8],detected_hand_points[12],detected_hand_points)

    #Index & weird
    ind_wrd = normalized_distance3D(detected_hand_points[8],detected_hand_points[16],detected_hand_points)

    #Index & pinky
    ind_pnky = normalized_distance3D(detected_hand_points[8],detected_hand_points[20],detected_hand_points)

    #thumb & middle
    thmb_mid = normalized_distance3D(detected_hand_points[2],detected_hand_points[12],detected_hand_points)

#    thmb2_12 = normalized_distance3D(detected_hand_points[2],detected_hand_points[12],detected_hand_points)
#    thmb3_12 = normalized_distance3D(detected_hand_points[3],detected_hand_points[12],detected_hand_points)
#    thmb4_12 = normalized_distance3D(detected_hand_points[4],detected_hand_points[12],detected_hand_points)
#    print("thmb2_12 : ",thmb2_12)
#    print("thmb3_12 : ",thmb3_12)
#    print("thmb4_12 : ",thmb4_12)

    if 150>=ind_mid>=90 and 160>=ind_wrd>=100 and 175>=ind_pnky>=100 and 60>=thmb_mid>=0:# and 18<=thmb2_12<=43 and 18<=thmb3_12<=53 and 18<=thmb4_12<=55:
        angle = ac.getAngle(detected_hand_points[8],detected_hand_points[5],detected_hand_points[9],gb.isAngleBaseHorizontal)
        if angle_min<angle<angle_max:
            return "Index_Up"
        elif (angle>=angle_max and hand_iden == "right") or (angle<=angle_min and hand_iden == "left"):
            return "Left_Lean"
        elif (angle>=angle_max and hand_iden == "left") or (angle<=angle_min and hand_iden == "right"):
            return "Right_Lean"

    if built_in_closest == "Pointing_Up":
        return "EPIC FAIL"
    return "None"

def fairs_pinch_perfect(detected_hand_points,hand_iden,built_in_closest):
    pass
