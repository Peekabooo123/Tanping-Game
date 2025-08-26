import pygame
import sys

from config import ROAD_CURVE_POINTS

pygame.init()

# 屏幕设置
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bezier Curve Example")

# 定义颜色
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# 二次贝塞尔曲线函数
def quadratic_bezier(p0, p1, p2, t):
    """计算二次贝塞尔曲线上的点"""
    x = (1 - t)**2 * p0[0] + 2 * (1 - t) * t * p1[0] + t**2 * p2[0]
    y = (1 - t)**2 * p0[1] + 2 * (1 - t) * t * p1[1] + t**2 * p2[1]
    return (x, y)

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
    pygame.draw.lines(screen, color, False, points, 2)


# 控制点（原p0-p3）
p0=(100, 100)
p1=(250, 100)
p2=(400, 600)
p3=(600, 600)

# 以y轴对称，WIDTH=1200
p4 = (1200-600, 600)
p5 = (1200-400, 600)
p6 = (1200-250, 100)
p7 = (1200-100, 100)



def BEZIER_FUNCTION():
    font = pygame.font.SysFont(None, 24)
    for idx, point in enumerate(ROAD_CURVE_POINTS):
        pygame.draw.circle(screen, RED, point, 5)
        label = font.render(str(idx), True, (0, 0, 0))
        screen.blit(label, (point[0] + 8, point[1] - 18))
    
    draw_bezier(screen, p0, p1, p2, p3, (0, 0, 0))
    draw_bezier(screen, p4, p5, p6, p7, (0, 0, 0))

    pygame.draw.lines(screen, BLUE, False, ROAD_CURVE_POINTS, 1) #按顺序连接这些点
        
    
# 主循环
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(WHITE)
    BEZIER_FUNCTION()

    # # 绘制控制点
    # pygame.draw.circle(screen, RED, p0, 5)
    # pygame.draw.circle(screen, RED, p1, 5)
    # pygame.draw.circle(screen, RED, p2, 5)
    # pygame.draw.circle(screen, RED, p3, 5)
    # pygame.draw.circle(screen, RED, p4, 5)
    # pygame.draw.circle(screen, RED, p5, 5)
    # pygame.draw.circle(screen, RED, p6, 5)
    # pygame.draw.circle(screen, RED, p7, 5)

    # # 绘制控制线
    # pygame.draw.lines(screen, BLUE, False, [p0, p1, p2, p3], 1) #按顺序连接这些点
    # pygame.draw.lines(screen, BLUE, False, [p4, p5, p6, p7], 1) #按顺序连接这些点

    # # 绘制贝塞尔曲线
    # draw_bezier(screen, p0, p1, p2, p3, (0, 0, 0))
    # draw_bezier(screen, p4, p5, p6, p7, (0, 0, 0))

    pygame.display.flip()
