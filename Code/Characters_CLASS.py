import pygame

from CONFIG_in_winsys import WIDTH, HEIGHT

class AnimatedSprite(pygame.sprite.Sprite):
    def __init__( self, image_paths, scale_flag=False, scale_size=(WIDTH, HEIGHT), flip_flag=False, remove_bg_flag=False, position=(0, 0), frame_delay=100):  
        super().__init__()
        self.image_paths      = image_paths
        self.scale_flag       = scale_flag
        self.scale_size       = scale_size
        self.flip_flag        = flip_flag
        self.remove_bg_flag   = remove_bg_flag
        self.position         = position
        self.current_point    = 0
        self.current_position = 0

        self.frame_index      = 0   # 当前帧编号
        self.frame_delay      = frame_delay
        self.last_update      = pygame.time.get_ticks()
        self.load_character()

    def load_character(self):
        # 加载character
        self.frames = [ pygame.image.load(path).convert_alpha() for path in self.image_paths ] # 加载动画所有帧image
        # 对背景素材进行预处理
        if self.scale_flag:
            '''scale?'''
            self.frames = [pygame.transform.scale(frame, self.scale_size) for frame in self.frames]
        if self.flip_flag:
            '''flip?'''
            self.frames = [pygame.transform.flip(frame, True, False) for frame in self.frames]  # 水平翻转 (如果需要的话)
        if self.remove_bg_flag:
            '''remove bg?'''
            bg_color = [frame.get_at((0, 0)) for frame in self.frames]
            [frame.set_colorkey(colorkey) for frame, colorkey in zip(self.frames, bg_color)]

        self.image = self.frames[self.frame_index]   # 当前显示的帧

        self.rect = self.image.get_rect(center = self.position)
        

    def keep_moving(self, waypoints, speed = 1):
        if self.current_point < len(waypoints):

            self.rect = self.image.get_rect(center = waypoints[self.current_point])
            # self.rect.center = self.waypoints[self.current_point]
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
        

    def test(self, events):
        for event in events:
            if event.type == pygame.TEXTINPUT: 
                print(event.text)
                pass  # event.text

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_delay:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = self.frames[self.frame_index]
            self.last_update = now