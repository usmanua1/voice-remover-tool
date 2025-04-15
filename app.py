<<<<<<< HEAD
from flask import Flask, render_template, request, send_file, redirect, url_for
import os
from spleeter.separator import Separator
from moviepy.editor import VideoFileClip
import uuid
import shutil
import subprocess

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "output"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

separator = Separator("spleeter:2stems")

def cleanup():
    shutil.rmtree(UPLOAD_FOLDER, ignore_errors=True)
    shutil.rmtree(OUTPUT_FOLDER, ignore_errors=True)
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/remove_music", methods=["POST"])
def remove_music():
    if 'audio_file' not in request.files:
        return "No file part"
    file = request.files['audio_file']
    if file.filename == '':
        return "No selected file"
    
    filename = f"{uuid.uuid4()}.mp3"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    output_path = os.path.join(OUTPUT_FOLDER, filename.split('.')[0])
    separator.separate_to_file(filepath, OUTPUT_FOLDER)

    vocals_path = os.path.join(output_path, "vocals.wav")
    return send_file(vocals_path, as_attachment=True)

@app.route("/auto_trim", methods=["POST"])
def auto_trim():
    if 'video_file' not in request.files:
        return "No file part"
    file = request.files['video_file']
    trim_seconds = int(request.form.get('trim_seconds', 10))
    
    filename = f"{uuid.uuid4()}.mp4"
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(input_path)

    clip = VideoFileClip(input_path)
    duration = clip.duration
    final_clips = []

    current = 0
    while current < duration:
        start = current
        end = min(current + 60, duration)
        if end - start > trim_seconds:
            final_clips.append(clip.subclip(start, end - trim_seconds))
        current += 60

    if not final_clips:
        return "Video too short to trim."

    final_video = concatenate_videoclips(final_clips)
    output_path = os.path.join(OUTPUT_FOLDER, f"trimmed_{filename}")
    final_video.write_videofile(output_path)

    return send_file(output_path, as_attachment=True)

@app.route("/custom_music_removal", methods=["POST"])
def custom_music_removal():
    if 'video_file' not in request.files:
        return "No video file uploaded"

    file = request.files['video_file']
    filename = f"{uuid.uuid4()}.mp4"
    video_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(video_path)

    # Extract audio
    audio_path = video_path.replace(".mp4", ".wav")
    subprocess.call(['ffmpeg', '-i', video_path, '-q:a', '0', '-map', 'a', audio_path, '-y'])

    # Separate using spleeter
    output_dir = os.path.join(OUTPUT_FOLDER, filename.split('.')[0])
    separator.separate_to_file(audio_path, OUTPUT_FOLDER)
    vocals_path = os.path.join(output_dir, "vocals.wav")

    # Combine new audio with original video
    final_output = os.path.join(OUTPUT_FOLDER, f"music_removed_{filename}")
    subprocess.call(['ffmpeg', '-i', video_path, '-i', vocals_path, '-c:v', 'copy', '-map', '0:v:0', '-map', '1:a:0', '-y', final_output])

    return send_file(final_output, as_attachment=True)

if __name__ == '__main__':
    cleanup()
    app.run(debug=True)
=======
from flask import Flask, render_template, request, send_file, redirect, url_for
import os
from spleeter.separator import Separator
from moviepy.editor import VideoFileClip
import uuid
import shutil
import subprocess

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "output"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

separator = Separator("spleeter:2stems")

def cleanup():
    shutil.rmtree(UPLOAD_FOLDER, ignore_errors=True)
    shutil.rmtree(OUTPUT_FOLDER, ignore_errors=True)
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/remove_music", methods=["POST"])
def remove_music():
    if 'audio_file' not in request.files:
        return "No file part"
    file = request.files['audio_file']
    if file.filename == '':
        return "No selected file"
    
    filename = f"{uuid.uuid4()}.mp3"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    output_path = os.path.join(OUTPUT_FOLDER, filename.split('.')[0])
    separator.separate_to_file(filepath, OUTPUT_FOLDER)

    vocals_path = os.path.join(output_path, "vocals.wav")
    return send_file(vocals_path, as_attachment=True)

@app.route("/auto_trim", methods=["POST"])
def auto_trim():
    if 'video_file' not in request.files:
        return "No file part"
    file = request.files['video_file']
    trim_seconds = int(request.form.get('trim_seconds', 10))
    
    filename = f"{uuid.uuid4()}.mp4"
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(input_path)

    clip = VideoFileClip(input_path)
    duration = clip.duration
    final_clips = []

    current = 0
    while current < duration:
        start = current
        end = min(current + 60, duration)
        if end - start > trim_seconds:
            final_clips.append(clip.subclip(start, end - trim_seconds))
        current += 60

    if not final_clips:
        return "Video too short to trim."

    final_video = concatenate_videoclips(final_clips)
    output_path = os.path.join(OUTPUT_FOLDER, f"trimmed_{filename}")
    final_video.write_videofile(output_path)

    return send_file(output_path, as_attachment=True)

@app.route("/custom_music_removal", methods=["POST"])
def custom_music_removal():
    if 'video_file' not in request.files:
        return "No video file uploaded"

    file = request.files['video_file']
    filename = f"{uuid.uuid4()}.mp4"
    video_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(video_path)

    # Extract audio
    audio_path = video_path.replace(".mp4", ".wav")
    subprocess.call(['ffmpeg', '-i', video_path, '-q:a', '0', '-map', 'a', audio_path, '-y'])

    # Separate using spleeter
    output_dir = os.path.join(OUTPUT_FOLDER, filename.split('.')[0])
    separator.separate_to_file(audio_path, OUTPUT_FOLDER)
    vocals_path = os.path.join(output_dir, "vocals.wav")

    # Combine new audio with original video
    final_output = os.path.join(OUTPUT_FOLDER, f"music_removed_{filename}")
    subprocess.call(['ffmpeg', '-i', video_path, '-i', vocals_path, '-c:v', 'copy', '-map', '0:v:0', '-map', '1:a:0', '-y', final_output])

    return send_file(final_output, as_attachment=True)

if __name__ == '__main__':
    cleanup()
    app.run(debug=True)
>>>>>>> 70b86dc75e986558012332804af42e2127627c39
