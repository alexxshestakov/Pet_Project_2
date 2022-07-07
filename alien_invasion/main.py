import sys
from time import sleep
import pygame
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    """общий класс для управления игрой"""

    def __init__(self):
        """инициализация игры"""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        # создание статистики
        #   и создание таблицы со статистикой
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # кнопка запуска игры
        self.play_button = Button(self, "Play")

    def run_game(self):
        """главный игровой цикл"""

        # clock = pygame.time.Clock()  # попытка использовать Clock для решения проблемы с замедлением
        while True:
            # clock.tick(60)  # попытка использовать Clock для решения проблемы с замедлением
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    def _check_events(self):
        """Обработка событий"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Начало новой игры при нажатии Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # сброс старых динамических настроек
            self.settings.initialize_dynamic_settings()

            # сброс статистики
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # удаление пришельцев и пуль
            self.aliens.empty()
            self.bullets.empty()

            # создание нового флота и корабля (истребителя)
            self._create_fleet()
            self.ship.center_ship()

            # скрываем курсор
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """обработка нажатия на клавиатуре"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self.settings.alien_speed += 0.1
        elif event.key == pygame.K_DOWN:
            if self.settings.alien_speed > 0.1:
                self.settings.alien_speed -= 0.1
        elif event.key == pygame.K_ESCAPE:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """обработка отжатия на клавиатуре"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """создание дополнительных пуль"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """обновление позиционирования пуль"""

        self.bullets.update()

        # удаление пуль вышедших за предел экрана.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """проверка встречи пули и пришельца"""
        # удаление пули и пришельца которые встретились.
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # если не осталось флота приельцев создаем новый флот
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # ... и повышаем уровень игры
            self.stats.level += 1
            self.sb.prep_level()

    def _update_aliens(self):
        """
        проверка позиционирования флота
        """
        self._check_fleet_edges()
        self.aliens.update()

        # проверка встречи флота с кораблем.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # проверка встречи флота с нижней границей экрана.
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        """проверка встречи флота с нижней границей экрана"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _ship_hit(self):
        """касание корабля флотом"""
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()

            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _create_fleet(self):
        """создание флота"""

        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # определяем колличество рядов пришельцев
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                             (4 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Создаем инопланетянина и помещаем его в ряд"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = 2*alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """проверки на касание граней для флота"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """изменение направления движения флота"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """обновление отображения"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        self.sb.show_score()

        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()


if __name__ == '__main__':
    # запуск игры.
    ai = AlienInvasion()
    ai.run_game()
