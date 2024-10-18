import pygame
from plane_sprites import *


class PlaneGame(object):
    def __init__(self):
        print("游戏初始化")
        # 创建游戏窗口
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        # 创建游戏时钟
        self.clock = pygame.time.Clock()
        # 调用私有方法创建精灵和精灵组
        self.__create_sprites()

        # 设置定时器事件，创建敌机
        pygame.time.set_timer(CREATE_ENEMY_EVENT, 1000)

        # 设置定时器事件，设置英雄自动开火，间隔1秒
        pygame.time.set_timer(HERO_FIRE_EVENT, 1500)

    def start_game(self):
        print("游戏开始")
        while True:
            # 设置刷新帧率
            self.clock.tick(FRAME_PER_SECOND)
            # 事件监听
            self.__event_handler()
            # 碰撞检测
            self.__check_collide()
            # 更新/绘制精灵组
            self.__update_sprites()
            # 更新显示
            pygame.display.update()

    def __event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                PlaneGame.__game_over()
            elif event.type == CREATE_ENEMY_EVENT:
                # 创建敌机精灵(定时器事件)
                enemy_sp = Enemy()
                self.enemy_group.add(enemy_sp)
            elif event.type == HERO_FIRE_EVENT:
                self.hero.fire()



        # 使用键盘提供的方法监听键盘事件,案件按下，值为1，返回的是元组
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_RIGHT]:
            # 向右移动，坐标值增加
            if self.hero.rect.right >= SCREEN_RECT.width:
                self.hero.speed = 0
            else:
                self.hero.speed = 2
        elif keys_pressed[pygame.K_LEFT]:
            if self.hero.rect.left <= 0:
                self.hero.speed = 0
            else:
                self.hero.speed = -2
        else:
            self.hero.speed = 0

    def __check_collide(self):
        # 子弹摧毁敌机
        pygame.sprite.groupcollide(self.hero.bullets, self.enemy_group, True, True)
        # 英雄与精灵组任意精灵碰撞，精灵被摧毁，英雄不会被摧毁
        clollide_enemys = pygame.sprite.spritecollide(self.hero, self.enemy_group, True)
        # 判断英雄碰撞的敌机数量，大于1，英雄需要被清除
        if len(clollide_enemys) > 0:
            self.hero.kill()
            PlaneGame.__game_over()


    @staticmethod
    def __game_over():
        pygame.quit()
        exit()

    def __create_sprites(self):
        print("创建精灵组")
        # 创建背景和背景组
        bg1 = Background()
        bg2 = Background(is_alter=True)
        self.bg_group = pygame.sprite.Group(bg1, bg2)

        # 创建敌机精灵组
        self.enemy_group = pygame.sprite.Group()

        # 创建英雄和英雄组,hero其他方法要使用，所以定义为属性
        self.hero = Hero()
        self.hero_group = pygame.sprite.Group(self.hero)

    def __update_sprites(self):
        # 更新背景组
        self.bg_group.update()
        self.bg_group.draw(self.screen)
        # 更新敌机组
        self.enemy_group.update()
        self.enemy_group.draw(self.screen)

        # 更新英雄组
        self.hero_group.update()
        self.hero_group.draw(self.screen)

        # 更新子弹精灵组
        self.hero.bullets.update()
        self.hero.bullets.draw(self.screen)



if __name__ == "__main__":
    # 创建游戏对象
    game = PlaneGame()
    game.start_game()