import pygame
import sys

class Map:
    def __init__(self, width=1200, height=800):
        self.width = width
        self.height = height
        self.segments = []  # 存储多段贝塞尔曲线的控制点
        self.all_points = []

    def add_segment(self, p0, p1, p2, p3):
        """添加一段贝塞尔曲线的控制点"""
        self.segments.append((p0, p1, p2, p3))

    def add_segments_from_list(self, points_list):
        """
        批量添加多段曲线
        points_list: [(x1,y1), (x2,y2), ...]  每4个点为一段曲线
        """
        if len(points_list) < 4:
            raise ValueError("至少需要4个点才能生成一段曲线")
        if len(points_list) % 4 != 0:
            raise ValueError("点的数量必须是4的倍数")

        for i in range(0, len(points_list), 4):
            p0, p1, p2, p3 = points_list[i:i+4]
            self.add_segment(p0, p1, p2, p3)

    def cubic_bezier(self, p0, p1, p2, p3, t):
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

    def get_curve_points(self, steps=100):
        """获取所有曲线的坐标点"""
        for seg in self.segments:
            p0, p1, p2, p3 = seg
            for i in range(steps + 1):
                t = i / steps
                self.all_points.append(self.cubic_bezier(p0, p1, p2, p3, t))
        return self.all_points

    def draw_bezier(self, screen, color, points,):
        points = self.all_points if len(self.all_points) > 0 else (0,0)
        pygame.draw.lines(screen, color, False, points, 2)

    def draw(self):
        """用pygame绘制地图曲线"""
        pygame.init()
        screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("贝塞尔地图轨迹")
        clock = pygame.time.Clock()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.fill((240, 240, 240))

            # 绘制每段曲线
            for seg in self.segments:
                p0, p1, p2, p3 = seg
                points = []
                for i in range(101):
                    t = i / 100
                    points.append(self.cubic_bezier(p0, p1, p2, p3, t))
                pygame.draw.lines(screen, (0, 100, 200), False, points, 3)

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
        sys.exit()


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