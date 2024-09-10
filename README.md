# 项目说明

## 项目简介

该项目旨在整理音频文件以便在 Plex 音频库中进行刮削使用。通过本项目，你可以批量更新音频文件的标签、重命名文件、整理文件结构，并查找重复文件，以确保你的音频库条理清晰，适合刮削工具。
绝大多数代码由 Cursor AI 生成。

## 功能列表与使用方式

### 主视图
- **功能**: 提供整体界面布局和导航。
- **使用方法**:
    - 选择目录: 点击“选择目录”按钮，选择包含音频文件的文件夹。
    - 查看文件统计: 显示选定目录中的文件类型、数量和总大小等信息。
    - 切换功能标签页: 使用标签页切换不同的功能视图。

### 更新 Track Tag
- **功能**: 批量更新音频文件的曲目编号，按照文件名从小到大排序，track tag 为 1 开始。
- **使用方法**:
    - 预览: 显示文件名、当前 Track Tag 和新 Track Tag。
    - 更新: 点击“开始更新 Track Tag”按钮执行更新操作。

### 整理音频文件
- **功能**: 根据艺术家和专辑信息自动移动音频文件到艺术家/专辑目录。
- **使用方法**:
    - 选项: 勾选“包含专辑文件夹”复选框决定是否创建专辑文件夹。
    - 预览: 显示文件名、艺术家、专辑和新路径。
    - 整理: 点击“开始整理”按钮执行文件整理操作。

### 批量重命名
- **功能**: 批量重命名音频文件。
- **使用方法**:
    - 输入: 在“要替换的文本”和“新文本”输入框中输入相应内容。
    - 预览: 显示原文件名和新文件名。
    - 重命名: 点击“确认重命名”按钮执行重命名操作。

### 重复文件搜索
- **功能**: 查找并管理重复的音频文件。
- **使用方法**:
    - 搜索: 自动搜索并显示重复文件。
    - 选择: 使用“自动选择”功能标记重复文件。
    - 处理: 选择要处理的文件，点击“删除选中项”或“移动待删除文件”进行处理。
- **重复标准**: 文件被视为重复是基于以下条件：
    - 相同的标题（不区分大小写）
    - 相同的艺术家（不区分大小写）
  注意：这种方法可能会将不同版本的同一首歌曲（如现场版、重混版等）也标记为重复。

## 推荐配套软件

本项目建议与以下软件配合使用，本软件不会实现以下软件包含的功能：

- **[音乐标签PC版](https://www.cnblogs.com/vinlxc/p/11347744.html)**: 用于批量编辑音频文件标签。
- **[MusicBrainz Picard](https://picard.musicbrainz.org/)**: 一款智能音乐标签管理器，支持从 MusicBrainz 数据库获取专辑元数据。
- **[CUETools](http://cue.tools/wiki/Main_Page)**: 用于分割整体音轨文件为多轨（plex不支持CUE文件）。
- **[decrypt-mflac-frida](https://github.com/yllhwa/decrypt-mflac-frida)**: 用于解密 Windows QQ 音乐下载的加密音频文件。

## 许可

本项目采用 [MIT 许可协议](https://opensource.org/license/mit)，详情请参阅 [LICENSE](https://opensource.org/license/mit) 文件。

## 附加功能

- **多语言支持**: 所有视图均支持多语言显示。
- **主题切换**: 可通过主视图的菜单更改应用主题。

---

# Project Description

## Project Introduction

This project aims to organize audio files for use in Plex audio library scraping. With this project, you can batch update audio file tags, rename files, organize file structures, and find duplicate files to ensure your audio library is well-organized and suitable for scraping tools.
Most of the code was generated by Cursor AI.

## Feature List and Usage

### Main View
- **Function**: Provides overall interface layout and navigation.
- **Usage**:
    - Select directory: Click the "Select Directory" button to choose a folder containing audio files.
    - View file statistics: Displays information such as file types, counts, and total sizes in the selected directory.
    - Switch function tabs: Use tabs to switch between different function views.

### Update Track Tag
- **Function**: Batch update track numbers of audio files, sorted by filename in ascending order, starting with track tag 1.
- **Usage**:
    - Preview: Displays filename, current Track Tag, and new Track Tag.
    - Update: Click the "Start Updating Track Tag" button to execute the update operation.

### Organize Audio Files
- **Function**: Automatically move audio files to Artist/Album directories based on artist and album information.
- **Usage**:
    - Options: Check the "Include Album Folder" checkbox to decide whether to create album folders.
    - Preview: Displays filename, artist, album, and new path.
    - Organize: Click the "Start Organizing" button to execute the file organization operation.

### Batch Rename
- **Function**: Batch rename audio files.
- **Usage**:
    - Input: Enter corresponding content in the "Text to Replace" and "New Text" input boxes.
    - Preview: Displays original filename and new filename.
    - Rename: Click the "Confirm Rename" button to execute the rename operation.

### Duplicate File Search
- **Function**: Find and manage duplicate audio files.
- **Usage**:
    - Search: Automatically search and display duplicate files.
    - Select: Use the "Auto Select" function to mark duplicate files.
    - Process: Select files to process, click "Delete Selected" or "Move Files to Delete" to process.

## Recommended Companion Software

This project is recommended to be used in conjunction with the following software. This software will not implement the functions included in the following software:

- **[Music Tag PC Version](https://www.cnblogs.com/vinlxc/p/11347744.html)**: Used for batch editing audio file tags.
- **[MusicBrainz Picard](https://picard.musicbrainz.org/)**: An intelligent music tag manager that supports retrieving album metadata from the MusicBrainz database.
- **[CUETools](http://cue.tools/wiki/Main_Page)**: Used for splitting single-track audio files into multiple tracks (Plex doesn't support CUE files).
- **[decrypt-mflac-frida](https://github.com/yllhwa/decrypt-mflac-frida)**: Used for decrypting encrypted audio files downloaded from Windows QQ Music.

## License

This project is licensed under the MIT License. For details, please refer to the LICENSE file.

## Additional Features

- **Multi-language Support**: All views support multi-language display.
- **Theme Switching**: The application theme can be changed through the menu in the main view.

---

## 安装依赖

1. 确保你的 Python 安装包含 `tkinter`。在大多数 Python 安装中，`tkinter` 是默认包含的。如果没有，你可能需要单独安装。

2. 安装其他依赖：
   ```bash
   pip install -r requirements.txt
   ```

这样可以确保用户了解所有必要的依赖，包括那些可能需要特别注意的依赖。
