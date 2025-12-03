import time

def printplus(txt:str,sec:float=0.3):
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
            time.sleep(sec/len(txt))
        print("")
        time.sleep(0.2)
    else:
        print(txt)