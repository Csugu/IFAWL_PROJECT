import pygame
import threading
import time
from pathlib import Path

# 初始化
pygame.init()
pygame.mixer.init()

class SoundsManager:
    """
    缩写与命名
    背景音乐 /music _bgm
    短音效 /sfx _sfx
    """

    def __init__(self):
        self.music_dir = Path(__file__).parent.parent / "resources" / "sounds" / "music"
        self.sfx_dir = Path(__file__).parent.parent / "resources" / "sounds" / "sfx"
        self.sfx_channel = pygame.mixer.Channel(0)

    def switch_to_bgm(self, filename, fade_ms=500):
        """
        在以异步方式切换播放背景音乐
        :param filename: 文件名，带后缀
        :param fade_ms: 淡入淡出毫秒数
        :return: 无
        """
        self.stop_bgm()
        pygame.mixer.music.load(self.music_dir / filename)
        pygame.mixer.music.play(loops=-1,fade_ms=fade_ms)

    def stop_bgm(self, fade_ms=500):
        """
        停止背景音乐
        :param fade_ms: 淡入淡出毫秒数
        :return: 无
        """
        pygame.mixer.music.fadeout(fade_ms)

    def play_sfx(self,filename):
        """
        在0号音轨上播放短音效
        :param filename: 文件名，带后缀
        :return: 无
        """
        sound = pygame.mixer.Sound(self.sfx_dir / filename)
        self.sfx_channel.play(sound)


sounds_manager = SoundsManager()