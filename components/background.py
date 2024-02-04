import pygame.sprite

from config import config
from config import assets
from config.layer import Layer

class Background(pygame.sprite.Sprite):
  def __init__(self, index, *groups):
    self._layer = Layer.BACKGROUND
    self.frame_index = 0
    
    original_image = assets.get_sprite("background")
    self.image = pygame.transform.scale(original_image, (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    
    self.width = int(self.image.get_width())
    self.height = int(self.image.get_height())
    self.position = ((config.SCREEN_WIDTH * index), (config.SCREEN_HEIGHT - self.height) / 2)
    self.rect = self.image.get_rect(topleft=self.position)
    
    super().__init__(*groups)
    
  def update(self):
    self.rect.x -= 1
    if self.rect.right <= 0:
      self.rect.x = config.SCREEN_WIDTH