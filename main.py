import sys
import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from controllers.main_controller import MainController
from views.main_view import MainView
from i18n import _

def main():
    root = tk.Tk()
    root.title(_("音频文件管理器"))
    
    # 设置应用程序图标
    icon_path = os.path.join(project_root, 'icons', 'app_icon.png')
    if os.path.exists(icon_path):
        try:
            icon_image = Image.open(icon_path)
            icon_photo = ImageTk.PhotoImage(icon_image)
            root.iconphoto(True, icon_photo)
        except Exception as e:
            print(f"无法加载应用程序图标: {e}")
    else:
        print(f"应用程序图标文件不存在: {icon_path}")
    
    # 创建全局样式
    style = ttk.Style()
    style.theme_use('clam')  # 使用 'clam' 主题作为基础
    
    # 自定义颜色和字体
    style.configure("TButton", padding=6, relief="flat", background="#4CAF50", foreground="white")
    style.map("TButton", background=[('active', '#45a049')])
    
    style.configure("TLabel", padding=6, font=('Helvetica', 10))
    style.configure("TEntry", padding=6)
    style.configure("Treeview", rowheight=25)
    style.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))
    
    style.configure("TNotebook", background="#f0f0f0")
    style.configure("TNotebook.Tab", padding=[10, 5], font=('Helvetica', 10))
    
    controller = MainController(root)
    view = MainView(root, controller, style)
    root.mainloop()

if __name__ == "__main__":
    main()