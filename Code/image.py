import pygame

pygame.init()

# 创建窗口
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Sprite Animation Example")
clock = pygame.time.Clock()

# 动画帧路径
image_paths = [
    'images/Character/0.png',
    'images/Character/1.png',
    'images/Character/2.png',
    'images/Character/3.png',
    'images/Character/4.png',
    'images/Character/5.png'
]

# 创建 Sprite
player = pygame.sprite.Sprite()
player.frames = [pygame.image.load(path).convert_alpha() for path in image_paths]  # 所有帧
player.frame_index = 0  # 当前帧编号
player.image = player.frames[player.frame_index]  # 当前显示的帧
player.rect = player.image.get_rect()
player.rect.topleft = (100, 100)

# 动画控制变量
player.frame_delay = 120  # 每帧持续时间（毫秒）
player.last_update = pygame.time.get_ticks()

# 自定义 update 方法
def player_update():
    now = pygame.time.get_ticks()
    if now - player.last_update > player.frame_delay:
        player.frame_index = (player.frame_index + 1) % len(player.frames)
        player.image = player.frames[player.frame_index]
        player.last_update = now

player.update = player_update  # 给 Sprite 绑定 update 方法

# 创建 Group
all_sprites = pygame.sprite.Group(player)

# 游戏循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()  # 调用 player_update()

    screen.fill((30, 30, 30))
    all_sprites.draw(screen)
    pygame.display.flip()

    clock.tick(60)

pygame.quit()

# import pygame

# pygame.init()
# screen = pygame.display.set_mode((800, 600))
# pygame.display.set_caption("忽略纯色背景")

# # 加载 PNG（无透明通道）
# sprite = pygame.image.load('images/Character/0.png').convert()  # 用 convert() 而不是 convert_alpha()

# # 获取左上角像素颜色（假设背景是纯色）
# bg_color = sprite.get_at((0, 0))

# # 设置透明色
# sprite.set_colorkey(bg_color)

# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     screen.fill((50, 50, 50))  # 背景色
#     screen.blit(sprite, (100, 100))
#     pygame.display.flip()

# pygame.quit()