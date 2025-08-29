import pygame
import sys
import numpy as np
from CONFIG_in_winsys import *
from Characters_CLASS import AnimatedSprite
from Map_CLASS import Map
from Background_CLASS import BackgroundSprite
from Word_CLASS import WordClass
# 初始化pygame
pygame.init()

# 设置窗口
screen_flag = pygame.HWSURFACE | pygame.DOUBLEBUF
screen = pygame.display.set_mode((WIDTH, HEIGHT), screen_flag)
pygame.display.set_caption("Tanping Game")

#===================================================================================
counter = 0
color = WHITE
typed_letter = "舗装された道路やコンクリートのビルが集まる都市は、大雨が降ると排水が追いつかなくなり「内水氾濫」が発生します。"
typed_letter = TYPED_WORDS
cursor_x = 70
cursor_y = HEIGHT - 140 + LETTER_HEIGHT*2
error_flag = False
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
CAT      = AnimatedSprite(CHARACTER_SETTINGS['CAT']['running'], flip_flag=CHARACTER_SETTINGS['CAT']['flip_flag'], remove_bg_flag=CHARACTER_SETTINGS['CAT']['remove_bg_flag'], position=CHARACTER_SETTINGS['CAT']['position'], frame_delay=80)
WALK_CAT = AnimatedSprite(CHARACTER_SETTINGS['CAT']['walk'],    flip_flag=CHARACTER_SETTINGS['CAT']['flip_flag'], remove_bg_flag=CHARACTER_SETTINGS['CAT']['remove_bg_flag'], position=(100, 500), frame_delay=150)
# 创建 Group
Character_group = pygame.sprite.Group( CAT, WALK_CAT )

#==================================================================================

#=================================文字处理=================================================
WORDS = WordClass(
    position=(WORD_ORIGIN_COORDINATES_X, WORD_ORIGIN_COORDINATES_Y)
)
WORDS.load_text(    
    text=WORD_LIST[0],
    font_size=MAIN_FONT_SIZE,
    color=BLUE,
    )
WORDS.build_cursor()
#==================================================================================

import pygame
import math

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
waypoints_0 = MAP.bezier_curve(p0, p1, p2, p3,num_points=STEPS)
waypoints_1 = MAP.bezier_curve(p4, p5, p6, p7,num_points=STEPS)
waypoints = np.concatenate([waypoints_0, waypoints_1], axis=0)

#=====================================================================================

# 移动参数
current_waypoint = 0
is_moving = False

def handle_text_input(event):

    global typed_letter, counter, is_moving, running, color, error_flag
    # print(counter)
    # if event.type == pygame.TEXTINPUT: pass  # event.text
    if event.type == pygame.KEYDOWN:         # event.unicode

        if event.key == pygame.K_ESCAPE:
            running = False

        elif event.key == pygame.K_BACKSPACE:
            if counter > 0:
                typed_letter = typed_letter[:-1]
                counter -= 1
            else:
                counter  = 0
        
        else:
            # 排除CapsLock（event.key == pygame.K_CAPSLOCK）
            if (event.unicode.isalpha() or event.unicode in '123456789,.! ') and event.key != pygame.K_CAPSLOCK:  # 只处理字母输入，排除CapsLock
            # if event.type == pygame.TEXTINPUT:   # event.text:    
                # print(event.unicode)
                if counter < len(WORD_LIST[0]):  # 防止越界
                    # typed_letter.append(event.unicode)
                    typed_letter += event.unicode
                    counter += 1
                    # print(typed_letter)
                    # print(WORD_LIST[0][:counter])
                    if typed_letter == WORD_LIST[0][:counter]:  #wanring 此处必须对比全部是否相同，而不能比较当前输入的字母

                        print("ok")
                        is_moving = True
                        error_flag = False

                    else:
                        error_flag = True
                        print("error")     
                        is_moving = False
                else:
                    is_moving = False
    color = GREEN if not error_flag else RED
    # error_flag = False

        # print(pygame.key.name(event.key))    #这种可以显示非字符按键的名字

        # if event.key == pygame.K_a:  # 按下A键开始移动
        #     is_moving = True

# 游戏主循环
clock = pygame.time.Clock()
running = True


def Painting():
    global is_moving, cursor_x, cursor_y
    # 绘制
    # Background_group.update()  # 调用 update()函数
    Background_group.draw(screen)
    MAP.draw_bezier(screen)
    is_moving = CAT.manual_moving(waypoints, is_moving, CHARACTER_SETTINGS['CAT']['speed'])
    WALK_CAT.keep_moving(waypoints, CHARACTER_SETTINGS['CAT']['speed'])
    print('yes')
    WORDS.draw(screen, WORD_ORIGIN_COORDINATES_X, WORD_ORIGIN_COORDINATES_Y)  # 绘制文字

    Character_group.update()  # 调用 update()函数
    Character_group.draw(screen)


while running:

    events = pygame.event.get()  # 获取所有事件
    for event in events: # 有事件才会进这个循环
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

        handle_text_input(event)


    Painting()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()