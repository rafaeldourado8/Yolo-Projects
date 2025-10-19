🖐️ Controle de Mídia por Gestos com YOLOv8 e PyAutoGUI
Este projeto utiliza Visão Computacional (YOLOv8) para detectar gestos de mão em tempo real através da webcam e traduzi-los em comandos de teclado para controlar aplicativos de mídia no seu computador (como Spotify, YouTube, VLC, etc.).
⚙️ Tecnologias Utilizadas
Python: Linguagem principal do projeto.

OpenCV (cv2): Para captura de vídeo da webcam e processamento de imagem.

Ultralytics (YOLO): Para carregar e executar o modelo de detecção de objetos (YOLOv8).

PyAutoGUI: Para simular o pressionamento de teclas do sistema operacional.

Time: Para gerenciar o sistema de cooldown.

🚀 Como Configurar e Rodar
1. Pré-requisitos
Certifique-se de ter o Python instalado em seu sistema.

2. Instalação de Dependências
Instale todas as bibliotecas necessárias via pip:

pip install opencv-python ultralytics pyautogui

3. Modelo YOLOv8
O script espera que o modelo treinado esteja no formato PyTorch (.pt).

Baixe ou treine seu modelo e salve-o na mesma pasta do script com o nome best.pt.

O modelo deve ser treinado para detectar classes de gestos, como fist, open_hand, thumbs_down, etc.

4. Configuração Inicial

MODEL_PATH	Caminho do arquivo do modelo.	'best.pt'
CONF_THRESHOLD	Limite de confiança para aceitar uma detecção (0.0 a 1.0).	0.7
COOLDOWN_PERIOD	Tempo (em segundos) que se deve esperar entre ações.	2.0
WEBCAM_INDEX	Índice da sua webcam (geralmente 0 para a câmera principal).	0
USE_IP_WEBCAM	Mude para True se usar um celular como câmera (ex: IP Webcam).	False
IP_WEBCAM_URL	URL do stream da IP Webcam (se USE_IP_WEBCAM=True).	'http://'

5. Mapeamento de Gestos

Ajuste o dicionário GESTURE_MAP para definir qual gesto (nome da classe) aciona qual tecla. As classes devem corresponder às do seu modelo.

GESTURE_MAP = {
    'fist': 'space',        # Ex: Punho Fechado -> Play/Pause
    'open_hand': 'volumeup',    # Ex: Mão Aberta -> Aumentar Volume
    'thumbs_down': 'volumedown', # Ex: Polegar para Baixo -> Diminuir Volume
    # Adicione mais gestos conforme seu modelo...
}

6. Execução

Rode o script no seu terminal:
python seu_script_nome.py

💻 Funcionamento do Código
O fluxo de trabalho do script segue uma estrutura robusta para garantir a detecção precisa e a estabilidade dos comandos:

Inicialização: O modelo YOLO é carregado (YOLO('best.pt')) e a conexão com a webcam é estabelecida.

Loop Principal (Por Frame):

O frame lido da webcam é espelhado (cv2.flip) para uma experiência mais intuitiva.

A inferência YOLO é executada (model(frame)).

Processamento dos Resultados:

O código itera sobre todas as detecções, desenhando caixas delimitadoras e rótulos para gestos com confiança acima de CONF_THRESHOLD.

O gesto válido com a maior confiança é selecionado para ser o comando potencial (current_action).

Lógica de Cooldown e Acionamento:

O script verifica duas condições cruciais:

Um comando válido (current_action) foi detectado.

O tempo de COOLDOWN_PERIOD passou desde a última ação (last_action_time).

Se ambas as condições forem atendidas, o comando de teclado é enviado via pyautogui.press(current_action), e o last_action_time é atualizado.

Essa lógica de cooldown é fundamental para evitar o disparo contínuo de comandos, tornando o controle prático e responsivo ao invés de caótico.
