import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import threading
import os
from PIL import Image, ImageTk
from views.update_tag_view import UpdateTagView
from views.organize_files_view import OrganizeFilesView
from views.batch_rename_view import BatchRenameView
from views.duplicate_search_view import DuplicateSearchView
from i18n import _, translate_class, i18n

@translate_class
class MainViewStrings:
    SELECT_DIRECTORY = _("选择目录")
    FILE_TYPE = _("文件类型")
    FILE_COUNT = _("文件数量")
    TOTAL_SIZE = _("总大小")
    PROPORTION = _("比例")
    UPDATE_TRACK_TAG = _("更新 Track Tag")
    ORGANIZE_AUDIO_FILES = _("整理音频文件")
    BATCH_RENAME = _("批量重命名")
    DUPLICATE_SEARCH = _("重复文件搜索")
    LANGUAGE = _("语言")
    CHINESE = _("中文")
    ENGLISH = _("英文")
    LIGHT_THEME = _("亮色主题")
    DARK_THEME = _("暗色主题")

class MainView:
    def __init__(self, root, controller, style):
        self.root = root
        self.controller = controller
        self.style = style
        self.directory = tk.StringVar()
        self.output_directory = tk.StringVar()
        self.strings = MainViewStrings()
        self.load_icons()
        self.create_widgets()
        self.load_window_settings()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # 绑定窗口大小变化事件
        self.root.bind("<Configure>", self.on_window_resize)

    def load_icons(self):
        icon_size = (24, 24)
        icons_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'icons')
        self.icons = {
            'folder': ImageTk.PhotoImage(Image.open(os.path.join(icons_dir, 'folder.png')).resize(icon_size)),
            'update': ImageTk.PhotoImage(Image.open(os.path.join(icons_dir, 'update.png')).resize(icon_size)),
            'organize': ImageTk.PhotoImage(Image.open(os.path.join(icons_dir, 'organize.png')).resize(icon_size)),
            'rename': ImageTk.PhotoImage(Image.open(os.path.join(icons_dir, 'rename.png')).resize(icon_size)),
            'search': ImageTk.PhotoImage(Image.open(os.path.join(icons_dir, 'search.png')).resize(icon_size))
        }

    def create_widgets(self):
        self.create_menu()
        self.create_main_frame()

    def create_main_frame(self):
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.create_directory_chooser(self.main_frame)
        self.create_file_stats_frame(self.main_frame)
        self.create_notebook(self.main_frame)

        # 配置main_frame的行列权重
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(2, weight=1)  # notebook所在的行

    def create_directory_chooser(self, parent):
        frame = ttk.Frame(parent, padding="5")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E))

        ttk.Label(frame, text=self.strings.SELECT_DIRECTORY, image=self.icons['folder'], compound=tk.LEFT).grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(frame, textvariable=self.directory, width=50).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(frame, text="...", command=self.choose_directory, width=3).grid(row=0, column=2, padx=5, pady=5)

        ttk.Label(frame, text=_("输出目录:")).grid(row=1, column=0, padx=5, pady=5)
        ttk.Entry(frame, textvariable=self.output_directory, width=50).grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(frame, text=_("选择输出目录"), command=self.choose_output_directory, width=15).grid(row=1, column=2, padx=5, pady=5)

    def create_file_stats_frame(self, parent):
        frame = ttk.Frame(parent, padding="5")
        frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        columns = (self.strings.FILE_TYPE, self.strings.FILE_COUNT, self.strings.TOTAL_SIZE, self.strings.PROPORTION)
        self.stats_tree = ttk.Treeview(frame, columns=columns, show="headings", height=5)
        
        for col in columns:
            self.stats_tree.heading(col, text=col)
            self.stats_tree.column(col, width=100, anchor="center")

        self.stats_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.stats_tree.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.stats_tree.configure(yscrollcommand=scrollbar.set)

        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)

    def create_notebook(self, parent):
        self.notebook = ttk.Notebook(parent)
        self.notebook.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)

        self.update_tag_view = UpdateTagView(self.notebook, self.controller, self.style)
        self.organize_files_view = OrganizeFilesView(self.notebook, self.controller, self.style)
        self.batch_rename_view = BatchRenameView(self.notebook, self.controller, self.style)
        self.duplicate_search_view = DuplicateSearchView(self.notebook, self.controller, self.style)

        self.notebook.add(self.update_tag_view.frame, text=self.strings.UPDATE_TRACK_TAG, image=self.icons['update'], compound=tk.LEFT)
        self.notebook.add(self.organize_files_view.frame, text=self.strings.ORGANIZE_AUDIO_FILES, image=self.icons['organize'], compound=tk.LEFT)
        self.notebook.add(self.batch_rename_view.frame, text=self.strings.BATCH_RENAME, image=self.icons['rename'], compound=tk.LEFT)
        self.notebook.add(self.duplicate_search_view.frame, text=self.strings.DUPLICATE_SEARCH, image=self.icons['search'], compound=tk.LEFT)

        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        language_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=self.strings.LANGUAGE, menu=language_menu)
        language_menu.add_command(label=self.strings.CHINESE, command=lambda: self.change_language('zh_CN'))
        language_menu.add_command(label=self.strings.ENGLISH, command=lambda: self.change_language('en_US'))

        theme_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=_("主题"), menu=theme_menu)
        theme_menu.add_command(label=self.strings.LIGHT_THEME, command=lambda: self.change_theme("light"))
        theme_menu.add_command(label=self.strings.DARK_THEME, command=lambda: self.change_theme("dark"))

    def change_language(self, lang):
        i18n.set_language(lang)
        self.strings = translate_class(MainViewStrings())
        self.update_ui_language()

    def update_ui_language(self):
        # 更新菜单语言
        self.root.config(menu='')
        self.create_menu()

        # 更新目录选择器
        self.directory_button.config(text=self.strings.SELECT_DIRECTORY)

        # 更新文件统计框
        self.stats_tree.heading("type", text=self.strings.FILE_TYPE)
        self.stats_tree.heading("count", text=self.strings.FILE_COUNT)
        self.stats_tree.heading("size", text=self.strings.TOTAL_SIZE)
        self.stats_tree.heading("bar", text=self.strings.PROPORTION)

        # 更新标签页
        self.notebook.tab(0, text=self.strings.UPDATE_TRACK_TAG)
        self.notebook.tab(1, text=self.strings.ORGANIZE_AUDIO_FILES)
        self.notebook.tab(2, text=self.strings.BATCH_RENAME)
        self.notebook.tab(3, text=self.strings.DUPLICATE_SEARCH)

        # 更新各个视图的语言
        self.update_tag_view.update_language()
        self.organize_files_view.update_language()
        self.batch_rename_view.update_language()
        self.duplicate_search_view.update_language()

    def change_theme(self, theme_name):
        if theme_name == "light":
            self.style.theme_use('clam')
            self.style.configure(".", background="#f0f0f0", foreground="black")
            self.style.configure("TButton", background="#4CAF50", foreground="white")
            self.style.map("TButton", background=[('active', '#45a049')])
            self.style.configure("Treeview", background="white", fieldbackground="white", foreground="black")
        else:  # dark theme
            self.style.theme_use('clam')
            self.style.configure(".", background="#2c2c2c", foreground="white")
            self.style.configure("TButton", background="#2196F3", foreground="white")
            self.style.map("TButton", background=[('active', '#1976D2')])
            self.style.configure("Treeview", background="#3c3c3c", fieldbackground="#3c3c3c", foreground="white")
        
        self.style.configure("TNotebook", background=self.style.lookup(".", "background"))
        self.style.configure("TNotebook.Tab", background=self.style.lookup(".", "background"), foreground=self.style.lookup(".", "foreground"))
        self.style.map("TNotebook.Tab", background=[("selected", self.style.lookup("TButton", "background"))])
        
        self.update_all_views()

    def choose_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.directory.set(_("选择的目录: {}").format(directory))
            if not self.output_directory.get():
                self.output_directory.set(_("选择的目录: {}").format(directory))
            self.controller.set_directory(directory, self.output_directory.get())
            
            # 创建进度条窗口
            progress_window = tk.Toplevel(self.root)
            progress_window.title(_("读取文件中"))
            progress_window.geometry("300x100")
            
            # 设置进度窗口在主窗口中间
            progress_window.update_idletasks()
            x = self.root.winfo_x() + (self.root.winfo_width() - progress_window.winfo_width()) // 2
            y = self.root.winfo_y() + (self.root.winfo_height() - progress_window.winfo_height()) // 2
            progress_window.geometry(f"+{x}+{y}")
            
            # 设置进度窗口为模态窗口
            progress_window.grab_set()
            
            progress_var = tk.DoubleVar()
            progress_bar = ttk.Progressbar(progress_window, variable=progress_var, maximum=100)
            progress_bar.pack(pady=20)
            
            progress_label = ttk.Label(progress_window, text="0%")
            progress_label.pack()
            
            # 更新进度的回调函数
            def update_progress(value):
                progress_var.set(value)
                progress_label.config(text=f"{value:.1f}%")
                progress_window.update()
            
            # 在新线程中执行文件缓存
            def cache_files_thread():
                self.root.config(cursor="wait")
                self.controller.cache_file_info(update_progress)
                self.root.config(cursor="")
                progress_window.grab_release()
                progress_window.destroy()
                self.update_file_stats()
                self.update_current_view()
            
            threading.Thread(target=cache_files_thread, daemon=True).start()

    def choose_output_directory(self):
        output_directory = filedialog.askdirectory()
        if output_directory:
            self.output_directory.set(_("选择的目录: {}").format(output_directory))
            self.controller.set_directory(self.controller.get_input_directory(), output_directory)
            self.refresh_all_views()

    def update_file_stats(self):
        stats = self.controller.get_file_stats()
        self.stats_tree.delete(*self.stats_tree.get_children())
        for file_type, data in stats.items():
            self.stats_tree.insert("", "end", values=(file_type, data["count"], f"{data['size']:.2f} MB", data["bar"]))

    def update_current_view(self):
        current_tab = self.notebook.index(self.notebook.select())
        if current_tab == 0:
            self.update_tag_view.update_preview()
        elif current_tab == 1:
            self.organize_files_view.update_preview()
        elif current_tab == 2:
            self.batch_rename_view.update_preview()
        elif current_tab == 3:
            self.duplicate_search_view.search_duplicates()

    def update_all_views(self):
        self.update_tag_view.update_preview()
        self.organize_files_view.update_preview()
        self.batch_rename_view.update_preview()
        self.duplicate_search_view.update_preview()
        # 更新主视图的样式
        self.root.update()

    def load_window_settings(self):
        try:
            with open('window_settings.json', 'r') as f:
                settings = json.load(f)
                self.root.geometry(f"{settings['width']}x{settings['height']}+{settings['x']}+{settings['y']}")
        except FileNotFoundError:
            self.root.geometry("800x600")

    def save_window_settings(self):
        settings = {
            'width': self.root.winfo_width(),
            'height': self.root.winfo_height(),
            'x': self.root.winfo_x(),
            'y': self.root.winfo_y()
        }
        with open('window_settings.json', 'w') as f:
            json.dump(settings, f)

    def on_closing(self):
        self.save_window_settings()
        self.root.destroy()

    def on_tab_change(self, event):
        self.update_current_view()

    def on_window_resize(self, event):
        # 当窗口大小变化时，更新当前视图
        self.update_current_view()

    def refresh_all_views(self):
        self.update_tag_view.update_preview()
        self.organize_files_view.refresh_preview()
        self.batch_rename_view.update_preview()
        self.duplicate_search_view.search_duplicates()
