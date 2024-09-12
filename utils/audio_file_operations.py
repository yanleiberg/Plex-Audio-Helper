import os
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
from mutagen import File
from mutagen.id3 import ID3, ID3NoHeaderError
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.wave import WAVE
from mutagen.oggvorbis import OggVorbis
from mutagen.aiff import AIFF
from utils.utils import format_time


def get_audio_files(directory, supported_formats):
    audio_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(supported_formats):
                audio_files.append(os.path.join(root, file))
    return audio_files


def get_audio_tags(file_path):
    try:
        audio = File(file_path, easy=True)
        if audio is None:
            return {}

        tags = {}
        if isinstance(audio, MP3):
            tags['length'] = audio.info.length
            try:
                id3 = ID3(file_path)
                tags['title'] = str(id3.get('TIT2', [''])[0])
                tags['artist'] = str(id3.get('TPE1', ['未知艺术家'])[0])
                tags['album'] = str(id3.get('TALB', ['未知专辑'])[0])
                tags['tracknumber'] = str(id3.get('TRCK', ['0/0'])[0])
            except ID3NoHeaderError:
                pass
        elif isinstance(audio, (FLAC, OggVorbis, AIFF)):
            tags['title'] = str(audio.get('title', [''])[0])
            tags['artist'] = str(audio.get('artist', ['未知艺术家'])[0])
            tags['album'] = str(audio.get('album', ['未知专辑'])[0])
            tags['tracknumber'] = str(audio.get('tracknumber', ['0/0'])[0])
            tags['length'] = audio.info.length
        elif isinstance(audio, WAVE):
            tags['length'] = audio.info.length
        else:
            tags['title'] = str(audio.get('title', [''])[0])
            tags['artist'] = str(audio.get('artist', ['未知艺术家'])[0])
            tags['album'] = str(audio.get('album', ['未知专辑'])[0])
            tags['tracknumber'] = str(audio.get('tracknumber', ['0/0'])[0])
            tags['length'] = audio.info.length if hasattr(audio.info, 'length') else 0

        return tags
    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {e}")
        return {}


def process_files_in_parallel(audio_files, max_workers=4):
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_file = {executor.submit(get_audio_tags, file): file for file in audio_files}
        for future in as_completed(future_to_file):
            file = future_to_file[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as exc:
                print(f"读取文件 {file} 时出错: {exc}")
    return results


def delete_file(file_path):
    os.remove(file_path)

def rename_file(old_path, new_path):
    os.rename(old_path, new_path)

def move_file(old_path, new_path):
    try:
        os.makedirs(os.path.dirname(new_path), exist_ok=True)
        shutil.move(old_path, new_path)
        print(f"Successfully moved: {old_path} -> {new_path}")
    except Exception as e:
        print(f"Error moving file {old_path} to {new_path}: {str(e)}")
        raise

# Example of usage
if __name__ == "__main__":
    supported_formats = ('.mp3', '.flac', '.wav', '.ogg', '.aiff')
    directory = 'path_to_your_audio_files'
    audio_files = get_audio_files(directory, supported_formats)
    
    # Process the audio files in parallel
    results = process_files_in_parallel(audio_files, max_workers=8)
    for tags in results:
        print(tags)
