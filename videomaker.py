import subprocess
from mutagen.mp3 import MP3

try:
    subprocess.run(["ffmpeg", "-version"], check=True)
    print("✅ FFmpeg is installed and accessible!")
except FileNotFoundError:
    print("❌ FFmpeg is NOT installed or not found in PATH!")
    exit(1)

# Your existing command
import subprocess

# Check if FFmpeg is installed
try:
    subprocess.run(["ffmpeg", "-version"], check=True)
    print("✅ FFmpeg is installed and accessible!")
except FileNotFoundError:
    print("❌ FFmpeg is NOT installed or not found in PATH!")
    exit(1)

# Your existing command
subprocess.run([
    "ffmpeg", "-i", "input.mp4", "-filter:v", "scale=1280:720",
    "-c:v", "libx264", "-preset", "slow", "-crf", "22", "output.mp4"
], check=True)
# File names
bg_video = "BGVid.mp4"
audio_file = "audio.mp3"
output_video = "final_video.mp4"

# Get duration of the audio file
audio_duration = MP3(audio_file).info.length

# Calculate new trimmed length (2x the audio duration)
trim_length = audio_duration * 2

# Trim background video
trimmed_video = "TrimmedBGVid.mp4"
subprocess.run([
    "ffmpeg", "-y", "-i", bg_video, "-t", str(trim_length), "-c:v", "libx264", "-preset", "fast", "-c:a", "aac", trimmed_video
])

# Merge the trimmed video with audio, adjusting volumes
subprocess.run([
    "ffmpeg", "-y", "-i", trimmed_video, "-i", audio_file, 
    "-filter_complex",
    "[0:a]volume=0.7[a1];"  # Reduce background volume
    "[1:a]adelay=0|0[a2];"  # Sync audio.mp3
    "[a1][a2]amix=inputs=2:duration=first[aout]",  # Mix both
    "-map", "0:v:0", "-map", "[aout]", "-c:v", "libx264", "-preset", "fast", "-c:a", "aac", output_video
])

print("Final video created successfully as", output_video)
