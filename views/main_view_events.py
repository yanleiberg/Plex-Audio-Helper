import tkinter as tk
from tkinter import filedialog
import threading
from views.ui_components import create_progress_window

class MainViewEvents:
    def on_closing(self):
        self.save_window_settings()
        self.root.destroy()

    def on_window_resize(self, event):
        self.update_current_view()

    def on_tab_change(self, event):
        self.update_current_view()

    def choose_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.directory.set(self.strings.SELECTED_DIRECTORY.format(directory))
            if not self.output_directory.get():
                self.output_directory.set(self.strings.SELECTED_DIRECTORY.format(directory))
            self.controller.set_directory(directory, self.output_directory.get())
            
            progress_window, progress_var, progress_label = create_progress_window(self.root, self.strings)
            
            def update_progress(processed_files, total_files):
                progress = (processed_files / total_files) * 100 if total_files > 0 else 0
                progress_var.set(progress)
                progress_label.config(text=f"{progress:.1f}% ({processed_files}/{total_files})")
                progress_window.update()
            
            def cache_files_thread():
                self.root.config(cursor="wait")
                self.controller.cache_file_info(update_progress)
                self.root.config(cursor="")
                progress_window.destroy()
                self.update_file_stats()
                self.update_current_view()
            
            threading.Thread(target=cache_files_thread, daemon=True).start()

    def choose_output_directory(self):
        output_directory = filedialog.askdirectory()
        if output_directory:
            self.output_directory.set(self.strings.SELECTED_DIRECTORY.format(output_directory))
            self.controller.set_directory(self.controller.get_input_directory(), output_directory)
            self.refresh_all_views()