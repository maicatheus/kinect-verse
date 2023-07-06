import cv2
import mediapipe as mp
import time

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
                    double_hands[i].append(
                        {
                            id:{
                                "x":cx,
                                "y":cy
                            }
                        }
                    )
                mpDraw.draw_landmarks(frame, handsLms, mpHand.HAND_CONNECTIONS)
        print("Double hand")
        print(double_hands)


        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime

        cv2.putText(frame,str(f"FPS: {int(fps)}"),(0,40),font,scale,color,thickness)

        cv2.imshow("Kinect Verse", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    except:
        print("Algum problema!")

camera.release()
cv2.destroyAllWindows()