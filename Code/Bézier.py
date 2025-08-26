import pygame
import sys
from config import *
# 初始化pygame
pygame.init()

# 设置窗口
screen_width = 1200
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("贝塞尔曲线路径")

counter = 0
color = WHITE
typed_letter = []
cursor_x = 70
cursor_y = HEIGHT - 140 + LETTER_HEIGHT*2
error_flag = False

# 加载人物素材
character = pygame.image.load(CHARACTER_SETTINGS['A']['image_path']).convert_alpha()  # 加载角色图像
character = pygame.transform.scale(character, (character.get_width() // 3, character.get_height() // 3))  # 缩放
character = pygame.transform.flip(character, True, False)  # 水平翻转（左右）

character_rect = character.get_rect()
character_rect.center = (100, 100) # 设置初始位置

# 绘制渐变背景
def draw_gradient_background(background_color):
    for y in range(HEIGHT):
        # 从深蓝色到黑色的渐变
        color = (
            max(0, background_color[0] * (HEIGHT - y) / HEIGHT),
            max(0, background_color[1] * (HEIGHT - y) / HEIGHT),
            max(0, background_color[2] * (HEIGHT - y) / HEIGHT)
        )
        pygame.draw.line(screen, color, (0, y), (WIDTH, y))

# 绘制打字区域
def draw_typing_area():
    # 绘制背景
    pygame.draw.rect(screen, REC_COLOR, (50, HEIGHT - 150, REC_WIDTH, REC_HEIGHT)) # 矩形背景
    pygame.draw.rect(screen, REC_BORDER_COLOR, (50, HEIGHT - 150, REC_WIDTH, REC_HEIGHT), 3) # 矩形边框,3表示边框宽度

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
def show_letters(WORD_LIST, first_x, first_y, color):
    global cursor_x, cursor_y

    cursor_x = 70
    cursor_y = HEIGHT - 140 + LETTER_HEIGHT*2
    for letter in WORD_LIST:
        letter_width, letter_height = main_font.size(letter)
        letter_surface = main_font.render(letter, True, color)

        screen.blit(letter_surface, (first_x, first_y))
        first_x += letter_width
        if first_x > REC_WIDTH + 50 - 20:  # 换行
            first_x = 70  # 重置x坐标
            first_y += letter_height  # y坐标增加
    cursor_x = first_x+1
    cursor_y = first_y

# 控制点（原p0-p3）
p0 = (100, 100)
p1 = (250, 100)
p2 = (400, 600)
p3 = (600, 600)
p4 = (1200-600, 600)
p5 = (1200-400, 600)
p6 = (1200-250, 100)
p7 = (1200-100, 100)

# 三次贝塞尔曲线函数
def cubic_bezier(p0, p1, p2, p3, t):
    """计算三次贝塞尔曲线上的点"""
    x = (
        (1 - t) ** 3 * p0[0]
        + 3 * (1 - t) ** 2 * t * p1[0]
        + 3 * (1 - t) * t ** 2 * p2[0]
        + t ** 3 * p3[0]
    )
    y = (
        (1 - t) ** 3 * p0[1]
        + 3 * (1 - t) ** 2 * t * p1[1]
        + 3 * (1 - t) * t ** 2 * p2[1]
        + t ** 3 * p3[1]
    )
    return (x, y)

# 绘制贝塞尔曲线
def draw_bezier(screen, p0, p1, p2, p3, color, steps):
    points = []
    for i in range(steps + 1):
        t = i / steps
        points.append(cubic_bezier(p0, p1, p2, p3, t))

    pygame.draw.circle(screen, RED, p0, 5)
    pygame.draw.circle(screen, RED, p1, 5)
    pygame.draw.circle(screen, RED, p2, 5)
    pygame.draw.circle(screen, RED, p3, 5)
    pygame.draw.lines(screen, color, False, points, 2)
    return points

# 生成路径点
waypoints = draw_bezier(screen, p0, p1, p2, p3, RED,STEPS)
waypoints = [(int(x), int(y)) for x, y in waypoints]
waypoints += draw_bezier(screen, p4, p5, p6, p7, RED,STEPS)
waypoints = [(int(x), int(y)) for x, y in waypoints]

# 移动参数
current_waypoint = 0
is_moving = False

def handle_text_input(event):

    global typed_letter, counter, is_moving, running, color, error_flag
    # print(counter)
    if event.type == pygame.TEXTINPUT: pass  # event.text
        
    if event.type == pygame.KEYDOWN:         # event.unicode

        if event.key == pygame.K_ESCAPE:
            running = False

        elif event.key == pygame.K_BACKSPACE:
            if counter > 0:
                typed_letter.pop()  # 删除最后一个字符
                print(counter)
                counter -= 1
            else:
                counter  = 0
        else:

            if counter < len(WORD_LIST[0]):  # 防止越界
                typed_letter.append(event.unicode)
                counter += 1
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

def move_character():
    screen.blit(character, character_rect)
    global is_moving, current_waypoint
    # 如果正在移动，更新位置
    if is_moving and current_waypoint < len(waypoints):
        character_rect.center = waypoints[current_waypoint]
        current_waypoint += CHARACTER_SETTINGS['A']['speed']
        is_moving = False
    
    # 如果到达最后一个点，停止移动
    if current_waypoint >= len(waypoints):
        is_moving = False

# 游戏主循环
clock = pygame.time.Clock()
running = True

while running:
    # screen.fill(LIGHT_GRAY)
    draw_gradient_background(DARK_BLUE)
    clock.tick(60)

    for event in pygame.event.get(): # 有事件才会进这个循环
        if event.type == pygame.QUIT:
            running = False

        handle_text_input(event)

    # 绘制
    draw_bezier(screen, p0, p1, p2, p3, WHITE, STEPS)
    draw_bezier(screen, p4, p5, p6, p7, WHITE, STEPS)
    draw_typing_area()
    move_character()
    show_letters(WORD_LIST[0],70, HEIGHT - 140, BLUE)
    show_letters(typed_letter,70, HEIGHT - 140 + LETTER_HEIGHT*2, color)
    draw_cursor(cursor_x, cursor_y)

    pygame.display.flip()
    # clock.tick(1)

pygame.quit()
sys.exit()