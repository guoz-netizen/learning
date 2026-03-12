import tkinter as tk
from game.config import GameConfig, DifficultyLevel
from game.engine import GameEngine
from systems.theme import ThemeManager, ThemeType
from systems.sound import SoundManager
from data.leaderboard import LeaderboardManager
from data.settings import SettingsManager
from ui.window_manager import WindowManager, Screen
from ui.screens import MenuScreen, GameScreen, SettingsScreen, LeaderboardScreen
from constants import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE

class GuessNumberGameApp:
    """游戏应用主类"""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.title(WINDOW_TITLE)
        self.root.resizable(False, False)
        
        # 初始化管理器
        self.settings_manager = SettingsManager()
        self.leaderboard_manager = LeaderboardManager()
        self.sound_manager = SoundManager()
        
        # 根据设置初始化主题
        theme_type = ThemeType.DARK if self.settings_manager.get('theme') == 'dark' else ThemeType.LIGHT
        self.theme_manager = ThemeManager(theme_type)
        
        # 初始化窗口管理器
        self.window_manager = WindowManager(self.root, self.theme_manager)
        
        # 创建游戏引擎（默认中等难度）
        self.game_engine = GameEngine(GameConfig.medium())
        
        # 设置主容器
        self.main_container = tk.Frame(self.root, bg=self.theme_manager.get_color('bg_main'))
        self.main_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 初始化所有屏幕
        self._setup_screens()
        
        # 显示菜单屏幕
        self.window_manager.switch_screen('menu')
    
    def _setup_screens(self):
        """设置所有屏幕"""
        # 菜单屏幕
        menu_frame = tk.Frame(self.main_container)
        menu_screen = MenuScreen(
            menu_frame,
            self.theme_manager,
            on_start_game=self._on_start_game,
            on_settings=self._on_settings,
            on_leaderboard=self._on_leaderboard
        )
        self.window_manager.register_screen('menu', menu_screen)
        
        # 游戏屏幕
        game_frame = tk.Frame(self.main_container)
        self.game_screen = GameScreen(
            game_frame,
            self.theme_manager,
            self.game_engine,
            self.sound_manager,
            self.settings_manager,
            self.leaderboard_manager,
            on_back=self._on_game_back
        )
        self.window_manager.register_screen('game', self.game_screen)
        
        # 设置屏幕
        settings_frame = tk.Frame(self.main_container)
        settings_screen = SettingsScreen(
            settings_frame,
            self.theme_manager,
            self.settings_manager,
            self.sound_manager,
            on_back=self._on_settings_back,
            on_theme_changed=self._on_theme_changed
        )
        self.window_manager.register_screen('settings', settings_screen)
        
        # 排行榜屏幕
        leaderboard_frame = tk.Frame(self.main_container)
        leaderboard_screen = LeaderboardScreen(
            leaderboard_frame,
            self.theme_manager,
            self.leaderboard_manager,
            on_back=self._on_leaderboard_back
        )
        self.window_manager.register_screen('leaderboard', leaderboard_screen)
    
    def _on_start_game(self):
        """开始游戏"""
        # 获取设置的难度
        difficulty = self.settings_manager.get('difficulty', 'medium')
        
        if difficulty == 'easy':
            config = GameConfig.easy()
        elif difficulty == 'hard':
            config = GameConfig.hard()
        else:
            config = GameConfig.medium()
        
        self.game_engine = GameEngine(config)
        
        # 重新创建游戏屏幕
        game_frame = tk.Frame(self.main_container)
        self.game_screen = GameScreen(
            game_frame,
            self.theme_manager,
            self.game_engine,
            self.sound_manager,
            self.settings_manager,
            self.leaderboard_manager,
            on_back=self._on_game_back
        )
        self.window_manager.screens['game'] = self.game_screen
        self.window_manager.switch_screen('game')
    
    def _on_settings(self):
        """打开设置"""
        self.window_manager.switch_screen('settings')
    
    def _on_leaderboard(self):
        """打开排行榜"""
        self.window_manager.switch_screen('leaderboard')
    
    def _on_game_back(self):
        """游戏返回菜单"""
        self.window_manager.switch_screen('menu')
    
    def _on_settings_back(self):
        """设置返回菜单"""
        self.window_manager.switch_screen('menu')
    
    def _on_leaderboard_back(self):
        """排行榜返回菜单"""
        self.window_manager.switch_screen('menu')
    
    def _on_theme_changed(self):
        """主题改变"""
        self.theme_manager.toggle_theme()
        self.settings_manager.set('theme', self.theme_manager.current_theme.value)
        self.window_manager.update_theme()
    
    def run(self):
        """运行程序"""
        self.window_manager.run()

def main():
    """主函数"""
    root = tk.Tk()
    app = GuessNumberGameApp(root)
    app.run()

if __name__ == '__main__':
    main()
