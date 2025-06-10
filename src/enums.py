from enum import Enum


class CardMap(Enum):
    A = 1
    B = 2
    C = 3


if __name__ == '__main__':
    print(CardMap.A.name)
    print(CardMap.A.value)
