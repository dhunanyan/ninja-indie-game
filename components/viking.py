import pygame
from config import config
from config import assets

from config.layer import Layer

class Viking(pygame.sprite.Sprite):
  def __init__(self, *groups):
    self._layer = Layer.VIKING
    self.jumping_height = config.VIKING_JUMPING_HEIGHT
    self.x_velocity = config.VIKING_X_VELOCITY
    self.y_velocity = config.VIKING_Y_VELOCITY
    
    self.is_falling = False
    self.is_jumping = False
    
    self.current_frame_index = 0
    self.current_frame = 0
    self.scaling_factor = 0.35
    
    original_image = assets.get_sprite("viking-stand-0")
    self.height = int(original_image.get_height() * self.scaling_factor)
    
    self.x_init = config.VIKING_DISTANCE
    self.y_init = config.SCREEN_HEIGHT - self.height - config.FLOOR_HEIGHT
    self.x = self.x_init
    self.y = self.y_init
    
    self.set_size(original_image)
    self.rect = self.image.get_rect(topleft=(self.x, self.y))
    
    self.mask = pygame.mask.from_surface(self.image)
    
    super().__init__(*groups)
    
  def set_position(self):
    self.rect.x = self.x
    self.rect.y = self.y
    
  def set_size(self, original_image):
    self.image = pygame.transform.scale(original_image, (int(original_image.get_width() * self.scaling_factor), int(original_image.get_height() * self.scaling_factor)))
    
  def set_sprite(self, n: int, movement: str):
    sprite_name = f"{movement}-{n // config.VIKING_WALKING_ANIMATION_SPEED}"
    original_image = assets.get_sprite(sprite_name)
    self.set_size(original_image)

  def animate(self, speed: int, movement: str, frames_count: int = 0, prefix: str = 'viking'):
    if not frames_count:
      self.set_sprite(self.current_frame, f"{prefix}-{movement}")
      return
    
    self.current_frame_index += 1
    if self.current_frame_index >= speed:
      self.current_frame += 1
      self.current_frame_index = 0
    if self.current_frame > frames_count - 1:
      self.current_frame = 0
      self.current_frame_index = 0
      
    self.set_sprite(self.current_frame, f"{prefix}-{movement}")

  def move_left(self):
    self.x -= self.x_velocity
    self.set_position()
    self.animate(config.VIKING_WALKING_ANIMATION_SPEED, 'move-left', 5)

  def move_right(self):
    self.x += self.x_velocity
    self.set_position()
    self.animate(config.VIKING_WALKING_ANIMATION_SPEED, 'move-right', 5)
  
  def fall(self, direction: str):
    if not self.is_falling:
      return

    if self.y >= self.y_init:
      self.is_falling = False
      self.y = self.y_init
      self.animate(config.VIKING_WALKING_ANIMATION_SPEED, "stand")
      return
    
    self.y_velocity -= config.GRAVITY
    self.y -= self.y_velocity
    
    self.set_position()
    self.animate(config.VIKING_JUMPING_ANIMATION_SPEED, f"move-{direction}-down", 2)
  
  def jump(self, direction: str):
    if not self.is_jumping:
      return
    self.y_velocity -= config.GRAVITY
    if self.y_velocity < -self.jumping_height:
      self.is_jumping = False
      self.y_velocity = self.jumping_height
    
    prev_y = self.y
    self.y -= self.y_velocity
    self.set_position()
    
    if prev_y > self.y:
      self.animate(config.VIKING_JUMPING_ANIMATION_SPEED, f"move-{direction}-up", 2)
    else:
      self.animate(config.VIKING_JUMPING_ANIMATION_SPEED, f"move-{direction}-down", 2)
    
  def update(self, direction: str, keys: list):
    if keys[getattr(pygame, config.RIGHT)]:
      direction = 'right'
      self.move_right()
    if keys[getattr(pygame, config.LEFT)]:
      direction = 'left'
      self.move_left()
    if keys[getattr(pygame, config.UP)]:
      self.is_jumping = True
      self.jump(direction)
    self.is_falling = True
    self.fall(direction)