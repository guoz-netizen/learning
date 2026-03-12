import json
import os
from datetime import datetime
from typing import List, Dict
from dataclasses import dataclass, field

LEADERBOARD_FILE = 'assets/leaderboard.json'

@dataclass
class GameRecord:
    """游戏记录"""
    player_name: str
    attempts: int
    max_attempts: int
    difficulty: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> dict:
        return {
            'player_name': self.player_name,
            'attempts': self.attempts,
            'max_attempts': self.max_attempts,
            'difficulty': self.difficulty,
            'timestamp': self.timestamp
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

class LeaderboardManager:
    """排行榜管理器"""
    
    def __init__(self, file_path: str = LEADERBOARD_FILE):
        self.file_path = file_path
        self.records = self._load_records()
    
    def _load_records(self) -> List[GameRecord]:
        """从文件加载记录"""
        if not os.path.exists(self.file_path):
            return []
        
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [GameRecord.from_dict(record) for record in data]
        except Exception as e:
            print(f"加载排行榜失败: {e}")
            return []
    
    def _save_records(self):
        """保存记录到文件"""
        try:
            os.makedirs(os.path.dirname(self.file_path) or '.', exist_ok=True)
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump([r.to_dict() for r in self.records], f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存排行榜失败: {e}")
    
    def add_record(self, record: GameRecord):
        """添加游戏记录"""
        self.records.append(record)
        self._save_records()
    
    def get_records_by_difficulty(self, difficulty: str) -> List[GameRecord]:
        """按难度筛选记录"""
        return [r for r in self.records if r.difficulty == difficulty]
    
    def get_top_records(self, difficulty: str = None, limit: int = 10) -> List[GameRecord]:
        """获取最好成绩（按尝试次数排序）"""
        if difficulty:
            filtered = self.get_records_by_difficulty(difficulty)
        else:
            filtered = self.records
        
        # 按尝试次数排序
        sorted_records = sorted(filtered, key=lambda r: r.attempts)
        return sorted_records[:limit]
    
    def clear_records(self):
        """清空所有记录"""
        self.records = []
        self._save_records()
    
    def get_statistics(self, difficulty: str = None) -> Dict:
        """获取统计信息"""
        if difficulty:
            records = self.get_records_by_difficulty(difficulty)
        else:
            records = self.records
        
        if not records:
            return {
                'total_games': 0,
                'win_rate': 0,
                'best_attempt': 0,
                'avg_attempts': 0
            }
        
        return {
            'total_games': len(records),
            'best_attempt': min(r.attempts for r in records) if records else 0,
            'avg_attempts': sum(r.attempts for r in records) / len(records),
            'last_played': records[-1].timestamp if records else None
        }
