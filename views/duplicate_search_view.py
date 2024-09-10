from i18n import _  # 添加这行
import tkinter as tk
from tkinter import ttk, messagebox
import os
import shutil

class DuplicateSearchView:
    def __init__(self, parent, controller, style):
        self.controller = controller
        self.style = style
        self.frame = ttk.Frame(parent)
        self.create_widgets()

    def create_widgets(self):
        button_frame = ttk.Frame(self.frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        self.auto_select_button = ttk.Button(button_frame, text=_("自动选择"), command=self.auto_select_duplicates)
        self.auto_select_button.pack(side=tk.LEFT, padx=5)
        
        self.delete_button = ttk.Button(button_frame, text=_("删除选中项"), command=self.delete_selected)
        self.delete_button.pack(side=tk.LEFT, padx=5)
        
        self.move_button = ttk.Button(button_frame, text=_("移动待删除文件"), command=self.move_files_to_delete)
        self.move_button.pack(side=tk.LEFT, padx=5)

        # 添加显示待删除目录的标签
        self.to_delete_dir_label = ttk.Label(self.frame, text="", wraplength=600)
        self.to_delete_dir_label.pack(pady=5)

        tree_frame = ttk.Frame(self.frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        self.columns = ("delete", "file", "ext", "dir", "title", "artist", "length", "size")
        self.duplicate_tree = ttk.Treeview(tree_frame, columns=self.columns, show="headings", style="Treeview")
        
        column_names = {
            "delete": _("删除"), "file": _("文件名"), "ext": _("扩展名"), "dir": _("目录"),
            "title": _("标题"), "artist": _("艺术家"), "length": _("时长"), "size": _("大小")
        }
        
        for col in self.columns:
            self.duplicate_tree.heading(col, text=column_names[col], command=lambda _col=col: self.treeview_sort_column(self.duplicate_tree, _col, False))
            if col == "delete":
                self.duplicate_tree.column(col, width=50, anchor="center")
            elif col in ["file", "dir", "title", "artist"]:
                self.duplicate_tree.column(col, width=150)
            else:
                self.duplicate_tree.column(col, width=100)
        
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.duplicate_tree.yview)
        self.duplicate_tree.configure(yscrollcommand=vsb.set)
        self.duplicate_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)

        self.duplicate_tree.tag_configure('delete', background='light pink')  # 添加这行

    def on_tab_selected(self):
        self.search_duplicates()
        self.update_to_delete_dir_label()

    def update_to_delete_dir_label(self):
        directory = self.controller.get_directory()
        if directory:
            to_delete_dir = os.path.join(directory, "To_Delete")
            self.to_delete_dir_label.config(text=_("待删除文件将被移动到: {}").format(to_delete_dir))
        else:
            self.to_delete_dir_label.config(text=_("请先选择一个目录"))

    def update_preview(self):
        # 清空树形视图
        self.duplicate_tree.delete(*self.duplicate_tree.get_children())

    def search_duplicates(self):
        duplicates = self.controller.find_duplicates()
        
        # 按照标题（升序）、艺术家（升序）和文件大小（降序）排序
        sorted_duplicates = sorted(duplicates, key=lambda x: (x[4].lower(), x[5].lower(), -float(x[9])))
        
        self.duplicate_tree.delete(*self.duplicate_tree.get_children())
        for file_info in sorted_duplicates:
            item = self.duplicate_tree.insert("", "end", values=file_info)
            if file_info[0] == _("✓"):  # 如果文件被标记为删除
                self.duplicate_tree.item(item, tags=('delete',))
        print(f"Debug: Found {len(duplicates)} potential duplicate files")

    def auto_select_duplicates(self):
        selected_count = self.controller.auto_select_duplicates(self.duplicate_tree)
        print(f"Debug: View received {selected_count} selected files")
        
        # 重新排序并更新树形视图
        items = [(self.duplicate_tree.item(item), item) for item in self.duplicate_tree.get_children()]
        sorted_items = sorted(items, key=lambda x: (x[0]['values'][4].lower(), x[0]['values'][5].lower(), -float(x[0]['values'][9])))
        
        for index, (item_values, item) in enumerate(sorted_items):
            self.duplicate_tree.move(item, '', index)
            if item_values['values'][0] == _("✓"):
                self.duplicate_tree.item(item, values=(item_values['values'][0], *item_values['values'][1:]), tags=('delete',))
            else:
                self.duplicate_tree.item(item, tags=())
        
        messagebox.showinfo(_("自动选择完成"), _("已选择 {} 个文件为待删除状态").format(selected_count))

    def delete_selected(self):
        selected_items = [item for item in self.duplicate_tree.get_children() if self.duplicate_tree.item(item)['values'][0] == "✓"]
        print(f"Debug: Selected items for deletion: {len(selected_items)}")
        if selected_items:
            if messagebox.askyesno(_("确认"), _("确定要删除选中的文件吗？")):
                deleted_count = self.controller.delete_selected_duplicates(selected_items, self.duplicate_tree)
                messagebox.showinfo(_("完成"), _("已删除 {} 个文件").format(deleted_count))
                self.search_duplicates()  # 刷新列表
        else:
            messagebox.showinfo(_("提示"), _("没有选中要删除的文件"))

    def move_files_to_delete(self):
        selected_items = [item for item in self.duplicate_tree.get_children() if self.duplicate_tree.item(item)['values'][0] == "✓"]
        print(f"Debug: Selected items for moving: {len(selected_items)}")
        if selected_items:
            directory = self.controller.get_output_directory()  # 使用输出目录
            if directory:
                # 移除可能的前缀
                directory = directory.replace("选择的目录: ", "").strip()
                to_delete_dir = os.path.join(directory, "To_Delete")
                os.makedirs(to_delete_dir, exist_ok=True)
                moved_count = 0
                for item in selected_items:
                    values = self.duplicate_tree.item(item)['values']
                    file_path = os.path.join(values[3], values[1])
                    new_path = os.path.join(to_delete_dir, values[1])
                    try:
                        shutil.move(file_path, new_path)
                        moved_count += 1
                        self.duplicate_tree.delete(item)
                    except Exception as e:
                        print(_("移动文件 {} 时出错: {}").format(file_path, e))
                messagebox.showinfo(_("完成"), _("已移动 {} 个文件到 To_Delete 目录").format(moved_count))
                self.search_duplicates()  # 刷新列表
            else:
                messagebox.showerror(_("错误"), _("未设置输出目录"))
        else:
            messagebox.showinfo(_("提示"), _("没有选中要移动的文件"))

    def treeview_sort_column(self, tv, col, reverse):
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        try:
            l.sort(key=lambda t: float(t[0]), reverse=reverse)
        except ValueError:
            l.sort(reverse=reverse)

        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)

        tv.heading(col, command=lambda: self.treeview_sort_column(tv, col, not reverse))

    def update_language(self):
        self.auto_select_button.config(text=_("自动选择"))
        self.delete_button.config(text=_("删除选中项"))
        self.move_button.config(text=_("移动待删除文件"))

        column_names = {
            "delete": _("删除"), "file": _("文件名"), "ext": _("扩展名"), "dir": _("目录"),
            "title": _("标题"), "artist": _("艺术家"), "length": _("时长"), "size": _("大小")
        }
        
        for col in self.columns:
            self.duplicate_tree.heading(col, text=column_names[col])

        self.search_duplicates()  # 刷新重复文件列表以使用新的翻译

        # 更新待删除目录标签
        to_delete_dir = os.path.join(self.controller.get_directory(), "To_Delete")
        self.to_delete_dir_label.config(text=_("待删除文件将被移动到: {}").format(to_delete_dir))

        self.update_to_delete_dir_label()

    def update_theme(self, theme):
        self.style.theme_use(theme)
        # 更新主题相关的样式
        if theme == "light":
            self.duplicate_tree.tag_configure('delete', background='light pink')
        else:
            self.duplicate_tree.tag_configure('delete', background='#8B0000')  # 深红色

        # 更新标签样式
        fg_color = self.style.lookup("TLabel", "foreground")
        self.to_delete_dir_label.configure(foreground=fg_color)