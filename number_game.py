import tkinter as tk
from tkinter import messagebox
import random

class GuessNumberGame:
    def __init__(self, root):
        self.root = root
        self.root.title("猜数字游戏")
        self.root.geometry("400x300")
        self.root.configure(bg="#f0f0f0")
        
        # 游戏变量
        self.secret_number = random.randint(1, 100)
        self.attempts = 0
        self.max_attempts = 7
        
        # 标题
        title_label = tk.Label(root, text="猜数字游戏", font=("Arial", 20, "bold"), bg="#f0f0f0")
        title_label.pack(pady=20)
        
        # 説明文本
        info_label = tk.Label(root, text="请猜一个1-100之间的数字\n你有7次机会", font=("Arial", 12), bg="#f0f0f0")
        info_label.pack(pady=10)
        
        # 输入框架
        input_frame = tk.Frame(root, bg="#f0f0f0")
        input_frame.pack(pady=10)
        
        tk.Label(input_frame, text="输入数字:", font=("Arial", 11), bg="#f0f0f0").pack(side=tk.LEFT, padx=5)
        self.entry = tk.Entry(input_frame, font=("Arial", 12), width=15)
        self.entry.pack(side=tk.LEFT, padx=5)
        self.entry.bind("<Return>", lambda e: self.guess_number())
        
        # 按钮框架
        button_frame = tk.Frame(root, bg="#f0f0f0")
        button_frame.pack(pady=15)
        
        guess_btn = tk.Button(button_frame, text="确定", command=self.guess_number, font=("Arial", 11), 
                              bg="#4CAF50", fg="white", padx=20, pady=10)
        guess_btn.pack(side=tk.LEFT, padx=5)
        
        reset_btn = tk.Button(button_frame, text="重新开始", command=self.reset_game, font=("Arial", 11),
                              bg="#2196F3", fg="white", padx=20, pady=10)
        reset_btn.pack(side=tk.LEFT, padx=5)
        
        # 结果标签
        self.result_label = tk.Label(root, text="", font=("Arial", 11), bg="#f0f0f0", fg="#FF5722")
        self.result_label.pack(pady=10)
        
        # 尝试次数标签
        self.attempts_label = tk.Label(root, text=f"剩余机会: {self.max_attempts}", font=("Arial", 10), bg="#f0f0f0")
        self.attempts_label.pack()
    
    def guess_number(self):
        try:
            guess = int(self.entry.get())
            
            if guess < 1 or guess > 100:
                messagebox.showwarning("输入错误", "请输入1-100之间的数字！")
                return
            
            self.attempts += 1
            remaining = self.max_attempts - self.attempts
            
            if guess == self.secret_number:
                messagebox.showinfo("成功!", f"恭喜！你用了{self.attempts}次猜测就猜对了！\n数字是{self.secret_number}")
                self.reset_game()
            elif guess < self.secret_number:
                self.result_label.config(text="提示：数字太小了！", fg="#FF9800")
                self.attempts_label.config(text=f"剩余机会: {remaining}")
            else:
                self.result_label.config(text="提示：数字太大了！", fg="#FF9800")
                self.attempts_label.config(text=f"剩余机会: {remaining}")
            
            if remaining <= 0:
                messagebox.showinfo("游戏结束", f"很遗憾，你没有猜对！\n正确答案是：{self.secret_number}")
                self.reset_game()
            
            self.entry.delete(0, tk.END)
            self.entry.focus()
        
        except ValueError:
            messagebox.showerror("输入错误", "请输入一个有效的整数！")
    
    def reset_game(self):
        self.secret_number = random.randint(1, 100)
        self.attempts = 0
        self.entry.delete(0, tk.END)
        self.result_label.config(text="")
        self.attempts_label.config(text=f"剩余机会: {self.max_attempts}")
        self.entry.focus()

if __name__ == "__main__":
    root = tk.Tk()
    game = GuessNumberGame(root)
    root.mainloop()