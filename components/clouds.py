import random
from components.cloud import Cloud

class Clouds:
  def __init__(self, cloud_images, count=16):
    self.clouds = []
    
    for _ in range(count):
      cloud = Cloud((random.random() * 99999, random.random() * 99999),
                     random.choice(cloud_images),
                     random.random() * 0.05 + 0.05,
                     random.random() * 0.6 + 0.2)
      self.clouds.append(cloud)
      
      self.clouds.sort(key=lambda x: x.depth) # LAYERING
      
  def update(self):
    for cloud in self.clouds:
      cloud.update()
      
  def render(self, surf, offset=(0, 0)):
    for cloud in self.clouds:
      cloud.render(surf, offset)