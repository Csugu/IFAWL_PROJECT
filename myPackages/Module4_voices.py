import random

import Module1_txt as Txt
from .Module2_json_loader import json_loader

class Voices:

    def __init__(self):
        self.voices:dict[str,dict[str,list[str]]] = json_loader.load("voices")

    def report(self, who:str, theme:str, print_who=True):
        """
        展示voices.json中记录的语音内容
        :param who: 语音发出者
        :param theme: 语音主题
        :param print_who: 是否打印语音发出者
        :return:
        """
        try:
            if print_who:
                txt = f"[{who}]" + random.choice(self.voices[who][theme])
            else:
                txt = random.choice(self.voices[who][theme])
            Txt.print_plus(txt)
        except KeyError:
            print(f"语音未定义-[{who}]{theme}")
voices = Voices()