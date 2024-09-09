from i18n import _  # 添加这行
import tkinter as tk
from tkinter import ttk, messagebox

class BatchRenameView:
    def __init__(self, parent, controller, style):
        self.controller = controller
        self.style = style
        self.frame = ttk.Frame(parent)
        self.old_text = tk.StringVar()
        self.new_text = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        self.old_text_label = ttk.Label(self.frame, text=_("要替换的文本:"))
        self.old_text_label.pack(pady=5)
        ttk.Entry(self.frame, textvariable=self.old_text).pack(pady=5)

        self.new_text_label = ttk.Label(self.frame, text=_("新文本:"))
        self.new_text_label.pack(pady=5)
        ttk.Entry(self.frame, textvariable=self.new_text).pack(pady=5)

        self.old_text.trace_add("write", self.update_preview)
        self.new_text.trace_add("write", self.update_preview)
        
        tree_frame = ttk.Frame(self.frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.rename_preview = ttk.Treeview(tree_frame, columns=("old", "new"), show="headings")
        self.rename_preview.heading("old", text=_("原文件名"))
        self.rename_preview.heading("new", text=_("新文件名"))
        
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.rename_preview.yview)
        self.rename_preview.configure(yscrollcommand=vsb.set)
        
        self.rename_preview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.rename_button = ttk.Button(self.frame, text=_("确认重命名"), command=self.confirm_rename)
        self.rename_button.pack(pady=5)

    def update_preview(self, *args):
        old_text = self.old_text.get()
        new_text = self.new_text.get()
        preview_data = self.controller.get_rename_preview(old_text, new_text)
        self.rename_preview.delete(*self.rename_preview.get_children())
        for old_name, new_name in preview_data:
            self.rename_preview.insert("", "end", values=(old_name, new_name))

    def confirm_rename(self):
        if messagebox.askyesno(_("确认"), _("确定要重命名这些文件吗？")):
            self.controller.batch_rename(self.old_text.get(), self.new_text.get())
            self.update_preview()
            messagebox.showinfo(_("完成"), _("文件重命名完成"))

    def update_language(self):
        self.old_text_label.config(text=_("要替换的文本:"))
        self.new_text_label.config(text=_("新文本:"))
        self.rename_preview.heading("old", text=_("原文件名"))
        self.rename_preview.heading("new", text=_("新文件名"))
        self.rename_button.config(text=_("确认重命名"))
        self.update_preview()  # 刷新预览以使用新的翻译

    def update_theme(self, theme):
        self.style.theme_use(theme)
        # 更新其他特定于此视图的主题设置