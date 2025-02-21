import pygame
import cv2
import sys
import os

# Inicializa o pygame
pygame.init()

# Configurações da tela
LARGURA, ALTURA = 800, 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo da Memória")

# Verifica se o arquivo de vídeo existe
VIDEO_PATH = "nuvem.mp4"
if not os.path.exists(VIDEO_PATH):
    print(f"Erro: Arquivo {VIDEO_PATH} não encontrado!")
    sys.exit()

# Carregar vídeo de fundo
video = cv2.VideoCapture(VIDEO_PATH)
sucesso, frame = video.read()
if not sucesso:
    print("Erro: Não foi possível carregar o vídeo.")
    sys.exit()

# Converte frame inicial para pygame
frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))

# Fonte para mensagens
fonte = pygame.font.Font(None, 36)

# Função para exibir mensagens na tela
def exibir_mensagem(texto):
    mensagem = fonte.render(texto, True, (255, 255, 255))
    retangulo = mensagem.get_rect(center=(LARGURA // 2, ALTURA // 2))
    TELA.blit(mensagem, retangulo)

# Loop principal do jogo
rodando = True
temporizador = 60
clock = pygame.time.Clock()
tempo_inicial = pygame.time.get_ticks()

while rodando:
    TELA.blit(frame, (0, 0))

    # Atualiza o vídeo de fundo
    sucesso, frame = video.read()
    if sucesso:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
    else:
        video.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Reinicia o vídeo se acabar

    # Atualiza o tempo
    tempo_atual = pygame.time.get_ticks()
    segundos_passados = (tempo_atual - tempo_inicial) // 1000
    tempo_restante = max(60 - segundos_passados, 0)

    # Exibe o temporizador na tela
    texto_tempo = fonte.render(f"Tempo: {tempo_restante}", True, (255, 255, 255))
    TELA.blit(texto_tempo, (20, 20))

    # Verifica condições de vitória/derrota
    if tempo_restante == 0:
        exibir_mensagem("Eita, você perdeu :( Aperte espaço para iniciar novamente")
    elif False:  # Substitua pela lógica de vitória
        exibir_mensagem("Parabéns, você venceu! Aperte espaço para iniciar novamente")

    # Eventos do jogo
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
            tempo_inicial = pygame.time.get_ticks()  # Reinicia o tempo

    pygame.display.update()
    clock.tick(30)

pygame.quit()
sys.exit()
