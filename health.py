import pygame
class Health:
    def __init__(self,ht):
        pygame.init()
        self.screen = ht.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ht.settings
        health_path= "images/health.bmp"
        empty_health_path= "images/empty_health.bmp"
        self.health_src = pygame.image.load(health_path)
        self.empty_health_src = pygame.image.load(empty_health_path)
        self.size = None

    def _scale(self, size):
        # cache the scaled hearts so we only rescale when max health changes
        if size != self.size:
            self.size = size
            self.health = pygame.transform.scale(self.health_src,(size,size))
            self.empty_health = pygame.transform.scale(self.empty_health_src,(size,size))

    def blitme(self):
        # hearts live in the left half of the bottom hud; shrink them if there are too many to fit
        margin = 40
        available = self.screen_rect.width // 2 - margin * 2
        count = max(1, self.settings.max_health)
        size = min(70, available // count, self.settings.hud_height - 20)
        self._scale(size)
        hud_center_y = self.screen_rect.height - self.settings.hud_height // 2
        y_pos = hud_center_y - size // 2
        for i in range(self.settings.max_health):
            x_pos = margin + size*i
            if i < self.settings.health_remain:
                self.screen.blit(self.health, (x_pos, y_pos))
            else:
                self.screen.blit(self.empty_health, (x_pos,y_pos))
