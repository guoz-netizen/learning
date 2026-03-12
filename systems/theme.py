from enum import Enum
from typing import Dict, Tuple

class ThemeType(Enum):
    LIGHT = "light"
    DARK = "dark"

class ThemeManager:
    """主题管理器"""
    
    LIGHT_PALETTE = {
        # 主要颜色
        'primary': '#2196F3',
        'secondary': '#FFC107',
        'accent': '#FF5722',
        
        # 背景和前景
        'bg_main': '#FFFFFF',
        'bg_secondary': '#F5F5F5',
        'fg_main': '#212121',
        'fg_secondary': '#757575',
        
        # 状态颜色
        'success': '#4CAF50',
        'error': '#F44336',
        'warning': '#FF9800',
        'info': '#2196F3',
        
        # 按钮颜色
        'button_bg': '#2196F3',
        'button_fg': '#FFFFFF',
        'button_hover': '#1976D2',
        'button_active': '#1565C0',
        
        # 输入框
        'input_bg': '#FFFFFF',
        'input_fg': '#212121',
        'input_border': '#BDBDBD',
        'input_focus': '#2196F3',
        
        # 其他
        'border': '#E0E0E0',
        'disabled': '#BDBDBD'
    }
    
    DARK_PALETTE = {
        # 主要颜色
        'primary': '#64B5F6',
        'secondary': '#FFD54F',
        'accent': '#FF7043',
        
        # 背景和前景
        'bg_main': '#121212',
        'bg_secondary': '#1E1E1E',
        'fg_main': '#FFFFFF',
        'fg_secondary': '#B0B0B0',
        
        # 状态颜色
        'success': '#81C784',
        'error': '#EF5350',
        'warning': '#FFB74D',
        'info': '#64B5F6',
        
        # 按钮颜色
        'button_bg': '#1976D2',
        'button_fg': '#FFFFFF',
        'button_hover': '#2196F3',
        'button_active': '#42A5F5',
        
        # 输入框
        'input_bg': '#2C2C2C',
        'input_fg': '#FFFFFF',
        'input_border': '#424242',
        'input_focus': '#64B5F6',
        
        # 其他
        'border': '#424242',
        'disabled': '#616161'
    }
    
    FONTS = {
        'title': ('Arial', 24, 'bold'),
        'heading': ('Arial', 18, 'bold'),
        'body': ('Arial', 12, 'normal'),
        'button': ('Arial', 11, 'normal'),
        'small': ('Arial', 10, 'normal'),
        'mono': ('Courier New', 11, 'normal')
    }
    
    def __init__(self, theme_type: ThemeType = ThemeType.LIGHT):
        self.current_theme = theme_type
        self.colors = self._get_palette()
    
    def _get_palette(self) -> Dict[str, str]:
        """获取当前主题的调色板"""
        if self.current_theme == ThemeType.LIGHT:
            return self.LIGHT_PALETTE.copy()
        else:
            return self.DARK_PALETTE.copy()
    
    def set_theme(self, theme_type: ThemeType):
        """切换主题"""
        self.current_theme = theme_type
        self.colors = self._get_palette()
    
    def get_color(self, key: str) -> str:
        """获取颜色值"""
        return self.colors.get(key, '#000000')
    
    def get_font(self, key: str = 'body') -> Tuple[str, int, str]:
        """获取字体"""
        return self.FONTS.get(key, self.FONTS['body'])
    
    def toggle_theme(self):
        """切换主题"""
        new_theme = ThemeType.DARK if self.current_theme == ThemeType.LIGHT else ThemeType.LIGHT
        self.set_theme(new_theme)
