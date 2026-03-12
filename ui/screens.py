import tkinter as tk
from tkinter import messagebox, ttk
from typing import Callable, Dict, Optional
from ui.window_manager import Screen
from systems.theme import ThemeManager
from game.engine import GameEngine
from game.config import GameConfig, DifficultyLevel
from data.leaderboard import LeaderboardManager, GameRecord
from data.settings import SettingsManager
from systems.sound import SoundManager

class MenuScreen(Screen):
    """菜单屏幕"""
    
    def __init__(self, parent: tk.Frame, theme: ThemeManager, 
                 on_start_game: Callable, on_settings: Callable, 
                 on_leaderboard: Callable):
        self.on_start_game = on_start_game
        self.on_settings = on_settings
        self.on_leaderboard = on_leaderboard
        super().__init__(parent, theme)
    
    def setup_ui(self):
        """设置菜单UI"""
        self.parent.config(bg=self.theme.get_color('bg_main'))
        
        # 标题
        title_label = tk.Label(
            self.parent,
            text='猜数字游戏',
            font=self.theme.get_font('title'),
            fg=self.theme.get_color('fg_main'),
            bg=self.theme.get_color('bg_main')
        )
        title_label.pack(pady=50)
        
        # 按钮框架
        button_frame = tk.Frame(self.parent, bg=self.theme.get_color('bg_main'))
        button_frame.pack(expand=True)
        
        # 开始游戏按钮
        start_btn = tk.Button(
            button_frame,
            text='开始游戏',
            font=self.theme.get_font('button'),
            bg=self.theme.get_color('button_bg'),
            fg=self.theme.get_color('button_fg'),
            width=20,
            height=2,
            command=self.on_start_game,
            relief=tk.FLAT,
            cursor='hand2'
        )
        start_btn.pack(pady=15)
        
        # 排行榜按钮
        leaderboard_btn = tk.Button(
            button_frame,
            text='排行榜',
            font=self.theme.get_font('button'),
            bg=self.theme.get_color('primary'),
            fg=self.theme.get_color('button_fg'),
            width=20,
            height=2,
            command=self.on_leaderboard,
            relief=tk.FLAT,
            cursor='hand2'
        )
        leaderboard_btn.pack(pady=15)
        
        # 设置按钮
        settings_btn = tk.Button(
            button_frame,
            text='设置',
            font=self.theme.get_font('button'),
            bg=self.theme.get_color('secondary'),
            fg='#000',
            width=20,
            height=2,
            command=self.on_settings,
            relief=tk.FLAT,
            cursor='hand2'
        )
        settings_btn.pack(pady=15)
        
        # 退出按钮
        exit_btn = tk.Button(
            button_frame,
            text='退出',
            font=self.theme.get_font('button'),
            bg=self.theme.get_color('error'),
            fg=self.theme.get_color('button_fg'),
            width=20,
            height=2,
            command=self.parent.quit,
            relief=tk.FLAT,
            cursor='hand2'
        )
        exit_btn.pack(pady=15)

class SettingsScreen(Screen):
    """设置屏幕"""
    
    def __init__(self, parent: tk.Frame, theme: ThemeManager, 
                 settings_manager: SettingsManager, sound_manager: SoundManager,
                 on_back: Callable, on_theme_changed: Callable):
        self.settings_manager = settings_manager
        self.sound_manager = sound_manager
        self.on_back = on_back
        self.on_theme_changed = on_theme_changed
        super().__init__(parent, theme)
    
    def setup_ui(self):
        """设置页面UI"""
        self.parent.config(bg=self.theme.get_color('bg_main'))
        
        # 标题
        title_label = tk.Label(
            self.parent,
            text='设置',
            font=self.theme.get_font('heading'),
            fg=self.theme.get_color('fg_main'),
            bg=self.theme.get_color('bg_main')
        )
        title_label.pack(pady=20)
        
        # 设置框架（可滚动）
        settings_frame = tk.Frame(self.parent, bg=self.theme.get_color('bg_secondary'))
        settings_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # 主题选择
        theme_frame = tk.Frame(settings_frame, bg=self.theme.get_color('bg_secondary'))
        theme_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(theme_frame, text='主题:', font=self.theme.get_font('body'),
                bg=self.theme.get_color('bg_secondary'),
                fg=self.theme.get_color('fg_main')).pack(side=tk.LEFT, padx=10)
        
        theme_var = tk.StringVar(value=self.settings_manager.get('theme'))
        theme_radio1 = tk.Radiobutton(theme_frame, text='浅色', variable=theme_var, 
                                     value='light', command=self._on_theme_change)
        theme_radio1.pack(side=tk.LEFT, padx=10)
        theme_radio2 = tk.Radiobutton(theme_frame, text='深色', variable=theme_var, 
                                     value='dark', command=self._on_theme_change)
        theme_radio2.pack(side=tk.LEFT, padx=10)
        
        # 音效设置
        sound_frame = tk.Frame(settings_frame, bg=self.theme.get_color('bg_secondary'))
        sound_frame.pack(fill=tk.X, pady=10)
        
        sound_var = tk.BooleanVar(value=self.settings_manager.get('sound_enabled'))
        sound_check = tk.Checkbutton(sound_frame, text='启用音效', variable=sound_var,
                                    command=lambda: self.settings_manager.set('sound_enabled', sound_var.get()),
                                    bg=self.theme.get_color('bg_secondary'),
                                    fg=self.theme.get_color('fg_main'),
                                    selectcolor=self.theme.get_color('bg_secondary'))
        sound_check.pack(side=tk.LEFT, padx=10)
        
        # 返回按钮
        back_btn = tk.Button(
            self.parent,
            text='返回',
            font=self.theme.get_font('button'),
            bg=self.theme.get_color('button_bg'),
            fg=self.theme.get_color('button_fg'),
            command=self.on_back,
            relief=tk.FLAT
        )
        back_btn.pack(pady=20)
    
    def _on_theme_change(self):
        """主题改变回调"""
        # 这里会从UI获取选择并更新
        self.on_theme_changed()

class GameScreen(Screen):
    """游戏屏幕"""
    
    def __init__(self, parent: tk.Frame, theme: ThemeManager,
                 game_engine: GameEngine, sound_manager: SoundManager,
                 settings_manager: SettingsManager, leaderboard_manager: LeaderboardManager,
                 on_back: Callable):
        self.game_engine = game_engine
        self.sound_manager = sound_manager
        self.settings_manager = settings_manager
        self.leaderboard_manager = leaderboard_manager
        self.on_back = on_back
        super().__init__(parent, theme)
    
    def setup_ui(self):
        """设置游戏UI"""
        self.parent.config(bg=self.theme.get_color('bg_main'))
        
        # 标题
        title_label = tk.Label(
            self.parent,
            text='猜数字游戏',
            font=self.theme.get_font('heading'),
            fg=self.theme.get_color('fg_main'),
            bg=self.theme.get_color('bg_main')
        )
        title_label.pack(pady=20)
        
        # 游戏信息
        info_label = tk.Label(
            self.parent,
            text=f"范围: {self.game_engine.config.min_number}-{self.game_engine.config.max_number}\n难度: {self.game_engine.config.difficulty_level.value}",
            font=self.theme.get_font('small'),
            fg=self.theme.get_color('fg_secondary'),
            bg=self.theme.get_color('bg_main')
        )
        info_label.pack(pady=10)
        
        # 剩余次数
        self.attempts_label = tk.Label(
            self.parent,
            text=f"剩余机会: {self.game_engine.config.max_attempts - self.game_engine.attempts}",
            font=self.theme.get_font('body'),
            fg=self.theme.get_color('primary'),
            bg=self.theme.get_color('bg_main')
        )
        self.attempts_label.pack(pady=10)
        
        # 输入框
        input_frame = tk.Frame(self.parent, bg=self.theme.get_color('bg_main'))
        input_frame.pack(pady=15)
        
        tk.Label(input_frame, text='输入数字:', font=self.theme.get_font('body'),
                bg=self.theme.get_color('bg_main'),
                fg=self.theme.get_color('fg_main')).pack(side=tk.LEFT, padx=10)
        
        self.entry = tk.Entry(input_frame, font=self.theme.get_font('body'),
                             bg=self.theme.get_color('input_bg'),
                             fg=self.theme.get_color('input_fg'),
                             width=10)
        self.entry.pack(side=tk.LEFT, padx=10)
        self.entry.bind('<Return>', lambda e: self.submit_guess())
        
        # 確定按钮
        submit_btn = tk.Button(
            input_frame,
            text='确定',
            font=self.theme.get_font('button'),
            bg=self.theme.get_color('button_bg'),
            fg=self.theme.get_color('button_fg'),
            command=self.submit_guess,
            relief=tk.FLAT
        )
        submit_btn.pack(side=tk.LEFT, padx=10)
        
        # 反馈标签
        self.feedback_label = tk.Label(
            self.parent,
            text='',
            font=self.theme.get_font('body'),
            fg=self.theme.get_color('warning'),
            bg=self.theme.get_color('bg_main')
        )
        self.feedback_label.pack(pady=15)
        
        # 下方按钮框
        button_frame = tk.Frame(self.parent, bg=self.theme.get_color('bg_main'))
        button_frame.pack(pady=20)
        
        # 重新开始按钮
        restart_btn = tk.Button(
            button_frame,
            text='重新开始',
            font=self.theme.get_font('button'),
            bg=self.theme.get_color('secondary'),
            fg='#000',
            command=self.restart_game,
            relief=tk.FLAT
        )
        restart_btn.pack(side=tk.LEFT, padx=10)
        
        # 返回菜单按钮
        back_btn = tk.Button(
            button_frame,
            text='返回菜单',
            font=self.theme.get_font('button'),
            bg=self.theme.get_color('primary'),
            fg=self.theme.get_color('button_fg'),
            command=self._on_menu_click,
            relief=tk.FLAT
        )
        back_btn.pack(side=tk.LEFT, padx=10)
        
        self.entry.focus()
    
    def submit_guess(self):
        """提交猜测"""
        try:
            guess = int(self.entry.get())
            result = self.game_engine.make_guess(guess)
            
            # 播放音效
            if result.is_correct:
                self.sound_manager.play_sound('correct')
                self.feedback_label.config(text=result.hint, fg=self.theme.get_color('success'))
                messagebox.showinfo('成功!', result.hint)
                self._save_record()
            elif result.game_state.value == 'lost':
                self.sound_manager.play_sound('game_over')
                self.feedback_label.config(text=result.hint, fg=self.theme.get_color('error'))
                messagebox.showinfo('游戏结束', result.hint)
            else:
                self.sound_manager.play_sound('wrong')
                self.feedback_label.config(text=result.hint, fg=self.theme.get_color('warning'))
            
            # 更新UI
            self.attempts_label.config(
                text=f"剩余机会: {result.attempts_left}"
            )
            self.entry.delete(0, tk.END)
            
            if self.game_engine.is_game_over():
                self.entry.config(state=tk.DISABLED)
        
        except ValueError:
            messagebox.showerror('输入错误', '请输入有效的数字!')
    
    def _save_record(self):
        """保存游戏记录"""
        player_name = self.settings_manager.get('player_name', 'Player')
        record = GameRecord(
            player_name=player_name,
            attempts=self.game_engine.attempts,
            max_attempts=self.game_engine.config.max_attempts,
            difficulty=self.game_engine.config.difficulty_level.value
        )
        self.leaderboard_manager.add_record(record)
    
    def restart_game(self):
        """重新开始游戏"""
        self.game_engine.start_game()
        self.entry.config(state=tk.NORMAL)
        self.feedback_label.config(text='')
        self.attempts_label.config(
            text=f"剩余机会: {self.game_engine.config.max_attempts}"
        )
        self.entry.delete(0, tk.END)
        self.entry.focus()
    
    def _on_menu_click(self):
        """菜单点击"""
        self.on_back()

class LeaderboardScreen(Screen):
    """排行榜屏幕"""
    
    def __init__(self, parent: tk.Frame, theme: ThemeManager,
                 leaderboard_manager: LeaderboardManager, on_back: Callable):
        self.leaderboard_manager = leaderboard_manager
        self.on_back = on_back
        super().__init__(parent, theme)
    
    def setup_ui(self):
        """设置排行榜UI"""
        self.parent.config(bg=self.theme.get_color('bg_main'))
        
        # 标题
        title_label = tk.Label(
            self.parent,
            text='排行榜',
            font=self.theme.get_font('heading'),
            fg=self.theme.get_color('fg_main'),
            bg=self.theme.get_color('bg_main')
        )
        title_label.pack(pady=20)
        
        # 难度筛选
        filter_frame = tk.Frame(self.parent, bg=self.theme.get_color('bg_main'))
        filter_frame.pack(pady=10)
        
        tk.Label(filter_frame, text='难度:', font=self.theme.get_font('body'),
                bg=self.theme.get_color('bg_main'),
                fg=self.theme.get_color('fg_main')).pack(side=tk.LEFT, padx=10)
        
        self.difficulty_var = tk.StringVar(value='all')
        for diff in ['all', 'easy', 'medium', 'hard']:
            tk.Radiobutton(filter_frame, text=diff, variable=self.difficulty_var,
                         value=diff, command=self.refresh_records,
                         bg=self.theme.get_color('bg_main'),
                         fg=self.theme.get_color('fg_main'),
                         selectcolor=self.theme.get_color('bg_secondary')).pack(side=tk.LEFT, padx=5)
        
        # 排行榜表格
        table_frame = tk.Frame(self.parent, bg=self.theme.get_color('bg_secondary'))
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # 创建Treeview
        columns = ('排名', '玩家', '尝试次数', '难度')
        self.tree = ttk.Treeview(table_frame, columns=columns, height=15, show='headings')
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=80)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # 返回按钮
        back_btn = tk.Button(
            self.parent,
            text='返回',
            font=self.theme.get_font('button'),
            bg=self.theme.get_color('button_bg'),
            fg=self.theme.get_color('button_fg'),
            command=self.on_back,
            relief=tk.FLAT
        )
        back_btn.pack(pady=20)
    
    def refresh_records(self):
        """刷新排行榜"""
        # 清空现有记录
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # 获取记录
        difficulty = self.difficulty_var.get()
        if difficulty == 'all':
            records = self.leaderboard_manager.get_top_records(limit=20)
        else:
            records = self.leaderboard_manager.get_top_records(difficulty, limit=20)
        
        # 添加到表格
        for idx, record in enumerate(records, 1):
            self.tree.insert('', tk.END, values=(
                idx,
                record.player_name,
                record.attempts,
                record.difficulty
            ))
    
    def on_enter(self):
        """进入屏幕时刷新"""
        self.refresh_records()
