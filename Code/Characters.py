import pygame

class AnimatedSprite(pygame.sprite.Sprite):
    def __init__( self, image_paths,flip_flag,bg_flag, position, frame_delay=100):
        super().__init__()
        self.flip_flag = flip_flag
        self.bg_flag   = bg_flag

        self.frames = [ pygame.image.load(path).convert_alpha() for path in image_paths ] # 加载动画所有帧image
        if self.flip_flag:
          self.frames = [pygame.transform.flip(frame, True, False) for frame in self.frames]  # 水平翻转 (如果需要的话)

        if self.bg_flag:
          # 去除背景
          bg_color = [frame.get_at((0, 0)) for frame in self.frames]
          [frame.set_colorkey(colorkey) for frame, colorkey in zip(self.frames, bg_color)]

        self.frame_index = 0                         # 当前帧编号
        self.image = self.frames[self.frame_index]   # 当前显示的帧

        self.rect = self.image.get_rect(center = position)

        self.frame_delay = frame_delay
        self.last_update = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_delay:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = self.frames[self.frame_index]
            self.last_update = now