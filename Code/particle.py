# import pygame
# import numpy as np

# # ========== 贝塞尔曲线向量化函数 ==========
# def bezier_curve(p0, p1, p2, p3, num_points=200):
#     t = np.linspace(0, 1, num_points, dtype=np.float32)
#     one_minus_t = 1 - t
#     x = (one_minus_t**3) * p0[0] \
#         + 3 * (one_minus_t**2) * t * p1[0] \
#         + 3 * one_minus_t * (t**2) * p2[0] \
#         + (t**3) * p3[0]
#     y = (one_minus_t**3) * p0[1] \
#         + 3 * (one_minus_t**2) * t * p1[1] \
#         + 3 * one_minus_t * (t**2) * p2[1] \
#         + (t**3) * p3[1]
#     return np.column_stack((x, y))  # (num_points, 2)

# # ========== 初始化 pygame ==========
# pygame.init()
# WIDTH, HEIGHT = 800, 600
# screen = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption("Multi-Segment Bezier Curve Movement (NumPy Vectorized)")
# clock = pygame.time.Clock()

# # ========== 定义多段贝塞尔曲线的控制点 ==========
# # 每四个点定义一段曲线
# control_points = [
#     (np.array([100, 500]), np.array([200, 100]), np.array([600, 100]), np.array([700, 500])),
#     (np.array([700, 500]), np.array([600, 300]), np.array([200, 300]), np.array([100, 100])),
#     (np.array([100, 100]), np.array([300, 400]), np.array([500, 200]), np.array([700, 100]))
# ]

# # ========== 生成所有轨迹点（一次性计算） ==========
# trajectories = [bezier_curve(*segment, num_points=300) for segment in control_points]
# trajectory = np.concatenate(trajectories, axis=0)  # 拼接成一个大轨迹
# index = 0  # 当前轨迹索引

# # ========== 创建精灵 ==========
# player = pygame.Surface((20, 20), pygame.SRCALPHA)
# pygame.draw.circle(player, (255, 0, 0), (10, 10), 10)

# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     # 清屏
#     screen.fill((30, 30, 30))

#     # 绘制轨迹（蓝色小点）
#     for point in trajectory:
#         pygame.draw.circle(screen, (100, 100, 255), point.astype(int), 2)

#     # 更新精灵位置
#     if index < len(trajectory):
#         pos = trajectory[index]
#         screen.blit(player, (pos[0] - 10, pos[1] - 10))
#         index += 1
#     else:
#         index = 0  # 循环播放

#     pygame.display.flip()
#     clock.tick(60)  # 60 FPS

# pygame.quit()

