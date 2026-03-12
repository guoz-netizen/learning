import tkinter as tk
from tkinter import messagebox

def main():
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    messagebox.showinfo("Hello", "Hello, world!")
    root.destroy()

if __name__ == "__main__":
    main()
