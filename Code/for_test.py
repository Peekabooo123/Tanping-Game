import pygame
import sys
import random
import time
from CONFIG import *
from particle import ParticleSystem
from audio import AudioManager

# 初始化pygame
pygame.init()


# 屏幕设置
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cops and Robbers -- A typing game")

# 字体设置 - 使用系统默认字体以支持中文
try:
    # 尝试使用微软雅黑或苹方字体（对中文支持较好的字体）
    title_font = pygame.font.SysFont("Microsoft YaHei" if sys.platform == "win32" else "PingFang SC", TITLE_FONT_SIZE)
    main_font = pygame.font.SysFont("Microsoft YaHei" if sys.platform == "win32" else "PingFang SC", MAIN_FONT_SIZE)
    small_font = pygame.font.SysFont("Microsoft YaHei" if sys.platform == "win32" else "PingFang SC", SMALL_FONT_SIZE)
except:
    # 如果找不到上述字体，退回到系统默认字体
    title_font = pygame.font.Font(None, TITLE_FONT_SIZE)
    main_font = pygame.font.Font(None, MAIN_FONT_SIZE)
    small_font = pygame.font.Font(None, SMALL_FONT_SIZE)

###########################游戏人物class################################
class Character:
    def __init__(self, x, y, character_type):
        self.clock = pygame.time.Clock()
        self.x = x
        self.y = y
        self.type = character_type
        self.speed = 1  # 默认移动速度
        self.width = 50  # 角色宽度
        self.height = 80  # 角色高度
    
    def move(self, dx, dy):
        # 限制角色在屏幕范围内移动
        self.x = max(25, min(WIDTH - 25, self.x + dx))
        self.y = max(40, min(HEIGHT - 40, self.y + dy))
    
    def draw(self, screen):
        if self.type == "thief":
            self.draw_thief(screen)
        else:
            self.draw_police(screen)
    
    def draw_thief(self, screen):
        # 身体 - 柔软的灰色
        pygame.draw.ellipse(screen, (160, 160, 160), (self.x - 25, self.y - 20, 50, 50))
        # 头部 - 更大更圆
        pygame.draw.circle(screen, (255, 230, 200), (self.x, self.y - 40), 25)
        # 可爱的面罩 - 紫色带白点
        pygame.draw.ellipse(screen, (120, 80, 180), (self.x - 20, self.y - 50, 40, 30))
        for i in range(5):  # 面罩上的白点装饰
            pygame.draw.circle(screen, (255, 255, 255), 
                            (self.x - 15 + i*10, self.y - 45 + (i%2)*10), 2)
        # 大大的眼睛 - 带高光
        pygame.draw.circle(screen, (255, 255, 255), (self.x - 10, self.y - 45), 8)
        pygame.draw.circle(screen, (255, 255, 255), (self.x + 10, self.y - 45), 8)
        pygame.draw.circle(screen, (50, 50, 150), (self.x - 10, self.y - 45), 4)
        pygame.draw.circle(screen, (50, 50, 150), (self.x + 10, self.y - 45), 4)
        pygame.draw.circle(screen, (255, 255, 255), (self.x - 12, self.y - 48), 2)
        pygame.draw.circle(screen, (255, 255, 255), (self.x + 8, self.y - 48), 2)
        # 腮红
        pygame.draw.circle(screen, (255, 150, 150), (self.x - 20, self.y - 35), 5)
        pygame.draw.circle(screen, (255, 150, 150), (self.x + 20, self.y - 35), 5)
        # 小嘴巴 - 惊讶表情
        pygame.draw.circle(screen, (255, 100, 100), (self.x, self.y - 30), 3)
        # 钱袋 - 更圆润
        pygame.draw.ellipse(screen, (180, 180, 50), (self.x + 10, self.y - 5, 20, 25))
        pygame.draw.line(screen, (120, 120, 30), (self.x + 20, self.y - 5), (self.x + 20, self.y - 15), 2)
        # 小手臂
        pygame.draw.ellipse(screen, (255, 230, 200), (self.x - 40, self.y - 10, 20, 15))
    
    def draw_police(self, screen):
        # 身体 - 明亮的蓝色
        pygame.draw.ellipse(screen, (80, 150, 255), (self.x - 25, self.y - 20, 50, 50))
        # 头部 - 更大更圆
        pygame.draw.circle(screen, (255, 230, 200), (self.x, self.y - 40), 25)
        # 可爱的警帽
        pygame.draw.rect(screen, (0, 80, 200), (self.x - 25, self.y - 60, 50, 25))
        pygame.draw.rect(screen, (0, 80, 200), (self.x - 15, self.y - 75, 30, 15))
        # 警徽 - 闪亮效果
        pygame.draw.circle(screen, (255, 215, 0), (self.x, self.y - 50), 8)
        pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y - 50), 8, 2)
        pygame.draw.line(screen, (255, 255, 255), (self.x - 5, self.y - 50), (self.x + 5, self.y - 50), 1)
        pygame.draw.line(screen, (255, 255, 255), (self.x, self.y - 55), (self.x, self.y - 45), 1)
        # 大大的眼睛 - 带高光
        pygame.draw.circle(screen, (255, 255, 255), (self.x - 10, self.y - 45), 8)
        pygame.draw.circle(screen, (255, 255, 255), (self.x + 10, self.y - 45), 8)
        pygame.draw.circle(screen, (50, 50, 50), (self.x - 10, self.y - 45), 4)
        pygame.draw.circle(screen, (50, 50, 50), (self.x + 10, self.y - 45), 4)
        pygame.draw.circle(screen, (255, 255, 255), (self.x - 12, self.y - 48), 2)
        pygame.draw.circle(screen, (255, 255, 255), (self.x + 8, self.y - 48), 2)
        # 腮红
        pygame.draw.circle(screen, (255, 150, 150), (self.x - 20, self.y - 35), 5)
        pygame.draw.circle(screen, (255, 150, 150), (self.x + 20, self.y - 35), 5)
        # 微笑
        pygame.draw.arc(screen, (50, 50, 50), (self.x - 12, self.y - 38, 24, 20), 0, 3.14, 2)
        # 小手铐
        pygame.draw.rect(screen, (180, 180, 200), (self.x + 30, self.y - 10, 15, 8))
        pygame.draw.circle(screen, (200, 200, 220), (self.x + 37, self.y - 10), 3)
######################################################################

################################地图类################################

class Map:
    def __init__(self):
        self.road_curve_points = self.generate_road_curve()
        self.road_width = 100

    def generate_road_curve(self):
        points = []

        return points

    def draw(self, screen):
        for i in range(len(self.road_curve_points) - 1):
            start = self.road_curve_points[i]
            end = self.road_curve_points[i + 1]
            pygame.draw.line(screen, (200, 200, 200), start, end, self.road_width)

######################################################################


# 游戏参数
class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.police_pos = ROAD_CURVE_POINTS[0][0]  # 起点x坐标
        self.thief_pos = self.police_pos + 50
        self.thief_speed = INITIAL_THIEF_SPEED
        
        self.typing_text = "TanTanTan"
        self.current_char = 0
        self.score = 0
        self.level = 1
        self.target_text = self.generate_text()

        self.game_over = False
        self.win = False
        
        self.start_time = time.time()
        self.typed_chars = 0
        self.correct_chars = 0
        self.background_x = 0
        self.particle_system = ParticleSystem()
        # self.audio = AudioManager()  # 暂时注释掉音频管理器
        self.smooth_police_pos = 100.0  # 添加平滑移动

        # 在游戏初始化部分
        self.thief = Character(WIDTH/4, HEIGHT/2, "thief")
        self.police = Character(3*WIDTH/4, HEIGHT/2, "police")
        # 绘制渐变背景
    def draw_gradient_background(self):
        for y in range(HEIGHT):
            # 从深蓝色到黑色的渐变
            color = (
                max(0, DARK_BLUE[0] * (HEIGHT - y) / HEIGHT),
                max(0, DARK_BLUE[1] * (HEIGHT - y) / HEIGHT),
                max(0, DARK_BLUE[2] * (HEIGHT - y) / HEIGHT)
            )
            pygame.draw.line(screen, color, (0, y), (WIDTH, y))

    def generate_text(self):
        # 根据等级生成不同难度的文本
        # 随着等级提高，文本长度增加
        length = min(5 + self.level, 15)
        text = ""
        for _ in range(length):
            text += random.choice(WORD_LIST) + " "
        return text.strip()

    # 绘制打字区域
    def draw_typing_area(self):
        # 绘制背景
        pygame.draw.rect(screen, (30, 40, 70), (50, HEIGHT - 150, WIDTH - 100, 100)) # 矩形背景
        pygame.draw.rect(screen, (60, 70, 120), (50, HEIGHT - 150, WIDTH - 100, 100), 3) # 矩形边框,3表示边框宽度

        # 绘制目标文本
        text_x = 70
        for i, char in enumerate(game.target_text):
            color = GREEN if i < 10 else WHITE
            char_surface = main_font.render(char, True, color)  
            screen.blit(char_surface, (text_x, HEIGHT - 140))

            text_x += main_font.size(char)[0]
        
        # # 绘制已输入文本
        typed_surface = main_font.render(game.typing_text, True, YELLOW)
        screen.blit(typed_surface, (70, HEIGHT - 100))
        
        # 绘制光标
        if int(time.time() * 2) % 2 == 0:
            pygame.draw.line(screen, YELLOW, (70, HEIGHT - 100), 
                            (70, HEIGHT - 70), 2)
    
    # 绘制赛道
    def draw_race_track(self):
        # 绘制主要道路
        for i in range(len(ROAD_CURVE_POINTS) - 1):
            start = ROAD_CURVE_POINTS[i]
            end = ROAD_CURVE_POINTS[i + 1]
        
        # 绘制起点和终点
        start_point = ROAD_CURVE_POINTS[0]
        end_point = ROAD_CURVE_POINTS[-1]
        
        # 起点线
        pygame.draw.line(screen, WHITE,
                        (start_point[0], start_point[1] - ROAD_WIDTH//2),
                        (start_point[0], start_point[1] + ROAD_WIDTH//2), 5)
        
        # 终点线和旗帜
        pygame.draw.line(screen, RED,
                        (end_point[0], end_point[1] - ROAD_WIDTH//2),
                        (end_point[0], end_point[1] + ROAD_WIDTH//2), 5)
    
    # 主游戏循环
    def run_game(self):
        running = True
        while running:
            # 事件处理
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    # 退出游戏
                    pygame.quit()
                    sys.exit()
 
            # 清空屏幕
            screen.fill((0, 0, 0))
            
            # 绘制渐变背景
            game.draw_gradient_background()

            game.draw_typing_area() #绘制打字区域
            game.draw_race_track() #绘制赛道和地图
            

            game.thief.draw(screen)
            game.police.draw(screen)
            game.police.move(-game.thief.speed, 0)

            # 更新显示
            pygame.display.flip()
            
            # 控制游戏帧率 (120 FPS)
            self.clock.tick(120)

    def reset(self):
        self.__init__()

if __name__ == "__main__":

    game = Game()
    game.run_game()
