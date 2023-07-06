import cv2
import mediapipe as mp
import keyboard
import time
import math

def calculate_angle(p1,p2):
    return math.tan(((p2[1]-p1[1])/(p2[0]-p1[0])))

def control_car(angle):
    if(angle > 0.15):
        keyboard.release('right')
        keyboard.press("left")
        print("Esquerda")
    elif(angle < -0.15):
        keyboard.release('left')
        keyboard.press("right")
        print("Direita")
    else:
        keyboard.release('right')
        keyboard.release('left')
        print("Reto")

def drive_car(p1,p2):
    if(p1[4][1] < p1[3][1] and p2[4][1] < p2[3][1]):
        keyboard.release('s')
        keyboard.press("w")
        print("ACELERA!")   
    elif((p1[4][1] > p1[3][1] and p2[4][1] < p2[3][1]) or (p1[4][1] < p1[3][1] and p2[4][1] > p2[3][1])):
        keyboard.release('w')
        keyboard.press("s")
        print("FREIA!")
    else:
        keyboard.release('w')
        keyboard.release('s')

def distancia_entre_pontos(p1,p2):
    return math.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)

camera = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_PLAIN
scale = 3
pTime = 0
color = (255,0,0)
thickness = 3

mpDraw = mp.solutions.drawing_utils
mpHand = mp.solutions.hands
hands = mpHand.Hands(max_num_hands=2)

while True:
    try:
        ret, frame = camera.read()
        frameRgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frameRgb)
        double_hands = ([],[])
        if results.multi_hand_landmarks:
            for i,handsLms in enumerate(results.multi_hand_landmarks):
                for id, lm in enumerate(handsLms.landmark):
                    h, w, c = frame.shape
                    cx, cy= int(lm.x*w), int(lm.y*h)
                    double_hands[i].append((cx,cy))

                mpDraw.draw_landmarks(frame, handsLms, mpHand.HAND_CONNECTIONS)
                try:
                    angle = calculate_angle(double_hands[0][0],double_hands[1][0])
                    control_car(angle)
                    drive_car(double_hands[0], double_hands[1])
                    cv2.line(frame, double_hands[0][0], double_hands[1][0], color, 1)
                except:
                    pass

        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime
        # cv2.putText(frame,str(f"angulo: {int(angle)}"),(0,50),font,scale,color,thickness)
        cv2.putText(frame,str(f"FPS: {int(fps)}"),(0,40),font,scale,color,thickness)

        cv2.imshow("Kinect Verse", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    except:
        print("Algum problema!")

camera.release()
cv2.destroyAllWindows()