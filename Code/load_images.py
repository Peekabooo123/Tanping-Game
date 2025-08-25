# import pygame
# pygame.init()

# # 窗口
# screen = pygame.display.set_mode((1000, 200))
# pygame.display.set_caption("Typing Game")

# # 字体
# font = pygame.font.SysFont(None, 36)

# # 目标文本
# target_text = "In the heart of the forest, sunlight filters through the leaves, creating a dappled pattern on the ground."
# user_input = ""

# # 颜色
# WHITE = (255, 255, 255)
# GREEN = (0, 255, 0)
# RED   = (255, 0, 0)

# running = True
# while running:
#     screen.fill((30, 30, 30))

#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_BACKSPACE:
#                 user_input = user_input[:-1]
#             elif event.key == pygame.K_RETURN:
#                 pass
#             else:
#                 user_input += event.unicode

#     # 绘制目标文本（逐字符对比）
#     x, y = 20, 50
#     for i, ch in enumerate(target_text):
#         if i < len(user_input):
#             if user_input[i] == ch:
#                 color = GREEN
#             else:
#                 color = RED
#         else:
#             color = WHITE
#         ch_surface = font.render(ch, True, color)
#         screen.blit(ch_surface, (x, y))
#         x += ch_surface.get_width()

#     # 绘制用户输入
#     input_surface = font.render(user_input, True, (0, 255, 255))
#     screen.blit(input_surface, (20, 100))

#     pygame.display.flip()

# pygame.quit()
import pygame
import time

# --- Constants ---
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BLUE = (173, 216, 230)
BACKGROUND_COLOR = (20, 30, 50)

class TypingApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Cursor Test")
        
        # --- Important: The font used for measuring MUST be the same as for rendering ---
        self.main_font = pygame.font.Font(None, 25) 
        self.typing_text = ""

    def draw_text(self):
        """Draws the text the user is typing."""
        text_surface = self.main_font.render(self.typing_text, True, WHITE)
        # We start drawing the text at the same start_x as the cursor calculation
        self.screen.blit(text_surface, (75, HEIGHT - 100))

    def flashing_cursor(self):
        """
        Draws a flashing cursor at the end of self.typing_text.
        """
        start_x = 75
        input_y = HEIGHT - 100

        # 1. Measure the width of the text that has been typed so far.
        text_width, text_height = self.main_font.size(self.typing_text)

        # 2. The cursor's X position is the starting point plus the measured text width.
        cursor_x = start_x + text_width

        # 3. Blinking logic
        if time.time() % 1 < 0.5:
            # Draw an I-beam style cursor
            pygame.draw.line(self.screen, LIGHT_BLUE, (cursor_x, input_y), (cursor_x, input_y + text_height), width=2)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.typing_text = self.typing_text[:-1]
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                    else:
                        self.typing_text += event.unicode

            # Drawing
            self.screen.fill(BACKGROUND_COLOR)
            self.draw_text()
            self.flashing_cursor()
            pygame.display.flip()

        pygame.quit()

# --- Run the App ---
if __name__ == '__main__':
    app = TypingApp()
    app.run()