import pygame
import math
import random

from components.physics import Physics
from components.particle import Particle

from config.constants import PLAYER_JUMPS, PLAYER_WALL_JUMP_X, PLAYER_WALL_JUMP_Y, PLAYER_MAX_AIR_TIME

class Player(Physics):
  def __init__(self, game, pos, size):
    self.air_time = 0
    self.jumps = PLAYER_JUMPS
    self.wall_slide = False
    self.dashing = 0
    
    super().__init__(game, 'player', pos, size)
  
  def update(self, tilemap, movement=(0, 0)):
    super().update(tilemap, movement=movement)
    
    self.air_time += 1
    
    if self.air_time > PLAYER_MAX_AIR_TIME:
      self.game.dead += 1
    
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
