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
        self.nome = filename  # Definir nome para referência
        self.original_image = pygame.image.load(os.path.join('imagens/figs', filename))
        self.back_image = self.original_image.copy()
        pygame.draw.rect(self.back_image, WHITE, self.back_image.get_rect())

        self.image = self.back_image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.shown = False

    def esconder(self):
        self.image = self.back_image  # Esconder a peça corretamente
        self.shown = False


class Game:
    def __init__(self):
        self.level = 1
        self.level_complete = False
        self.all_figs = [f for f in os.listdir('imagens/figs') if f.endswith(('.png', '.jpg'))]
        self.img_width, self.img_height = 128, 128
        self.padding = 20
        self.margin_top = 160
        self.cols = 4
        self.rows = 2
        self.width = WINDOW_WIDTH
        self.tiles_group = pygame.sprite.Group()
        self.flipped = []
        self.frame_count = 0
        self.block_game = False
        self.game_over = False
        self.timer = 60  # Tempo do jogo

        self.generate_level(self.level)

        # Iniciando o vídeo
        self.is_video_playing = True
        self.play = pygame.image.load('imagens/play2.png').convert_alpha()
        self.stop = pygame.image.load('imagens/pause2.png').convert_alpha()
        self.video_toggle = self.play
        self.video_toggle_rect = self.video_toggle.get_rect(topright=(WINDOW_WIDTH - 50, 10))
        self.get_video()

        # Iniciando a música
        self.is_music_playing = True
        self.sound_on = pygame.image.load('imagens/sound2.png').convert_alpha()
        self.sound_off = pygame.image.load('imagens/mute2.png').convert_alpha()
        self.music_toggle = self.sound_on
        self.music_toggle_rect = self.music_toggle.get_rect(topright=(WINDOW_WIDTH - 100, 10))

        # Carregando a música
        pygame.mixer.music.load('som/picnic.mp3')
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play()

        # Carregar fontes
        self.title_font = pygame.font.Font('fonte/font.ttf', 44)
        self.content_font = pygame.font.Font('fonte/font.ttf', 24)

    def update(self, event_list):
        if self.is_video_playing:
            self.success, self.img = self.cap.read()

        self.user_input(event_list)
        self.check_level_complete()
        self.draw()

    def check_level_complete(self):
        if not self.block_game and len(self.flipped) == 2:
            if self.flipped[0] != self.flipped[1]:
                self.block_game = True
            else:
                self.flipped.clear()
                self.level_complete = all(tile.shown for tile in self.tiles_group)
        elif self.block_game:
            self.frame_count += 1
            if self.frame_count == FPS:
                self.frame_count = 0
                self.block_game = False
                for tile in self.tiles_group:
                    tile.esconder()
                self.flipped.clear()

    def generate_level(self, level):
        self.figs = self.select_random_figs(level)
        self.level_complete = False
        self.rows = level + 1
        self.cols = max(4, self.rows)
        self.generate_tileset(self.figs)

    def generate_tileset(self, figs):
        self.tiles_group.empty()
        left_margin = (self.width - (self.img_width * self.cols + self.padding * (self.cols - 1))) // 2
        for i, fig in enumerate(figs):
            x = left_margin + (self.img_width + self.padding) * (i % self.cols)
            y = self.margin_top + (i // self.cols * (self.img_height + self.padding))
            self.tiles_group.add(Tile(fig, x, y))

    def select_random_figs(self, level):
        figs = random.sample(self.all_figs, level * 2) * 2
        random.shuffle(figs)
        return figs

    def user_input(self, event_list):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.music_toggle_rect.collidepoint(pygame.mouse.get_pos()):
                    self.is_music_playing = not self.is_music_playing
                    self.music_toggle = self.sound_on if self.is_music_playing else self.sound_off
                    pygame.mixer.music.pause() if not self.is_music_playing else pygame.mixer.music.unpause()

                if self.video_toggle_rect.collidepoint(pygame.mouse.get_pos()):
                    self.is_video_playing = not self.is_video_playing
                    self.video_toggle = self.play if self.is_video_playing else self.stop

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and self.level_complete:
                self.level = 1 if self.level >= 6 else self.level + 1
                self.generate_level(self.level)

    def draw(self):
        screen.fill(BLACK)

        screen.blit(self.title_font.render('Jogo da Memória', True, WHITE), (WINDOW_WIDTH // 2 - 100, 10))
        screen.blit(self.content_font.render(f'Fase {self.level}', True, WHITE), (WINDOW_WIDTH // 2 - 50, 80))

        if self.is_video_playing and self.success:
            screen.blit(pygame.image.frombuffer(self.img.tobytes(), self.shape, 'BGR'), (0, 120))

        screen.blit(self.video_toggle, self.video_toggle_rect)
        screen.blit(self.music_toggle, self.music_toggle_rect)

        self.tiles_group.draw(screen)

    def get_video(self):
        self.cap = cv2.VideoCapture('video/nuvem.mp4')
        self.success, self.img = self.cap.read()
        if self.success:
            self.shape = self.img.shape[1::-1]


game = Game()

running = True
while running:
    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            running = False

    game.update(event_list)
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()