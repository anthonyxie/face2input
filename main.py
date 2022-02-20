from cmath import pi
from turtle import width
import keyboard
import cv2
import dlib
import imutils
from imutils import face_utils
import math

detector = dlib.get_frontal_face_detector()


MOUTH_AR_THRESH = 0.22
EYE_AR_THRESH = 0.13
TILT_AR_THRESH = 79
EYE_AR_CONSEC_FRAMES = 3
COUNTERLEFT = 0
COUNTERRIGHT = 0
COUNTERMOUTH = 0
TOTALMOUTH = 0
TOTALLEFT = 0
TOTALRIGHT = 0 

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
cap = cv2.VideoCapture(0)

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

        
        earright = eye_aspect_ratio([landmarks.part(42), landmarks.part(43), landmarks.part(44), landmarks.part(45), landmarks.part(46), landmarks.part(47)])
        earmouth = eye_aspect_ratio([landmarks.part(60), landmarks.part(61), landmarks.part(63), landmarks.part(64), landmarks.part(65), landmarks.part(67)])

        headtilt = angle_calc(landmarks.part(27), landmarks.part(8))

        cv2.putText(frame, "EARRIGHT: {:.2f}".format(earright), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        cv2.putText(frame, "HEADTILT: {:.2f}".format(headtilt), (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(frame, "EARMOUTH: {:.2f}".format(earmouth), (300, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

                
        if earright < EYE_AR_THRESH:
            COUNTERRIGHT += 1
        else:
            if COUNTERRIGHT >= EYE_AR_CONSEC_FRAMES:
                TOTALRIGHT += 1
                #keyboard.send("r")
                print("blink")
			# reset the eye frame counter
                COUNTERRIGHT = 0

        if earmouth > MOUTH_AR_THRESH:
            COUNTERMOUTH += 1
        else:
            if COUNTERMOUTH >= EYE_AR_CONSEC_FRAMES:
                TOTALMOUTH += 1
                #keyboard.send("m")
                print("m")
			# reset the eye frame counter
                COUNTERMOUTH = 0
    
        if headtilt < TILT_AR_THRESH:
            #keyboard.press("u")
        else:
            #if keyboard.is_pressed("u"):
                #keyboard.release("u")
        
        cv2.putText(frame, "TOTALBLINK: {:.2f}".format(TOTALRIGHT), (10, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, "TOTALMOUTH: {:.2f}".format(TOTALMOUTH), (100, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # Loop through all the points
        for n in range(0, 68):
            x = landmarks.part(n).x
            y = landmarks.part(n).y

            # Draw a circle
            cv2.circle(img=frame, center=(x, y), radius=3, color=(0, 255, 0), thickness=-1)


    # show the image
    cv2.imshow(winname="Face", mat=frame)

    # Exit when escape is pressed
    if cv2.waitKey(delay=1) == 27:
        break

# When everything done, release the video capture and video write objects
cap.release()

# Close all windows
cv2.destroyAllWindows()