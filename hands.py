import cv2
import pyautogui
import time
from ultralytics import YOLO

MODEL_PATH = 'best.pt'

CONF_THRESHOLD = 0.7 

COOLDOWN_PERIOD = 2.0 

# Lista de teclas do pyautogui: https://pyautogui.readthedocs.io/en/latest/keyboard.html
GESTURE_MAP = {
    'fist': 'space',        # Ex: "Punho fechado" -> "Barra de espaço" (Play/Pause)
    'open_hand': 'volumeup',    # Ex: "Mão aberta" -> "Aumentar volume"
    'thumbs_down': 'volumedown', # Ex: "Polegar para baixo" -> "Diminuir volume"
}


# Tente os índices 0, 1, 2...
WEBCAM_INDEX = 0

USE_IP_WEBCAM = False # Mude para True se usar IP Webcam
IP_WEBCAM_URL = 'http://' 


# Variável para rastrear o tempo do último comando
last_action_time = 0

# Carregar seu modelo YOLO customizado
try:
    model = YOLO(MODEL_PATH)
    print(f"Modelo '{MODEL_PATH}' carregado com sucesso.")
except Exception as e:
    print(f"Erro ao carregar o modelo: {e}")
    print("Verifique se o arquivo 'best.pt' está na mesma pasta do script.")
    exit()

# Capturar vídeo da webcam
if USE_IP_WEBCAM:
    cap = cv2.VideoCapture(IP_WEBCAM_URL)
else:
    cap = cv2.VideoCapture(WEBCAM_INDEX)

if not cap.isOpened():
    print(f"Erro: Não foi possível abrir a webcam (Índice: {WEBCAM_INDEX} ou URL: {IP_WEBCAM_URL}).")
    print("Verifique se a câmera está conectada ou se o índice/URL está correto.")
    exit()

print("Webcam iniciada. Pressione 'q' para sair.")
print(f"Mapeamento de gestos ATIVO: {GESTURE_MAP}")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Erro ao ler o frame da webcam. Encerrando.")
        break

    # Inverter o frame horizontalmente (efeito espelho, mais intuitivo)
    frame = cv2.flip(frame, 1)

    # Rodar a inferência YOLO (verbose=False para não poluir o terminal)
    results = model(frame, verbose=False) 

    current_action = None
    highest_conf = 0.0

    # Processar os resultados da detecção
    for result in results:
        for box in result.boxes:
            conf = float(box.conf[0])
            
            # 1. Checa a confiança
            if conf > CONF_THRESHOLD:
                cls_id = int(box.cls[0])
                class_name = model.names[cls_id]

                # Desenhar a caixa e o rótulo no frame
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f"{class_name} ({conf:.2f})", (x1, y1 - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                # 2. Checa se o gesto está no nosso mapa e tem a maior confiança
                if conf > highest_conf and class_name in GESTURE_MAP:
                    highest_conf = conf
                    current_action = GESTURE_MAP[class_name]
                    # Guardamos o nome da classe para o print
                    detected_gesture_name = class_name 

    # --- LÓGICA DE COOLDOWN E ACIONAMENTO ---
    current_time = time.time()
    
    # 3. Se um gesto válido foi detectado E o cooldown já passou...
    if current_action and (current_time - last_action_time) > COOLDOWN_PERIOD:
        print(f"AÇÃO: Gesto '{detected_gesture_name}' detectado. Pressionando: '{current_action}'")
        
        try:
            pyautogui.press(current_action)
            last_action_time = current_time # Reinicia o timer do cooldown
        except Exception as e:
            print(f"Erro ao pressionar a tecla '{current_action}': {e}")

    # Exibir o frame da webcam
    cv2.imshow('Controle de Gestos - Pressione "q" para sair', frame)

    # Sair do loop se 'q' for pressionado
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()
print("Encerrando...")