import sys
import pygame

from components.entities import PhysicsEntity

from config import config 
from config import utils 


class Game:
  def __init__(self) -> None:
    pygame.init()

    pygame.display.set_caption("Smash Ninja")
    self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))

    self.clock = pygame.time.Clock()
    
    self.movement = [False, False]
    
    self.assets = {
      'player': utils.load_image('entities/player.png')
    }
    
    self.player = PhysicsEntity(self, 'player', (50, 50), (8, 15))

  def run(self) -> None:
    while True:
      self.screen.fill((14, 219, 248)) #moves object without copying prev frame

      self.player.update((self.movement[1] - self.movement[0], 0))
      self.player.render(self.screen)

      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_LEFT:
            self.movement[0] = True
          if event.key == pygame.K_RIGHT:
            self.movement[1] = True
        if event.type == pygame.KEYUP:
          if event.key == pygame.K_LEFT:
            self.movement[0] = False
          if event.key == pygame.K_RIGHT:
            self.movement[1] = False
      
      pygame.display.update()
      self.clock.tick(60)
      
Game().run()