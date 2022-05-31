import pygame
from pygame.sprite import Sprite
 
class Alien(Sprite):
    """Класс, представляющий инопланетянина во флоте"""

    def __init__(self, ai_game):
        """Инициализция инопланетянина и установка его начального положения"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Закгрузка изображения инопланетянина
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # добавление нового прешельца в левый верхний угол
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #  горизонтальное положение инопланетянина
        self.x = float(self.rect.x)

    def check_edges(self):
        """Возвращает значение True, если прешелец находится на краю экрана"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        """движение прешельца в лево или право"""
        self.x += (self.settings.alien_speed *
                        self.settings.fleet_direction)
        self.rect.x = self.x
