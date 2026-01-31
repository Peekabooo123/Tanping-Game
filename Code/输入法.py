import os
os.environ["SDL_IME_SHOW_UI"] = "1"  # 让系统输入法候选框显示

import pygame
import sys

pygame.init()
pygame.key.start_text_input()

W, H = 800, 500
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("多行中文输入框示例 - pygame-ce / SDL2")

# 字体
font = pygame.font.SysFont("SimHei", 28)

# 输入框矩形
input_rect = pygame.Rect(50, 50, 700, 380)

# 内容 & 光标位置
lines = [""]
cursor_line = 0
cursor_col = 0

# 输入法组合串
composing_text = ""

# 滚动条参数
scroll_offset = 0
line_height = font.get_height()

clock = pygame.time.Clock()
caret_visible = True
caret_timer = 0
caret_interval = 500


def get_caret_xy():
    """计算光标在屏幕上的坐标（相对于 input_rect）"""
    y = cursor_line * line_height - scroll_offset
    prefix = lines[cursor_line][:cursor_col]
    x = font.size(prefix)[0]
    return input_rect.x + 5 + x, input_rect.y + 5 + y


def update_ime_rect():
    """让系统候选框出现在光标位置"""
    x, y = get_caret_xy()
    ime_rect = pygame.Rect(x, y, 30, line_height)
    pygame.key.set_text_input_rect(ime_rect)


def insert_text(text: str):
    """在光标处插入文字"""
    global cursor_col, cursor_line
    line = lines[cursor_line]
    lines[cursor_line] = line[:cursor_col] + text + line[cursor_col:]
    cursor_col += len(text)


def new_line():
    """换行"""
    global cursor_line, cursor_col
    line = lines[cursor_line]
    left, right = line[:cursor_col], line[cursor_col:]
    lines[cursor_line] = left
    lines.insert(cursor_line + 1, right)
    cursor_line += 1
    cursor_col = 0


def backspace():
    """退格"""
    global cursor_line, cursor_col
    if cursor_col > 0:
        line = lines[cursor_line]
        lines[cursor_line] = line[:cursor_col - 1] + line[cursor_col:]
        cursor_col -= 1
    elif cursor_line > 0:
        # 合并上一行
        prev_len = len(lines[cursor_line - 1])
        lines[cursor_line - 1] += lines[cursor_line]
        del lines[cursor_line]
        cursor_line -= 1
        cursor_col = prev_len


def move_cursor(dx, dy):
    """光标移动"""
    global cursor_line, cursor_col
    cursor_line = max(0, min(cursor_line + dy, len(lines) - 1))
    cursor_col = max(0, min(cursor_col + dx, len(lines[cursor_line])))


def ensure_visible():
    """让光标可见（滚动条自动调整）"""
    global scroll_offset
    caret_y = cursor_line * line_height
    if caret_y - scroll_offset < 0:
        scroll_offset = caret_y
    elif caret_y - scroll_offset > input_rect.height - line_height:
        scroll_offset = caret_y - (input_rect.height - line_height)


while True:
    dt = clock.tick(60)
    caret_timer += dt
    if caret_timer >= caret_interval:
        caret_timer = 0
        caret_visible = not caret_visible

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.TEXTEDITING:
            composing_text = event.text

        elif event.type == pygame.TEXTINPUT:
            insert_text(event.text)
            composing_text = ""

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                if composing_text:
                    composing_text = composing_text[:-1]
                else:
                    backspace()
            elif event.key == pygame.K_RETURN:
                new_line()
            elif event.key == pygame.K_LEFT:
                move_cursor(-1, 0)
            elif event.key == pygame.K_RIGHT:
                move_cursor(1, 0)
            elif event.key == pygame.K_UP:
                move_cursor(0, -1)
            elif event.key == pygame.K_DOWN:
                move_cursor(0, 1)

    ensure_visible()
    update_ime_rect()

    # 绘制
    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, (245, 245, 245), input_rect, border_radius=8)
    pygame.draw.rect(screen, (200, 200, 200), input_rect, width=2, border_radius=8)

    y = input_rect.y + 5 - scroll_offset
    for i, line in enumerate(lines):
        txt = line
        if i == cursor_line and composing_text:
            txt = line[:cursor_col] + composing_text + line[cursor_col:]
        surf = font.render(txt, True, (0, 0, 0))
        screen.blit(surf, (input_rect.x + 5, y))
        y += line_height

    # 光标
    if caret_visible:
        x, y = get_caret_xy()
        if composing_text:
            x += font.size(composing_text)[0]
        pygame.draw.line(screen, (0, 0, 0), (x, y), (x, y + line_height), 2)

    pygame.display.flip()
