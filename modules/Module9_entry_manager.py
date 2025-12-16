from typing import Literal

from core.Module1_txt import print_plus,Tree
from core.Module2_json_loader import json_loader
from core.Module5_dice import dice

ALL_ENTRY_METADATA = json_loader.load("entries_meta_data")

class Modes:
    """游戏模式枚举"""
    FIGHT = "FIGHT"
    DISASTER = "DISASTER"
    INFINITY = "INFINITY"

class Entry:

    def __init__(self,index:str):
        # 元数据字段
        self.index:str                  = index
        self.metadata:dict              = ALL_ENTRY_METADATA[index]
        self.max_rank:int               = len(self.metadata["points"]) - 1
        self.title:str                  = self.metadata["title"]
        self.points_list:list[int]      = self.metadata["points"]
        self.description_list:list[str] = self.metadata["description_txt"]
        self.summary:str                = self.metadata["summary"]

        # 通用查表字段
        self.RANK_STR_LIST = ["","I","II","III","IV","V"]

        # 调用字段
        self.selected_rank = 0
        self.flow_rank = 0
        self.point = 0

    def set_rank(self,rank:int):
        """
        设置词条等级，若输入非法则报ValueError
        :param rank: 要设置的等级
        :return: 无
        """
        if rank < 0 or rank > self.max_rank:
            raise ValueError
        self.selected_rank = rank
        self.point = self.points_list[rank]

    def print_description(self):
        title = f"[{self.index}]“{self.title}”：{self.summary}"
        body = []
        for rank in range(1,len(self.description_list)):
            is_chosen="[●已选中]" if rank == self.selected_rank else ""
            body.append(f"[{self.RANK_STR_LIST[rank]}]{self.description_list[rank]}[{self.points_list[rank]}分]{is_chosen}")

        Tree(title,body).print_self()

class EntryManager:

    def __init__(self):
        self.all_entries = {index:Entry(index) for index in ALL_ENTRY_METADATA}
        self.current_mode:Literal["FIGHT","DISASTER","INFINITY"] = "FIGHT"

    # 词条选择方法

    def print_all_descriptions(self):
        for entry in self.all_entries.values():
            entry.print_description()

    def clear_all(self):
        for entry in self.all_entries.values():
            entry.selected_rank = 0

    def push_all_full(self):
        for entry in self.all_entries.values():
            entry.selected_rank = entry.max_rank

    def set_all_rank(self,all_entry_rank:dict[str,int]):
        for entry_index,rank in all_entry_rank.items():
            self.all_entries[entry_index].selected_rank = rank

    def get_all_rank(self) -> dict[str,int]:
        return {entry_index: entry.selected_rank for entry_index, entry in self.all_entries.items()}

    # 级别检索

    def get_rank_of(self,index:str) -> int:
        """
        基于当前模式得到词条的正确等级
        :param index: 词条编号
        :return: 词条等级。战死之地返回selected_rank，其它则返回flow_rank
        """
        if self.current_mode == Modes.DISASTER:
            return self.all_entries[index].selected_rank
        return self.all_entries[index].flow_rank

    # 战斗方法

    def check_and_add_atk(self,atk) -> int:
        if dice.probability(self.get_rank_of("1")*0.2):
            atk += 1
        return atk

entry_manager = EntryManager()