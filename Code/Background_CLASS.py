import pygame

from CONFIG_in_winsys import HEIGHT, WIDTH

class BackgroundSprite(pygame.sprite.Sprite):
    def __init__( self, image_paths, scale_flag=True, scale_size=(WIDTH, HEIGHT), flip_flag=False, bg_flag=False, position=(0, 0), frame_delay=100):
        super().__init__()
        self.scale_flag       = scale_flag
        self.flip_flag        = flip_flag
        self.bg_flag          = bg_flag
        self.position         = position

        # 加载background
        self.background = [ pygame.image.load(path).convert_alpha() for path in image_paths ] # 加载动画所有帧image
        if self.scale_flag:
            '''scale?'''
            self.background = [pygame.transform.scale(frame, (scale_size)) for frame in self.background]
        if self.flip_flag:
          self.background = [pygame.transform.flip(frame, True, False) for frame in self.background]  # 水平翻转 (如果需要的话)

        if self.bg_flag:
          # 去除素材背景
          bg_color = [frame.get_at((0, 0)) for frame in self.background]
          [frame.set_colorkey(colorkey) for frame, colorkey in zip(self.background, bg_color)]


        self.frame_index = 0                         # 当前帧编号
        self.image = self.background[self.frame_index]   # 当前显示的帧

        self.rect = self.image.get_rect(topleft = self.position)

        self.frame_delay = frame_delay
        self.last_update = pygame.time.get_ticks()

    def keep_moving(self):
        pass

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_delay:
            self.frame_index = (self.frame_index + 1) % len(self.background)
            self.image = self.background[self.frame_index]
            self.last_update = now
