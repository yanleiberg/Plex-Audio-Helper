from models.audio_manager import AudioManager
from i18n import _  # 添加这行

class MainController:
    def __init__(self, root):
        self.root = root
        self.audio_manager = AudioManager()

    def set_directory(self, input_directory, output_directory=None):
        self.audio_manager.set_directory(input_directory, output_directory)

    def cache_file_info(self, progress_callback):
        self.audio_manager.cache_file_info(progress_callback)

    def get_file_stats(self):
        return self.audio_manager.get_file_stats()

    def get_tag_preview(self):
        return self.audio_manager.get_tag_preview()

    def get_organize_preview(self, include_album):
        return self.audio_manager.get_organize_preview(include_album)

    def get_rename_preview(self, old_text, new_text):
        return self.audio_manager.get_rename_preview(old_text, new_text)

    def find_duplicates(self):
        return self.audio_manager.find_duplicates()

    def auto_select_duplicates(self, tree):
        selected_count = self.audio_manager.auto_select_duplicates(tree)
        print(f"Debug: Controller received {selected_count} selected files")  # 添加调试输出
        return selected_count

    def delete_selected_duplicates(self, selected_items, tree):
        return self.audio_manager.delete_selected_duplicates(selected_items, tree)

    def update_tags(self):
        self.audio_manager.update_tags()

    def organize_files(self, include_album, include_lrc):
        self.audio_manager.organize_files(include_album, include_lrc)

    def batch_rename(self, old_text, new_text):
        self.audio_manager.batch_rename(old_text, new_text)

    def get_directory(self):
        return self.audio_manager.input_directory or ""  # 如果没有选择目录，返回空字符串

    def get_input_directory(self):
        return self.audio_manager.input_directory

    def get_output_directory(self):
        output_dir = self.audio_manager.output_directory or self.audio_manager.input_directory
        return output_dir.replace("选择的目录: ", "").strip()