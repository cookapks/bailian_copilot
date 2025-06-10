

# 相关按键
BUTTONS = {"rate": (1087, 694), "draw": (960, 754), "drop": (956, 793),
           "tran": (1000, 413), "tran_back": (993, 467), "home": (1145, 836),
           "center": (960, 760), "ok": (1050, 605), "floor": (1165, 748),
           "reward": (1000, 641), "cancel_ad": (1147, 170), "receive": (1000, 641),
           "back_home": (815, 878), "floor1": (1091, 256),

           # PK竞技场
           "pk": (1160, 450), "bt_field": (1067, 694), "vs": (1078, 737),

           # 商店
           "shop": (767, 231), "th_gift": (987, 882), "day_bo": (906, 798),
           "day_gift": (1098, 465), "week_bo": (1019, 796), "week_gift": (1087, 470),
           "fuli": (764, 282), "daily_sign": (1136, 878), "get_sign": (964, 788),
           "act": (1155, 507), "act_hero": (1115, 880), "get_hero": (954, 793),
           }
# 日常按钮
DAILY_BUTS = {}

# 按键颜色
BUTTONS_COLORS = {"rate": (36, 201, 83), "draw": (690, 960, 754),
                  "tran": (54, 195, 55), "ok": (66, 224, 24),
                  "reward": (245, 222, 77), "floor1": (50, 101, 150)}
# 抽到卡后的勾颜色RGB: 66,224,24
CARD_SHOW_STATUS = {"A": (831, 518), "B": (954, 550), "C": (1083, 518)}

# 一些名字定义
BT_RATE = 'rate'
BT_DRAW = 'draw'
BT_TRAN = 'tran'
BT_TRAN_BACK = 'tran_back'
BT_HOME = 'home'
BT_OK = 'ok'
CENTER = 'center'
FLOOR = 'floor'
FLOOR1 = 'floor1'
REWARD = 'reward'
RECEIVE = 'receive'
CANCEL_AD = "cancel_ad"
PK = "pk"
VS = "vs"
BT_FIELD = "bt_field"
BACK_HOME = "back_home"
SHOP = "shop"
TH_GIFT = "th_gift"
DAY_BAO = "day_bo"
DAY_GIFT = "day_gift"
WEEK_BAO = "week_bo"
WEEK_GIFT = "week_gift"
FULI = "fuli"
DAILY_SIGN = "daily_sign"
GET_SIGN = "get_sign"
ACT = "act"
ACT_HERO = "act_hero"
GET_HERO = "get_hero"

# 关卡相关
MAP_LEVEL_A_BUTTON = {
    "LEVEL_1": (860, 340),
    "LEVEL_2": (860, 390),
    "LEVEL_3": (860, 440),
    "LEVEL_4": (860, 490),
    "LEVEL_5": (860, 540),
    "LEVEL_6": (860, 590),
    "LEVEL_7": (860, 640),
    "LEVEL_8": (860, 690)
}
MAP_LEVEL_A_SUB_BUTTON = {
    "1-1": (1000, 350), "1-2": (1000, 420),
    "2-1": (1000, 350), "2-2": (1000, 420),
    "3-1": (1000, 350), "3-2": (1000, 420), "3-3": (1000, 490),
    "4-1": (1000, 350), "4-2": (1000, 420),
    "5-1": (1000, 350), "5-2": (1000, 420), "5-3": (1000, 490), "5-4": (1000, 560),
    "6-1": (1000, 350), "6-2": (1000, 420), "6-3": (1000, 490),
    "7-1": (1000, 350), "7-2": (1000, 420),
    "8-1": (1000, 350), "8-2": (1000, 420), "8-3": (1000, 490), "8-4": (1000, 560), "8-5": (1000, 630),
}

MAP_LEVEL_B_BUTTON = {"endless": ()}
MAP_LEVEL_B_SUB_BUTTON = {}

# 长按鼠标拖拽的目标点坐标
FORWARD_POINT = {"up": (960, 705), "down": (960, 815),
                 "left": (905, 760), "right": (1015, 760),
                 "left_up": (912, 732), "left_down": (912, 788),
                 "right_up": (1008, 710), "right_down": (1008, 780)
                 }

# 定制路线
# 刷木头
WOOD_LEVEL = '5-1'
DAILY_LEVEL = '8-2'

WOOD_ROUTER = [
    ("left_up", 2), ("left_up", 2), ("right_up", 2), ("right_up", 2),
    ("right_up", 2), ("right_up", 2), ("right_up", 2), ("left_up", 2),
    ("left_up", 2), ("left_down", 2), ("left_down", 2), ("left_down", 2),
    ("left_up", 2), ("left_down", 2), ("left_down", 2), ("left_down", 2),
    ("left_down", 2), ("right_down", 2), ("left_down", 2), ("left_up", 2),
    ("right_down", 8), ("right_down", 2), ("right_up", 4)
]

# 目前仅支持刷粉毛
BOX_BUTTON = [(1022, 633)]
F4_ROUTER = [("right_down", 1.5), ("left_down", 4)]

# 刷蓝水晶
