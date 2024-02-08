import math
import random
import pygame

from components.particle import Particle
from config.constants import Y_MAX_VELOCITY, PLAYER_JUMPS, PLAYER_WALL_JUMP_X, PLAYER_WALL_JUMP_Y

class PhysicsEntity:
  def __init__(self, game, e_type, pos, size) -> None:
    self.game = game
    self.type = e_type
    self.pos = list(pos)
    self.size = size
    self.velocity = [0, 0]
    self.collisions = {
      'up': False, 
      'down': False, 
      'right': False, 
      'left': False
      }
    self.y_max_velocity = Y_MAX_VELOCITY
    
    #ANIMATION
    self.action = ''
    self.anim_offset = (-3, -3)
    self.flip = False # True=facing_right False=facing_left
    self.set_action('idle')
    
    self.last_movement = [0, 0]
    
  def rect(self):
    return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])  
  
  def set_action(self, action):
    if action == self.action:
      return
    
    self.action = action
    self.animation = self.game.assets[self.type + '/' + self.action].copy()
  
  def update(self, tilemap, movement=(0,0)):
    self.collisions = {
      'up': False, 
      'down': False, 
      'right': False, 
      'left': False
      }
    frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])
    
    self.pos[0] += frame_movement[0]
    entity_rect = self.rect()
    for rect in tilemap.physics_rects_around(self.pos):
      if entity_rect.colliderect(rect):
        if frame_movement[0] > 0: #moving right
          entity_rect.right = rect.left
          self.collisions['right'] = True
        if frame_movement[0] < 0:
          entity_rect.left = rect.right
          self.collisions['left'] = True
        self.pos[0] = entity_rect.x
    
    self.pos[1] += frame_movement[1]
    entity_rect = self.rect()
    for rect in tilemap.physics_rects_around(self.pos):
      if entity_rect.colliderect(rect):
        if frame_movement[1] > 0:
          entity_rect.bottom = rect.top
          self.collisions['down'] = True
        if frame_movement[1] < 0:
          entity_rect.top = rect.bottom
          self.collisions['up'] = True
        self.pos[1] = entity_rect.y
    
    if movement[0] > 0:
      self.flip = False
    if movement[0] < 0:
      self.flip = True
    
    self.last_movement = movement
    
    self.velocity[1] = min(self.y_max_velocity, self.velocity[1] + 0.1)
    
    if self.collisions['down'] or self.collisions['up']:
      self.velocity[1] = 0
    
    self.animation.update()
    
  def render(self, surf, offset):
    img = self.animation.img()
    pos_x = self.pos[0] - offset[0] + self.anim_offset[0]
    pos_y = self.pos[1] - offset[1] + self.anim_offset[1]
    entity = pygame.transform.flip(img, self.flip, False)
    
    surf.blit(entity, (pos_x, pos_y))
    
    
class Player(PhysicsEntity):
  def __init__(self, game, pos, size):
    self.air_time = 0
    self.jumps = PLAYER_JUMPS
    self.wall_slide = False
    self.dashing = 0
    
    super().__init__(game, 'player', pos, size)
  
  def update(self, tilemap, movement=(0, 0)):
    super().update(tilemap, movement=movement)
    
    self.air_time += 1
    
    if self.collisions['down']:
      self.air_time = 0
      self.jumps = PLAYER_JUMPS
      
    self.wall_slide = False
    if (self.collisions['right'] or self.collisions['left']) and self.air_time > 4:
      self.wall_slide = True
      self.velocity[1] = min(self.velocity[1], 0.5)
      if self.collisions['right']:
        self.flip = False
      if self.collisions['left']:
        self.flip = True
      self.set_action("wall_slide")
        
    if not self.wall_slide:
      if self.air_time > 4:
        self.set_action('jump')
      elif movement[0] != 0:
        self.set_action('run')
      else:
        self.set_action('idle')
  
    if self.dashing > 0:
      self.dashing = max(0, self.dashing - 1)
    if self.dashing < 0:
      self.dashing = min(0, self.dashing + 1)
    
     # This is also cool down - you can't dash as much as you want! :D
    if abs(self.dashing) > 50:
      self.velocity[0] = abs(self.dashing) / self.dashing * 8
      if abs(self.dashing) == 51:
        self.velocity[0] *= 0.1
      self.particles_animation('stream')
    if abs(self.dashing) in {60, 50}:
      self.particles_animation('dash')
      
    if self.velocity[0] > 0:
      self.velocity[0] = max(self.velocity[0] - 0.1, 0)
    else:
      self.velocity[0] = min(self.velocity[0] + 0.1, 0)
    
  # Overriding parent render so the player disappears when dashing
  def render(self, surf, offset=(0,0)):
    if abs(self.dashing) <= 50:
      super().render(surf, offset=offset)
  
  def animate_stream(self):
    p_velocity = [abs(self.dashing) / self.dashing * random.random() * 3, 0] # random from 0 to 3
    p_dash = Particle(
      self.game, 
      'particle', 
      self.rect().center, 
      velocity=p_velocity,
      frame=random.randint(0, 7)
    )
    self.game.particles.append(p_dash)
  
  def animate_dash(self):
    for _ in range(20):
      angle = random.random() * math.pi * 2
      speed = random.random() * 0.5 + 0.5
      p_velocity = [math.cos(angle) * speed, math.sin(angle) * speed]
      p_double_jump = Particle(
        self.game, 
        'particle', 
        self.rect().center, 
        velocity=p_velocity,
        frame=random.randint(0, 7)
      )
      self.game.particles.append(p_double_jump)
  
  def animate_double_jump(self):
    for _ in range(10):
      angle = random.random() * math.pi * 2
      speed = random.random() * 0.5 + 0.5
      p_velocity = [math.cos(angle) * speed, speed]
      p_double_jump = Particle(
        self.game, 
        'light-sparkle', 
        self.rect().center, 
        velocity=p_velocity,
        frame=random.randint(0, 7)
      )
      self.game.particles.append(p_double_jump)

  def particles_animation(self, animation_type):
    match animation_type:
      case 'dash':
        self.animate_dash()
      case 'stream':
        self.animate_stream()
      case 'double_jump':
        self.animate_double_jump()
      
  def jump(self):
    if self.wall_slide:
      self.jumps = 1
      self.air_time = 5
      self.velocity[1] = PLAYER_WALL_JUMP_Y
      if self.flip and self.last_movement[0] < 0:
        self.velocity[0] = PLAYER_WALL_JUMP_X
        return True
      elif not self.flip and self.last_movement[0] > 0:
        self.velocity[0] = -PLAYER_WALL_JUMP_X
        return True
    elif self.jumps == 2:
      self.velocity[1] =- 3
      self.jumps -= 1
      self.air_time = 5
      return True
    elif self.jumps == 1:
      self.particles_animation('double_jump')
      self.velocity[1] =- 2
      self.jumps -= 1
      self.air_time = 5
      
      return True
    
  def dash(self):
    if not self.dashing:
      if self.flip:
        self.dashing = -60
      else:
        self.dashing = 60