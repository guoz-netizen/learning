import json
import os
from typing import Dict, Any

SETTINGS_FILE = 'data/settings.json'

class SettingsManager:
    """设置管理器"""
    
    DEFAULT_SETTINGS = {
        'theme': 'light',
        'sound_enabled': True,
        'volume': 1.0,
        'difficulty': 'medium',
        'player_name': 'Player',
        'show_hints': True
    }
    
    def __init__(self, file_path: str = SETTINGS_FILE):
        self.file_path = file_path
        self.settings = self._load_settings()
    
    def _load_settings(self) -> Dict[str, Any]:
        """加载设置"""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # 合并默认设置和加载的设置
                    return {**self.DEFAULT_SETTINGS, **data}
            except Exception as e:
                print(f"加载设置失败: {e}")
        
        return self.DEFAULT_SETTINGS.copy()
    
    def _save_settings(self):
        """保存设置"""
        try:
            os.makedirs(os.path.dirname(self.file_path) or '.', exist_ok=True)
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存设置失败: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取设置值"""
        return self.settings.get(key, default)
    
    def set(self, key: str, value: Any):
        """设置值"""
        self.settings[key] = value
        self._save_settings()
    
    def update(self, settings_dict: Dict[str, Any]):
        """批量更新设置"""
        self.settings.update(settings_dict)
        self._save_settings()
    
    def reset_to_default(self):
        """重置为默认设置"""
        self.settings = self.DEFAULT_SETTINGS.copy()
        self._save_settings()
