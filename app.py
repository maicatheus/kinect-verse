import cv2
import mediapipe as mp
import math
import pyautogui
import time

camera = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_PLAIN
scale = 3
pTime = 0
color = (255,0,0)
thickness = 3

mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()

while True:
    
    ret, frame = camera.read()
    frameRgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(frameRgb)
    if results.pose_landmarks:
        mpDraw.draw_landmarks(frame, results.pose_landmarks, mpPose.POSE_CONNECTIONS)

    

    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    cv2.putText(frame,str(f"FPS: {int(fps)}"),(0,40),font,scale,color,thickness)


    cv2.imshow("Kinect Verse", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()