import winsound
from typing import Optional
import os

class SoundManager:
    """音效管理器"""
    
    def __init__(self, enabled: bool = True, volume: float = 1.0):
        self.enabled = enabled
        self.volume = max(0.0, min(1.0, volume))  # 限制在0-1之间
        
        # 音效文件路径（如果有的话）
        self.sounds = {
            'correct': None,  # 正确
            'wrong': None,    # 错误
            'game_over': None,  # 游戏结束
            'button_click': None,  # 按钮点击
            'background': None  # 背景音乐
        }
    
    def play_sound(self, sound_type: str) -> None:
        """播放音效"""
        if not self.enabled or sound_type not in self.sounds:
            return
        
        try:
            if sound_type == 'correct':
                # 成功音效：两个短促的声音
                winsound.Beep(800, 200)
                winsound.Beep(1000, 300)
            elif sound_type == 'wrong':
                # 错误音效：低频声
                winsound.Beep(400, 300)
            elif sound_type == 'game_over':
                # 游戏结束音效
                winsound.Beep(600, 200)
                winsound.Beep(400, 200)
            elif sound_type == 'button_click':
                # 按钮点击音效
                winsound.Beep(600, 100)
        except Exception as e:
            print(f"播放音效时出错: {e}")
    
    def set_volume(self, volume: float) -> None:
        """设置音量（0-1）"""
        self.volume = max(0.0, min(1.0, volume))
    
    def toggle_sound(self) -> None:
        """切换音效开关"""
        self.enabled = not self.enabled
    
    def load_custom_sound(self, sound_type: str, file_path: str) -> bool:
        """加载自定义音效文件"""
        if os.path.exists(file_path):
            self.sounds[sound_type] = file_path
            return True
        return False
