import pygame
import sys
import random
import time
from config import *

#################################################################################
#################################################################################

# 游戏参数
class Game:
    def __init__(self):
        
        pygame.init()
        pygame.display.set_caption("Cops and Robbers -- A typing game")
        self.exception_process()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.background = (100,100,100)  # 设置背景颜色

        self.position   = CHARACTER_SETTINGS['A']['position']
        self.speed      = CHARACTER_SETTINGS['A']['speed']
        self.character  = self.load_character()

        self.score = 0
        self.level = 1
        self.diction_library = self.generate_text()

        self.typing_text = ""
        self.current_char = 0

        self.moving_LEFT = False
        self.moving_RIGHT = False
        self.moving_UP = False
        self.moving_DOWN = False
        self.deleting_flag = False

        self.game_over = False
        self.win = False
        
        self.start_time = time.time()

        self.correct_chars = 0
        self.background_x = 0

        self.smooth_police_pos = 100.0  # 添加平滑移动

    def generate_text(self):
        text = WORD_LIST[0]

        return text.strip()
    
    def typing_area(self):
        # 绘制背景
        pygame.draw.rect(self.screen, (30, 40, 70), (50, HEIGHT - 150, WIDTH - 100, 100))
        pygame.draw.rect(self.screen, (60, 70, 120), (50, HEIGHT - 150, WIDTH - 100, 100), 3)
        self.flashing_cursor() # 绘制cursor光标


        # 第一行（目标字符串）
        ch_surface = self.main_font.render(self.diction_library, True, WHITE)
        self.screen.blit(ch_surface, (70, HEIGHT-140))

        # 第二行（用户输入）
        ch_surface = self.main_font.render(self.typing_text, True, (0, 255, 255))
        self.screen.blit(ch_surface, (70, HEIGHT-100))

    def flashing_cursor(self):
      start_x = 75
      input_y = HEIGHT - 100
      text_width, text_height = self.main_font.size(self.typing_text)
      # 光标闪烁
      if int(time.time() * 2) % 2 == 0:
          cursor_x = start_x + text_width

          # shadow
          pygame.draw.line(self.screen, BLACK, (cursor_x+1, input_y+3), (cursor_x+5, input_y + 3), width = 2)     # -
          pygame.draw.line(self.screen, BLACK, (cursor_x+3, input_y+3), (cursor_x+3, input_y + 28+3), width = 2)  # |
          pygame.draw.line(self.screen, BLACK, (cursor_x+1, input_y+28+3), (cursor_x+5, input_y+28+3), width = 2) # -
          # cursor
          pygame.draw.line(self.screen, LIGHT_BLUE, (cursor_x-2, input_y), (cursor_x+2, input_y), width = 2)              # -
          pygame.draw.line(self.screen, LIGHT_BLUE, (cursor_x, input_y), (cursor_x, input_y + 28), width = 1)             # |
          pygame.draw.line(self.screen, LIGHT_BLUE, (cursor_x-2, input_y + 28), (cursor_x+2, input_y+ 28), width = 2)     # -

        #pygame.draw.line(surface,     color,       start_pos,           end_pos,           width=1)

    def functions(self):
        print("这是functions方法中的输出字符串。")

    def load_character(self):
        character = pygame.image.load("images\Dragon - Fully Animated\Attack 1/001.png").convert_alpha()  # 加载角色图像
        character = pygame.transform.scale(character, (character.get_width() // 3, character.get_height() // 3))  # 缩放
        flipped_character = pygame.transform.flip(character, True, False)  # 水平翻转（左右）

        self.character_position = flipped_character.get_rect(midleft = self.position) # 让图片居中

        return flipped_character
    
    def moving(self):
        if self.moving_LEFT:
            self.character_position.x -= self.speed
        if self.moving_RIGHT:
            self.character_position.x += self.speed
        if self.moving_UP:
            self.character_position.y -= self.speed
        if self.moving_DOWN:
            self.character_position.y += self.speed

    def deleting(self):
        if self.deleting_flag:
            self.typing_text = self.typing_text[:-1]

    def run_game(self):
        while not self.game_over:
          self.check_events()
          self.moving()
          # self.deleting()
          self.screen.fill(self.background)
          self.screen.blit(self.character, self.character_position)  # 使用 rect 位置绘制
          self.typing_area()
          pygame.display.flip() # 一次性更新整个屏幕
          self.clock.tick(FPS)

    def check_events(self):
        for event in pygame.event.get():
          if event.type == pygame.QUIT:
              self.game_over = True
              pygame.quit()
              sys.exit()

          elif event.type == pygame.KEYDOWN:
              self.key_down_events(event)

          elif event.type == pygame.KEYUP:
              self.key_up_events(event)

    def key_down_events(self,event):
        if event.key == pygame.K_RIGHT:
            self.moving_RIGHT = True
        elif event.key == pygame.K_LEFT:
            self.moving_LEFT = True 
        elif event.key == pygame.K_UP:
            self.moving_UP = True
        elif event.key == pygame.K_DOWN:
            self.moving_DOWN = True

        elif event.key == pygame.K_BACKSPACE:
            self.deleting_flag = True
            self.deleting()
        else:
            self.typing_text += event.unicode

    def key_up_events(self,event):
        if event.key == pygame.K_RIGHT:
            self.moving_RIGHT = False
        elif event.key == pygame.K_LEFT:
            self.moving_LEFT = False
        elif event.key == pygame.K_UP:
            self.moving_UP = False
        elif event.key == pygame.K_DOWN:
            self.moving_DOWN = False

        elif event.key == pygame.K_BACKSPACE:
            self.deleting_flag = False
        else:
            print(event.unicode)

    def exception_process(self):
      try:
        # 尝试使用微软雅黑或苹方字体（对中文支持较好的字体）
        self.title_font = pygame.font.SysFont("Microsoft YaHei" if sys.platform == "win32" else "PingFang SC", TITLE_FONT_SIZE)
        self.main_font = pygame.font.SysFont("Microsoft YaHei" if sys.platform == "win32" else "PingFang SC", MAIN_FONT_SIZE)
        self.small_font = pygame.font.SysFont("Microsoft YaHei" if sys.platform == "win32" else "PingFang SC", SMALL_FONT_SIZE)
      except:
        # 如果找不到上述字体，退回到系统默认字体
        self.title_font = pygame.font.Font(None, TITLE_FONT_SIZE)
        self.main_font = pygame.font.Font(None, MAIN_FONT_SIZE)
        self.small_font = pygame.font.Font(None, SMALL_FONT_SIZE)

if __name__ == "__main__":
    game = Game()
    game.run_game()