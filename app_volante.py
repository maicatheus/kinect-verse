import cv2
import math
import vgamepad as vg
import mediapipe as mp


def normalizar_angulo(angulo,a_min,a_max):
    return((abs(angulo)- a_min)/(a_max-a_min))

def calcular_angulo(p1,p2):
    theta = math.atan((p2[1] - p1[1])/(p2[0] - p1[0]))
    return theta*180/math.pi

def controlar_velocidade(pontos):
    hand1,hand2 = pontos
    if(hand1[4][1]<hand1[3][1] and hand2[4][1]<hand2[3][1]):
        gamepad.left_trigger_float(0)
        gamepad.right_trigger_float(0.86)
        print("Acelera!")
    elif(hand1[4][1]<hand1[3][1] and hand2[4][1]>hand2[3][1] or hand1[4][1]>hand1[3][1] and hand2[4][1]<hand2[3][1]):
        gamepad.right_trigger_float(0)
        gamepad.left_trigger_float(1)
        print("Freio!")
    else:
        gamepad.right_trigger_float(0)
        gamepad.left_trigger_float(0)

def controlar_volante(angulo):
    a_min, a_max = 1, 30
    if angulo > a_min:
        if angulo > a_max:
            angulo = a_max
        gamepad.left_joystick_float(-normalizar_angulo(angulo,a_min,a_max),0)
        print("Esquerda")

    elif angulo < -a_min:
        if angulo < - a_max:
            angulo = -a_max
        gamepad.left_joystick_float(normalizar_angulo(angulo,a_min,a_max),0)
        print("Direita")
    
    else:
        gamepad.left_joystick_float(0,0)
        print("Reto")
    

camera = cv2.VideoCapture(0)

mpDraw = mp.solutions.drawing_utils
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=2)
gamepad = vg.VX360Gamepad()
while True:
    try:
        ret, frame = camera.read()

        frameRgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        results = hands.process(frameRgb)

        double_hands = ([],[])
        if results.multi_hand_landmarks:
            for index, handsLms in enumerate(results.multi_hand_landmarks):
                for id, lm in enumerate(handsLms.landmark):
                    h, w, _ = frame.shape
                    cx , cy = int(lm.x*w), int(lm.y*h)
                    double_hands[index].append((cx,cy))

                mpDraw.draw_landmarks(frame,handsLms,mpHands.HAND_CONNECTIONS)  
            
            try:
                angulo = calcular_angulo(double_hands[0][0],double_hands[1][0])
                controlar_volante(angulo)
                controlar_velocidade(double_hands)
                gamepad.update()
                cv2.line(frame,double_hands[0][0],double_hands[1][0],(255,0,0),3)
            except:
                print("Problema")


        cv2.imshow("Volante virtual",frame)
    except:
        pass
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break