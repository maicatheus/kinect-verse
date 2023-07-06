import cv2
import mediapipe as mp
import threading
import keyboard
import time

def subir(points):
    if(points[13].y < points[11].y):
        keyboard.press(keyboard.KEY_UP)
        time.sleep(0.2)
        keyboard.release(keyboard.KEY_UP)
        print("subiu!")
def pular(points):
    if (points[0].y < 0.084):
        keyboard.press("x")
        time.sleep(0.2)
        keyboard.release('x')
        print("pulou!")

def atirar(points):
    if (points[15].y < points[13].y):
        keyboard.press("z")
        time.sleep(0.03)
        keyboard.release('z')
        print("Atirou!")

def andar(points):
    if(points[16].y < points[14].y and points[16].x < points[24].x):
        keyboard.release('left')
        keyboard.press("right")
        print("Andando ---->!")
    elif(points[16].y < points[14].y and points[16].x > points[24].x):
        keyboard.release('right')
        keyboard.press("left")
    else:
        keyboard.release('right')
        keyboard.release('left')

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
    try:
        ret, frame = camera.read()
        frameRgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(frameRgb)
        if results.pose_landmarks:
            mpDraw.draw_landmarks(frame, results.pose_landmarks, mpPose.POSE_CONNECTIONS)

        threading.Thread(target=subir(results.pose_landmarks.landmark)).start()
        atirar(results.pose_landmarks.landmark)
        andar(results.pose_landmarks.landmark)
        pular(results.pose_landmarks.landmark)
        threading.Thread(target=pular(results.pose_landmarks.landmark)).start()
        

        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime

        cv2.putText(frame,str(f"FPS: {int(fps)}"),(0,40),font,scale,color,thickness)
        cv2.line(frame, (0,50), (700,50), color, 1)
        cv2.line(frame, (0,350), (700,350), color, 1)

        cv2.imshow("Kinect Verse", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    except:
        print("Algum problema!")

camera.release()
cv2.destroyAllWindows()