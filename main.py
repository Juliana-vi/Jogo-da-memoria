import cv2
import os
import pygame
import random


class Tile(pygame.sprite.Sprite):
    def __init__(self, filename, x, y):
        super().__init__()

        self.name = filename.split('.')[0]

        self.original_image = pygame.image.load('imagens/figs/' + filename)

        self.back_image = pygame.image.load('imagens/figs/' + filename)
        pygame.draw.rect(self.back_image, WHITE, self.back_image.get_rect())

        self.image = self.back_image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.shown = False

    def update(self):
        self.image = self.original_image if self.shown else self.back_image

    def show(self):
        self.shown = True

    def hide(self):
        self.shown = False

def format_time(seconds):
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:02}:{seconds:02}"

class Game():
    def __init__(self):
        self.level = 1
        self.level_complete = False
        self.time_left = 100  
        self.last_time_update = pygame.time.get_ticks()
        self.game_over = False
        self.is_video_playing = True
        self.img = None

        # figs
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

        # gerar nivel 1
        self.generate_level(self.level)
        self.play_video('video/intro.mp4')

    def play_video(self, video_path):
        cap = cv2.VideoCapture(video_path)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.img = frame
            frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            screen.blit(frame_surface, (0, 0))
            pygame.display.update()
            if pygame.event.get(pygame.QUIT):
                cap.release()
                pygame.quit()
                exit()
        cap.release()
        self.is_video_playing = False

    def update_timer(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_time_update >= 1000:
            self.last_time_update = current_time
            if self.time_left > 0:
                self.time_left -= 1
            else:
                self.game_over = True
                self.level_complete = False

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

        # Carregando a música
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
            for event in event_list:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for tile in self.tiles_group:
                        if tile.rect.collidepoint(event.pos):
                            self.flipped.append(tile.name)
                            tile.show()
                            if len(self.flipped) == 2:
                                if self.flipped[0] != self.flipped[1]:
                                    self.block_game = True
                                else:
                                    self.flipped = []
                                    for tile in self.tiles_group:
                                        if tile.shown:
                                            self.level_complete = True
                                        else:
                                            self.level_complete = False
                                            break
        else:
            self.frame_count += 1
            if self.frame_count == FPS:
                self.frame_count = 0
                self.block_game = False

                for tile in self.tiles_group:
                    if tile.name in self.flipped:
                        tile.hide()
                self.flipped = []

    def generate_level(self, level):
        self.figs = self.select_random_figs(self.level)
        self.level_complete = False
        self.time_left = 100 
        self.game_over = False 
        self.rows = self.level + 1
        self.cols = 4
        self.generate_tileset(self.figs)

    def generate_tileset(self, figs):
        self.cols = self.rows = self.cols if self.cols >= self.rows else self.rows

        TILES_WIDTH = (self.img_width * self.cols + self.padding * 3)
        LEFT_MARING = RIGHT_MARGIN = (self.width - TILES_WIDTH) // 2
        # tiles = []
        self.tiles_group.empty()

        for i in range(len(figs)):
            x = LEFT_MARING + ((self.img_width + self.padding) * (i % self.cols))
            y = self.margin_top + (i // self.rows * (self.img_height + self.padding))
            tile = Tile(figs[i], x, y)
            self.tiles_group.add(tile)

    def select_random_figs(self, level):
        figs = random.sample(self.all_figs, (self.level + self.level + 2))
        figs_copy = figs.copy()
        figs.extend(figs_copy)
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

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if self.level_complete or self.game_over:
                    self.level = 1 if self.level >= 6 else self.level + 1
                    self.generate_level(self.level)
                    self.play_video('video/next_level.mp4')


    def draw(self):
        screen.fill(BLACK)

        # fonte
        title_font = pygame.font.Font('fonte/font.ttf', 44)
        content_font = pygame.font.Font('fonte/font.ttf', 24)

        # texto
        title_text = title_font.render('Jogo da Memória', True, WHITE)
        title_rect = title_text.get_rect(midtop=(WINDOW_WIDTH // 2, 10))

        level_text = content_font.render('Fase ' + str(self.level), True, WHITE)
        level_rect = level_text.get_rect(midtop=(WINDOW_WIDTH // 2, 80))

        info_text = content_font.render('Encontre os animais semelhantes', True, WHITE)
        info_rect = info_text.get_rect(midtop=(WINDOW_WIDTH // 2, 120))

        timer_text = content_font.render(f'Tempo: {format_time(self.time_left)}', True, WHITE)
        timer_rect = timer_text.get_rect(midtop=(WINDOW_WIDTH // 2, 120))
        screen.blit(timer_text, timer_rect)

        if self.img is not None:
            screen.blit(pygame.image.frombuffer(self.img.tobytes(), self.img.shape[1::-1], "BGR"), (0, 120))

        if self.is_video_playing:
            if self.success:
                screen.blit(pygame.image.frombuffer(self.img.tobytes(), self.shape, 'BGR'), (0, 120))
            else:
                self.get_video()
        else:
            screen.blit(pygame.image.frombuffer(self.img.tobytes(), self.shape, 'BGR'), (0, 120))

        if not self.level == 5:
            next_text = content_font.render('Fase concluída. Aperte Espaço para próxima fase!', True, WHITE)
        else:
            next_text = content_font.render('Parabéns, você venceu!!! Aperte espaço para iniciar novamente', True, WHITE)
        next_rect = next_text.get_rect(midbottom=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 40))

        screen.blit(title_text, title_rect)
        screen.blit(level_text, level_rect)
        screen.blit(info_text, info_rect)
        pygame.draw.rect(screen, BLACK, (WINDOW_WIDTH - 110, 0, 130, 70))
        screen.blit(self.video_toggle, self.video_toggle_rect)
        screen.blit(self.music_toggle, self.music_toggle_rect)

        self.tiles_group.draw(screen)
        self.tiles_group.update()

        if self.level_complete:
            msg = 'Parabéns, você venceu! Aperte espaço para iniciar novamente' if self.level == 5 else 'Fase concluída. Aperte Espaço para próxima fase!'
            next_text = content_font.render(msg, True, WHITE)
            next_rect = next_text.get_rect(midbottom=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 40))
            screen.blit(next_text, next_rect)
        
        if self.game_over:
            lose_text = content_font.render('Eita, você perdeu :( Aperte espaço para iniciar novamente', True, WHITE)
            lose_rect = lose_text.get_rect(midbottom=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 40))
            screen.blit(lose_text, lose_rect)

    def get_video(self):
        self.cap = cv2.VideoCapture('video/clouds.mp4')
        self.success, self.img = self.cap.read()
        self.shape = self.img.shape[1::-1]


pygame.init()

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 860
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Memory Game')

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

FPS = 60
clock = pygame.time.Clock()

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