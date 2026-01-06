from core.Module1_txt import print_plus,input_plus
from core.Module2_json_loader import json_loader

ALL_POLT_DATA:dict[str,dict[str,dict[str,str]]] = json_loader.load("plots")

class Plot:

    def __init__(self,session:str,paragraph:str):
        # 元数据字段
        self.title = ALL_POLT_DATA[session][paragraph]["title"]
        self.raw_txt = ALL_POLT_DATA[session][paragraph]["raw_txt"]
        # 原始文本
        self.lines = self.raw_txt.split("\n\n")
        # 下一段落
        self.next_paragraphs:list[Plot] = []

    @staticmethod
    def __processed(line:str):
        out = line
        if line.startswith("-"):
            out = "[" + line[1:]
            out = out.replace("-","]")
            return out
        if line.startswith("【") and line.endswith("】"):
            content = line[1:-1]
            out = "[enter]" + content
            return out
        return out

    def play(self,info_map):
        next_index = 0
        for line in self.lines:
            processed = self.__processed(line)
            processed = processed.format_map(info_map)
            if processed.startswith("[enter]"):
                input_plus(processed)
                print()
            else:
                print_plus(processed)
                print()
        return self.next_paragraphs[next_index]

class PlotManager:
    def __init__(self):
        self.plots:dict[int,dict[int,Plot]] = {}
        # 指针生成
        for session in ALL_POLT_DATA:
            self.plots[int(session)] = {}
            for paragraph in ALL_POLT_DATA[session]:
                self.plots[int(session)][int(paragraph)] = Plot(session,paragraph)
        # 设置每个段落的后续段落链接
        for session_key, session_data in ALL_POLT_DATA.items():
            session_id = int(session_key)
            for paragraph_key, paragraph_data in session_data.items():
                paragraph_id = int(paragraph_key)
                current_plot = self.plots[session_id][paragraph_id]

                # 如果明确定义了下一个段落，则使用它
                if "next_paragraph" in paragraph_data:
                    for next_paragraph_index in paragraph_data["next_paragraph"]:
                        next_plot = self.plots[session_id][int(next_paragraph_index)]
                        current_plot.next_paragraphs.append(next_plot)
                # 否则，自动链接到下一个段落（如果是最后一个段落则链接到None）
                else:
                    is_last_paragraph = (paragraph_id == len(self.plots[session_id]) - 1)
                    next_plot = None if is_last_paragraph else self.plots[session_id][paragraph_id + 1]
                    current_plot.next_paragraphs.append(next_plot)
        # 信息映射表
        self.information_map = {}

    def set_information_map(self,info_map:dict):
        self.information_map = info_map

    def play_session(self,session:int):
        """
        播放一个会话|核心业务封装
        :param session: 会话编号
        :return: 无
        """
        current = self.plots[session][0]
        while current is not None:
            current = current.play(self.information_map)

plot_manager = PlotManager()