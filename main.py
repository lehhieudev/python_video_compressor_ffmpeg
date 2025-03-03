import os
import json
import subprocess
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from threading import Thread
from queue import Queue

global stop_processing
stop_processing = False

CONFIG_FILE = "config.json"

def load_config():
    """Load configuration from config.json."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            return json.load(file)
    return {
        "source_folder": "",
        "destination_folder": "",
        "crf": 28,
        "codec": "libx265",
        "ffmpeg_path": "ffmpeg"
    }

def save_config(source, destination, crf, codec, ffmpeg_path):
    """Save the current settings to config.json."""
    config_data = {
        "source_folder": source,
        "destination_folder": destination,
        "crf": crf,
        "codec": codec,
        "ffmpeg_path": ffmpeg_path
    }
    with open(CONFIG_FILE, "w") as file:
        json.dump(config_data, file, indent=4)
    messagebox.showinfo("Saved", "Settings have been saved successfully.")

def get_unique_filename(output_file):
    """Generate a unique filename by appending _1, _2, etc., if the file already exists."""
    base, ext = os.path.splitext(output_file)
    counter = 1
    new_output = output_file

    while os.path.exists(new_output):
        new_output = f"{base}_{counter}{ext}"
        counter += 1

    return new_output

def compress_video(input_file, output_file, crf, codec, ffmpeg_path, status_queue, log_queue):
    """Compress a video file using FFmpeg."""
    global stop_processing
    try:
        command = [
            ffmpeg_path, "-i", input_file,
            "-c:v", codec, "-crf", str(crf), "-preset", "slow",
            output_file
        ]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

        for line in process.stderr:
            if stop_processing:
                process.terminate()
                if os.path.exists(output_file):
                    os.remove(output_file)
                status_queue.put("Processing Stopped")
                return
            log_queue.put(line.strip())

        process.wait()
        status_queue.put(f"Completed: {os.path.basename(output_file)}")
    except Exception as e:
        status_queue.put(f"Error: {e}")

def process_videos(status_queue, log_queue, source_folder, destination_folder, crf, codec, ffmpeg_path):
    """Process all videos in the source folder."""
    global stop_processing
    stop_processing = False

    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    
    for file in os.listdir(source_folder):
        if stop_processing:
            break
        if file.lower().endswith((".mp4", ".avi", ".mkv", "mov")):
            input_file = os.path.join(source_folder, file)
            output_file = os.path.join(destination_folder, file)
            unique_output_file = get_unique_filename(output_file)

            status_queue.put(f"Processing: {file} -> {os.path.basename(unique_output_file)}")
            compress_video(input_file, unique_output_file, crf, codec, ffmpeg_path, status_queue, log_queue)

def update_status(status_label, status_queue, log_listbox, log_queue):
    """Update the status label and log listbox from the queue."""
    while not status_queue.empty():
        status_label.config(text=status_queue.get())
    while not log_queue.empty():
        log_listbox.insert(tk.END, log_queue.get())
        log_listbox.yview(tk.END)
    
    status_label.after(500, lambda: update_status(status_label, status_queue, log_listbox, log_queue))

def start_processing(status_label, status_queue, log_listbox, log_queue, start_btn, stop_btn, source_entry, dest_entry, crf_combo, codec_combo, ffmpeg_entry):
    """Start video processing in a separate thread."""
    source_folder = source_entry.get()
    destination_folder = dest_entry.get()
    crf = int(crf_combo.get())
    codec = codec_combo.get()
    ffmpeg_path = ffmpeg_entry.get()

    if not source_folder or not destination_folder:
        messagebox.showerror("Error", "Please select both source and destination folders.")
        return

    log_listbox.delete(0, tk.END)
    
    # 🔹 Disable Start, Enable Stop khi đang chạy
    start_btn.config(state=tk.DISABLED)
    stop_btn.config(state=tk.NORMAL)

    Thread(target=process_videos, args=(status_queue, log_queue, source_folder, destination_folder, crf, codec, ffmpeg_path), daemon=True).start()

def stop_processing_confirm(stop_btn, start_btn):
    """Confirm before stopping video processing."""
    global stop_processing
    if messagebox.askyesno("Confirm", "If you stop, the current video conversion will be incomplete. Do you want to proceed?"):
        stop_processing = True
        stop_btn.config(state=tk.DISABLED)
        start_btn.config(state=tk.NORMAL)  # 🔹 Re-enable Start when stopping

def create_ui():
    """Create a GUI for the application."""
    config = load_config()
    root = tk.Tk()
    root.title("Video Compressor")

    status_queue = Queue()
    log_queue = Queue()

    tk.Label(root, text="Source Folder:").grid(row=0, column=0)
    source_entry = tk.Entry(root, width=50)
    source_entry.insert(0, config.get("source_folder", ""))
    source_entry.grid(row=0, column=1)
    tk.Button(root, text="Browse", command=lambda: select_folder(source_entry)).grid(row=0, column=2)

    tk.Label(root, text="Destination Folder:").grid(row=1, column=0)
    dest_entry = tk.Entry(root, width=50)
    dest_entry.insert(0, config.get("destination_folder", ""))
    dest_entry.grid(row=1, column=1)
    tk.Button(root, text="Browse", command=lambda: select_folder(dest_entry)).grid(row=1, column=2)

    tk.Label(root, text="CRF (Quality):").grid(row=2, column=0)
    crf_values = [18, 20, 23, 28, 30, 35, 40, 50]
    crf_combo = ttk.Combobox(root, values=crf_values, width=10)
    crf_combo.set(config.get("crf", 28))
    crf_combo.grid(row=2, column=1)

    tk.Label(root, text="Codec:").grid(row=3, column=0)
    codec_values = ["libx264", "libx265", "vp9", "av1"]
    codec_combo = ttk.Combobox(root, values=codec_values, width=10)
    codec_combo.set(config.get("codec", "libx265"))
    codec_combo.grid(row=3, column=1)

    tk.Label(root, text="FFmpeg Path:").grid(row=4, column=0)
    ffmpeg_entry = tk.Entry(root, width=50)
    ffmpeg_entry.insert(0, config.get("ffmpeg_path", "ffmpeg"))
    ffmpeg_entry.grid(row=4, column=1)
    tk.Button(root, text="Browse", command=lambda: select_ffmpeg_path(ffmpeg_entry)).grid(row=4, column=2)

    # 🔹 Thêm status_label để tránh lỗi
    status_label = tk.Label(root, text="Idle", fg="blue")
    status_label.grid(row=5, column=0, columnspan=3)

    # 🔹 Thêm danh sách log
    log_listbox = tk.Listbox(root, width=80, height=10)
    log_listbox.grid(row=6, column=0, columnspan=3)

    # 🔹 Nút Start và Stop
    start_btn = tk.Button(root, text="Start", command=lambda: start_processing(status_label, status_queue, log_listbox, log_queue, start_btn, stop_btn, source_entry, dest_entry, crf_combo, codec_combo, ffmpeg_entry))
    stop_btn = tk.Button(root, text="Stop", command=lambda: stop_processing_confirm(stop_btn, start_btn), state=tk.DISABLED)

    start_btn.grid(row=7, column=0)
    stop_btn.grid(row=7, column=1)

    # 🔹 Gọi update_status sau khi status_label đã được khai báo
    update_status(status_label, status_queue, log_listbox, log_queue)

    root.mainloop()

if __name__ == "__main__":
    create_ui()
