import pygame
import math
from CONFIG_in_winsys import LETTER_HEIGHT, LIGHT_BLUE, WORD_ORIGIN_COORDINATES_X, TYPED_WORDS_ORIGIN_COORDINATES_X, TYPED_WORDS_ORIGIN_COORDINATES_Y

class WordClass:
    def __init__(self, position):
        """
        text: 初始显示的字符串
        font_path: 字体文件路径（.ttf）
        font_size: 字号
        color: (R, G, B) 或 (R, G, B, A)
        position: (x, y) 坐标
        """
        self.position = pygame.math.Vector2(position) # 向量化坐标元组，方便控制移动

    def build_cursor(self):
        """
        绘制一个颜色渐变闪烁的矩形光标
        :param cursor_x: 光标左上角X坐标
        :param cursor_y: 光标左上角Y坐标
        :param blink_speed: 闪烁速度（越大闪烁越快）
        """
        # 获取时间（毫秒）
        blink_speed = 15
        t = pygame.time.get_ticks() / 1000.0  # 转换为秒

        # 计算alpha（0~255之间波动）
        alpha = int((math.sin(t * blink_speed) + 1) / 2 * 255)

        # 创建带透明通道的Surface
        self.cursor_surface = pygame.Surface((2, LETTER_HEIGHT), pygame.SRCALPHA)
        self.cursor_surface.fill((*LIGHT_BLUE, alpha))  # RGB + Alpha

        # 绘制到屏幕
        self.cursor_x = TYPED_WORDS_ORIGIN_COORDINATES_X
        self.cursor_rect = self.cursor_surface.get_rect()
    
    def draw_cursor(self,screen,typed_text, color):
        # 获取时间（毫秒）
        blink_speed = 10
        t = pygame.time.get_ticks() / 1000.0  # 转换为秒
        # 计算alpha（0~255之间波动）
        alpha = int((math.sin(t * blink_speed) + 1) / 2 * 255)

        self.cursor_surface.fill((*LIGHT_BLUE, alpha))  # RGB + Alpha
        font = pygame.font.SysFont(["Microsoft YaHei", "Arial"], 36)

        word_width = font.size(typed_text)[0]
        self.cursor_x = TYPED_WORDS_ORIGIN_COORDINATES_X + word_width
        self.cursor_rect.topleft = (self.cursor_x,TYPED_WORDS_ORIGIN_COORDINATES_Y + 12)
        screen.blit(self.cursor_surface, self.cursor_rect)
        self.build_typed_text(screen, typed_text, color)
        

    def load_text(self, text, font_size, color, font_path=None):
        self.text = text
        self.font_path = font_path
        self.font_size = font_size
        self.color = color

        if self.font_path: # 如果有字体文件
            font = pygame.font.Font(self.font_path, self.font_size)
        else:
            font = pygame.font.SysFont(["Microsoft YaHei", "Arial"], 36)
        self.rendered_surface = font.render(self.text, True, self.color)

        self.rendered_surface_rec = self.rendered_surface.get_rect(topleft=self.position) # 获取矩形对象
        return self.rendered_surface, self.rendered_surface_rec

    def build_typed_text(self,screen, typed_text, color):
        font = pygame.font.SysFont(["Microsoft YaHei", "Arial"], 36)

        self.typed_text = font.render(typed_text, True, color)
        self.typed_text_rec = self.typed_text.get_rect(topleft=(TYPED_WORDS_ORIGIN_COORDINATES_X,TYPED_WORDS_ORIGIN_COORDINATES_Y)) # 获取矩形对象

        screen.blit(self.typed_text, self.typed_text_rec)
    # def update_text(self, new_text):
    #     """更新文本内容"""
    #     self.text = new_text
    #     self.rendered_surface = self.font.render(self.text, True, self.color)

    # def update_color(self, new_color):
    #     """更新颜色"""
    #     self.color = new_color
    #     self.rendered_surface = self.font.render(self.text, True, self.color)

    # def update_font(self, new_font_path, new_size=None):
    #     """更新字体和字号"""
    #     if new_size:
    #         self.font_size = new_size
    #     self.font_path = new_font_path
    #     self.font = pygame.font.Font(self.font_path, self.font_size)
    #     self.rendered_surface = self.font.render(self.text, True, self.color)

    # def update_position(self, new_position):
    #     """更新位置"""
    #     self.position = new_position
    #     self.rendered_surface_rec = self.rendered_surface.get_rect(center=self.position)

    # def draw(self, surface):
    #     """绘制到目标 surface"""
    #     self.position.x -= 1
    #     self.rendered_surface_rec = self.rendered_surface.get_rect(topleft=self.position)
    #     surface.blit(self.rendered_surface, self.rendered_surface_rec)

    def draw(self, surface,x,y, typed_text, color):
        """绘制到目标 surface，左边小于100的部分不显示"""
        self.draw_cursor(surface, typed_text, color)
        # 让文字向左移动
        if self.rendered_surface_rec.right < 100:
            return

        #   self.position.x += 1
        # if self.cursor_x >= 300:
        #     self.position.x -= 1

        self.rendered_surface_rec.topleft = self.position
        # print(self.rendered_surface_rec.right)

        # 定义裁剪区域（只显示 x >= 100 的部分）
        clip_rect = pygame.Rect(x, y, surface.get_width() - 2 * x, surface.get_height())

        # 保存原来的裁剪区域
        old_clip = surface.get_clip()

        # 设置裁剪区域
        surface.set_clip(clip_rect)

        # 绘制文字
        surface.blit(self.rendered_surface, self.rendered_surface_rec)

        # 恢复原来的裁剪区域
        surface.set_clip(old_clip)

    # def draw(self, surface):
    #   """绘制到目标 surface，x<100 的部分裁掉"""
    #   # 让文字向左移动
    #   self.position.x -= 1

    #   # 获取文字的矩形（位置）
    #   text_rect = self.rendered_surface.get_rect(topleft=self.position)

    #   # 如果文字完全在裁剪线左边，就不画
    #   if text_rect.right <= 100:
    #       return

    #   # 计算可见区域
    #   if text_rect.left < 100:
    #       # 裁掉左边部分
    #       cut_x = 100 - text_rect.left
    #       visible_width = text_rect.width - cut_x
    #       if visible_width > 0:
    #           visible_surface = self.rendered_surface.subsurface(
    #               (cut_x, 0, visible_width, text_rect.height)
    #           )
    #           surface.blit(visible_surface, (100, text_rect.top))
    #   else:
    #       # 完全在右边，直接画
    #       surface.blit(self.rendered_surface, text_rect)


    def event_handle(self, events):
        for event in events:
            if event.type == pygame.TEXTINPUT:
                pass

# 示例使用
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Dynamic Text Example")

    WORDS = WordClass(
        text="Hello Pyagem!dfskdflkj",
        font_size=36,
        color=(0,255,255),
        position=(100, 100)
    )

    clock = pygame.time.Clock()
    running = True
    counter = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        WORDS.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()