import cv2
import os
import pygame
import random

pygame.init()

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 860
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Jogo da Memória')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

FPS = 60
clock = pygame.time.Clock()

class Tile(pygame.sprite.Sprite):
    def __init__(self, filename, x, y):
        super().__init__()
        self.nome = filename 
        self.original_image = pygame.image.load(os.path.join('imagens/figs', filename))
        self.original_image = pygame.transform.scale(self.original_image, (160, 160))
        self.back_image = self.original_image.copy()
        pygame.draw.rect(self.back_image, WHITE, self.back_image.get_rect())
        
        self.image = self.back_image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.shown = False
    
    def esconder(self):
        self.image = self.back_image  
        self.shown = False

class Game:
    def __init__(self):
        self.level = 1
        self.level_complete = False
        self.all_figs = [f for f in os.listdir('imagens/figs') if f.endswith(('.png', '.jpg'))]
        self.img_width, self.img_height = 160, 160
        self.padding = 15
        self.margin_top = 250
        self.cols = 4
        self.rows = 2
        self.tiles_group = pygame.sprite.Group()
        self.flipped = []
        self.frame_count = 0
        self.block_game = False
        self.game_over = False
        self.timer = 60
        
        self.generate_level(self.level)
        
        self.is_video_playing = True
        self.get_video()

    def update(self, event_list):
        if self.is_video_playing:
            self.success, self.img = self.cap.read()

        self.user_input(event_list)
        self.check_level_complete()
        self.draw()

    def generate_level(self, level):
        self.figs = self.select_random_figs(level)
        self.rows = level + 1
        self.cols = max(4, self.rows)
        self.generate_tileset(self.figs)

    def generate_tileset(self, figs):
        self.tiles_group.empty()
        left_margin = (WINDOW_WIDTH - (self.img_width * self.cols + self.padding * (self.cols - 1))) // 2
        for i, fig in enumerate(figs):
            x = left_margin + (self.img_width + self.padding) * (i % self.cols)
            y = self.margin_top + (i // self.cols) * (self.img_height + self.padding)
            self.tiles_group.add(Tile(fig, x, y))

    def select_random_figs(self, level):
        figs = random.sample(self.all_figs, level * 2) * 2
        random.shuffle(figs)
        return figs

    def user_input(self, event_list):
        for event in event_list:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    def draw(self):
        screen.fill(BLACK)
        
        if self.is_video_playing and self.success:
            video_surface = pygame.image.frombuffer(self.img.tobytes(), self.shape, 'BGR')
            video_surface = pygame.transform.scale(video_surface, (WINDOW_WIDTH, WINDOW_HEIGHT))
            screen.blit(video_surface, (0, 0))
        
        self.tiles_group.draw(screen)
        pygame.display.update()

    def get_video(self):
        self.cap = cv2.VideoCapture('video/nuvem.mp4')
        if not self.cap.isOpened():
            print("Erro ao abrir o vídeo.")
            self.is_video_playing = False  
        else:
            self.success, self.img = self.cap.read()
            if self.success:
                self.shape = self.img.shape[1::-1]

if not os.path.exists('imagens/figs'):
    print("Pasta 'imagens/figs' não encontrada.")
if not os.path.exists('video/nuvem.mp4'):
    print("Vídeo 'nuvem.mp4' não encontrado.")

game = Game()

running = True
while running:
    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            running = False

    game.update(event_list)
    clock.tick(FPS)

pygame.quit()

