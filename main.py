import sys
import pygame

from config import config 

pygame.init()

pygame.display.set_caption("Smash Ninja")
screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))

clock = pygame.time.Clock()

running = True

while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
  
  pygame.display.update()
  clock.tick(60)
  
pygame.quit()
sys.exit()