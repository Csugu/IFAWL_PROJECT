from __future__ import annotations

class My_ship:

    def __init__(self):
        self.shelter = 0
        self.missile = 0

    def print_self(self):
        for _ in range(self.shelter):
            print("-----")
        for _ in range(self.missile):
            print("[] ",end="")

    @staticmethod
    def attack(atk:int,target:Enemy_ship):
        """
        根据原始伤害进行加减并对敌方造成攻击
        :param atk: 原始伤害
        :param target: 承受攻击的敌方船只
        :return: 无
        """
        target.shelter -= atk

class Enemy_ship:
    def __init__(self):
        self.shelter = 0
        self.missile = 0

    def print_self(self):
        for _ in range(self.missile):
            print("[] ",end="")
        print()
        for _ in range(self.shelter):
            print("-----")

    @staticmethod
    def attack(atk:int,target:My_ship):
        """
        根据原始伤害进行加减并对我方造成攻击
        :param atk: 原始伤害
        :param target: 承受攻击的我方船只
        :return: 无
        """
        target.shelter -= atk


if __name__ == "__main__":
    enemy = Enemy_ship()
