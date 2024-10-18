import random
import sys

import pygame
import time
# 定义以西窗口其实坐标位0，0 窗口宽度和高度
SCREEN_RECT = pygame.Rect(0, 0, 450, 700)
# 刷新帧率，每秒60帧
FRAME_PER_SECOND = 60
# 创建敌机的定时器常量
CREATE_ENEMY_EVENT = pygame.USEREVENT

# 创建英雄开火事件
HERO_FIRE_EVENT = pygame.USEREVENT + 1
pygame.init()
pygame.mixer.init()


class GameSprite(pygame.sprite.Sprite):
    def __init__(self, image_para, speed_para=1):
        # 父类不是object时都需要调用父类初始化方法
        super().__init__()
        self.image = pygame.image.load(image_para)
        self.rect = self.image.get_rect()
        self.speed = speed_para

    def update(self):
        # 精灵父类update，设置飞行为垂直方向飞行
        self.rect.y += self.speed




    def display_score(self):
        print(f"Player '{self.player_name}' score: {self.score}")

class Background(GameSprite):

    def __init__(self, is_alter=False):
        super().__init__("D:/飞机大战2/雷霆战机/images/背景图片bg.jpg")
        # 如果时替换的背景
        # 加载背景音乐
        pygame.mixer.music.load("D:/飞机大战2/雷霆战机/晴天mp3/756351052.mp3")
        # 设置音量
        pygame.mixer.music.set_volume(0.1)
        # 设置播放次数, -1 表示无限循环
        pygame.mixer.music.play()

        if is_alter:
            # bg2 初始位置要设置在窗口上方
            self.rect.y = -self.rect.height

    def update(self):
        # 调用父类的update方法，向下移动
        super().update()
        # 如果背景图片向下移出窗口，y坐标=700
        if self.rect.y > SCREEN_RECT.height:
            self.rect.y = -SCREEN_RECT.height


class Enemy(GameSprite):
    def __init__(self):
        # 调用父类方法，创建敌机，加载敌机图片
        super().__init__("D:/飞机大战2/雷霆战机/images/敌机 enemy1.png")

        # 指定敌机初始位置是在窗口正上方
        # self.rect.y = -SCREEN_RECT.height 等价于下面的语句
        self.rect.bottom = 0
        # 指定敌机的初始随机速度,敌机速度要大于 否则跟背景速度一样，会显示静止
        self.speed = random.randint(2, 3)

        # 指定敌机的初始随机位置
        self.rect.x = random.randint(0, SCREEN_RECT.width-self.rect.width)

    def update(self):
        # 调用父类方法，实现垂直向下飞行
        super().update()

        # 判断是否废除屏幕，如果是，从精灵组移除
        if self.rect.y >= SCREEN_RECT.height:
            # kill方法会将精灵从所有组中删除
            self.kill()

    def __del__(self):
        print("敌机%s被销毁" % self.rect)


class Hero(GameSprite):
    def __init__(self):
        # 调用父类方法，设置图片和速度
        super().__init__("D:/飞机大战2/雷霆战机/images/英雄飞机 hero.png", speed_para=0)

        # 设置英雄的初始位置
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.bottom - 20

        # 创建子弹精灵组
        self.bullets = pygame.sprite.Group()

    def update(self):
        # 英雄只能左右移动，不能上下移动
        self.rect.x += self.speed

        # 限定英雄不能飞出屏幕，等价于eventhandle中的代码
        # if self.rect.right >= SCREEN_RECT.right:
        #     self.rect.right = SCREEN_RECT.right
        # elif self.rect.x < 0:
        #     self.rect.x = 0


    def fire(self):
        # 创建子弹精灵,一次发射2发子弹
        for i in (0,1):
            bullet = Bullet()
            # 设置子弹精灵的位置,在飞机正上方60单位,间隔60
            bullet.rect.bottom = self.rect.y - i*60
            bullet.rect.centerx = self.rect.centerx
            # 将精灵添加到精灵组
            self.bullets.add(bullet)
        print("开火")


class Bullet(GameSprite):

    def __init__(self):
        # 调用父类方法，设置子弹图片，设置初始速度
        super().__init__("D:/飞机大战2/雷霆战机/images/子弹bullet1.png", speed_para=-2)

    def update(self):
        # 调用父类方法，让子弹沿着垂直方向飞行
        super().update()
        # 子弹飞出窗口，则销毁 bpottom 为图像的底部
        if self.rect.bottom < 0:
            self.kill()

    def __del__(self):
        print("子弹被销毁")


