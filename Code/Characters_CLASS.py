import pygame

from CONFIG_in_winsys import WIDTH, HEIGHT

class AnimatedSprite(pygame.sprite.Sprite):
    def __init__( self, image_paths, flip_flag=False, bg_flag=False, position=(0, 0), frame_delay=100, scale_flag=False, scale_size=(WIDTH, HEIGHT)):  
        super().__init__()
        self.scale_flag       = scale_flag
        self.flip_flag        = flip_flag
        self.bg_flag          = bg_flag
        self.current_point    = 0
        self.current_position = 0

        self.frames = [ pygame.image.load(path).convert_alpha() for path in image_paths ] # 加载动画所有帧image
        if self.scale_flag:
            '''scale?'''
            self.frames = [pygame.transform.scale(frame, (scale_size)) for frame in self.frames]
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

    def keep_moving(self, waypoints, speed = 1):
        if self.current_point < len(waypoints):
            self.rect = self.image.get_rect(center = waypoints[self.current_point])
            self.current_point += speed
        else:
            self.current_point = len(waypoints)

    def manual_moving(self, waypoints, is_moving, speed = 1):

        if is_moving and self.current_position < len(waypoints):

            self.rect = self.image.get_rect(center = waypoints[self.current_position])
            self.current_position += speed
            return not is_moving
        
        if self.current_position >= len(waypoints):
            
            self.current_position = len(waypoints)
            print('到达终点')
            return not is_moving


    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_delay:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = self.frames[self.frame_index]
            self.last_update = now