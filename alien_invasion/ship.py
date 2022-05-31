import pygame
 
from pygame.sprite import Sprite
 
class Ship(Sprite):
    """класс корабля"""
 
    def __init__(self, ai_game):
        """инициализация обьекта и позиционирование"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        # загрузка изображения
        self.image = pygame.image.load('images/su57__.bmp')
        self.rect = self.image.get_rect()
        # позиционирование
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        # флаги для движения
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """движение/изменение положения"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        self.rect.x = self.x

    def blitme(self):
        """отрисовка корабля в актуальном положении"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """позициониование в центре"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
