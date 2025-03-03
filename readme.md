# Video Compressor with FFmpeg

## 📌 Introduction
This is a **Python-based video compression tool** that uses **FFmpeg** to compress videos efficiently while maintaining good quality. It provides a **graphical user interface (GUI) using Tkinter**, allowing users to easily select source and destination folders, configure compression settings, and monitor the process in real-time.

## 🚀 Features
- **Supports multiple video formats**: `.mp4`, `.avi`, `.mkv`, etc.
- **GUI-based configuration**
- **CRF quality control** (lower CRF means better quality, higher CRF means smaller file size)
- **Supports multiple codecs** (`libx265`, `libx264`, etc.)
- **Handles duplicate file names** by appending `_1`, `_2`, etc.
- **Real-time logging in Listbox**
- **Start/Stop functionality** to control the conversion process
- **FFmpeg path selection** via file dialog
- **Configuration saved in `config.json`**

## 🛠 Requirements
- Python 3.7+
- FFmpeg installed and accessible via command line
- Required Python packages:
  ```sh
  pip install tk
  ```

## 💾 Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/lehhieudev/python_video_compressor_ffmpeg.git
   cd video-compressor
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Make sure **FFmpeg** is installed and available in the system path. You can check by running:
   ```sh
   ffmpeg -version
   ```
4. Run the program:
   ```sh
   python main.py
   ```

## 🖥️ Usage
1. Select the **source folder** containing videos.
2. Select the **destination folder** where compressed videos will be saved.
3. Choose **CRF quality** (recommended: `23` for balance between size & quality).
4. Choose **video codec** (`libx265` for HEVC, `libx264` for H.264, etc.).
5. Browse and set **FFmpeg path** if needed.
6. Click **Start Compression** to begin the process.
7. Logs will be displayed in the **Listbox**.
8. If needed, click **Stop Processing** to interrupt the process.

## 🔧 Configuration
All settings are stored in `config.json`. Example:
```json
{
  "source_folder": "C:/Videos/Source",
  "destination_folder": "C:/Videos/Compressed",
  "crf": 28,
  "codec": "libx265",
  "ffmpeg_path": "C:/ffmpeg/bin/ffmpeg.exe"
}
```

## 📝 Notes
- The output file name is modified to avoid overwriting existing files by appending `_1`, `_2`, etc.
- Lower CRF means **better quality but larger file size** (recommended: 23-28).
- If `FFmpeg` is not found, manually set the path in the application.

## 🤝 Contributing
Feel free to fork this repository, submit issues, and suggest improvements!

## 📜 License
This project is **open-source** and available under the **MIT License**.

---
**Happy compressing! 🚀**

