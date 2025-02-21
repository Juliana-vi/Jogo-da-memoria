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

        self.original_image = pygame.image.load(os.path.join('imagens/figs', filename))
        self.back_image = self.original_image.copy()
        pygame.draw.rect(self.back_image, WHITE, self.back_image.get_rect())

        self.image = self.back_image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.shown = False

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
        self.width = 1280
        self.width = WINDOW_WIDTH
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

    def update(self, event_list):
        if self.is_video_playing:
            self.success, self.img = self.cap.read()

        self.user_input(event_list)
        self.draw()
        self.check_level_complete(event_list)

    def check_level_complete(self, event_list):
        if not self.block_game:
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
             if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.music_toggle_rect.collidepoint(pygame.mouse.get_pos()):
                    if self.is_music_playing:
                        self.is_music_playing = False
                        self.music_toggle = self.sound_off
                        pygame.mixer.music.pause()
                    else:
                        self.is_music_playing = True
                        self.music_toggle = self.sound_on
                        pygame.mixer.music.unpause()
                if self.video_toggle_rect.collidepoint(pygame.mouse.get_pos()):
                    if self.is_video_playing:
                        self.is_video_playing = False
                        self.video_toggle = self.stop
                    else:
                        self.is_video_playing = True
                        self.video_toggle = self.play

             if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.level_complete:
                    self.level += 1
                    if self.level >= 6:
                        self.level = 1
                    self.generate_level(self.level)

        def draw(self):
         screen.fill(BLACK)

        title_font = pygame.font.Font('fonte/font.ttf', 44)
        content_font = pygame.font.Font('fonte/font.ttf', 24)

        self.title_text = title_font.render('Jogo da Memória', True, WHITE)
        self.title_rect = self.title_text.get_rect(midtop=(WINDOW_WIDTH // 2, 10))

        self.level_text = content_font.render('Fase ' + str(self.level), True, WHITE)
        self.level_rect = self.level_text.get_rect(midtop=(WINDOW_WIDTH // 2, 80))

        self.info_text = content_font.render('Encontre as figurinhas semelhantes', True, BLACK)
        self.info_rect = self.info_text.get_rect(midtop=(WINDOW_WIDTH // 2, 120))

        if self.is_video_playing:
            if self.success:
                screen.blit(pygame.image.frombuffer(self.img.tobytes(), self.shape, 'BGR'), (0, 120))
            else:
                self.get_video()
        else:
            screen.blit(pygame.image.frombuffer(self.img.tobytes(), self.shape, 'BGR'), (0, 120))

        if self.game_over:
            game_over_text = content_font.render('Eita, você perdeu :( Aperte espaço para iniciar novamente', True, BLACK)
            game_over_rect = game_over_text.get_rect(midbottom=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 40))
            screen.blit(game_over_text, game_over_rect)

        elif self.level_complete:
            if self.level != 5:
                next_text = content_font.render('Fase concluída. Aperte Espaço para próxima fase!', True, BLACK)
            else:
                next_text = content_font.render('Parabéns, você venceu!!! Aperte espaço para iniciar novamente', True, BLACK)
            next_rect = next_text.get_rect(midbottom=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 40))
            screen.blit(next_text, next_rect)

    def check_loss(self):
        if self.timer <= 0 or self.some_loss_condition:
            self.game_over = True

    def update(self, event_list):
        if self.game_over:
            for event in event_list:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.restart_game()
            return
        
        self.timer -= 1 / 60
        if self.timer <= 0:
            self.game_over = True

    def restart_game(self):
        self.level = 1
        self.game_over = False
        self.timer = 60 
        self.generate_level(self.level)

    def start_level(self):
        self.timer = 60

        screen.blit(self.title_text, self.title_rect)
        screen.blit(self.level_text, self.level_rect)
        screen.blit(self.info_text, self.info_rect)
        pygame.draw.rect(screen, BLACK, (WINDOW_WIDTH - 110, 0, 130, 70))
        screen.blit(self.video_toggle, self.video_toggle_rect)
        screen.blit(self.music_toggle, self.music_toggle_rect)
        self.tiles_group.draw(screen)
        self.tiles_group.update()
    
    def get_video(self):
        self.cap = cv2.VideoCapture('video/nuvem.mp4')
        self.success, self.img = self.cap.read()
        self.shape = self.img.shape[1::-1]

pygame.init()
game = Game()
if game.level_complete:
    message = "Parabéns, você venceu!!! Aperte espaço para iniciar novamente" if game.level == 6 else "Fase concluída! Aperte espaço para a próxima fase"
    text = game.font.render(message, True, WHITE)
    screen.blit(text, text.get_rect(midbottom=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 40)))

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 860
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Jogo da memoria')

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

FPS = 60
clock = pygame.time.Clock()
if hasattr(game, 'game_over') and Game.game_over:
            text = game.font.render("Eita, você perdeu :( Aperte espaço para iniciar novamente", True, WHITE)
            screen.blit(text, text.get_rect(midbottom=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 40)))

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


















           


