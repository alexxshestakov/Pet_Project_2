import pygame
from pygame.sprite import Sprite
 
class Bullet(Sprite):
    """Класс для управления пулями, выпущенными с корабля"""

    def __init__(self, ai_game):
        """Cоздание обьекта пули"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # позиционированние пули
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
            self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop
        
        # десятичная величина позиционирования
        self.y = float(self.rect.y)

    def update(self):
        """движение пули"""
        # обновление положения
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        """отрисовка пули"""
        pygame.draw.rect(self.screen, self.color, self.rect)
