import pygame

# Screen settings
WIDTH = 1200
HEIGHT = 800
FPS = 60

# Track settings
ROAD_WIDTH = 120
ROAD_CURVE_POINTS = [
    (100, HEIGHT//2),  # 起点
    (300, HEIGHT//2 - 100),  # 第一个转弯点
    (500, HEIGHT//2 + 50),   # 第二个转弯点
    (700, HEIGHT//2 - 80),   # 第三个转弯点
    (900, HEIGHT//2 + 30),   # 第四个转弯点
    (WIDTH - 100, HEIGHT//2) # 终点
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
LIGHT_BLUE = (100, 180, 255)

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
TITLE_FONT_SIZE = 48
MAIN_FONT_SIZE = 32
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
    "python", "programming", "keyboard", "velocity", "algorithm",
    "function", "variable", "statement", "conditional", "iteration",
    "dictionary", "exception", "framework", "generator", "decorator",
    "inheritance", "polymorphism", "encapsulation", "abstraction",
    "interface", "module", "package", "library", "dynamic", "static"
]
