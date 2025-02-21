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

