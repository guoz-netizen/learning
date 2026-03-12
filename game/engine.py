from enum import Enum
from dataclasses import dataclass
from typing import Tuple
import random
from game.config import GameConfig, DifficultyLevel

class GameState(Enum):
    IDLE = "idle"
    PLAYING = "playing"
    WON = "won"
    LOST = "lost"

@dataclass
class GuessResult:
    """猜测结果"""
    guess: int
    is_correct: bool
    hint: str
    attempts_left: int
    game_state: GameState

class GameEngine:
    """游戏引擎"""
    
    def __init__(self, config: GameConfig):
        self.config = config
        self.secret_number = 0
        self.attempts = 0
        self.game_state = GameState.IDLE
        self.guesses_history = []
        self.start_game()
    
    def start_game(self):
        """开始新游戏"""
        self.secret_number = random.randint(self.config.min_number, self.config.max_number)
        self.attempts = 0
        self.game_state = GameState.PLAYING
        self.guesses_history = []
    
    def make_guess(self, guess: int) -> GuessResult:
        """提交猜测"""
        if self.game_state != GameState.PLAYING:
            return GuessResult(
                guess=guess,
                is_correct=False,
                hint="游戏未开始或已结束",
                attempts_left=self.config.max_attempts - self.attempts,
                game_state=self.game_state
            )
        
        if guess < self.config.min_number or guess > self.config.max_number:
            return GuessResult(
                guess=guess,
                is_correct=False,
                hint=f"请输入{self.config.min_number}-{self.config.max_number}之间的数字",
                attempts_left=self.config.max_attempts - self.attempts,
                game_state=self.game_state
            )
        
        self.attempts += 1
        self.guesses_history.append(guess)
        
        if guess == self.secret_number:
            self.game_state = GameState.WON
            return GuessResult(
                guess=guess,
                is_correct=True,
                hint=f"恭喜！你用了{self.attempts}次就猜对了！",
                attempts_left=0,
                game_state=self.game_state
            )
        
        # 生成提示
        hint = self._generate_hint(guess)
        
        if self.attempts >= self.config.max_attempts:
            self.game_state = GameState.LOST
            return GuessResult(
                guess=guess,
                is_correct=False,
                hint=f"游戏结束！正确答案是{self.secret_number}",
                attempts_left=0,
                game_state=self.game_state
            )
        
        return GuessResult(
            guess=guess,
            is_correct=False,
            hint=hint,
            attempts_left=self.config.max_attempts - self.attempts,
            game_state=self.game_state
        )
    
    def _generate_hint(self, guess: int) -> str:
        """生成提示"""
        if not self.config.hint_enabled:
            return ""
        
        if self.config.hint_type == "range":
            if guess < self.secret_number:
                return f"数字太小了！范围：{guess} - {self.config.max_number}"
            else:
                return f"数字太大了！范围：{self.config.min_number} - {guess}"
        
        return ""
    
    def get_statistics(self) -> dict:
        """获取游戏统计信息"""
        return {
            "attempts": self.attempts,
            "max_attempts": self.config.max_attempts,
            "difficulty": self.config.difficulty_level.value,
            "secret_number": self.secret_number if self.game_state != GameState.PLAYING else None,
            "guesses_history": self.guesses_history,
            "game_state": self.game_state.value
        }
    
    def is_game_over(self) -> bool:
        """游戏是否结束"""
        return self.game_state in [GameState.WON, GameState.LOST]
