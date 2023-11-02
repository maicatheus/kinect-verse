import cv2
import mediapipe as mp


def magiaAcontece(isHand1Up, isHand2Up, pontoImagem):
    if imagem is not None:
        if(not isHand1Up and isHand2Up):
            x_offset, y_offset = pontoImagem  # Ajuste conforme necessário
            frame[y_offset:y_offset + imagem.shape[0], x_offset:x_offset + imagem.shape[1]] = imagem

def ishandUp(hand):
    if (hand[8][1] < hand[7][1] and hand[12][1] < hand[11][1] and hand[16][1] < hand[15][1] and hand[20][1] < hand[19][1]):
        return True
    return False

def maosLevantadas(double_hands):
    h1, h2 = double_hands

    hand1 = ishandUp(h1)
    hand2 = ishandUp(h2)

    magiaAcontece(hand1,hand2,h2[17])



    print(f"Mao 1 levantada: {hand1} | Mao 2 levantada: {hand2}")

# Carregue a imagem
imagem = cv2.imread('./sicredi.jpg')
novo_tamanho = (70, 70)  
imagem = cv2.resize(imagem, novo_tamanho)

camera = cv2.VideoCapture(2)
mpDraw = mp.solutions.drawing_utils
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=2)

while True:
    try:
        ret, frame = camera.read()
        frame = cv2.flip(frame, 1)
        frameRgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frameRgb)

        double_hands = ([], [])
        if results.multi_hand_landmarks:
            for index, handsLms in enumerate(results.multi_hand_landmarks):
                for id, lm in enumerate(handsLms.landmark):
                    h, w, _ = frame.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    double_hands[index].append((cx, cy))

                # mpDraw.draw_landmarks(frame, handsLms, mpHands.HAND_CONNECTIONS)

        try:
            maosLevantadas(double_hands)
            

        except:
            pass

        cv2.imshow("Magica", frame)
    except:
        pass
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Libere a câmera e feche a janela quando a tecla 'q' for pressionada
camera.release()
cv2.destroyAllWindows()
