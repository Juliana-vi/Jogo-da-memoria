import cv2
import os
import pygame
import random
import time

def show_opening_screen():
    cap = cv2.VideoCapture('video/clouds.mp4')
    success, img = cap.read()
    shape = img.shape[1::-1]

    waiting = True
    while waiting:
        if success:
            screen.blit(pygame.image.frombuffer(img.tobytes(), shape, 'BGR'), (0, 0))
        else:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            success, img = cap.read()
            continue

        title_font = pygame.font.Font('fonte/font.ttf', 64)
        content_font = pygame.font.Font('fonte/font.ttf', 32)
        objective_font = pygame.font.Font('fonte/font.ttf', 24)

        title_text = title_font.render('Jogo da Memória', True, WHITE)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 150))

        start_text = content_font.render('Pressione ENTER para começar', True, WHITE)
        start_rect = start_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))

        objective_text = objective_font.render('OBJETIVO: Encontrar todos os pares escondidos das figurinhas antes que o tempo acabe', True, WHITE)
        objective_rect = objective_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))

        screen.blit(title_text, title_rect)
        screen.blit(start_text, start_rect)
        screen.blit(objective_text, objective_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False

        success, img = cap.read()

def show_victory_screen():
    cap = cv2.VideoCapture('video/clouds.mp4')
    success, img = cap.read()
    shape = img.shape[1::-1]

    waiting = True
    while waiting:
        if success:
            screen.blit(pygame.image.frombuffer(img.tobytes(), shape, 'BGR'), (0, 0))
        else:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            success, img = cap.read()
            continue

        title_font = pygame.font.Font('fonte/font.ttf', 64)
        content_font = pygame.font.Font('fonte/font.ttf', 32)

        title_text = title_font.render('Parabéns, você venceu!', True, WHITE)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 200))

        image = pygame.image.load('imagens/fig1-128x128.png')
        image = pygame.transform.scale(image, (256, 256))
        image_rect = image.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))

        restart_text = content_font.render('Aperte espaço para iniciar novamente', True, WHITE)
        restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 200))

        screen.blit(title_text, title_rect)
        screen.blit(image, image_rect)
        screen.blit(restart_text, restart_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False

        success, img = cap.read()

def show_defeat_screen():
    cap = cv2.VideoCapture('video/clouds.mp4')
    success, img = cap.read()
    shape = img.shape[1::-1]

    waiting = True
    while waiting:
        if success:
            screen.blit(pygame.image.frombuffer(img.tobytes(), shape, 'BGR'), (0, 0))
        else:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            success, img = cap.read()
            continue

        title_font = pygame.font.Font('fonte/font.ttf', 64)
        content_font = pygame.font.Font('fonte/font.ttf', 32)

        title_text = title_font.render('Eita, você perdeu :(', True, WHITE)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 200))

        image = pygame.image.load('imagens/figs/fig12-128x128.jpg')
        image = pygame.transform.scale(image, (256, 256))
        image_rect = image.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))

        restart_text = content_font.render('Aperte espaço para iniciar novamente', True, WHITE)
        restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 200))

        screen.blit(title_text, title_rect)
        screen.blit(image, image_rect)
        screen.blit(restart_text, restart_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False

        success, img = cap.read()

def show_level_complete_screen():
    cap = cv2.VideoCapture('video/clouds.mp4')
    success, img = cap.read()
    shape = img.shape[1::-1]

    waiting = True
    while waiting:
        if success:
            screen.blit(pygame.image.frombuffer(img.tobytes(), shape, 'BGR'), (0, 0))
        else:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            success, img = cap.read()
            continue

        title_font = pygame.font.Font('fonte/font.ttf', 64)
        content_font = pygame.font.Font('fonte/font.ttf', 32)

        title_text = title_font.render('Fase concluída!', True, WHITE)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 150))

        next_text = content_font.render('Aperte espaço para a próxima fase', True, WHITE)
        next_rect = next_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))

        screen.blit(title_text, title_rect)
        screen.blit(next_text, next_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False

        success, img = cap.read()

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

class Game():
    def __init__(self):
        self.level = 1
        self.level_complete = False
        self.time_left = 60
        self.start_time = time.time()

        # figs
        self.all_figs = [f for f in os.listdir('imagens/figs') if os.path.join('imagens/figs', f)]

        self.img_width, self.img_height = (128, 128)
        self.padding = 20
        self.margin_top = 200
        self.cols = 4
        self.rows = 2
        self.width = 1280

        self.tiles_group = pygame.sprite.Group()

        self.flipped = []
        self.frame_count = 0
        self.block_game = False

        # gerar nivel 1
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
        self.music_toggle_rect = self.music_toggle.get_rect(topright=(WINDOW_WIDTH - 50, 10))

        # Carregando a música
        pygame.mixer.music.load('som/picnic.mp3')
        pygame.mixer.music.set_volume(.3)
        pygame.mixer.music.play(-1)

    def update(self, event_list):
        if self.is_video_playing:
            self.success, self.img = self.cap.read()

        self.user_input(event_list)
        self.draw()
        self.check_level_complete(event_list)
        self.update_timer()

    def update_timer(self):
        elapsed_time = time.time() - self.start_time
        self.time_left = self.initial_time - int(elapsed_time)
        if self.time_left <= 0:
            self.time_left = 0
            self.level_complete = True
            self.show_defeat_message()

    def show_defeat_message(self):
        self.level_complete = True
        self.block_game = True
        show_defeat_screen()
        self.reset_game()

    def show_victory_message(self):
        self.level_complete = True
        self.block_game = True
        show_victory_screen()
        self.reset_game()

    def show_level_complete_message(self):
        self.level_complete = True
        self.block_game = True
        show_level_complete_screen()
        self.level += 1
        self.generate_level(self.level)

    def reset_game(self):
        self.level = 1
        self.generate_level(self.level)
        self.start_time = time.time()
        self.block_game = False

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
                                        if not tile.shown:
                                            self.level_complete = False
                                            break
                                    else:
                                        self.level_complete = True
                                        self.show_level_complete_message()
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
        self.figs = self.select_random_figs(level)
        self.level_complete = False
        self.rows = level + 1
        self.cols = 4
        self.generate_tileset(self.figs)
        self.start_time = time.time()

        if level == 1:
            self.initial_time = 20
        elif level == 2:
            self.initial_time = 30
        elif level == 3:
            self.initial_time = 45
        elif level == 4:
            self.initial_time = 60
        else:
            self.initial_time = 80

    def generate_tileset(self, figs):
        self.cols = self.rows = self.cols if self.cols >= self.rows else self.rows

        TILES_WIDTH = (self.img_width * self.cols + self.padding * 3)
        LEFT_MARING = RIGHT_MARGIN = (self.width - TILES_WIDTH) // 2

        self.tiles_group.empty()

        for i in range(len(figs)):
            x = LEFT_MARING + ((self.img_width + self.padding) * (i % self.cols))
            y = self.margin_top + (i // self.rows * (self.img_height + self.padding))
            tile = Tile(figs[i], x, y)
            self.tiles_group.add(tile)

    def select_random_figs(self, level):
        figs = random.sample(self.all_figs, (level + level + 2))
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

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.level_complete:
                    if self.time_left == 0:
                        self.show_defeat_message()
                    else:
                        if self.level >= 6:
                            self.show_victory_message()
                        else:
                            self.show_level_complete_message()

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

        info_text = content_font.render('Encontre as figurinhas semelhantes', True, WHITE)
        info_rect = info_text.get_rect(midtop=(WINDOW_WIDTH // 2, 120))

        timer_text = content_font.render(f'Tempo restante: {self.time_left} segundos', True, WHITE)
        timer_rect = timer_text.get_rect(topleft=(10, 120))

        screen.blit(title_text, title_rect)
        screen.blit(level_text, level_rect)
        screen.blit(info_text, info_rect)
        screen.blit(timer_text, timer_rect)

        if self.is_video_playing:
            if self.success:
                screen.blit(pygame.image.frombuffer(self.img.tobytes(), self.shape, 'BGR'), (0, 160))
            else:
                self.get_video()
        else:
            screen.blit(pygame.image.frombuffer(self.img.tobytes(), self.shape, 'BGR'), (0, 160))

        pygame.draw.rect(screen, BLACK, (WINDOW_WIDTH - 110, 0, 130, 70))
        screen.blit(self.video_toggle, self.video_toggle_rect)
        screen.blit(self.music_toggle, self.music_toggle_rect)

        self.tiles_group.draw(screen)
        self.tiles_group.update()

    def get_video(self):
        self.cap = cv2.VideoCapture('video/clouds.mp4')
        self.success, self.img = self.cap.read()
        self.shape = self.img.shape[1::-1]


pygame.init()

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 860
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Jogo da Memória')

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

FPS = 60
clock = pygame.time.Clock()

show_opening_screen()

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