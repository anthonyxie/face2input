from cmath import pi
from telnetlib import DO
from tkinter import HORIZONTAL
import pyautogui
import pydirectinput
import keyboard
import cv2
import dlib
import math
import time 
detector = dlib.get_frontal_face_detector()


MOUTH_AR_THRESH = 0.1
EYE_AR_THRESH = 0.15
TILT_AR_THRESH = 76
EYE_AR_CONSEC_FRAMES = 2
COUNTERLEFT = 0
COUNTERRIGHT = 0
COUNTERMOUTH = 0
TOTALMOUTH = 0
TOTALLEFT = 0
TOTALRIGHT = 0 
BOXHORIZONTAL = 70
BOXVERTICAL = 45

pydirectinput.PAUSE = 0
pyautogui.PAUSE = 0

minecraft = {'up': "w" , 'down': "s", 'left': "a", 'right': "d", "jump": "space"}
celeste  = {'up': "[", 'down': "]", 'left': ";", 'right':"'", "dash":"x" ,"jump":"c", "grab":"t"}
hollowknight = {'up': "up", 'down': "down", 'left': "left", 'right':"right"}
DASH = celeste["dash"]
JUMP = minecraft["jump"]
GRAB = celeste["grab"]
UP = minecraft["up"]
DOWN = minecraft["down"]
LEFT = minecraft["left"]
RIGHT = minecraft["right"]

def angle_calc(land1, land2):
    x = ((land1.x - land2.x)**2)**(1/2) + 0.005
    y = ((land1.y - land2.y)**2)**(1/2)
    angle = math.atan(y / x) * (180 / math.pi)
    return angle

def eye_aspect_ratio(eye):
	# compute the euclidean distances between the two sets of
	# vertical eye landmarks (x, y)-coordinates
	A = ((eye[1].x - eye[5].x)**2 + (eye[1].y - eye[5].y)**2)**(1/2)
	B = ((eye[2].x - eye[4].x)**2 + (eye[2].y - eye[4].y)**2)**(1/2)
	# compute the euclidean distance between the horizontal
	# eye landmark (x, y)-coordinates
	C = ((eye[0].x - eye[3].x)**2 + (eye[0].y - eye[3].y)**2)**(1/2)
	# compute the eye aspect ratio
	ear = (A + B) / (2.0 * C)
	# return the eye aspect ratio
	return ear


# Load the predictor
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# read the image
cap = cv2.VideoCapture(1)

while True:
    _, frame = cap.read()
    # Convert image into grayscale
    gray = cv2.cvtColor(src=frame, code=cv2.COLOR_BGR2GRAY)
    # Use detector to find landmarks
    faces = detector(gray)
    

    for face in faces:
        x1 = face.left()  # left point
        y1 = face.top()  # top point
        x2 = face.right()  # right point
        y2 = face.bottom()  # bottom point

        # Create landmark object

        landmarks = predictor(image=gray, box=face)
        cv2.rectangle(frame, (320 - BOXHORIZONTAL,0), (320 + BOXHORIZONTAL, 480), (0,255,0), 1)
        cv2.rectangle(frame, (0,240 - BOXVERTICAL), (640, 240 + BOXVERTICAL), (0,255,0), 1)
 
        faceposX = 0
        faceposY = 0
        # Loop through all the points
        for n in range(0, 68):
            x = landmarks.part(n).x
            y = landmarks.part(n).y

            # Draw a circle
            if n == 28:
                cv2.circle(img=frame, center=(x, y), radius=3, color=(0, 255, 0), thickness=-1)
                faceposX = x
                faceposY = y
           
        earright = eye_aspect_ratio([landmarks.part(42), landmarks.part(43), landmarks.part(44), landmarks.part(45), landmarks.part(46), landmarks.part(47)])
        earmouth = eye_aspect_ratio([landmarks.part(60), landmarks.part(61), landmarks.part(63), landmarks.part(64), landmarks.part(65), landmarks.part(67)])

        headtilt = angle_calc(landmarks.part(27), landmarks.part(8))


        if not keyboard.is_pressed("/"):        
            if earright < EYE_AR_THRESH:
                pydirectinput.keyDown(DASH)
                COUNTERRIGHT += 1
            else:
                if COUNTERRIGHT >= EYE_AR_CONSEC_FRAMES:
                    pydirectinput.keyUp(DASH)
                    COUNTERRIGHT = 0

            if earmouth > MOUTH_AR_THRESH:
                pydirectinput.keyDown(JUMP)
                COUNTERMOUTH += 1
            else:
                if COUNTERMOUTH > EYE_AR_CONSEC_FRAMES:
                    TOTALMOUTH += 1    
                    COUNTERMOUTH = 0
                    pydirectinput.keyUp(JUMP)
        
            if headtilt < TILT_AR_THRESH:
                pydirectinput.keyDown(GRAB)
            else:
                if keyboard.is_pressed(GRAB):
                    pydirectinput.keyUp(GRAB)

        #is head in the neutral zone
        if 320 - BOXHORIZONTAL <=  faceposX <= 320 + BOXHORIZONTAL and 240 - BOXVERTICAL <=  faceposY <= 240 + BOXVERTICAL:
            if keyboard.is_pressed(UP):
                pydirectinput.keyUp(UP)
            if keyboard.is_pressed(DOWN):
                pydirectinput.keyUp(DOWN)
            if keyboard.is_pressed(LEFT):
                pydirectinput.keyUp(LEFT)
            if keyboard.is_pressed(RIGHT):
                pydirectinput.keyUp(RIGHT)
        
            #head in left
        if not keyboard.is_pressed("/"):
            if faceposX < 320 - BOXHORIZONTAL:
                pydirectinput.keyDown(LEFT)
            #head in right
            if faceposX > 320 + BOXHORIZONTAL:
                pydirectinput.keyDown(RIGHT)
            #head in up
            if faceposY < 240 - BOXVERTICAL:
                pydirectinput.keyDown(UP)
            #head in down
            if faceposY > 240 + BOXVERTICAL:
                pydirectinput.keyDown(DOWN)
        
        

        

    # show the image
    cv2.imshow(winname="Face", mat=frame)

    # Exit when escape is pressed
    if cv2.waitKey(delay=1) == 27:
        break

# When everything done, release the video capture and video write objects
cap.release()

# Close all windows
cv2.destroyAllWindows()
