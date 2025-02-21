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
        self.back_image = pygame.Surface(self.original_image.get_size())
        self.back_image.fill(WHITE)

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
        self.timer = 60  
        self.last_tick = pygame.time.get_ticks()

        self.background = pygame.image.load('imagens/background.jpg').convert()
        
        self.generate_level()
        
        self.is_video_playing = True
        self.play = pygame.image.load('imagens/play2.png').convert_alpha()
        self.stop = pygame.image.load('imagens/pause2.png').convert_alpha()
        self.video_toggle = self.play
        self.video_toggle_rect = self.video_toggle.get_rect(topright=(WINDOW_WIDTH - 50, 10))
        self.get_video()

        self.is_music_playing = True
        self.sound_on = pygame.image.load('imagens/sound2.png').convert_alpha()
        self.sound_off = pygame.image.load('imagens/mute2.png').convert_alpha()
        self.music_toggle = self.sound_on
        self.music_toggle_rect = self.music_toggle.get_rect(topright=(WINDOW_WIDTH - 100, 10))

        pygame.mixer.music.load('som/picnic.mp3')
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play()

        self.title_font = pygame.font.Font('fonte/font.ttf', 44)
        self.content_font = pygame.font.Font('fonte/font.ttf', 24)

    def generate_level(self):
        self.tiles_group.empty()
        selected_figs = random.sample(self.all_figs, self.cols * self.rows // 2) * 2
        random.shuffle(selected_figs)

        for row in range(self.rows):
            for col in range(self.cols):
                x = col * (self.img_width + self.padding) + (WINDOW_WIDTH - (self.cols * (self.img_width + self.padding))) // 2
                y = row * (self.img_height + self.padding) + self.margin_top
                tile = Tile(selected_figs.pop(), x, y)
                self.tiles_group.add(tile)

    def update(self, event_list):
        if self.is_video_playing and hasattr(self, 'cap'):
            self.success, self.img = self.cap.read()

        self.user_input(event_list)
        self.update_timer()
        self.check_level_complete()
        self.draw()

    def user_input(self, event_list):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                for tile in self.tiles_group:
                    if tile.rect.collidepoint(pos) and not tile.shown:
                        tile.image = tile.original_image
                        tile.shown = True
                        self.flipped.append(tile)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and (self.game_over or self.level_complete):
                    self.__init__()

    def update_timer(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_tick >= 1000:
            self.timer -= 1
            self.last_tick = current_time
            if self.timer <= 0:
                self.game_over = True

    def check_level_complete(self):
        if not self.block_game and len(self.flipped) == 2:
            if self.flipped[0].nome != self.flipped[1].nome:
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

    def draw(self):
        screen.blit(self.background, (0, 0))
        screen.blit(self.title_font.render('Jogo da Memória', True, WHITE), (WINDOW_WIDTH // 2 - 100, 10))
        screen.blit(self.content_font.render(f'Fase {self.level}', True, WHITE), (WINDOW_WIDTH // 2 - 50, 80))
        screen.blit(self.content_font.render(f'Tempo: {self.timer}', True, WHITE), (50, 50))

        if self.is_video_playing and self.success:
            screen.blit(pygame.image.frombuffer(self.img.tobytes(), self.shape, 'BGR'), (0, 120))

        screen.blit(self.video_toggle, self.video_toggle_rect)
        screen.blit(self.music_toggle, self.music_toggle_rect)
        self.tiles_group.draw(screen)

        if self.level_complete and not self.game_over:
            self.display_message("Fase concluída! Aperte espaço para a próxima fase")
        elif self.game_over:
            if self.level_complete:
                self.display_message("Parabéns, você venceu! Aperte espaço para iniciar novamente")
            else:
                self.display_message("Eita, você perdeu :( Aperte espaço para iniciar novamente")

    def get_video(self):
        self.cap = cv2.VideoCapture('video/nuvem.mp4')
        if not self.cap.isOpened():
            print("Erro ao abrir o vídeo.")
            self.is_video_playing = False
        else:
            self.success, self.img = self.cap.read()
            if self.success:
                self.shape = self.img.shape[1::-1]

    def display_message(self, message):
        message_text = self.content_font.render(message, True, WHITE)
        screen.blit(message_text, (WINDOW_WIDTH // 2 - message_text.get_width() // 2, WINDOW_HEIGHT - 100))

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
