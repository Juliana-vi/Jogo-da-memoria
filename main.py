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
        self.nome = filename.split('.')[0]
        self.original_image = pygame.image.load(os.path.join('imagens/figs', filename))
        self.back_image = self.original_image.copy()
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
        self.generate_level(self.level)
        self.is_music_playing = True
        pygame.mixer.music.load('som/picnic.mp3')
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

    def update(self, event_list):
        self.user_input(event_list)
        self.check_level_complete(event_list)
        self.tiles_group.update()
        self.draw()

    def check_level_complete(self, event_list):
        if not self.block_game:
            for event in event_list:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for tile in self.tiles_group:
                        if tile.rect.collidepoint(event.pos):
                            self.flipped.append(tile.nome)
                            tile.mostrar()
                            if len(self.flipped) == 2:
                                if self.flipped[0] != self.flipped[1]:
                                    self.block_game = True
                                else:
                                    self.flipped.clear()
                                    self.level_complete = all(tile.shown for tile in self.tiles_group)
        else:
            self.frame_count += 1
            if self.frame_count == FPS:
                self.frame_count = 0
                self.block_game = False
                for tile in self.tiles_group:
                    if tile.nome in self.flipped:
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
        figs = random.sample(self.all_figs, level * 2)
        figs *= 2
        random.shuffle(figs)
        return figs

    def user_input(self, event_list):
        for event in event_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.level_complete:
                    self.level = 1 if self.level > 5 else self.level + 1
                    self.generate_level(self.level)

    def draw(self):
        screen.fill(BLACK)
        font = pygame.font.Font('fonte/font.ttf', 44)
        text = font.render(f'Jogo da Memória - Fase {self.level}', True, WHITE)
        screen.blit(text, text.get_rect(midtop=(WINDOW_WIDTH // 2, 20)))
        self.tiles_group.draw(screen)

        if self.level_complete:
            message = "Parabéns, você venceu!!! Aperte espaço para iniciar novamente" if self.level == 6 else "Fase concluída! Aperte espaço para a próxima fase"
            text = font.render(message, True, WHITE)
            screen.blit(text, text.get_rect(midbottom=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 40)))

        if hasattr(self, 'game_over') and self.game_over:
            text = font.render("Eita, você perdeu :( Aperte espaço para iniciar novamente", True, WHITE)
            screen.blit(text, text.get_rect(midbottom=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 40)))

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
