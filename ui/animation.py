import tkinter as tk
from typing import Callable, Optional

class AnimationManager:
    """动画管理器"""
    
    @staticmethod
    def fade_in(widget: tk.Widget, duration: int = 300, callback: Optional[Callable] = None):
        """淡入动画"""
        # 由于tkinter限制，这里采用简化的实现
        widget.pack()
        if callback:
            widget.after(duration, callback)
    
    @staticmethod
    def fade_out(widget: tk.Widget, duration: int = 300, callback: Optional[Callable] = None):
        """淡出动画"""
        widget.pack_forget()
        if callback:
            widget.after(duration, callback)
    
    @staticmethod
    def color_flash(widget: tk.Widget, target_color: str, original_color: str, 
                   duration: int = 200, callback: Optional[Callable] = None):
        """颜色闪烁动画"""
        widget.config(bg=target_color)
        def restore():
            widget.config(bg=original_color)
            if callback:
                callback()
        widget.after(duration, restore)
    
    @staticmethod
    def pulse(widget: tk.Widget, duration: int = 500, callback: Optional[Callable] = None):
        """脉冲动画（缩放）"""
        # 这是一个简化的实现，真实脉冲需要更复杂的计算
        if callback:
            widget.after(duration, callback)
