import pygame

# Screen settings
WIDTH = 1200
HEIGHT = 800
FPS = 60

# Track settings
ROAD_WIDTH = 120
# ROAD_CURVE_POINTS = [
#     (10, HEIGHT//2),  # 起点
#     (300, HEIGHT//2 - 100),  # 第一个转弯点
#     (500, HEIGHT//2 + 50),   # 第二个转弯点
#     (700, HEIGHT//2 - 80),   # 第三个转弯点
#     (900, HEIGHT//2 + 30),   # 第四个转弯点
#     (WIDTH - 100, HEIGHT//2) # 终点
# ]

ROAD_CURVE_POINTS = [
    
    (100, 100),
    (250, 100),
    (400, 600),
    (600, 600),

    (1200-600, 600),
    (1200-400, 600),
    (1200-250, 100),
    (1200-100, 100)
]

DECORATION_COLORS = [
    (80, 80, 80),    # 深灰色路面
    (100, 100, 100), # 浅灰色路面
    (120, 120, 120)  # 最浅灰色路面
]

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 50, 50)
BLUE = (50, 150, 255)
GREEN = (50, 255, 100)
YELLOW = (255, 255, 100)
PURPLE = (180, 50, 230)
DARK_BLUE = (20, 30, 60)
LIGHT_BLUE = (0, 255, 255)

# Game settings
INITIAL_THIEF_SPEED = 0.2
POLICE_MOVE_SPEED = 5
LEVEL_SPEED_MULTIPLIER = 0.1
SCORE_PER_LEVEL = 10

# Particle settings
PARTICLE_COUNT = 8
PARTICLE_LIFETIME = (20, 40)
PARTICLE_SPEED = (0.5, 2)
PARTICLE_SIZE = (2, 5)

# Text settings
TITLE_FONT_SIZE = 40
MAIN_FONT_SIZE  = 25
SMALL_FONT_SIZE = 24

# Sound files
SOUND_FILES = {
    'correct': 'correct.wav',
    'wrong': 'wrong.wav',
    'win': 'win.wav',
    'lose': 'lose.wav'
}

# Word list for typing
WORD_LIST = [
'''
In the heart of the forest, sunlight filters through the leaves, creating a dappled pattern on the ground. The gentle rustle of leaves and the sweet chirping of birds form a harmonious melody. This is the enchanting beauty of nature, a sight that soothes the soul.
'''
]

# Character settings
CHARACTER_SETTINGS = {
    'A': {
        'position': ROAD_CURVE_POINTS[0],  # 起点,
        'speed': 1
    },

    'police': {
        'position': (ROAD_CURVE_POINTS[0][0] + 10, ROAD_CURVE_POINTS[0][1]),  # 第二个转弯点
        'speed': 8
    }
}
