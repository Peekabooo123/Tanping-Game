import pygame
import sys
import numpy as np

class Map:
    def __init__(self, width=1200, height=800):
        self.width = width
        self.height = height
        self.segments = []  # 存储多段贝塞尔曲线的控制点
        self.all_points = []

    # def add_segment(self, p0, p1, p2, p3):
    #     """添加一段贝塞尔曲线的控制点"""
    #     self.segments.append((p0, p1, p2, p3))

    # def add_segments_from_list(self, points_list):
    #     """
    #     批量添加多段曲线
    #     points_list: [(x1,y1), (x2,y2), ...]  每4个点为一段曲线
    #     """
    #     if len(points_list) < 4:
    #         raise ValueError("至少需要4个点才能生成一段曲线")
    #     if len(points_list) % 4 != 0:
    #         raise ValueError("点的数量必须是4的倍数")

    #     for i in range(0, len(points_list), 4):
    #         p0, p1, p2, p3 = points_list[i:i+4]
    #         self.add_segment(p0, p1, p2, p3)


    def linear_bezier(self, p0, p1, num_points=100):
        """
        向量化计算一次贝塞尔曲线上的点
        p0, p1: 起点和终点，格式为(x, y)
        num_points: 采样点数量
        返回: numpy数组，形状为(num_points, 2)
        """
        t = np.linspace(0, 1, num_points, dtype=np.float64)
        x = (1 - t) * p0[0] + t * p1[0]
        y = (1 - t) * p0[1] + t * p1[1]

        self.trajectory = np.column_stack((x, y))
        # print(self.trajectory)
        self.draw_trajectory()
        return self.trajectory

    # def quadratic_bezier(self, p0, p1, p2, t):
    #     """计算二次贝塞尔曲线上的点"""
    #     x = (
    #         (1 - t) ** 2 * p0[0]
    #         + 2 * (1 - t)  * t * p1[0]
    #         + t ** 2 * p2[0]
    #     )
    #     y = (
    #         (1 - t) ** 2 * p0[1]
    #         + 2 * (1 - t) * t * p1[1]
    #         + t ** 2 * p2[1]
    #     )
    #     return (x, y)


    # def cubic_bezier(self, p0, p1, p2, p3, t):
    #     """计算三次贝塞尔曲线上的点"""
    #     x = (
    #         (1 - t) ** 3 * p0[0]
    #         + 3 * (1 - t) ** 2 * t * p1[0]
    #         + 3 * (1 - t) * t ** 2 * p2[0]
    #         + t ** 3 * p3[0]
    #     )
    #     y = (
    #         (1 - t) ** 3 * p0[1]
    #         + 3 * (1 - t) ** 2 * t * p1[1]
    #         + 3 * (1 - t) * t ** 2 * p2[1]
    #         + t ** 3 * p3[1]
    #     )
    #     return (x, y)
    #================向量化，三次贝塞尔曲线================
    def bezier_curve(self, p0, p1, p2, p3, num_points=1000):
        """计算三次贝塞尔曲线上的点"""
        t = np.linspace(0, 1, num_points, dtype=np.float64)

        x = (
            (1 - t) ** 3 * p0[0]
            + 3 * (1 - t) ** 2 * t * p1[0]
            + 3 * (1 - t) * (t ** 2) * p2[0]
            + (t ** 3) * p3[0]
        )
        y = (
            (1 - t) ** 3 * p0[1]
            + 3 * (1 - t) ** 2 * t * p1[1]
            + 3 * (1 - t) * (t ** 2) * p2[1]
            + (t ** 3) * p3[1]
        )

        self.trajectory = np.column_stack((x, y))
        self.draw_trajectory()
        return self.trajectory  # (num_points, 2)

    def draw_trajectory(self):
        # 在这里绘制轨迹， 先定义一个surface，把曲线画在surface上
        self.trajectory_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        # pygame.draw.lines(self.trajectory_surface, (0, 255, 255), False, self.trajectory.astype(int), 2) # 用直线连接的，不够平滑
        for point in self.trajectory:
            pygame.draw.circle(self.trajectory_surface, (0, 255, 255), point.astype(int), 1)
        # return np.column_stack((x, y))  # (num_points, 2)


    def draw_bezier(self, screen):
        return
        # 每次循环直接blit这个surface，而不是重新绘制曲线
        screen.blit(self.trajectory_surface, (0, 0))

    # def draw(self):
    #     """用pygame绘制地图曲线"""
    #     pygame.init()
    #     screen = pygame.display.set_mode((self.width, self.height))
    #     pygame.display.set_caption("贝塞尔地图轨迹")
    #     clock = pygame.time.Clock()

    #     running = True
    #     while running:
    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT:
    #                 running = False

    #         screen.fill((240, 240, 240))

    #         # 绘制每段曲线
    #         for seg in self.segments:
    #             p0, p1, p2, p3 = seg
    #             points = []
    #             for i in range(101):
    #                 t = i / 100
    #                 points.append(self.cubic_bezier(p0, p1, p2, p3, t))
    #             pygame.draw.lines(screen, (0, 100, 200), False, points, 3)

    #         pygame.display.flip()
    #         clock.tick(60)

    #     pygame.quit()
    #     sys.exit()


# 使用示例
if __name__ == "__main__":
    my_map = Map(1200, 800)

    # 方式1：单独添加
    my_map.add_segment((100, 700), (400, 100), (800, 900), (1100, 200))
    my_map.add_segment((1100, 200), (900, 500), (600, 300), (300, 600))

    # 方式2：批量添加
    points_list = [
        (300, 600), (200, 400), (500, 200), (1000, 500),
        (1000, 500), (1100, 700), (800, 750), (200, 300)
    ]
    my_map.add_segments_from_list(points_list)

    # 获取所有曲线的坐标点
    points = my_map.get_curve_points()
    print("曲线总点数:", len(points))
    print("前10个点:", points[:10])

    # 绘制
    my_map.draw()