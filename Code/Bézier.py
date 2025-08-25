import pygame
import sys
import numpy as np
import math

# 初始化pygame
pygame.init()

# 设置窗口
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("贝塞尔曲线路径")

# 加载人物素材
character = pygame.image.load("Code/images/Dragon - Fully Animated/Attack 1/001.png")
character_rect = character.get_rect()

# 设置初始位置
character_rect.center = (100, 100)

# 定义贝塞尔曲线的控制点
control_points = [
    (100, 100),
    (200, 50),
    (300, 200),
    (400, 100),
    (500, 300),
    (600, 200),
    (700, 100)
]

# 生成贝塞尔曲线路径
def bezier_curve(points, num=100):
    n = len(points) - 1
    t = np.linspace(0, 1, num)
    curve = np.zeros((num, 2))
    
    for i in range(n + 1):
        binom = math.comb(n, i)
        curve += np.outer(binom * (t ** i) * ((1 - t) ** (n - i)), points[i])
    
    return curve

# 生成路径点
waypoints = bezier_curve(control_points, 200)
waypoints = [(int(x), int(y)) for x, y in waypoints]

# 移动参数
speed = 1
current_waypoint = 0
is_moving = False

# 游戏主循环
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:  # 按下A键开始移动
                is_moving = True
                current_waypoint = 0
                character_rect.center = waypoints[0]
    
    # 如果正在移动，更新位置
    if is_moving and current_waypoint < len(waypoints):
        character_rect.center = waypoints[current_waypoint]
        current_waypoint += speed
    
    # 如果到达最后一个点，停止移动
    if current_waypoint >= len(waypoints):
        is_moving = False
    
    # 绘制
    screen.fill((0, 0, 0))
    screen.blit(character, character_rect)
    
    # 绘制控制点和路径
    for point in control_points:
        pygame.draw.circle(screen, (255, 0, 0), point, 5)
    
    if len(waypoints) > 1:
        pygame.draw.lines(screen, (0, 255, 0), False, waypoints, 1)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()