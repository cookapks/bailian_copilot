"""
百炼英雄小程序游戏辅助脚本
"""

import pyautogui
import time
import random
from datetime import datetime

from conf import *
from src.router import RouterA


class Base:

    def __init__(self):
        self.duration = 0.5  # 鼠标移动间隙速度

    @staticmethod
    def timeout(sec):
        # 设置延迟，防止操作太快
        time.sleep(sec)  # 等待2秒，给你时间将鼠标移出脚本运行区域

    def move_mouse(self, x, y, click=False, click_count=1, sec=0):
        # 移动鼠标到指定坐标 (1000, 410)
        pyautogui.moveTo(x, y, duration=self.duration)  # 用0.5秒时间移动鼠标到目标位置
        # 点击鼠标左键
        if click:
            print(f'点击了按钮', x, y)
            for i in range(click_count):
                pyautogui.click()
                self.timeout(1.2)
        self.timeout(sec)

    def click(self, button_name, sec=0, if_click=True, click_count=1):
        self.move_mouse(*BUTTONS[button_name], click=if_click, click_count=click_count)
        self.timeout(sec)

    def click_back_home(self, sec=8):
        # 每个地图回城的时间不同，王座大厅图回城需要8s， 黑市堡垒需要10s
        self.click(BT_HOME)
        self.click(BT_OK, sec=sec)

    def click_level(self, level, raw="A", sec=10, if_click=True):
        area = MAP_LEVEL_A_BUTTON[f'LEVEL_{level[:1]}']
        if raw == "A":
            self.move_mouse(*area, click=if_click)
            self.move_mouse(*MAP_LEVEL_A_SUB_BUTTON[level], click=if_click)
        if raw == "B":
            self.move_mouse(*MAP_LEVEL_B_SUB_BUTTON[level], click=if_click)
        self.timeout(sec)

    def move(self, direction, cons_sec, sec=2):
        pyautogui.moveTo(*BUTTONS[CENTER])
        pyautogui.mouseDown()
        pyautogui.moveTo(*FORWARD_POINT[direction], duration=cons_sec)
        pyautogui.mouseUp()

        print(f'往{direction}行动了')
        self.timeout(sec)

    def check_city_load_complete(self, limit=12):
        # 因为各个地图的回城的加载时间不一致，所以这里稍微多等待几秒,最多等待12s则报错
        count = 0
        status = False
        while True:
            count += 1
            if pyautogui.pixel(*BUTTONS[BT_TRAN]) == BUTTONS_COLORS[BT_TRAN]:
                self.click(BT_TRAN)
                status = True
            if pyautogui.pixel(*BUTTONS[BT_TRAN_BACK]) == BUTTONS_COLORS[BT_TRAN]:
                self.click(BT_TRAN_BACK)
                status = True
            if status:
                print(f'该地图加载时间为{count}s')
                return
            self.timeout(1)
            if count >= limit:
                raise TimeoutError('加载主地图失败，请保证主窗口为初始位置')


class DrawCard(Base):
    """
    抽卡脚本v1.0
        1、通过特定坐标颜色RGB值，判定是否为白卡，蓝卡，紫卡，金卡，红卡，灰色
            如果存在金卡，或者红卡，则自动调整金币300进行抽卡
    """

    def __init__(self):
        super().__init__()
        # 初始化抽卡状态存储
        self.card_pos_color = {"A": "", "B": "", "C": ""}
        self.card_color = list()
        self.card_status = {"A": False, "B": False, "C": False}

        # 统计
        self.count = 0
        self.red_count = 0
        self.gold_count = 0

    def check_card_color(self):
        for card, pos in CARD_SHOW_POS.items():
            self.card_pos_color[card] = COLOR_POINT[pyautogui.pixel(*pos)]
        self.card_color = list(self.card_pos_color.values())
        print(f'本次三张卡颜色分别为: {self.card_color}')

    def refresh_card_status(self):
        for card, pos in CARD_SHOW_STATUS.items():
            self.card_status[card] = True if pyautogui.pixel(*pos) == BUTTONS_COLORS[BT_OK] else False
        print(f'本次三张卡抽取状态分别为: {list(self.card_status.values())}')

    def check_card_status(self):
        """
        todo 目前仅支持抽取一次
        return 0 表示不抽取，1表示可抽取"""
        if any(list(self.card_status.values())):
            return 0
        return 1

    def click_drop(self, sec=4):
        self.move_mouse(*BUTTONS['drop'], click=True)
        # 统计抽到的卡数
        for card, status in list(zip(self.card_color, list(self.card_status.values()))):
            if card == 'red' and status:
                self.red_count += 1
            if card == 'gold' and status:
                self.gold_count += 1
        self.timeout(sec + random.randint(2, 4))

    def check_new_page(self):
        if not any(list(self.card_status.values())):
            print(f'目前是新的一页抽卡')
        else:
            print(f'目前是旧的一页待第二次抽卡')

    def run(self):
        """主逻辑执行"""
        while True:
            print('')
            # 判断ABC三张卡颜色
            self.check_card_color()
            # 刷新卡状态
            self.refresh_card_status()
            self.check_new_page()

            # 如果金卡或红卡状态未抽取就进行抽取, 若已经抽取完了某个，就点放弃，直接进入下一轮
            if self.check_card_status():
                # 如果有金卡或红卡，则调整倍数为最大
                if "gold" in self.card_color or "red" in self.card_color:
                    self.click(BT_RATE)
                self.click(BT_DRAW, sec=4)
                self.count += 1
            else:
                self.click_drop()
                print(
                    f'目前抽取结果汇总=======>> 抽取次数：{self.count}, 红卡次数：{self.red_count}, 金卡次数：{self.gold_count}')
            print('开启循环下一次')


class AutoFight(Base, RouterA):
    """指定特定关卡进行自动路线清本"""

    def __init__(self):
        super().__init__()
        # 首先确保自己自己在主城
        self.click_back_home()

    def rush_all(self):

        # todo on develop 遍历地图序号，开始刷图，
        for level in list(MAP_LEVEL_A_SUB_BUTTON.keys())[:1]:
            # 若不是1-1关，则打开传送阵，点击传送到对应关卡位置
            if level != "1-1":
                self.click(BT_TRAN)
                self.click_level(MAP_LEVEL_A_SUB_BUTTON)
            self.rush_map(level)

    def rush_wood(self):
        # 进入战斗
        while True:
            self.check_city_load_complete()
            self.click_level(WOOD_LEVEL)
            for direction, sec in WOOD_ROUTER:
                self.move(direction, sec)
            self.click_back_home()


class DailyTask(Base):
    """日常"""

    def __init__(self):
        super().__init__()
        self.duration = 0.2  # 鼠标移动间隙速度
        self.box_limit = 30  # 每日箱子最大领取次数
        self.pk_limit = 4  # 每日免费战斗次数
        # 首先确保自己自己在主城
        # self.click_back_home()

    def rush_all(self):
        # 点掉初始的各种活动弹窗, 点个什么五六次
        self.click(FLOOR, click_count=5)
        # 点商城,其中每周礼包只有周一才能点
        self.click_shop()
        # 每日签到
        self.click_sign()
        # 每日挑战
        self.click_battle()
        # 英雄馈赠
        self.click_hero_card()
        # 刷箱子
        self.rush_quick()

    def click_battle(self):
        # PK竞技场 每日4次

        self.click(PK, sec=5)   # 第一次加载比较慢
        self.click(BT_FIELD)

        while self.pk_limit:
            self.click(VS, sec=12)
            self.click(FLOOR, sec=3)
            self.pk_limit -= 1
        self.click(BACK_HOME, sec=2)

    def rush_quick(self):
        # 快速拿箱子，刷8-2 F4
        # 进入战斗
        while self.box_limit:
            self.check_city_load_complete()
            self.click_level(DAILY_LEVEL)
            for num, router in enumerate(F4_ROUTER, start=1):
                self.move(router[0], router[1], sec=1)
                if num % 2 == 0:
                    time.sleep(4)
                    self.pick_box(num // 2)
                    self.click_back_home()

    def pick_box(self, num):
        # todo 箱子刷新的位置有时候会有变动,需增加一个适配坐标
        self.move_mouse(*BOX_BUTTON[num - 1], click=True, sec=1)
        # 如果可以看视频双倍，则点击,看广告30s
        if pyautogui.pixel(*BUTTONS[REWARD]) == BUTTONS_COLORS[REWARD]:
            self.click(REWARD, sec=35)
            self.click(CANCEL_AD, click_count=3)
        else:
            self.click(RECEIVE, sec=2)
            self.click(FLOOR)
        self.box_limit -= 1

    def click_shop(self):

        self.click(SHOP)    # 点击商店
        self.click(TH_GIFT)  # 点击特惠礼包
        self.click(DAY_BAO)  # 点击每日礼包
        self.click(DAY_GIFT)  # 点击免费领取
        if not self.check_monday():  # 周一执行
            self.click(WEEK_BAO)  # 点击每周礼包
            # self.click(WEEK_GIFT)  # 点击免费领取
        self.click(BACK_HOME, sec=2)  # 点击退出

    def click_sign(self):
        self.click(FULI)    # 点击福利
        self.click(DAILY_SIGN)    # 点击福利
        self.click(GET_SIGN)    # 点击福利
        self.click(BACK_HOME, sec=2)    # 点击福利

    def click_hero_card(self):
        self.click(ACT)  # 点击福利
        self.click(ACT_HERO)  # 点击福利
        self.click(GET_HERO)  # 点击福利
        self.click(BACK_HOME, sec=2)  # 点击福利

    @staticmethod
    def check_monday():
        return datetime.now().weekday()


if __name__ == '__main__':
    # 抽卡
    # DrawCard().run()

    # 刷木头
    # AutoFight().rush_wood()

    # 刷日常
    DailyTask().rush_all()
    # DailyTask().rush_quick()
    # DailyTask().click_battle()
    # DailyTask().click_hero_card()




