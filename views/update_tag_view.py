from i18n import _  # 添加这行
import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkfont  # 添加这行
from utils.utils import save_settings, load_settings

class UpdateTagView:
    def __init__(self, parent, controller, style, settings):
        self.controller = controller
        self.style = style
        self.frame = ttk.Frame(parent)
        self.settings = settings
        self.create_widgets()
        self.load_column_widths()

    def create_widgets(self):
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)

        title_label = ttk.Label(self.frame, text=_("更新 Track Tag"))
        title_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        ToolTip(title_label, _("在此视图中，您可以预览和更新音频文件的 Track Tag"))

        self.tree_frame = ttk.Frame(self.frame)
        self.tree_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.tree_frame.columnconfigure(0, weight=1)
        self.tree_frame.rowconfigure(0, weight=1)
        
        self.tag_preview = ttk.Treeview(self.tree_frame, columns=("file", "current_tag", "new_tag"), show="headings")
        self.tag_preview.heading("file", text=_("文件名"))
        self.tag_preview.heading("current_tag", text=_("当前 Track Tag"))
        self.tag_preview.heading("new_tag", text=_("新 Track Tag"))
        
        self.tag_preview.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        ToolTip(self.tag_preview, _("此表格显示文件名、当前的 Track Tag 和将要更新的新 Track Tag"))
        
        self.vsb = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tag_preview.yview)
        self.vsb.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.tag_preview.configure(yscrollcommand=self.vsb.set)
        
        self.update_button = ttk.Button(self.frame, text=_("开始更新 Track Tag"), command=self.start_update_tag)
        self.update_button.grid(row=2, column=0, pady=(10, 0))
        ToolTip(self.update_button, _("点击此按钮开始更新所有音频文件的 Track Tag"))

    def create_tooltip(self, widget, text):
        tooltip = ToolTip(widget, text)

    def update_preview(self):
        preview_data = self.controller.get_tag_preview()
        self.tag_preview.delete(*self.tag_preview.get_children())
        
        # 批量插入数据，只包含所需的三列
        for i in range(0, len(preview_data), 1000):
            batch = preview_data[i:i+1000]
            for file_name, current_tag, new_tag in batch:
                self.tag_preview.insert("", "end", values=(file_name, current_tag, new_tag))
        
        # 只有在没有保存的列宽时才调整列宽
        if 'update_tag_column_widths' not in self.settings:
            self.load_column_widths()

    def load_column_widths(self):
        column_widths = self.settings.get('update_tag_column_widths', {})
        if column_widths:
            for col in ("file", "current_tag", "new_tag"):
                width = column_widths.get(col)
                if width:
                    self.tag_preview.column(col, width=width)
        else:
            # 如果没有保存的列宽，平分 treeview 的总宽度
            total_width = self.tag_preview.winfo_width()
            if total_width > 0:  # 确保 treeview 已经被渲染
                column_width = total_width // 3
                for col in ("file", "current_tag", "new_tag"):
                    self.tag_preview.column(col, width=column_width)
            else:
                # 如果 treeview 还没有被渲染，设置一个默认宽度
                default_width = 200
                for col in ("file", "current_tag", "new_tag"):
                    self.tag_preview.column(col, width=default_width)

    def save_column_widths(self, settings):
        column_widths = {}
        for col in ("file", "current_tag", "new_tag"):
            column_widths[col] = self.tag_preview.column(col, 'width')
        settings['update_tag_column_widths'] = column_widths

    def start_update_tag(self):
        if messagebox.askyesno(_("确认"), _("确定要更新所有音频文件的 Track Number 吗？")):
            self.controller.update_tags()
            self.update_preview()
            messagebox.showinfo(_("完成"), _("Track Number 更新完成"))

    def update_language(self):
        self.tag_preview.heading("file", text=_("文件名"))
        self.tag_preview.heading("current_tag", text=_("当前 Track Tag"))
        self.tag_preview.heading("new_tag", text=_("新 Track Tag"))
        self.update_button.config(text=_("开始更新 Track Tag"))
        self.update_preview()  # 刷新预览以使用新的翻译

    def update_theme(self, theme):
        self.style.theme_use(theme)
        # 更新其他特定于此视图的主题设置

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        x = self.widget.winfo_rootx() + self.widget.winfo_width() // 2
        y = self.widget.winfo_rooty() + self.widget.winfo_height()

        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")

        label = ttk.Label(self.tooltip, text=self.text, background="#ffffe0", relief="solid", borderwidth=1)
        label.pack()

    def hide_tooltip(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None