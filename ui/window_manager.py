import tkinter as tk
from typing import Dict, Optional, Callable
from abc import ABC, abstractmethod
from systems.theme import ThemeManager, ThemeType

class Screen(ABC):
    """屏幕基类"""
    
    def __init__(self, parent: tk.Frame, theme: ThemeManager):
        self.parent = parent
        self.theme = theme
        self._widgets: Dict[str, tk.Widget] = {}
        self.setup_ui()
    
    @abstractmethod
    def setup_ui(self):
        """设置UI，子类必须实现"""
        pass
    
    def show(self):
        """显示屏幕"""
        self.parent.pack(fill=tk.BOTH, expand=True)
        self.on_enter()
    
    def hide(self):
        """隐藏屏幕"""
        self.parent.pack_forget()
        self.on_exit()
    
    def on_enter(self):
        """进入屏幕时调用"""
        pass
    
    def on_exit(self):
        """离开屏幕时调用"""
        pass
    
    def apply_theme(self):
        """应用主题"""
        self.parent.config(bg=self.theme.get_color('bg_main'))
    
    def clear_widgets(self):
        """清空所有控件"""
        for widget in self.parent.winfo_children():
            widget.destroy()
        self._widgets.clear()

class WindowManager:
    """窗口管理器"""
    
    def __init__(self, root: tk.Tk, theme: ThemeManager):
        self.root = root
        self.theme = theme
        self.screens: Dict[str, Screen] = {}
        self.screen_stack: list = []
        self.current_screen: Optional[Screen] = None
        self._setup_window()
    
    def _setup_window(self):
        """设置主窗口"""
        self.root.configure(bg=self.theme.get_color('bg_main'))
    
    def register_screen(self, name: str, screen: Screen):
        """注册屏幕"""
        self.screens[name] = screen
    
    def switch_screen(self, screen_name: str, **kwargs):
        """切换屏幕"""
        if screen_name not in self.screens:
            raise ValueError(f"屏幕 {screen_name} 未注册")
        
        # 隐藏当前屏幕
        if self.current_screen:
            self.current_screen.hide()
            self.screen_stack.append(self.current_screen)
        
        # 显示新屏幕
        self.current_screen = self.screens[screen_name]
        self.current_screen.show()
    
    def go_back(self):
        """返回上一个屏幕"""
        if self.screen_stack:
            if self.current_screen:
                self.current_screen.hide()
            self.current_screen = self.screen_stack.pop()
            self.current_screen.show()
    
    def update_theme(self):
        """更新主题"""
        for screen in self.screens.values():
            screen.apply_theme()
        self._setup_window()
    
    def run(self):
        """运行程序主循环"""
        self.root.mainloop()
