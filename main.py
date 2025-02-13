import subprocess
import os

# Function to delete temporary files
def delete_temp_files():
    files_to_delete = ["story.txt", "audio.mp3", "TrimmedBGVid.mp4", "final_video.mp4", "video_title.txt"]
    for file in files_to_delete:
        if os.path.exists(file):
            os.remove(file)
            print(f"Deleted {file}")

# Function to run a script and check for errors
def run_script(script_name):
    try:
        print(f"Running {script_name}...")
        result = subprocess.run(["python", script_name], check=True, capture_output=True, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error in {script_name}:\n{e.stderr}")
        exit(1)  # Stop execution if an error occurs

# Extract title from the last line of story.txt
def extract_title_from_story(story_file):
    if not os.path.exists(story_file):
        print("Error: story.txt not found for title extraction.")
        exit(1)
    
    with open(story_file, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    
    prefix = "Soothing Sleep Story & Cozy Music for Deep Relaxation | "
    title_line = lines[-1] if lines else ""

    if title_line.startswith(prefix):
        return title_line
    else:
        print("Warning: Title line not found or doesn't match expected format. Using default title.")
        return "Soothing Sleep Story & Cozy Music for Deep Relaxation"  # Default title without "Untitled Story"

# ---- Pipeline Execution ----

# Step 1: Clean up old files before starting
delete_temp_files()

# Step 2: Generate story.txt
run_script("story.py")

# Step 3: Generate audio.mp3
if os.path.exists("story.txt"):
    run_script("tts.py")
else:
    print("Error: story.txt not found.")
    exit(1)

# Step 4: Generate final_video.mp4
if os.path.exists("audio.mp3"):
    run_script("videomaker.py")
else:
    print("Error: audio.mp3 not found.")
    exit(1)

# Step 5: Extract title for upload
video_title = extract_title_from_story("story.txt")
print(f"Extracted Title: {video_title}")

# Step 6: Upload final_video.mp4 with extracted title
if os.path.exists("final_video.mp4"):
    try:
        print("Running upload.py...")
        subprocess.run(["python", "upload.py", video_title], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error in upload.py: {e}")
        exit(1)
else:
    print("Error: final_video.mp4 not found.")
    exit(1)

# Step 7: Confirm successful upload before deleting temp files
confirm = input("Was the upload successful? (yes/no): ").strip().lower()
if confirm == "yes":
    delete_temp_files()
else:
    print("Skipping file deletion.")

print("Pipeline execution completed!")
