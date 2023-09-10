import cv2
import numpy as np
import mediapipe as mp
import math
import pyautogui as pg

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
camera = cv2.VideoCapture(0)
hands = mp_hands.Hands()
pinch_position = []
direction = [0,0]

def moveCursor():
    try:
        x = pg.position().x
        y = pg.position().y
        new_x = x + direction[0]*8
        new_y = y + direction[1]*8
        #slope*(-x+new_x)
        pg.moveTo(new_x, new_y)
    except:
        pass
    
def changeDirections(pinch_position, curr_pos):
    if curr_pos[0] > pinch_position[0]:
        direction[0] = 1
    elif curr_pos[0] == pinch_position[0]:
        direction[0] = 0
    else:
        direction[0] = -1
        
    if curr_pos[1] > pinch_position[1]:
        direction[1] = 1
    elif curr_pos[1] == pinch_position[1]:
        direction[1] = 0
    else:
        direction[1] = -1
   # if pinch_position[0] != curr_pos[0]:
    #    slope = (curr_pos[1]-pinch_position[1])/(curr_pos[0]-pinch_position[0])
        
def getCurrentPosition(landmarks):
    (h, w, c) = image_frame.shape
    #print(h, w, c)
    thumb_position = []
    index_position = []
    for index, lm in enumerate(landmarks.landmark):
        if index == 8:
            index_position = (lm.x*w, lm.y*h)
        if index == 4:
            thumb_position = (lm.x*w, lm.y*h)
    if len(index_position) ==2 and len(thumb_position) ==2:
        return ((thumb_position[0]+index_position[0])/2,
                (thumb_position[1]+index_position[1])/2)
    return []
        
def isPinch(landmarks):
    global pinch_position 
    (h, w, c) = image_frame.shape
    #print(h, w, c)
    thumb_position = []
    index_position = []
    for index, lm in enumerate(landmarks.landmark):
        if index == 8:
            index_position = (lm.x*w, lm.y*h)
        if index == 4:
            thumb_position = (lm.x*w, lm.y*h)
    if len(index_position) ==2 and len(thumb_position) ==2:
        distance = math.dist(index_position, thumb_position)
        if distance <= 50:
            if len(pinch_position) == 0:
                pinch_position = ((thumb_position[0]+index_position[0])/2,
                              (thumb_position[1]+index_position[1])/2)            
            return True
        else:
            return False
    else:
        return False
        

while True:
    ret, image_frame = camera.read()
    cimg = cv2.cvtColor(image_frame, cv2.COLOR_BGR2RGB)
    results = hands.process(cimg)
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        mp_drawing.draw_landmarks(image_frame, hand_landmarks, mp_hands.HAND_CONNECTIONS, mp_drawing_styles.get_default_hand_landmarks_style(), mp_drawing_styles.get_default_hand_connections_style())
        if isPinch(hand_landmarks):
            pg.mouseDown()
            currpos = getCurrentPosition(hand_landmarks)
            changeDirections(pinch_position, currpos)
            moveCursor()
        else:
            pg.mouseUp()
            pich_position = []
            direction = [0,0]

    cv2.imshow("image",image_frame)
    #cv2.imshow("converted image", cimg)
    if cv2.waitKey(1) == ord('q'):
        break
