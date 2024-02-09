import pygame
import random
import math

from components.physics import Physics
from components.particle import Particle
from components.spark import Spark

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
            self.game.sfx['shoot'].play()
            proj_speed = -1.5
            timer = 0
            self.game.projectiles.append([[
              self.rect().centerx - 7,
              self.rect().centery
            ], proj_speed, timer])
            
            # Diamond animation
            for _ in range(4):
              spark = Spark(
                self.game.projectiles[-1][0],
                random.random() - 0.5 + math.pi,
                2 + random.random()
              )
              self.game.sparks.append(spark)
          if not self.flip and dis[0] > 0:
            # spawns to the right
            proj_speed = 1.5
            timer = 0
            self.game.projectiles.append([[
              self.rect().centerx + 7,
              self.rect().centery
            ], proj_speed, timer]) 
            
            # Diamond animation
            for _ in range(4):
              spark = Spark(
                self.game.projectiles[-1][0],
                random.random() - 0.5,
                2 + random.random()
              )
              self.game.sparks.append(spark)
    elif random.random() < 0.01:
      self.walking = random.randint(30, 120)
    
    super().update(tilemap, movement=movement)
  
    if movement[0] != 0:
      self.set_action('run')
    else:
      self.set_action('idle')
      
    if abs(self.game.player.dashing) >= 50:
      if self.rect().colliderect(self.game.player.rect()):
        #EXPLOSION
        self.game.sfx['hit'].play()
        for i in range(30):
          rw = (196, 44, 54) if random.randint(0, 1) else (160, 160, 160)
          rgb = [
            min(rw[0] + i * 2, 196),
            min(rw[1] + i * 2, 44),
            min(rw[2] + i * 2, 54)
          ]
          angle = random.random() * math.pi * 2
          speed = random.random() * 5
          spark = Spark(
            self.rect().center,
            angle,
            2 + random.random(),
            color=(rgb[0], rgb[1], rgb[2])
          )
          self.game.sparks.append(spark)
          particle = Particle(
            self.game,
            'particle',
            self.rect().center,
            velocity=[
              math.cos(angle + math.pi) * speed * 0.5,
              math.sin(angle + math.pi) * speed * 0.5,
            ],
            frame=random.randint(0, 7)
          )
          self.game.particles.append(particle)
          
         
        big_spark_right = Spark(
          self.rect().center,
          0,
          5 + random.random()
        )
        big_spark_left = Spark(
          self.rect().center,
          math.pi,
          5 + random.random()
        ) 
        self.game.sparks.append(big_spark_right)
        self.game.sparks.append(big_spark_left)
        return True
      
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
