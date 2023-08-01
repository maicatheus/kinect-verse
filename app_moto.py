import cv2
import math
import vgamepad as vg
import mediapipe as mp

def distancia_entre_pontos(p1,p2):
    return int(math.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2))

def calcular_angulo(p1,p2):
    theta = math.atan((p2[0] - p1[0])/(p2[1] - p1[1]))
    return int(theta*180/math.pi)


def acelerar_moto(mao,ombro,dist):
    acel_val = 0.9

    if mao[1] < ombro[1]:
        gamepad.left_trigger_float(0.8)
        gamepad.right_trigger_float(0.0)
    elif dist < 140:
        gamepad.left_trigger_float(0.0)
        gamepad.right_trigger_float(acel_val)
    elif dist < 160 and dist >=140:
        gamepad.left_trigger_float(0.0)
        gamepad.right_trigger_float(0.0)
    elif dist >= 160 and dist < 250:
        gamepad.left_trigger_float(0.4)
        gamepad.right_trigger_float(0.0)
    elif dist >300:
        gamepad.left_trigger_float(0.0)
        gamepad.right_trigger_float(0.0)





def normalizar_angulo(angulo,a_min,a_max):
    return((abs(angulo)- a_min)/(a_max-a_min))

def controlar_moto(angulo):
    a_min,a_max = 1,30
    if angulo > a_min:
        if angulo > a_max:
            angulo = a_max
        if abs(angulo) > 15:
            gamepad.left_joystick_float(-0.7,0)
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
            gamepad.left_joystick_float(0.7,0)
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

camera = cv2.VideoCapture(0)
mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()
gamepad = vg.VX360Gamepad()

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
                p_medio = ponto_medio(body[24],body[23])
                angulo = calcular_angulo(p_medio,body[0])
                controlar_moto(angulo)
                dist = distancia_entre_pontos(p_medio,body[0])
                
                #mão esquerda
                mao = body[16]
                ombro = body[12]
                acelerar_moto(mao, ombro, dist)

                gamepad.update()
                cv2.putText(frame,f"dist: {str(dist)}",(150,50),cv2.FONT_HERSHEY_SIMPLEX,1,255,3)
                cv2.putText(frame,f"ang: {str(int(angulo))}",(300,50),cv2.FONT_HERSHEY_SIMPLEX,1,255,3)
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
