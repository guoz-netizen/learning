from dataclasses import dataclass
from enum import Enum

class DifficultyLevel(Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    CUSTOM = "custom"

@dataclass
class GameConfig:
    """游戏配置类"""
    min_number: int
    max_number: int
    max_attempts: int
    difficulty_level: DifficultyLevel
    hint_enabled: bool = False
    hint_type: str = "range"
    
    @classmethod
    def easy(cls):
        """简单难度"""
        return cls(
            min_number=1,
            max_number=50,
            max_attempts=10,
            difficulty_level=DifficultyLevel.EASY,
            hint_enabled=True,
            hint_type="range"
        )
    
    @classmethod
    def medium(cls):
        """中等难度"""
        return cls(
            min_number=1,
            max_number=100,
            max_attempts=7,
            difficulty_level=DifficultyLevel.MEDIUM,
            hint_enabled=True,
            hint_type="range"
        )
    
    @classmethod
    def hard(cls):
        """困难难度"""
        return cls(
            min_number=1,
            max_number=200,
            max_attempts=5,
            difficulty_level=DifficultyLevel.HARD,
            hint_enabled=False,
            hint_type="none"
        )
    
    @classmethod
    def custom(cls, min_num: int, max_num: int, attempts: int):
        """自定义难度"""
        return cls(
            min_number=min_num,
            max_number=max_num,
            max_attempts=attempts,
            difficulty_level=DifficultyLevel.CUSTOM,
            hint_enabled=True,
            hint_type="range"
        )
