import pygame
import sys
from CONFIG_in_winsys import *
from Characters_CLASS import AnimatedSprite
from Map_CLASS import Map
from Background_CLASS import BackgroundSprite
# 初始化pygame
pygame.init()

# 设置窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tanping Game")

#====================加载背景====================================================

# 实例化
BACKGROUND = BackgroundSprite(BACKGROUND_PIC, position=(0, 0), frame_delay=100)
# 创建group
all_sprites_0 = pygame.sprite.Group(BACKGROUND)

#================================================================================

# 加载打字区域
typing_area = pygame.image.load(REC_PIC[0]).convert_alpha() # 自带透明通道
bbox = typing_area.get_bounding_rect()
# 裁剪出有效区域
typing_area = typing_area.subsurface(bbox).copy()
typing_area = pygame.transform.scale(typing_area, (REC_WIDTH, REC_HEIGHT))

#=============================加载角色动图===========================================

# 实例化
CAT      = AnimatedSprite(CHARACTER_SETTINGS['CAT']['running'], CHARACTER_SETTINGS['CAT']['flip_flag'], CHARACTER_SETTINGS['CAT']['bg_flag'], CHARACTER_SETTINGS['CAT']['position'], 80)
WALK_CAT = AnimatedSprite(CHARACTER_SETTINGS['CAT']['walk'],    CHARACTER_SETTINGS['CAT']['flip_flag'], CHARACTER_SETTINGS['CAT']['bg_flag'], (100, 200),150)
# 创建 Group
all_sprites = pygame.sprite.Group(CAT, WALK_CAT)

#==================================================================================

counter = 0
color = WHITE
typed_letter = "舗装された道路やコンクリートのビルが集まる都市は、大雨が降ると排水が追いつかなくなり「内水氾濫」が発生します。"
typed_letter = TYPED_WORDS
cursor_x = 70
cursor_y = HEIGHT - 140 + LETTER_HEIGHT*2
error_flag = False

# 绘制打字区域
def draw_typing_area():

    typing_area = pygame.image.load(REC_PIC[0]).convert_alpha() # 自带透明通道
    bbox = typing_area.get_bounding_rect()

    # 裁剪出有效区域
    typing_area = typing_area.subsurface(bbox).copy()
    typing_area = pygame.transform.scale(typing_area, (REC_WIDTH, REC_HEIGHT))

    screen.blit(typing_area, (REC_ORIGIN_COORDINATES_X, REC_ORIGIN_COORDINATES_Y))
    # pygame.draw.rect(screen, REC_COLOR, (REC_ORIGIN_COORDINATES_X, REC_ORIGIN_COORDINATES_Y, REC_WIDTH, REC_HEIGHT)) # 矩形背景
    # pygame.draw.rect(screen, REC_BORDER_COLOR, (REC_ORIGIN_COORDINATES_X, REC_ORIGIN_COORDINATES_Y, REC_WIDTH, REC_HEIGHT), 3) # 矩形边框,3表示边框宽度

# Cursor
def draw_cursor(cursor_x, cursor_y):
    import time
    if int(time.time() * 2) % 2 == 0:
        # shadow
        # pygame.draw.line(screen, BLACK, (70+1, HEIGHT - 140 + LETTER_HEIGHT*2+3), (70+5, HEIGHT - 140 + LETTER_HEIGHT*2+3), width = 2)          # -
        # pygame.draw.line(screen, BLACK, (70+3, HEIGHT - 140+3), (70+3, HEIGHT - 140 + 28+3), width = 2)                                         # |
        # pygame.draw.line(screen, BLACK, (70+1, HEIGHT - 140 + LETTER_HEIGHT*2+28+3), (70+5, HEIGHT - 140 + LETTER_HEIGHT*2 + 28+3), width = 2)  # -
        
        # cursor
        pygame.draw.line(screen, LIGHT_BLUE, (cursor_x-2, cursor_y), (cursor_x+2, cursor_y), width = 1)         # -
        pygame.draw.line(screen, LIGHT_BLUE, (cursor_x, cursor_y), (cursor_x, cursor_y + LETTER_HEIGHT), width = 1)         # |
        pygame.draw.line(screen, LIGHT_BLUE, (cursor_x-2, cursor_y + LETTER_HEIGHT), (cursor_x+2, cursor_y + LETTER_HEIGHT), width = 1)         # -

# 显示文字
def show_letters(WORD_LIST, current_x, current_y, color):
    global cursor_x, cursor_y

    cursor_x = current_x + 1
    cursor_y = current_y + LETTER_HEIGHT * 2
    for letter in WORD_LIST:
        letter_width, letter_height = main_font.size(letter)
        letter_surface = main_font.render(letter, True, color)

        screen.blit(letter_surface, (current_x, current_y))
        current_x += letter_width
        if current_x >= REC_WIDTH - 9:  # 换行
            current_x = WORD_ORIGIN_COORDINATES_X  # 重置x坐标
            current_y += LETTER_HEIGHT  # y坐标增加
    cursor_x = current_x + 1
    cursor_y = current_y

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
MAP.add_segment(p0, p1, p2, p3)
MAP.add_segment(p4, p5, p6, p7)
waypoints = MAP.get_curve_points(steps=STEPS)

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

while running:

    all_sprites_0.draw(screen)
    clock.tick(60)

    for event in pygame.event.get(): # 有事件才会进这个循环
        if event.type == pygame.QUIT:
            running = False

        handle_text_input(event)

    # 绘制
    MAP.draw_bezier(screen, RED, waypoints)
    draw_typing_area()

    is_moving = CAT.manual_moving(waypoints, is_moving, CHARACTER_SETTINGS['CAT']['speed'])
    WALK_CAT.keep_moving(waypoints, CHARACTER_SETTINGS['CAT']['speed'])

    show_letters(WORD_LIST[0], WORD_ORIGIN_COORDINATES_X, WORD_ORIGIN_COORDINATES_Y, BLUE)
    show_letters(typed_letter, TYPED_WORDS_ORIGIN_COORDINATES_X, TYPED_WORDS_ORIGIN_COORDINATES_Y, color)
    draw_cursor(cursor_x, cursor_y)
    all_sprites.update()  # 调用 update()函数
    all_sprites.draw(screen)

    pygame.display.flip()
    # clock.tick(1)

pygame.quit()
sys.exit()