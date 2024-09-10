import tkinter as tk
from tkinter import ttk

def create_directory_chooser(parent, strings, directory, output_directory, choose_directory, choose_output_directory):
    frame = ttk.Frame(parent, padding="5")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E))

    ttk.Label(frame, text=strings.INPUT_DIRECTORY).grid(row=0, column=0, padx=5, pady=5)
    ttk.Entry(frame, textvariable=directory, width=50).grid(row=0, column=1, padx=5, pady=5)
    directory_button = ttk.Button(frame, text=strings.SELECT_DIRECTORY, command=choose_directory, width=15)
    directory_button.grid(row=0, column=2, padx=5, pady=5)

    ttk.Label(frame, text=strings.OUTPUT_DIRECTORY).grid(row=1, column=0, padx=5, pady=5)
    ttk.Entry(frame, textvariable=output_directory, width=50).grid(row=1, column=1, padx=5, pady=5)
    output_directory_button = ttk.Button(frame, text=strings.SELECT_OUTPUT_DIRECTORY, command=choose_output_directory, width=15)
    output_directory_button.grid(row=1, column=2, padx=5, pady=5)

    return frame, directory_button, output_directory_button

def create_file_stats_frame(parent, strings):
    frame = ttk.Frame(parent, padding="5")
    frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    columns = (strings.FILE_TYPE, strings.FILE_COUNT, strings.TOTAL_SIZE, strings.PROPORTION)
    stats_tree = ttk.Treeview(frame, columns=columns, show="headings", height=5)
    
    for col in columns:
        stats_tree.heading(col, text=col)
        stats_tree.column(col, width=100, anchor="center")

    stats_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=stats_tree.yview)
    scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
    stats_tree.configure(yscrollcommand=scrollbar.set)

    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(0, weight=1)

    return frame, stats_tree

def create_progress_window(parent, strings):
    progress_window = tk.Toplevel(parent)
    progress_window.title(strings.READING_FILES)
    progress_window.geometry("400x150")
    progress_window.resizable(False, False)
    
    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(progress_window, variable=progress_var, maximum=100, length=350)
    progress_bar.pack(pady=30)
    
    progress_label = ttk.Label(progress_window, text="0%")
    progress_label.pack()

    return progress_window, progress_var, progress_label