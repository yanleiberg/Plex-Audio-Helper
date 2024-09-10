import tkinter as tk
from tkinter import ttk
from views.ui_components import create_directory_chooser, create_file_stats_frame

def create_main_layout(view):
    create_menu(view)
    create_main_frame(view)

def create_menu(view):
    view.menubar = tk.Menu(view.root)
    view.root.config(menu=view.menubar)

    view.language_menu = tk.Menu(view.menubar, tearoff=0)
    view.menubar.add_cascade(label=view.strings.LANGUAGE, menu=view.language_menu)
    view.language_menu.add_command(label=view.strings.CHINESE, command=lambda: view.change_language('zh_CN'))
    view.language_menu.add_command(label=view.strings.ENGLISH, command=lambda: view.change_language('en_US'))

    view.theme_menu = tk.Menu(view.menubar, tearoff=0)
    view.menubar.add_cascade(label=view.strings.THEME, menu=view.theme_menu)
    view.theme_menu.add_command(label=view.strings.LIGHT_THEME, command=lambda: view.change_theme("light"))
    view.theme_menu.add_command(label=view.strings.DARK_THEME, command=lambda: view.change_theme("dark"))

def create_main_frame(view):
    view.main_frame = ttk.Frame(view.root, padding="10")
    view.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    view.root.columnconfigure(0, weight=1)
    view.root.rowconfigure(0, weight=1)

    directory_frame, view.directory_button, view.output_directory_button = create_directory_chooser(
        view.main_frame, view.strings, view.directory, view.output_directory, 
        view.choose_directory, view.choose_output_directory
    )
    directory_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))

    stats_frame, view.stats_tree = create_file_stats_frame(view.main_frame, view.strings)
    stats_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    create_notebook(view)

    view.main_frame.columnconfigure(0, weight=1)
    view.main_frame.rowconfigure(2, weight=1)

def create_notebook(view):
    # Implement notebook creation code here
    view.notebook = ttk.Notebook(view.main_frame)
    view.notebook.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    # Add tabs and their content here