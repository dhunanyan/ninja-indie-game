import pygame
import random
from components.physics import Physics

class Enemy(Physics):
  def __init__(self, game, pos, size):
    super().__init__(game, 'enemy', pos, size)
    
    self.walking = 0
    
  def update(self, tilemap, movement=(0, 0)):
    if self.walking:
      # This check if there is a tile on next block enemy stepped - to not walk at the edge
      if tilemap.solid_check((self.rect().centerx + (-7 if self.flip else 7), self.pos[1] + 23)):
        if (self.collisions['right'] or self.collisions['left']):
          self.flip = not self.flip
        else:
          movement = (
            movement[0] - 0.5 if self.flip else 0.5, 
            movement[1]
            )
      else:
        self.flip = not self.flip
      self.walking = max(0, self.walking - 1)
      # this can be set to true at the line above
      if not self.walking:
        # distance - diff between enemy pos and player pos
        dis = (
          self.game.player.pos[0] - self.pos[0],
          self.game.player.pos[1] - self.pos[1]
        )
        if (abs(dis[1]) < 16):
          if self.flip and dis[0] < 0:
            # spawns to the left
            proj_speed = -1.5
            timer = 0
            self.game.projectiles.append([[
              self.rect().centerx - 7,
              self.rect().centery
            ], proj_speed, timer]) 
          if not self.flip and dis[0] > 0:
            # spawns to the right
            proj_speed = 1.5
            timer = 0
            self.game.projectiles.append([[
              self.rect().centerx + 7,
              self.rect().centery
            ], proj_speed, timer]) 
    elif random.random() < 0.01:
      self.walking = random.randint(30, 120)
    
    super().update(tilemap, movement=movement)
  
    if movement[0] != 0:
      self.set_action('run')
    else:
      self.set_action('idle')
      
  def render(self, surf, offset=(0, 0)):
    super().render(surf, offset=offset)
    
    if self.flip:
      surf.blit(
        pygame.transform.flip(self.game.assets['gun'], True, False),
        (self.rect().centerx - 4 - self.game.assets['gun'].get_width() - offset[0],
         self.rect().centery - offset[1])
        )
    else:
      surf.blit(self.game.assets['gun'], (self.rect().centerx + 4 - offset[0], self.rect().centery - offset[1]))