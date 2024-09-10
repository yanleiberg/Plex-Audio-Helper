import tkinter as tk
from tkinter import ttk
from views.main_view_layout import create_main_layout
from views.main_view_events import MainViewEvents
from views.main_view_actions import MainViewActions
from views.main_view_strings import MainViewStrings
from views.update_tag_view import UpdateTagView
from views.organize_files_view import OrganizeFilesView
from views.batch_rename_view import BatchRenameView
from views.duplicate_search_view import DuplicateSearchView

class MainView(MainViewEvents, MainViewActions):
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
        self.setup_events()

    def load_icons(self):
        # Implement icon loading logic here
        pass

    def create_widgets(self):
        create_main_layout(self)
        self.create_views()

    def create_views(self):
        self.update_tag_view = UpdateTagView(self.notebook, self.controller, self.style)
        self.organize_files_view = OrganizeFilesView(self.notebook, self.controller, self.style)
        self.batch_rename_view = BatchRenameView(self.notebook, self.controller, self.style)
        self.duplicate_search_view = DuplicateSearchView(self.notebook, self.controller, self.style)

        self.notebook.add(self.update_tag_view.frame, text=self.strings.UPDATE_TRACK_TAG)
        self.notebook.add(self.organize_files_view.frame, text=self.strings.ORGANIZE_AUDIO_FILES)
        self.notebook.add(self.batch_rename_view.frame, text=self.strings.BATCH_RENAME)
        self.notebook.add(self.duplicate_search_view.frame, text=self.strings.DUPLICATE_SEARCH)

    def setup_events(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.bind("<Configure>", self.on_window_resize)
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)

    def update_ui_language(self):
        self.root.title(self.strings.TITLE)
        self.notebook.tab(0, text=self.strings.UPDATE_TRACK_TAG)
        self.notebook.tab(1, text=self.strings.ORGANIZE_AUDIO_FILES)
        self.notebook.tab(2, text=self.strings.BATCH_RENAME)
        self.notebook.tab(3, text=self.strings.DUPLICATE_SEARCH)
        
        # Update language for each view
        self.update_tag_view.update_language()
        self.organize_files_view.update_language()
        self.batch_rename_view.update_language()
        self.duplicate_search_view.update_language()

    def update_current_view(self):
        current_tab = self.notebook.index(self.notebook.select())
        if current_tab == 0:
            self.update_tag_view.update_preview()  # 使用 update_preview 而不是 update_view
        elif current_tab == 1:
            self.organize_files_view.update_preview()  # 假设这个方法存在
        elif current_tab == 2:
            self.batch_rename_view.update_preview()  # 假设这个方法存在
        elif current_tab == 3:
            self.duplicate_search_view.search_duplicates()  # 假设这个方法存在

    def refresh_all_views(self):
        self.update_tag_view.update_preview()
        self.organize_files_view.update_preview()
        self.batch_rename_view.update_preview()
        self.duplicate_search_view.search_duplicates()

    # Add any other methods that don't fit well in other files here
