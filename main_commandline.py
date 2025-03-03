import ffmpeg

ffmpeg_path = "C:/ffmpeg/bin/ffmpeg.exe"  # Thay đổi đường dẫn đúng với máy bạn

def compress_video(input_file, output_file, crf=28, codec="libx265"):
    (
        ffmpeg
        .input(input_file)
        .output(output_file, vcodec=codec, crf=crf, preset="slow")
        .run()
    )

compress_video("HDSD Dang ky dich vu.mp4", "output.mp4")
