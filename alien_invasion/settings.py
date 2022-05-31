class Settings:
    """класс настроек игры"""

    def __init__(self):
        """Инициализация игровой статистики"""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 500
        self.bg_color = (230, 230, 230)

        # количество кораблей (жизней)
        self.ship_limit = 3

        # настройки пуль (снарядов)
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (200, 60, 60)
        self.bullets_allowed = 5

        # настройка пришельцев
        self.fleet_drop_speed = 10

        # ускорение (усложнение игры)
        self.speedup_scale = 1.3
        # ускорение количества набранных очков
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Настройка динамики игры"""
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 0.5

        # начальное направление движения флота пришельцев. 1 - право, -1 - лево
        self.fleet_direction = 1

        # очки
        self.alien_points = 50

    def increase_speed(self):
        """увеличение характеристик со временем"""
        #self.ship_speed *= self.speedup_scale
        #self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
