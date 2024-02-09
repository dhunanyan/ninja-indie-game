# GLOBAL
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
FPS = 60
RENDER_SCALE = 2.0
BASE_IMG_PATH = 'assets/images/'
TRANSITION_COLOR = (255, 255, 255)
TRANSITION_SPEED = 30

# PHYSICS
Y_MAX_VELOCITY = 5


# TILEMAP
NEIGHBOR_OFFSET = [(-1, 0), (-1, -1), (0, -1), 
                   (1, 0), (0, 0), (0, 1),
                   (-1, 1), (1, 1), (1, -1)]
PHYSICS_TILE_TYPES = {"grass", "stone"}

AUTOTILE_NEIGHBORS = [(1, 0), (-1, 0), (0, -1), (0, 1)]
AUTOTILE_TYPES = {"grass", "stone"}
AUTOTILE_MAP = {
  tuple(sorted([(1, 0), (0, 1)])): 0,
  tuple(sorted([(1, 0), (0, 1), (-1, 0)])): 1,
  tuple(sorted([(-1, 0), (0, 1)])): 2,
  tuple(sorted([(-1, 0), (0, -1), (0, 1)])): 3,
  tuple(sorted([(-1, 0), (0, -1)])): 4,
  tuple(sorted([(-1, 0), (0, -1), (1, 0)])): 5,
  tuple(sorted([(1, 0), (0, -1)])): 6,
  tuple(sorted([(1, 0), (0, -1), (0, 1)])): 7,
  tuple(sorted([(1, 0), (-1, 0), (0, 1), (0, -1)])): 8,
}

# ANIMATION
LEAF_ANIMATION_INTENSITY = 49999
LEFT_VELOCITY = [-0.1, 0.3]

# PLAYER
PLAYER_DIM = (8, 15)
PLAYER_JUMPS = 2
PLAYER_WALL_JUMP_X = 3.5
PLAYER_WALL_JUMP_Y = -2.5
PLAYER_MAX_AIR_TIME = 120

# ENEMY
ENEMY_DIM = (8, 15)
