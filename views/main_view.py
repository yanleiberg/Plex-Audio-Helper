import sys
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
from utils.utils import save_settings, load_settings

class MainView(MainViewEvents, MainViewActions):
    def __init__(self, root, controller, style):
        self.root = root
        self.controller = controller
        self.style = style
        self.directory = tk.StringVar()
        self.output_directory = tk.StringVar()
        self.strings = MainViewStrings()
        self.settings = load_settings()
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
        self.update_tag_view = UpdateTagView(self.notebook, self.controller, self.style, self.settings)
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

    def load_window_settings(self):
        if 'window' in self.settings:
            window_settings = self.settings['window']
            if window_settings.get('maximized', False):
                self.root.state('zoomed')
            else:
                width = window_settings.get('width', 800)
                height = window_settings.get('height', 600)
                x = window_settings.get('x', 0)
                y = window_settings.get('y', 0)

                # Ensure the window is visible on the screen
                screen_width = self.root.winfo_screenwidth()
                screen_height = self.root.winfo_screenheight()

                x = max(0, min(x, screen_width - width))
                y = max(0, min(y, screen_height - height))

                self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.update_idletasks()

    def save_window_settings(self):
        is_maximized = self.root.state() == 'zoomed'
        self.settings['window'] = {
            'width': self.root.winfo_width(),
            'height': self.root.winfo_height(),
            'x': self.root.winfo_x(),
            'y': self.root.winfo_y(),
            'maximized': is_maximized
        }

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
            self.update_tag_view.update_preview()
        elif current_tab == 1:
            self.organize_files_view.update_preview()
        elif current_tab == 2:
            self.batch_rename_view.update_preview()
        elif current_tab == 3:
            self.duplicate_search_view.search_duplicates()

    def refresh_all_views(self):
        self.update_tag_view.update_preview()
        self.organize_files_view.update_preview()
        self.batch_rename_view.update_preview()
        self.duplicate_search_view.search_duplicates()

    def save_all_settings(self):
        self.save_window_settings()
        self.save_all_column_widths()
        # Add similar calls for other views if they have settings to save
        # self.organize_files_view.save_settings(self.settings)
        # self.batch_rename_view.save_settings(self.settings)
        # self.duplicate_search_view.save_settings(self.settings)

    def save_all_column_widths(self):
        self.update_tag_view.save_column_widths(self.settings)
        # Add similar calls for other views if they have column widths to save
        # self.organize_files_view.save_column_widths(self.settings)
        # self.batch_rename_view.save_column_widths(self.settings)
        # self.duplicate_search_view.save_column_widths(self.settings)

    def on_closing(self):
        self.save_all_settings()
        save_settings(self.settings)
        print("Closing application...")
        self.root.destroy()

    # Add any other methods that don't fit well in other files here
