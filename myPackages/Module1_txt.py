from __future__ import annotations
import time

def get_shell_len(txt):#求字符串在Shell中的显示长度
    """求字符串在Shell中的显示长度"""
    len1=r"0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz<>/|-+\[]= :!@#%^&*()\{\}_.,;~"
    l=0
    for i in txt:
        if i in len1:
            l+=1
        else:
            l+=2
    return l

def print_plus(txt:str, sec:float=0.3):
    """
    增强视觉print函数
    :param txt: 文本
    :param sec: 打印总时长
    :return:
    """
    i=len(txt)
    if i<10:
        sec-=0.1
    if sec != 0:
        for j in txt:
            print(j,end="")
            time.sleep(sec/i)
        print("")
        time.sleep(0.2)
    else:
        print(txt)

def input_plus(txt:str,sec:float=0.3):
    """
    增强视觉input函数
    :param txt: 文本
    :param sec: 打印总时长
    :return:
    """
    length=len(txt)
    for j in txt:
        print(j,end="")
        time.sleep(sec/length)
    if not txt.endswith(">>>"):
        print(">>>",end="")
    return input("")

class Tree:#打印用tree对象

    def __init__(self,topic,*ag:str|int|list|dict|Tree):
        self.topic=topic
        self.body=[]
        for i in ag:
            if type(i) == str or type(i) == int:
                self.body.append(i)
            elif isinstance(i, list):
                for j in i:
                    self.body.append(j)
            elif isinstance(i, dict):
                for j in i:
                    self.body.append(j+" "*(10-get_shell_len(j))+f" *{i[j]}")
            elif type(i) == Tree:
                i:Tree
                self.body.append(i.topic)
                for j in i.body:
                    self.body.append(f" -{j}")

    def tree_print(self, can_be_folded=False):
        print(self.topic)
        if can_be_folded and len(self.body) > 3:
            for i in self.body[0:3]:
                print("|")
                print("|-"+str(i))
            print("|")
            print("|>>[已折叠]")
            print("")
        else:
            for i in self.body:
                print("|")
                print("|-"+str(i))
            print("")

    def generate_line_list(self, can_be_folded=False):
        """
        行切片生成函数
        """
        printlist=[]
        printlist.append(self.topic)
        if can_be_folded and len(self.body) > 3:
            for i in self.body[0:3]:
                printlist.append("|")
                printlist.append("|-"+str(i))
            printlist.append("|")
            printlist.append("|>>[已折叠]")
            printlist.append("")
        else:
            for i in self.body:
                printlist.append("|")
                printlist.append("|-"+i)
            printlist.append("")
        return printlist