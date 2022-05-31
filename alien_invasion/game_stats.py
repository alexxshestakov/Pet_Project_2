class GameStats:
    """класс статистики"""
    
    def __init__(self, ai_game):
        """инициализация статистики"""
        self.settings = ai_game.settings
        self.reset_stats()
        self.game_active = False
        # Высокий балл никогда не должен быть сброшен
        self.high_score = 0
        
    def reset_stats(self):
        """обновление статистики в течение игры"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1