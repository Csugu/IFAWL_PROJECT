from __future__ import annotations

import random
from typing import Literal
import json
import os

from myPackages import Module1_txt

class Voices:
    file_path = os.path.join('resources', 'voices.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        voices:dict[str:dict[str:list[str]]] = json.load(f)

    @classmethod
    def report(cls,who:str,theme:str,print_who=True):
        try:
            if print_who:
                txt = f"[{who}]" + random.choice(cls.voices[who][theme])
            else:
                txt = random.choice(cls.voices[who][theme])
            Module1_txt.printplus(txt)
        except KeyError:
            pass

class Dice:
    """
    Dice.set_probability(0.7)
    Dice.decide_who()
    """

    probability = 0.5
    di = 0.2

    @classmethod
    def set_probability(cls,val:float):
        """
        设置当前的动态概率(摇到我方的概率)
        :param val: 动态概率的取值
        :return: 无
        """
        cls.probability = val

    @classmethod
    def decide_who(cls) -> Literal[0,1]:
        """
        决定谁来进行下一回合，并进行马尔科夫链变化
        :return:
        """
        if random.random()<cls.probability:
            cls.probability -= cls.di
            return 1
        else:
            cls.probability += cls.di
            return 0

class Printer:
    def __init__(self):
        ...
    @classmethod
    def print_single_day(cls,me:My_ship,enemy:Enemy_ship):
        enemy.print_self()
        print("\n\n\n")
        me.print_self()
        print("\n")

class My_ship:
    """
    ship.print_self()
    ship.attack(3,enemy)
    ship.heal(2)
    """

    def __init__(self):
        self.shelter = 0
        self.missile = 0

    def print_self(self):
        for _ in range(self.shelter):
            print("-----")
        for _ in range(self.missile):
            print("[] ",end="")

    def initialize(self):
        self.missile = 1
        self.shelter = 1

    def attack(self,atk:int,target:Enemy_ship):
        """
        根据原始伤害进行加减并对目标造成攻击
        :param atk: 原始伤害
        :param target: 承受攻击的敌方船只
        :return: 无
        """
        target.shelter -= atk

    def heal(self,hp:int):
        """
        根据原始回血量进行加减并进行治疗
        :param hp: 原始回血量
        :return: 无
        """
        self.shelter += hp

    def load(self,num:int):
        """
        根据原始上弹量进行加减并进行上弹
        :param num: 原始上弹量
        :return: 无
        """
        self.missile += num

    def react(self,enemy:Enemy_ship):
        """
        进行回合中响应
        :param enemy: 当前敌方
        :return: 无
        """
        operation = input(">>>")
        if self.missile < 1 and operation == "1":
            operation = "0"
        match operation:
            case "0":
                self.load(1)
            case "1":
                self.attack(1,enemy)
                self.load(-1)
            case "2":
                self.heal(1)
            case _:
                Module1_txt.printplus("你跳过了这一天！")
my_ship = My_ship()

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

    def attack(self,atk:int):
        """
        根据原始伤害进行加减并对目标造成攻击
        :param atk: 原始伤害
        :return: 无
        """
        my_ship.shelter -= atk

    def heal(self,hp:int):
        """
        根据原始回血量进行加减并进行治疗
        :param hp: 原始回血量
        :return: 无
        """
        self.shelter += hp

    def load(self,num:int):
        """
        根据原始上弹量进行加减并进行上弹
        :param num: 原始上弹量
        :return: 无
        """
        self.missile += num

    def initialize(self):
        self.missile = 2
        self.shelter = 2

    def react(self):
        operation = random.choice(["0","1","2"])
        if self.missile < 1 and operation == "1":
            operation = "0"
        match operation:
            case "0":
                self.load(1)
            case "1":
                self.attack(1)
                self.load(-1)
            case "2":
                self.heal(1)
            case _:
                Module1_txt.printplus("敌人跳过了这一天！")

enemy = Enemy_ship()

class Main_loops:

    days = 0

    @staticmethod
    def is_over() -> Literal[-1,0,1]:
        """
        判定是否有一方死亡
        :return: -1代表敌方胜利 0表示游戏继续 1表示我方胜利
        """
        if my_ship.shelter<0:
            return -1
        if enemy.shelter<0:
            return 1
        return 0

    @classmethod
    def initialize_before_fight(cls):
        my_ship.initialize()
        enemy.initialize()
        cls.days = 1

    @classmethod
    def fight_mainloop(cls):
        while 1:
            Module1_txt.printplus(f"战斗的第{cls.days}天")
            Printer.print_single_day(my_ship,enemy)
            who = Dice.decide_who()
            if who==1:
                Module1_txt.printplus("今天由我方行动")
                my_ship.react(enemy)
            else:
                Module1_txt.printplus("今天由敌方行动")
                enemy.react()
            if (result := cls.is_over()) != 0:
                if result == 1:
                    Module1_txt.printplus("我方胜利")
                else:
                    Module1_txt.printplus("敌方胜利")
                return

if __name__ == "__main__":
    Main_loops.initialize_before_fight()
    Main_loops.fight_mainloop()