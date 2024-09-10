import os
import shutil
from mutagen import File
from mutagen.id3 import ID3, ID3NoHeaderError
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.wave import WAVE
from mutagen.oggvorbis import OggVorbis  # 添加这行
from mutagen.aiff import AIFF  # 添加这行
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
        if isinstance(audio, (MP3, FLAC, WAVE, OggVorbis, AIFF)):  # 修改这行
            tags['title'] = str(audio.get('title', [''])[0])
            tags['artist'] = str(audio.get('artist', ['未知艺术家'])[0])
            tags['album'] = str(audio.get('album', ['未知专辑'])[0])
            tags['tracknumber'] = str(audio.get('tracknumber', ['0/0'])[0])
            tags['length'] = audio.info.length
        else:
            # 处理其他文件类型
            tags['title'] = str(audio.get('title', [''])[0])
            tags['artist'] = str(audio.get('artist', ['未知艺术家'])[0])
            tags['album'] = str(audio.get('album', ['未知专辑'])[0])
            tags['tracknumber'] = str(audio.get('tracknumber', ['0/0'])[0])
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
    try:
        # 确保目标目录存在
        os.makedirs(os.path.dirname(new_path), exist_ok=True)
        shutil.move(old_path, new_path)
        print(f"Successfully moved: {old_path} -> {new_path}")
    except Exception as e:
        print(f"Error moving file {old_path} to {new_path}: {str(e)}")
        raise
