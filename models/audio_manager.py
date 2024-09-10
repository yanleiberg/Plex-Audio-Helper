import os
from collections import defaultdict
from utils.audio_file_operations import get_audio_tags, delete_file, rename_file, move_file
from utils.utils import format_time, time_to_seconds
from i18n import _  # 添加这行

class AudioManager:
    def __init__(self):
        self.input_directory = None
        self.output_directory = None
        self.supported_formats = ('.mp3', '.flac', '.ape', '.wav', '.m4a')
        self.audio_files = []
        self.audio_tags = {}

    def set_directory(self, input_directory, output_directory=None):
        self.input_directory = input_directory
        self.output_directory = output_directory if output_directory else input_directory

    def cache_file_info(self, progress_callback=None):
        self.audio_files = []
        self.audio_tags = {}
        total_files = sum([len(files) for _, _, files in os.walk(self.input_directory)])
        processed_files = 0
        for root, _, files in os.walk(self.input_directory):
            for file in files:
                if file.lower().endswith(self.supported_formats):
                    file_path = os.path.join(root, file)
                    self.audio_files.append(file_path)
                    self.audio_tags[file_path] = get_audio_tags(file_path)
                    processed_files += 1
                    if progress_callback:
                        progress_callback(processed_files / total_files * 100)

    def get_file_stats(self):
        stats = defaultdict(lambda: {"count": 0, "size": 0})
        total_size = 0

        for file_path in self.audio_files:
            file_ext = os.path.splitext(file_path)[1].lower()
            file_size = os.path.getsize(file_path)

            stats[file_ext]["count"] += 1
            stats[file_ext]["size"] += file_size
            total_size += file_size

        for file_type, data in stats.items():
            data["size"] /= (1024 * 1024)  # Convert to MB
            data["bar"] = "█" * int((data["size"] / total_size) * 100)

        return dict(sorted(stats.items(), key=lambda x: x[1]["size"], reverse=True))

    def get_tag_preview(self):
        preview_data = []
        sorted_files = sorted(self.audio_files)
        for i, file in enumerate(sorted_files, 1):
            tags = self.audio_tags[file]
            current_track = tags.get('tracknumber', ['0/0'])[0].split('/')[0]
            new_track = str(i)
            preview_data.append((os.path.basename(file), current_track, new_track))
        return preview_data

    def generate_new_track_number(self, index, total):
        return str(index)

    def get_organize_preview(self, include_album=True):
        preview = []
        for file_path, tags in self.audio_tags.items():
            artist = tags.get('artist', _('未知艺术家'))
            album = tags.get('album', _('未知专辑'))
            
            if include_album:
                new_path = os.path.normpath(os.path.join(self.output_directory, artist, album, os.path.basename(file_path)))
            else:
                new_path = os.path.normpath(os.path.join(self.output_directory, artist, os.path.basename(file_path)))
            
            preview.append((file_path, new_path, artist, album))
        return preview

    def get_rename_preview(self, old_text, new_text):
        preview_data = []
        for root, _, files in os.walk(self.input_directory):
            for file in files:
                if file.lower().endswith(self.supported_formats):
                    name, ext = os.path.splitext(file)
                    new_name = name.replace(old_text, new_text)
                    new_filename = new_name + ext
                    if file != new_filename:
                        preview_data.append((file, new_filename))
        return preview_data

    def find_duplicates(self):
        duplicates = defaultdict(list)
        for file_path in self.audio_files:
            tags = self.audio_tags[file_path]
            title = tags.get('title', '').lower()
            artist = tags.get('artist', '').lower()
            key = (title, artist)
            duplicates[key].append(file_path)

        duplicate_list = []
        for (title, artist), files in duplicates.items():
            if len(files) > 1:
                for file_path in files:
                    tags = self.audio_tags[file_path]
                    length = tags.get('length', 0)
                    size = os.path.getsize(file_path) / (1024 * 1024)  # 转换为MB
                    file_name = os.path.basename(file_path)
                    ext = os.path.splitext(file_name)[1]
                    dir_path = os.path.dirname(file_path)
                    duplicate_list.append(("", file_name, ext, dir_path, title, artist, format_time(length), f"{size:.2f} MB", length, size))
        return duplicate_list

    def auto_select_duplicates(self, tree):
        duplicates = defaultdict(list)
        for item in tree.get_children():
            values = tree.item(item)['values']
            if len(values) >= 6:  # 确保有足够的值
                key = (values[4].lower(), values[5].lower())  # title, artist
                duplicates[key].append(item)

        selected_count = 0
        for items in duplicates.values():
            if len(items) > 1:  # 只处理真正的重复项
                # 按文件类型和大小排序
                sorted_items = sorted(items, key=lambda x: (
                    tree.item(x)['values'][2] not in ['.flac', '.ape'],  # 文件类型
                    -float(tree.item(x)['values'][9])  # 文件大小（负值用于降序排序）
                ))
                
                # 保留第一个（最高质量）文件，标记其余为待删除
                for item in sorted_items[1:]:
                    tree.set(item, "delete", "✓")
                    selected_count += 1

        print(f"Debug: Found {len(duplicates)} duplicate groups")
        print(f"Debug: Selected {selected_count} files for deletion")
        return selected_count

    def delete_selected_duplicates(self, selected_items, tree):
        deleted_count = 0
        for item in selected_items:
            values = tree.item(item)['values']
            file_path = os.path.join(values[3], values[1])
            try:
                os.remove(file_path)
                tree.delete(item)
                deleted_count += 1
                # 从 audio_files 和 audio_tags 中移除已删除的文件
                if file_path in self.audio_files:
                    self.audio_files.remove(file_path)
                if file_path in self.audio_tags:
                    del self.audio_tags[file_path]
            except Exception as e:
                print(_("删除文件 {} 时出错: {}").format(file_path, e))
        return deleted_count

    def update_tags(self):
        sorted_files = sorted(self.audio_files)
        total = len(sorted_files)
        for i, file_path in enumerate(sorted_files, 1):
            new_track_number = self.generate_new_track_number(i, total)
            self.update_track_number(file_path, new_track_number)

    def update_track_number(self, file_path, new_track_number):
        # 这里实现更新文件 track number 的逻辑
        # 您需要根据文件类型（mp3, flac 等）使用适当的库来更新标签
        # 这里只是一个示例
        tags = self.audio_tags[file_path]
        tags['tracknumber'] = new_track_number
        # 在这里保存更新后的标签到文件
        # 例如，对于 MP3 文件：
        # audio = MP3(file_path, ID3=ID3)
        # audio.tags.add(TRCK(encoding=3, text=new_track_number))
        # audio.save()
        print(_("已更新 {} 的新曲目编号: {}").format(file_path, new_track_number))

    def organize_files(self, include_album, include_lrc):
        for file_path in self.audio_files:
            try:
                tags = self.audio_tags[file_path]
                artist = tags.get('artist', '未知艺术家')
                album = tags.get('album', '未知专辑')
                file_name = os.path.basename(file_path)
                
                if include_album:
                    new_path = os.path.normpath(os.path.join(self.output_directory, artist, album, file_name))
                else:
                    new_path = os.path.normpath(os.path.join(self.output_directory, artist, file_name))
                
                # 确保目标目录存在
                os.makedirs(os.path.dirname(new_path), exist_ok=True)
                
                # 移动文件
                move_file(file_path, new_path)
                print(f"Moved file: {file_path} -> {new_path}")
                
                # 移动同名的 .lrc 文件
                if include_lrc:
                    lrc_file = os.path.splitext(file_path)[0] + '.lrc'
                    if os.path.exists(lrc_file):
                        new_lrc_path = os.path.normpath(os.path.splitext(new_path)[0] + '.lrc')
                        move_file(lrc_file, new_lrc_path)
                        print(f"Moved LRC file: {lrc_file} -> {new_lrc_path}")
                
                # 更新 audio_files 中的路径
                index = self.audio_files.index(file_path)
                self.audio_files[index] = new_path
                
                # 更新 audio_tags 中的键
                self.audio_tags[new_path] = self.audio_tags.pop(file_path)
            
            except Exception as e:
                print(f"Error organizing file {file_path}: {str(e)}")

    def batch_rename(self, old_text, new_text):
        for i, file_path in enumerate(self.audio_files):
            directory, file_name = os.path.split(file_path)
            name, ext = os.path.splitext(file_name)
            new_name = name.replace(old_text, new_text)
            new_file_name = new_name + ext
            
            if file_name != new_file_name:
                new_path = os.path.join(directory, new_file_name)
                rename_file(file_path, new_path)
                
                # 更新 audio_files 中的路径
                self.audio_files[i] = new_path
                
                # 更新 audio_tags 中的键
                self.audio_tags[new_path] = self.audio_tags.pop(file_path)