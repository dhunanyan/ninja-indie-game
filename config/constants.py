# GLOBAL
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
FPS = 60
RENDER_SCALE = 2.0
BASE_IMG_PATH = 'assets/images/'

# PHYSICS
Y_MAX_VELOCITY = 5


# TILEMAP
NEIGHBOR_OFFSET = [(-1, 0), (-1, -1), (0, -1), 
                   (1, 0), (0, 0), (0, 1),
                   (-1, 1), (1, 1), (1, -1)]
PHYSICS_TILE_TYPES = {"grass", "stone"}