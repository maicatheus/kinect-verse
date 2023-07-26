import cv2
import math
import vgamepad as vg
import mediapipe as mp
import threading
import time

def distancia_entre_pontos(p1,p2):
    return int(math.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2))

def calcular_angulo(p1,p2):
    theta = math.atan((p2[0] - p1[0])/(p2[1] - p1[1]))
    return int(theta*180/math.pi)

global press
press = False

def pedalar(mao,ombro):
    global rpm, press,tick
    # if rpm > 80 or press:
    #     gamepad.left_trigger_float(0.0)
    #     gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
    #     gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
    #     if not press:
    #         gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
    #         press = True
    #     elif press:
    #         gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
    #         press = False
    #     time.sleep(0.1)
    if mao[1] < ombro[1]:
        gamepad.left_trigger_float(0.8)
        gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
        gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
        rpm =0
        tick = 0
    elif rpm >= 40:
        gamepad.left_trigger_float(0.0)
        gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
        gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
    elif rpm < 40:
        gamepad.left_trigger_float(0.0)
        gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
        gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
    
    else:
        gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
        gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_A)



def normalizar_angulo(angulo,a_min,a_max):
    return((abs(angulo)- a_min)/(a_max-a_min))

def controlar_bike(angulo):
    a_min,a_max = 1,30
    if angulo > a_min:
        if angulo > a_max:
            angulo = a_max
        if abs(angulo) > 15:
            gamepad.left_joystick_float(-0.58   ,0)
        elif abs(angulo) > 12:
            gamepad.left_joystick_float(-0.5,0)
        elif abs(angulo) > 5:
            gamepad.left_joystick_float(-0.4,0)
        else:
            gamepad.left_joystick_float(-0.3,0)
        

    elif angulo < -a_min:
        if angulo < -a_max:
            angulo = -a_max
        if abs(angulo) > 15:
            gamepad.left_joystick_float(0.58    ,0)
        elif abs(angulo) > 12:
            gamepad.left_joystick_float(0.5,0)
        elif abs(angulo) > 5:
            gamepad.left_joystick_float(0.4,0)
        else:
            gamepad.left_joystick_float(0.3,0)   
    else:
        gamepad.left_joystick_float(0,0)


def ponto_medio(p1,p2):
    return(int((p2[0]+p1[0])/2),int((p2[1]+p1[1])/2))

def calcula_rpm(tf):
    return(60*4/tf)


def controla_rotacao(dist,body):
    global rpm, t1, t2, tick,flag
    try:
        if body:
            if dist <= 170 and not flag:
                tick += 1
                flag = True
            if dist > 170 and flag:
                tick += 1 
                flag = False

            
            if tick ==1:
                t1 = time.time()
            if tick == 9:
                t2 = time.time()
                flag = False
                temp = [t1,t2]
                tf = abs(max(temp)-min(temp))
                tick = 0
                rpm = calcula_rpm(tf)  
        
    except:
        pass

camera = cv2.VideoCapture(0)

mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()
gamepad = vg.VX360Gamepad()
global rpm,tick,flag
rpm = 0
flag = False
tick = 0

global t1, t2
t1=t2=time.time()

# Função para processar o vídeo em uma thread separada
while True:
    try:
        ret, frame = camera.read()
        frame =cv2.flip(frame, 1)
        frameRgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(frameRgb)
        body = []
        if results.pose_landmarks:
            for index, lm in enumerate(results.pose_landmarks.landmark):
                h, w, _ = frame.shape
                cx , cy = int(lm.x*w), int(lm.y*h)
                body.append((cx,cy))
            mpDraw.draw_landmarks(frame, results.pose_landmarks, mpPose.POSE_CONNECTIONS)

            try:
                dist = distancia_entre_pontos(body[28],body[24])
                controla_rotacao(dist,body)
                p_medio = ponto_medio(body[24],body[23])
                angulo = calcular_angulo(p_medio,body[0])
                controlar_bike(angulo)

                #mão esquerda
                mao = body[16]
                ombro = body[12]
                pedalar(mao, ombro)

                gamepad.update()
                cv2.putText(frame,f"dist: {str(dist)}",(55,50),cv2.FONT_HERSHEY_SIMPLEX,1,255,3)
                cv2.putText(frame,f"rpm: {str(int(rpm))}",(450,100),cv2.FONT_HERSHEY_SIMPLEX,1,255,3)
                cv2.putText(frame,f"ang: {str(int(angulo))}",(450,50),cv2.FONT_HERSHEY_SIMPLEX,1,255,3)
                cv2.line(frame,body[28],body[24],(255,0,0),2)
                cv2.line(frame,p_medio,body[0],(0,255,0),2)
            except:
                pass

        cv2.imshow("Bike Virtual",frame)
    except:
        pass

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


camera.release()
cv2.destroyAllWindows()
