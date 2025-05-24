import pyautogui
import time
import random
from abc import ABC, abstractmethod

from conf import *


class Router(ABC):
    """各关卡路线坐标"""

    def __init__(self):
        pass

    @abstractmethod
    def rush_map(self, level): ...


class RouterA(Router):

    def __init__(self):
        super().__init__()

    def rush_map(self, level):
        pass


class RouterB(Router):

    def __init__(self):
        super().__init__()

    def rush_map(self, level):
        pass
