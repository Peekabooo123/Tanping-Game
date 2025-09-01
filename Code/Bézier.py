import pygame
import sys
import numpy as np
from CONFIG_in_winsys import *
from Characters_CLASS import AnimatedSprite
from Map_CLASS import Map
from Background_CLASS import BackgroundSprite
from Word_CLASS import WordClass
import os
import japan_to_roma as convert
os.environ["SDL_IME_SHOW_UI"] = "1"  # 让系统输入法候选框显示
# 初始化pygame
pygame.init()
pygame.key.start_text_input()

# 设置窗口
screen_flag = pygame.HWSURFACE | pygame.DOUBLEBUF
screen = pygame.display.set_mode((WIDTH, HEIGHT), screen_flag)
pygame.display.set_caption("Tanping Game")

#===================================================================================
color = WHITE
typed_letter = "舗装された道路やコンクリートのビルが集まる都市は、大雨が降ると排水が追いつかなくなり「内水氾濫」が発生します。"
typed_letter = TYPED_WORDS
# cursor_x = 70
# cursor_y = HEIGHT - 140 + LETTER_HEIGHT*2
error_flag = False
start_point = (15, 780)
Language = 1
#===================================================================================


#====================加载背景========================================================

# 实例化
BACKGROUND    = BackgroundSprite(BACKGROUND_PIC)
BACKGROUND_1  = BackgroundSprite(["images/BackGround/Background/parallax-mountain-mountains.png"])
BACKGROUND_2  = BackgroundSprite(["images/BackGround/Background/parallax-mountain-montain-far.png"])
BACKGROUND_3  = BackgroundSprite(["images/BackGround/Background/parallax-mountain-foreground-trees.png"])
BACKGROUND_4  = BackgroundSprite(["images/BackGround/Background/parallax-mountain-trees.png"])  # 贴近底部显示
TYPING_AREA   = BackgroundSprite(REC_PIC, box_flag = True, scale_size=(REC_WIDTH, REC_HEIGHT), position=(REC_ORIGIN_COORDINATES_X, REC_ORIGIN_COORDINATES_Y))

# 创建group
Background_group = pygame.sprite.Group(BACKGROUND,BACKGROUND_1,BACKGROUND_2,BACKGROUND_3,BACKGROUND_4,TYPING_AREA)

#================================================================================

#=============================加载角色动图===========================================

# 实例化
CAT      = AnimatedSprite(CHARACTER_SETTINGS['CAT']['running'], flip_flag=CHARACTER_SETTINGS['CAT']['flip_flag'], remove_bg_flag=CHARACTER_SETTINGS['CAT']['remove_bg_flag'], position=start_point, frame_delay=80)
WALK_CAT = AnimatedSprite(CHARACTER_SETTINGS['CAT']['walk'],    flip_flag=CHARACTER_SETTINGS['CAT']['flip_flag'], remove_bg_flag=CHARACTER_SETTINGS['CAT']['remove_bg_flag'], position=start_point, frame_delay=150)
# 创建 Group
Character_group = pygame.sprite.Group( CAT, WALK_CAT )

#==================================================================================

#=================================文字处理=================================================
WORDS = WordClass(
    position=(WORD_ORIGIN_COORDINATES_X, WORD_ORIGIN_COORDINATES_Y)
)
WORDS.load_text(    
    text=WORD_LIST[Language],
    font_size=SMALL_FONT_SIZE,
    color=BLUE,
    )
WORDS.build_cursor()


ROMA = WordClass(
    position=(WORD_ORIGIN_COORDINATES_X, WORD_ORIGIN_COORDINATES_Y - 30)
)

surface, rect = ROMA.load_text(    
    text=convert.convert_japan_to_roma(WORD_LIST[Language]),
    font_size=MAIN_FONT_SIZE,
    color=BLUE,
    )
#==================================================================================

# 假设这些常量已定义
LETTER_HEIGHT = 28
LIGHT_BLUE = (0, 255, 255)

# 控制点
p0 = ROAD_CURVE_POINTS[0]
p1 = ROAD_CURVE_POINTS[1]
p2 = ROAD_CURVE_POINTS[2]
p3 = ROAD_CURVE_POINTS[3]
p4 = ROAD_CURVE_POINTS[4]
p5 = ROAD_CURVE_POINTS[5]
p6 = ROAD_CURVE_POINTS[6]
p7 = ROAD_CURVE_POINTS[7]

#==============================路径点==================================================

#实例化
MAP = Map(WIDTH, HEIGHT)
waypoints = MAP.linear_bezier(start_point, (start_point[0] + 1685, start_point[1]), num_points=STEPS)
# waypoints_0 = MAP.bezier_curve(p0, p1, p2, p3,num_points=STEPS)
# waypoints_1 = MAP.bezier_curve(p4, p5, p6, p7,num_points=STEPS)
# waypoints = np.concatenate([waypoints_0, waypoints_1], axis=0)

#=====================================================================================

# 移动参数
current_waypoint = 0
is_moving = False


# color = GREEN if not error_flag else RED


# 游戏主循环
clock = pygame.time.Clock()
running = True

def Painting():
    
    # 绘制
    # Background_group.update()  # 调用 update()函数
    Background_group.draw(screen)
    MAP.draw_bezier(screen)

    WALK_CAT.keep_moving(waypoints, 3)
    typed_text, typed_text_color = CAT.Control_logic(events, WORD_LIST[Language], waypoints)

    WORDS.draw(screen, WORD_ORIGIN_COORDINATES_X, WORD_ORIGIN_COORDINATES_Y, typed_text, typed_text_color)  # 绘制文字
    # ROMA.draw(screen, WORD_ORIGIN_COORDINATES_X, WORD_ORIGIN_COORDINATES_Y - 20, typed_text, typed_text_color)  # 绘制文字
    screen.blit(surface, rect)
    Character_group.update()  # 调用 update()函数
    Character_group.draw(screen)


while running:

    events = pygame.event.get()  # 获取所有事件
    for event in events: # 有事件才会进这个循环
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    Painting()
    pygame.display.flip()
    clock.tick(120)

pygame.quit()
sys.exit()