from typing import Literal
import random

from core.Module1_txt import print_plus, Tree, ask_plus
from core.Module2_json_loader import json_loader

ALL_CARD_METADATA = json_loader.load("cards_meta_data")

class CardManager:

    def __init__(self,my_ship,enemy,entry_manager):
        self.my_ship = my_ship
        self.enemy = enemy
        self.entry_manager = entry_manager
        self.all_cards:dict[str,CardGeneral] = {
            index:globals()[f"Card{index}"](index,self.my_ship,self.enemy,self.entry_manager)
            for index in ALL_CARD_METADATA
        }

    def choose_card(self):
        choose_list:list[CardGeneral] = random.sample(list(self.all_cards.values()),k=2)
        for card in choose_list:
            card.print_self()
        result = ask_plus("请输入要选择的协议>>>",[card.index for card in choose_list])
        self.all_cards[result].react()

class CardGeneral:

    def __init__(self,index,my_ship,enemy,entry_manager):
        # 元数据字段
        self.index = str(index)
        self.metadata = ALL_CARD_METADATA[index]
        self.title = self.metadata["title"]
        self.story_txt = self.metadata["story_txt"]
        self.description_txt = self.metadata["description_txt"]
        # 依赖字段
        self.my_ship = my_ship
        self.enemy = enemy
        self.entry_manager = entry_manager

    def print_self(self):
        Tree(
            "-------------------------->>",
            f"|协议[{self.index}]>{self.title}",
            f"|{self.description_txt}",
            f"|---{self.story_txt}"
        ).print_self()

    def react(self):
        ...

class Card1(CardGeneral): # 紧急回站

    def react(self):
        shelter = random.randint(1,5)
        self.my_ship.heal(shelter)
        self.my_ship.load(5-shelter)
        print_plus(f"护盾回充>{shelter}")
        print_plus(f"导弹装载>{5-shelter}")

class Card2(CardGeneral): # 抑制剂

    def react(self):
        self.entry_manager.pull_down()