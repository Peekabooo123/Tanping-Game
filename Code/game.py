import pygame
import sys
import random
import time
from pygame import mixer
from config import *
from particle import ParticleSystem
from audio import AudioManager

# 初始化pygame
pygame.init()
mixer.init()

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

# 游戏参数
class Game:
    def __init__(self):
        self.police_pos = ROAD_CURVE_POINTS[0][0]  # 起点x坐标
        self.thief_pos = self.police_pos + 50
        self.thief_speed = INITIAL_THIEF_SPEED
        
        self.typing_text = ""
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
        
    def generate_text(self):
        # 根据等级生成不同难度的文本
        # 随着等级提高，文本长度增加
        length = min(5 + self.level, 15)
        text = ""
        for _ in range(length):
            text += random.choice(WORD_LIST) + " "
        return text.strip()
    
    def reset(self):
        self.__init__()
        
    def reset(self):
        self.__init__()

# 创建游戏实例
game = Game()

# 绘制渐变背景
def draw_gradient_background():
    for y in range(HEIGHT):
        # 从深蓝色到黑色的渐变
        color = (
            max(0, DARK_BLUE[0] * (HEIGHT - y) / HEIGHT),
            max(0, DARK_BLUE[1] * (HEIGHT - y) / HEIGHT),
            max(0, DARK_BLUE[2] * (HEIGHT - y) / HEIGHT)
        )
        pygame.draw.line(screen, color, (0, y), (WIDTH, y))

# 绘制赛道
def draw_race_track():
    # 绘制主要道路
    for i in range(len(ROAD_CURVE_POINTS) - 1):
        start = ROAD_CURVE_POINTS[i]
        end = ROAD_CURVE_POINTS[i + 1]
        
        # 绘制道路主体
        points = []
        for offset in [-ROAD_WIDTH//2, ROAD_WIDTH//2]:
            points.append((start[0], start[1] + offset))
            points.append((end[0], end[1] + offset))
        
        pygame.draw.polygon(screen, DECORATION_COLORS[0], points)
        
        # 绘制道路分隔线
        pygame.draw.line(screen, WHITE, start, end, 2)
        
        # 绘制道路标记
        num_marks = 10
        for j in range(num_marks):
            t = j / (num_marks - 1)
            x = start[0] + (end[0] - start[0]) * t
            y = start[1] + (end[1] - start[1]) * t
            mark_length = 20
            pygame.draw.rect(screen, YELLOW,
                           (x - game.background_x % 50, y - 2 + ROAD_WIDTH//4, mark_length, 4))
    
    # 绘制装饰元素
    for i in range(len(ROAD_CURVE_POINTS)):
        point = ROAD_CURVE_POINTS[i]
        # 绘制路标
        pygame.draw.circle(screen, WHITE, (point[0], point[1] - ROAD_WIDTH//2), 5)
        pygame.draw.circle(screen, WHITE, (point[0], point[1] + ROAD_WIDTH//2), 5)
    
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
    
    # 绘制终点旗帜
    flag_height = ROAD_WIDTH//4
    for i in range(8):
        color = RED if i % 2 == 0 else WHITE
        points = [
            (end_point[0], end_point[1] - ROAD_WIDTH//2 + i*flag_height),
            (end_point[0] + 20, end_point[1] - ROAD_WIDTH//2 + (i+0.5)*flag_height),
            (end_point[0], end_point[1] - ROAD_WIDTH//2 + (i+1)*flag_height)
        ]
        pygame.draw.polygon(screen, color, points)

# 获取赛道上的Y坐标
def get_track_y(x):
    for i in range(len(ROAD_CURVE_POINTS) - 1):
        start = ROAD_CURVE_POINTS[i]
        end = ROAD_CURVE_POINTS[i + 1]
        if start[0] <= x <= end[0]:
            # 计算插值
            t = (x - start[0]) / (end[0] - start[0])
            return start[1] + (end[1] - start[1]) * t
    return HEIGHT//2  # 默认值

# 绘制角色
def draw_characters():
    # 获取角色在赛道上的Y坐标
    thief_y = get_track_y(game.thief_pos)
    police_y = get_track_y(game.police_pos)
    
    # 绘制小偷
    pygame.draw.rect(screen, RED, (game.thief_pos - 20, thief_y - 20, 40, 40))
    pygame.draw.circle(screen, (200, 100, 100), (game.thief_pos, thief_y - 40), 15)
    
    # 绘制警察
    pygame.draw.rect(screen, BLUE, (game.police_pos - 20, police_y - 20, 40, 40))
    pygame.draw.circle(screen, LIGHT_BLUE, (game.police_pos, police_y - 40), 15)
    
    # 绘制眼睛
    pygame.draw.circle(screen, WHITE, (game.thief_pos - 5, thief_y - 43), 5)
    pygame.draw.circle(screen, WHITE, (game.police_pos + 5, police_y - 43), 5)
    pygame.draw.circle(screen, BLACK, (game.thief_pos - 5, thief_y - 43), 2)
    pygame.draw.circle(screen, BLACK, (game.police_pos + 5, police_y - 43), 2)

# 绘制打字区域
def draw_typing_area():
    # 绘制背景
    pygame.draw.rect(screen, (30, 40, 70), (50, HEIGHT - 150, WIDTH - 100, 100))
    pygame.draw.rect(screen, (60, 70, 120), (50, HEIGHT - 150, WIDTH - 100, 100), 3)
    
    # 绘制目标文本
    text_x = 70
    for i, char in enumerate(game.target_text):
        color = GREEN if i < game.current_char else WHITE
        if i == game.current_char:
            pygame.draw.rect(screen, (100, 100, 150), (text_x - 2, HEIGHT - 140, 20, 30))
        char_surface = main_font.render(char, True, color)
        screen.blit(char_surface, (text_x, HEIGHT - 140))
        text_x += main_font.size(char)[0]
    
    # 绘制已输入文本
    typed_surface = main_font.render(game.typing_text, True, YELLOW)
    screen.blit(typed_surface, (70, HEIGHT - 100))
    
    # 绘制光标
    if int(time.time() * 2) % 2 == 0:
        cursor_x = 70 + main_font.size(game.typing_text[:game.current_char])[0]
        pygame.draw.line(screen, YELLOW, (cursor_x, HEIGHT - 100), 
                         (cursor_x, HEIGHT - 70), 2)

# 绘制粒子效果
def draw_particles():
    game.particle_system.draw(screen)

# 绘制状态信息
def draw_status():
    # 绘制分数和等级
    score_text = small_font.render(f"Mark: {game.score}", True, YELLOW)
    level_text = small_font.render(f"Level: {game.level}", True, YELLOW)
    # 调整位置以确保文本不会被裁切
    score_width = score_text.get_width()
    level_width = level_text.get_width()
    screen.blit(score_text, (max(20, score_width//2), 20))
    screen.blit(level_text, (max(20, level_width//2), 50))
    
    # 绘制准确率
    if game.typed_chars > 0:
        accuracy = (game.correct_chars / game.typed_chars) * 100
    else:
        accuracy = 100
    accuracy_text = small_font.render(f"Accuracy: {accuracy:.1f}%", True, YELLOW)
    time_text = small_font.render(f"Time: {time.time() - game.start_time:.1f}Seconds", True, YELLOW)
    
    # 确保右上角的文本正确对齐且不会超出屏幕
    accuracy_width = accuracy_text.get_width()
    time_width = time_text.get_width()
    screen.blit(accuracy_text, (WIDTH - accuracy_width - 20, 20))
    screen.blit(time_text, (WIDTH - time_width - 20, 50))

# 绘制游戏结束画面
def draw_game_over():
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    screen.blit(overlay, (0, 0))
    
    if game.win:
        text = title_font.render("Gottcha!", True, GREEN)
    else:
        text = title_font.render("Lost!", True, RED)
    
    screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - 50))
    
    score_text = main_font.render(f"Final Mark: {game.score}", True, YELLOW)
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2 + 20))
    
    restart_text = main_font.render("Restart (Enter)", True, WHITE)
    screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 80))

# 主游戏循环
clock = pygame.time.Clock()
running = True

while running:
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if game.game_over:
                if event.key == pygame.K_RETURN:
                    game.reset()
            else:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_BACKSPACE:
                    if game.typing_text:
                        # 删除最后一个字符
                        game.typing_text = game.typing_text[:-1]
                        # 重新检查已输入的文本与目标文本的匹配情况
                        matched_chars = 0
                        for i, (typed, target) in enumerate(zip(game.typing_text, game.target_text)):
                            if typed == target:
                                matched_chars = i + 1
                            else:
                                break
                        game.current_char = matched_chars
                elif event.key == pygame.K_RETURN:
                    game.typing_text = ""
                    game.current_char = 0
                else:
                    # 只处理可打印字符
                    if event.unicode.isprintable() and len(event.unicode) == 1:
                        game.typed_chars += 1
                        game.typing_text += event.unicode
                        
                        # 检查输入是否正确
                        if game.current_char < len(game.target_text) and event.unicode == game.target_text[game.current_char]:
                            game.correct_chars += 1
                            game.current_char += 1
                            # 警察前进
                            game.police_pos += 5 + game.level * 0.5
                            # game.audio.play('correct')
                            # 添加粒子效果
                            game.particle_system.emit(game.police_pos + 20, HEIGHT//2 + 60, BLUE)
                        else:
                            # game.audio.play('wrong')
                            # 添加粒子效果
                            game.particle_system.emit(game.police_pos + 20, HEIGHT//2 + 60, RED)
                        
                        # 如果输入完成整个文本
                        if game.current_char >= len(game.target_text):
                            game.score += 10 * game.level
                            game.level += 1
                            game.target_text = game.generate_text()
                            game.typing_text = ""
                            game.current_char = 0
    
    # 更新游戏状态
    if not game.game_over:
        # 小偷移动
        game.thief_pos += game.thief_speed + game.level * LEVEL_SPEED_MULTIPLIER
        
        # 平滑警察移动
        target_police_pos = game.police_pos
        game.smooth_police_pos += (target_police_pos - game.smooth_police_pos) * 0.2
        game.police_pos = int(game.smooth_police_pos)
        
        # 平滑背景滚动
        game.background_x = (game.background_x - (game.thief_speed + game.level * LEVEL_SPEED_MULTIPLIER) * 0.5) % 50
        
        # 更新粒子
        game.particle_system.update()
        
        # 检查游戏结束条件
        finish_line = ROAD_CURVE_POINTS[-1][0]
        if game.thief_pos >= finish_line:
            game.game_over = True
            # game.audio.play('lose')
        
        if game.police_pos >= game.thief_pos - 30:
            game.game_over = True
            game.win = True
            # game.audio.play('win')
    
    # 绘制游戏
    draw_gradient_background()
    draw_race_track()
    draw_particles()
    draw_characters()
    draw_typing_area()
    draw_status()
    
    if game.game_over:
        draw_game_over()
    
    # 更新屏幕
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()