from i18n import _  # 添加这行
import tkinter as tk
from tkinter import ttk, messagebox
import os

class OrganizeFilesView:
    def __init__(self, parent, controller, style):
        self.controller = controller
        self.style = style
        self.frame = ttk.Frame(parent)
        self.include_album = tk.BooleanVar(value=True)
        self.include_lrc = tk.BooleanVar(value=True)  # 新增变量控制是否包含 .lrc 文件
        self.create_widgets()

    def create_widgets(self):
        include_album_checkbox = ttk.Checkbutton(self.frame, text=_("包含专辑文件夹"), variable=self.include_album, command=self.update_preview)
        include_album_checkbox.pack(pady=5)
        self.create_tooltip(include_album_checkbox, _("选中此项将在整理时创建专辑文件夹"))
        
        include_lrc_checkbox = ttk.Checkbutton(self.frame, text=_("包含同名歌词文件"), variable=self.include_lrc)  # 新增复选框
        include_lrc_checkbox.pack(pady=5)
        self.create_tooltip(include_lrc_checkbox, _("选中此项将同时移动同名的 .lrc 歌词文件"))
        
        tree_frame = ttk.Frame(self.frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.organize_preview = ttk.Treeview(tree_frame, columns=("file", "artist", "album", "new_path"), show="headings")
        self.organize_preview.heading("file", text=_("文件名"))
        self.organize_preview.heading("artist", text=_("艺术家"))
        self.organize_preview.heading("album", text=_("专辑"))
        self.organize_preview.heading("new_path", text=_("新路径"))
        
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.organize_preview.yview)
        self.organize_preview.configure(yscrollcommand=vsb.set)
        
        self.organize_preview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        
        organize_button = ttk.Button(self.frame, text=_("开始整理"), command=self.start_organize_files)
        organize_button.pack(pady=5)
        self.create_tooltip(organize_button, _("点击此按钮开始整理音频文件"))

    def update_preview(self):
        preview_data = self.controller.get_organize_preview(self.include_album.get())
        self.organize_preview.delete(*self.organize_preview.get_children())
        for old_path, new_path, artist, album in preview_data:
            file_name = os.path.basename(old_path)
            self.organize_preview.insert("", "end", values=(file_name, artist, album, new_path))

    def start_organize_files(self):
        if messagebox.askyesno(_("确认"), _("确定要整理文件吗？")):
            self.controller.organize_files(self.include_album.get(), self.include_lrc.get())  # 传递 include_lrc 参数
            self.update_preview()
            messagebox.showinfo(_("完成"), _("文件整理完成"))

    def update_language(self):
        # 更新复选框文本
        self.frame.children['!checkbutton'].config(text=_("包含专辑文件夹"))
        self.frame.children['!checkbutton2'].config(text=_("包含同名歌词文件"))  # 更新新复选框的文本
        
        # 更新表格头部
        self.organize_preview.heading("file", text=_("文件名"))
        self.organize_preview.heading("artist", text=_("艺术家"))
        self.organize_preview.heading("album", text=_("专辑"))
        self.organize_preview.heading("new_path", text=_("新路径"))
        
        # 更新按钮文本
        self.frame.children['!button'].config(text=_("开始整理"))
        
        self.update_preview()  # 刷新预览以使用新的翻译

    def update_theme(self, theme):
        self.style.theme_use(theme)
        # 更新其他特定于此视图的主题设置

    def create_tooltip(self, widget, text):
        ToolTip(widget, text)

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25

        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")

        label = ttk.Label(self.tooltip, text=self.text, background="#ffffe0", relief="solid", borderwidth=1)
        label.pack()

    def hide_tooltip(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None