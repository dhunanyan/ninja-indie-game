import sys
import pygame

from components.entities import Player
from components.tilemap import Tilemap
from components.clouds import Clouds

from config.utils import load_image, load_images, Animation
from config.constants import SCREEN_HEIGHT, SCREEN_WIDTH, FPS

class Game:
  def __init__(self) -> None:
    pygame.init()

    pygame.display.set_caption("Smash Ninja")
    self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    self.display = pygame.Surface((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)) # SCALING UP

    self.clock = pygame.time.Clock()
    
    self.movement = [False, False]
    
    self.assets = {
      'decor': load_images('tiles/decor'),
      'grass': load_images('tiles/grass'),
      'large_decor': load_images('tiles/large_decor'),
      'stone': load_images('tiles/stone'),
      'background': load_image('background.png'),
      'clouds': load_images('clouds'),
      'player': load_image('entities/player.png'),
      'player/idle': Animation(load_images('entities/player/idle'), img_dur=6),
      'player/run': Animation(load_images('entities/player/run'), img_dur=4),
      'player/jump': Animation(load_images('entities/player/jump')),
      'player/slide': Animation(load_images('entities/player/slide')),
      'player/wall_slide': Animation(load_images('entities/player/wall_slide'))
    }
    
    self.clouds = Clouds(self.assets['clouds'], count=16)
    
    self.player = Player(self, (50, 50), (8, 15))
    self.tilemap = Tilemap(self, tile_size=16)

    #CAMERA
    self.scroll = [0, 0]

  def run(self) -> None:
    while True:
      self.display.blit(self.assets['background'], (0, 0))

      self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
      self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
      render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

      self.clouds.update()
      self.clouds.render(self.display, offset=render_scroll)
      
      self.tilemap.render(self.display, offset=render_scroll)

      self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
      self.player.render(self.display, offset=render_scroll)
      
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_LEFT:
            self.movement[0] = True
          if event.key == pygame.K_RIGHT:
            self.movement[1] = True
          if event.key == pygame.K_UP:
            self.player.velocity[1] = -3
          if event.key == pygame.K_DOWN:
            self.player.velocity[1] = 3
        if event.type == pygame.KEYUP:
          if event.key == pygame.K_LEFT:
            self.movement[0] = False
          if event.key == pygame.K_RIGHT:
            self.movement[1] = False
      
      self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0)) # BLIT FOR SCALING UP
      pygame.display.update()
      self.clock.tick(FPS)
      
Game().run()