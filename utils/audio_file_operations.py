import os
import shutil
from mutagen import File
from mutagen.id3 import ID3, ID3NoHeaderError
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.wave import WAVE
from utils.utils import format_time  # 使用相对导入

def get_audio_files(directory, supported_formats):
    audio_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(supported_formats):
                audio_files.append(os.path.join(root, file))
    return audio_files


def get_audio_tags(file_path):
    try:
        audio = File(file_path)
        if audio is None:
            return {}

        tags = {}
        if isinstance(audio, MP3):
            try:
                id3 = ID3(file_path)
                tags['title'] = str(id3.get('TIT2', [''])[0])
                tags['artist'] = str(id3.get('TPE1', ['未知艺术家'])[0])
                tags['album'] = str(id3.get('TALB', ['未知专辑'])[0])
                tags['tracknumber'] = str(id3.get('TRCK', ['0/0'])[0])  # 添加这行
            except ID3NoHeaderError:
                pass
            tags['length'] = audio.info.length
        elif isinstance(audio, FLAC):
            tags['title'] = str(audio.get('title', [''])[0])
            tags['artist'] = str(audio.get('artist', ['未知艺术家'])[0])
            tags['album'] = str(audio.get('album', ['未知专辑'])[0])
            tags['tracknumber'] = str(audio.get('tracknumber', ['0/0'])[0])  # 添加这行
            tags['length'] = audio.info.length
        elif isinstance(audio, WAVE):
            tags['length'] = audio.info.length
        else:
            tags['title'] = str(audio.get('title', [''])[0])
            tags['artist'] = str(audio.get('artist', ['未知艺术家'])[0])
            tags['album'] = str(audio.get('album', ['未知专辑'])[0])
            tags['tracknumber'] = str(audio.get('tracknumber', ['0/0'])[0])  # 添加这行
            tags['length'] = audio.info.length if hasattr(audio.info, 'length') else 0

        return tags
    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {e}")
        return {}

def delete_file(file_path):
    os.remove(file_path)

def rename_file(old_path, new_path):
    os.rename(old_path, new_path)

def move_file(old_path, new_path):
    shutil.move(old_path, new_path)
