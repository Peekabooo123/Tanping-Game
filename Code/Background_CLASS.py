
import pygame
from CONFIG_in_winsys import HEIGHT, WIDTH, REC_PIC, REC_WIDTH, REC_HEIGHT, REC_ORIGIN_COORDINATES_X, REC_ORIGIN_COORDINATES_Y

class BackgroundSprite(pygame.sprite.Sprite):

    def __init__( self, image_paths, box_flag=False, scale_flag=True, scale_size=(WIDTH, HEIGHT), flip_flag=False, remove_bg_flag=False, position=(0, 0), frame_delay=100):
        super().__init__()
        self.image_paths      = image_paths
        self.box_flag         = box_flag
        self.scale_flag       = scale_flag
        self.scale_size       = scale_size
        self.flip_flag        = flip_flag
        self.remove_bg_flag   = remove_bg_flag
        self.position         = position

        self.frame_index      = 0            # 当前帧编号
        self.frame_delay      = frame_delay
        self.last_update      = pygame.time.get_ticks()
        self.load_background()
    
    
    def load_background(self):
        # 加载background
        self.background = [ pygame.image.load(path).convert_alpha() for path in self.image_paths ] # 加载动画所有帧image
        # 对背景素材进行预处理
        if self.box_flag:
            '''box?是否要贴边处理'''
            Bbox = [frame.get_bounding_rect() for frame in self.background]
            self.background = [frame.subsurface(bbox).copy() for frame, bbox in zip(self.background, Bbox)]

        if self.scale_flag:
            '''scale?'''
            self.background = [pygame.transform.scale(frame, self.scale_size) for frame in self.background]

        if self.flip_flag:
            '''flip?'''
            self.background = [pygame.transform.flip(frame, True, False) for frame in self.background]  # 水平翻转 (如果需要的话)

        if self.remove_bg_flag:
            '''remove bg?'''
            bg_color = [frame.get_at((0, 0)) for frame in self.background]
            [frame.set_colorkey(colorkey) for frame, colorkey in zip(self.background, bg_color)]

        self.image = self.background[self.frame_index]   # 当前显示的帧
        self.rect  = self.image.get_rect(topleft = self.position)


    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_delay:
            self.frame_index = (self.frame_index + 1) % len(self.background)
            self.image = self.background[self.frame_index]
            self.last_update = now
