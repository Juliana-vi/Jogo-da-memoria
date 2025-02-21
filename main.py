import cv2
import os
import pygame
import random


class Tile(pygame.sprite.Sprite):
    def __init__(self, filename, x, y):
        super().__init__()

        self.name = filename.split('.')[0]

        self.original_image = pygame.image.load('imagens/figs/'+ filename)

        self.back_image = pygame.image.load('imagens/figs/'+ filename)
        pygame.draw.rect(self.back_image, WHITE, self.back_image.get_rect())

        self.image = self.back_image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.shown = False

        def update(self):
        self.image = self.original_image if self.shown else self.back_image

    def mostrar(self):
        self.shown = True

    def esconder(self):
        self.shown = False

        class Game():
    def __init__(self):
        self.level = 1
        self.level_complete = False

        self.all_figs = [f for f in os.listdir('imagens/figs') if os.path.join('imagens/figs', f)]

        self.img_width, self.img_height = (128, 128)
        self.padding = 20
        self.margin_top = 160
        self.cols = 4
        self.rows = 2
        self.width = 1280

        self.tiles_group = pygame.sprite.Group()

        self.flipped = []
        self.frame_count = 0
        self.block_game = False

        self.generate_level(self.level)

        # iniciando o vídeo
        self.is_video_playing = True
        self.play = pygame.image.load('imagens/play2.png').convert_alpha()
        self.stop = pygame.image.load('imagens/pause2.png').convert_alpha()
        self.video_toggle = self.play
        self.video_toggle_rect = self.video_toggle.get_rect(topright=(WINDOW_WIDTH - 50, 10))
        self.get_video()

         # iniciando a música
        self.is_music_playing = True
        self.sound_on = pygame.image.load('imagens/sound2.png').convert_alpha()
        self.sound_off = pygame.image.load('imagens/mute2.png').convert_alpha()
        self.music_toggle = self.sound_on
        self.music_toggle_rect = self.music_toggle.get_rect(topright=(WINDOW_WIDTH - -1, 10))

        # carregando a música
        pygame.mixer.music.load('som/picnic.mp3')
        pygame.mixer.music.set_volume(.3)
        pygame.mixer.music.play()










        




