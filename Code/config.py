import pygame
import sys

# Screen settings
WIDTH = 1200
HEIGHT = 800
FPS = 60

STEPS = 500  # 贝塞尔曲线的细分步数

ROAD_WIDTH = 120
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
LIGHT_GRAY = (100, 100, 100)

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

# Initialize Pygame
pygame.init()
# 字体设置 - 使用系统默认字体以支持中文
try:
    # 尝试使用微软雅黑或苹方字体（对中文支持较好的字体）
    title_font = pygame.font.SysFont("Microsoft YaHei" if sys.platform == "win32" else "PingFang SC", TITLE_FONT_SIZE)
    main_font = pygame.font.SysFont("Microsoft YaHei" if sys.platform == "win32" else "PingFang SC", MAIN_FONT_SIZE)
    small_font = pygame.font.SysFont("Microsoft YaHei" if sys.platform == "win32" else "PingFang SC", SMALL_FONT_SIZE)
except:
    # 如果找不到上述字体，退回到系统默认字体
    title_font = pygame.font.Font(None, TITLE_FONT_SIZE)
    main_font = pygame.font.Font(None, MAIN_FONT_SIZE)
    small_font = pygame.font.Font(None, SMALL_FONT_SIZE)


# Sound files
SOUND_FILES = {
    'correct': 'correct.wav',
    'wrong': 'wrong.wav',
    'win': 'win.wav',
    'lose': 'lose.wav'
}

# Word list for typing
WORD_LIST = [
    "in the heart of the forest, sunlight filters through the leaves, creating a dappled pattern on the ground. The gentle rustle of leaves and the sweet chirping of birds form a harmonious melody. This is the enchanting beauty of nature, a sight that soothes the soul."
]
# ssss = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789,.!?  '
# for char in ssss:
#     print(main_font.size(char)[0]) # 计算单个字母的宽


LETTER_WIDTH, LETTER_HEIGHT = main_font.size('m') # 计算单个字母的宽高

# Character settings
CHARACTER_SETTINGS = {
    'A': {
        'position': ROAD_CURVE_POINTS[0],  # 起点,
        'speed': int(2 * STEPS/len(WORD_LIST[0]) + 1), # 每次移动的点数
        'image_path': "Code/images/Dragon - Fully Animated/Attack 1/001.png" if sys.platform == "darwin" else "images\Dragon - Fully Animated\Attack 1/001.png"   
    },

    'police': {
        'position': (ROAD_CURVE_POINTS[0][0] + 10, ROAD_CURVE_POINTS[0][1]),  # 第二个转弯点
        'speed': 8
    }
}
# print(2 * STEPS / len(WORD_LIST[0]))

# rec width and height
REC_COLOR        = (30, 40, 70) # 矩形背景颜色
REC_BORDER_COLOR = (60, 70, 120) # 矩形边
REC_WIDTH        = WIDTH - 100
REC_HEIGHT       = LETTER_HEIGHT * 4 + 20

print(sys.platform)