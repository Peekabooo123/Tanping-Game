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

sss='''abcdefghijklmnopqrstuvwxyz'''
# 加载人物素材
character = pygame.image.load("images\Dragon - Fully Animated\Attack 1/001.png").convert_alpha()  # 加载角色图像
character = pygame.transform.scale(character, (character.get_width() // 3, character.get_height() // 3))  # 缩放
character = pygame.transform.flip(character, True, False)  # 水平翻转（左右）

character_rect = character.get_rect()
character_rect.center = (100, 100) # 设置初始位置

# 控制点（原p0-p3）
p0=(100, 100)
p1=(250, 100)
p2=(400, 600)
p3=(600, 600)
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
def draw_bezier(screen, p0, p1, p2, p3, color, steps=100):
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
waypoints = draw_bezier(screen, p0, p1, p2, p3, RED)
waypoints = [(int(x), int(y)) for x, y in waypoints]

# 移动参数
speed = 1
current_waypoint = 0
is_moving = False

def handle_text_input(event):
    global counter, is_moving, running
    # print(counter)
    if event.type == pygame.TEXTINPUT: pass  # event.text
        
    if event.type == pygame.KEYDOWN:         # event.unicode
        print(event.unicode)
        # print(counter)
        if event.unicode == sss[counter]: 
            print("ok")
            is_moving = True
        elif event.key == pygame.K_ESCAPE:
            running = False
        else: 
            print("error")
            is_moving = False
        counter += 1

        # print(pygame.key.name(event.key))    #这种可以显示非字符按键的名字

        # if event.key == pygame.K_a:  # 按下A键开始移动
        #     is_moving = True

def move_character():
    screen.blit(character, character_rect)
    global is_moving, current_waypoint
    # 如果正在移动，更新位置
    if is_moving and current_waypoint < len(waypoints):
        character_rect.center = waypoints[current_waypoint]
        current_waypoint += speed
        is_moving = False
    
    # 如果到达最后一个点，停止移动
    if current_waypoint >= len(waypoints):
        is_moving = False

# 游戏主循环
clock = pygame.time.Clock()
running = True

while running:
    screen.fill((0, 0, 0))
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        handle_text_input(event)

    # 绘制
    move_character()
    draw_bezier(screen, p0, p1, p2, p3, WHITE)
    draw_bezier(screen, p4, p5, p6, p7, WHITE)
    pygame.display.flip()

pygame.quit()
sys.exit()