import random

from core.Module1_txt import Tree,adjust
from core.Module2_json_loader import json_loader

ALL_MATERIALS:list[str] = list(
    json_loader.load("storage_template")["materials"].keys()
)

AL_META_DATA = json_loader.load("al_meta_data")
"""所有AL的元数据"""

AL_RANK_LIST:dict[str,int]
"""
从AL的字符串序号获取其级数
"""
for key in AL_META_DATA:
    AL_RANK_LIST = AL_META_DATA[key]["rank_num"]

AL_NAME_LIST:dict[str,int]
"""
从AL的字符串序号获取其短名称
"""
for key in AL_META_DATA:
    AL_NAME_LIST = AL_META_DATA[key]["short_name"] + f"#{key}"

class Tools:

    @staticmethod
    def create_material_list(total:int) -> dict[str,int]:
        """
        创建一个八种材料中选择的materials字典，材料总量大致与total相当
        :param total: 需求的材料总量
        :return: 一个材料字典，键为材料名，值为材料的数目
        """
        output_list = {}
        material_num = random.randint(2, 4)
        num_expect = total // material_num

        material_list = random.sample(ALL_MATERIALS, material_num)

        for material in material_list:
            output_list[material] = random.randint(num_expect - 3, num_expect + 3)
        return output_list

    @staticmethod
    def is_affordable(cost:dict[str,int],budget:dict[str,int]) -> bool:
        """
        判断cost中的每一项是否小于budget中的对应项。若cost出现budget没有的项目，直接抛出KeyError
        :param cost: 账单
        :param budget: 预算
        :return: True表示cost可以被budget支付，False反之
        """
        for item in cost:
            if cost[item] > budget[item]:
                return False
        return True

    @staticmethod
    def clear_0_in(dic: dict[any,int]) -> None:
        """
        在 原 地 清除字典中值为0的项目
        :param dic:
        :return: 无
        """
        for key in list(dic.keys()):
            if dic[key] == 0:
                dic.pop(key)
tools = Tools()

class Contract:

    def __init__(self,index):
        self.index = index
        self.title = ""
        self.rank = random.randint(1,8)
        self.is_traded = False
        self.get_list = {}
        self.give_list = {}
        self.give_tree:Tree = Tree("")
        self.get_tree:Tree = Tree("")

    def print_self(self):
        print("┌──────────┐")
        print(adjust(f"丨{self.title}",22)+"丨")
        for line in self.give_tree.generate_line_list():
            print(adjust(f"丨{line}",22)+"丨")
        for line in self.get_tree.generate_line_list():
            print(adjust(f"丨{line}",22)+"丨")
        print("└──────────┘")

    def generate_line_list(self) -> list[str]:
        """
        生成Contract对象的行切片
        :return: 一个字符串列表，包含Contract的每一行
        """
        line_list = ["┌──────────┐", adjust(f"丨{self.title}", 22) + "丨"]
        if self.is_traded:
            for _ in self.give_tree.generate_line_list():
                line_list.append(adjust(f"丨", 22) + "丨")
            for _ in self.get_tree.generate_line_list():
                line_list.append(adjust(f"丨", 22) + "丨")
        else:
            for line in self.give_tree.generate_line_list():
                line_list.append(adjust(f"丨{line}", 22) + "丨")
            for line in self.get_tree.generate_line_list():
                line_list.append(adjust(f"丨{line}", 22) + "丨")
        line_list.append("└──────────┘")
        return line_list

class MaterialContract(Contract):
    """
    易物合同
    """
    def __init__(self,index):
        super().__init__(index)
        self.title = f"{self.index} 易物合同 [{self.rank}级]"

        # 生成交接物品列表
        self.give_list = tools.create_material_list(25 * self.rank)
        self.get_list = tools.create_material_list(30 * self.rank)

        # 去除重复
        common_items = set(self.give_list.keys()) & set(self.get_list.keys())
        for item in common_items:
            give_qty = self.give_list[item]
            get_qty = self.get_list[item]
            min_qty = min(give_qty,get_qty)
            self.get_list[item] -= min_qty
            self.give_list[item] -= min_qty
        tools.clear_0_in(self.get_list)
        tools.clear_0_in(self.give_list)

        # 打印树构建
        self.get_tree=Tree("你将得到>>>",self.get_list)
        self.give_tree = Tree("你将支付>>>", self.give_list)


class GoodsContract(Contract):
    """
    货品合同
    """

    def __init__(self, index):
        super().__init__(index)
        self.title = f"{self.index} 货品合同 [{self.rank}级]"

        # 生成支付物品列表（25倍rank）
        self.give_list = tools.create_material_list(25 * self.rank)

        # 生成获取的信用点（1000倍rank，有±100浮动）
        self.get_list = {
            "联邦信用点": random.randint(
                1100 * self.rank - 100,
                1100 * self.rank + 100
            )
        }

        # 50%概率交换give和get列表
        if random.random() < 0.5:
            self.give_list, self.get_list = self.get_list, self.give_list

        # 清理数量为0的物品
        tools.clear_0_in(self.get_list)
        tools.clear_0_in(self.give_list)

        # 打印树构建
        self.get_tree = Tree("你将得到>>>", self.get_list)
        self.give_tree = Tree("你将支付>>>", self.give_list)

if __name__ == "__main__":
    test = GoodsContract(0)
    test.print_self()