import os
import logging
import time
import random
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("youtube_upload.log"), logging.StreamHandler()],
)

# Constants
SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.force-ssl"  # Allows managing YouTube comments
]
CLIENT_SECRETS_FILE = "client_secret.json"
TOKEN_FILE = "token.json"
VIDEO_FILENAME = "final_video.mp4"  # Your final output video file
THUMBNAIL_FILENAME = "thumbnail.jpeg"  # Your thumbnail file

# List of relaxing, channel-relevant comments
RELAXING_COMMENTS = [
    "Take a deep breath, relax, and let this story guide you into a peaceful sleep. ",
    "Drift away into a world of calm and serenity. Sleep well, dream beautifully. ",
    "Close your eyes, breathe deeply, and let this soothing tale carry you into restful sleep. ",
    "Your journey to a restful night begins here. Let go of the day and embrace the calm.",
    "If you find peace in these stories, consider subscribing for more dreamy nights.",
]

def authenticate_youtube():
    """Authenticate with YouTube API, handling both initial auth and token refresh."""
    credentials = None

    if os.path.exists(TOKEN_FILE):
        credentials = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())  # Use refresh token to get a new access token
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
            credentials = flow.run_local_server(port=0)

        with open(TOKEN_FILE, "w") as token:
            token.write(credentials.to_json())  # Save both access and refresh tokens


    return build("youtube", "v3", credentials=credentials)

def upload_video(youtube, title, video_path, thumbnail_path, privacy_status="public"):
    """Upload video to YouTube with a given title and thumbnail."""
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")

    try:
        logging.info("Preparing video upload...")

        request_body = {
            "snippet": {
                "title": title,
                "description": """✨ Welcome to Sleep Zone - Your Gateway to Restful Sleep ✨

Drift into a peaceful night's sleep with our carefully crafted sleep stories, designed to help you relax, unwind, and escape into a world of gentle imagination. Whether you're struggling with insomnia, anxiety, or stress, our calming narrations and soothing background music will guide you to a restful night.

🌙 What You'll Find Here:
✔️ Tranquil bedtime stories for deep relaxation
✔️ Soft-spoken narration in a soothing voice
✔️ Serene visuals to create a peaceful atmosphere
✔️ Gentle sleep music & ambient sounds

Subscribe now and let us help you find your way to a better night's sleep. Sweet dreams! 🌟😴

#SleepStories #RelaxingNarration #DeepSleep #CalmAndRelax #BedtimeStories
                """,
                "tags": [
                    "sleep story", "sleep music", "deep sleep", "bedtime story", "cozy sleep", "relaxation", 
                    "calming story", "soothing narration", "fantasy sleep story", "meditation", "stress relief", 
                    "anxiety relief", "sleep aid", "insomnia relief", "nature sounds", "dreamscape", 
                    "magical bedtime story", "peaceful sleep", "soft spoken story", "ASMR sleep", "guided sleep", 
                    "sleep relaxation", "sleep meditation", "ethereal music", "deep relaxation", 
                    "storytelling for sleep", "enchanted forest", "fantasy relaxation", "slow sleep music"
                ],
                "categoryId": "22"  # People & Blogs (Change if needed)
            },
            "status": {
                "privacyStatus": privacy_status,
                "selfDeclaredMadeForKids": False
            }
        }

        media = MediaFileUpload(video_path, mimetype="video/mp4", resumable=True)

        insert_request = youtube.videos().insert(
            part=",".join(request_body.keys()),
            body=request_body,
            media_body=media
        )

        logging.info("Starting video upload...")
        response = None
        last_progress = 0

        while response is None:
            try:
                status, response = insert_request.next_chunk(num_retries=5)
                if status:
                    progress = int(status.progress() * 100)
                    if progress != last_progress:
                        # logging.info(f"Upload progress: {progress}%")
                        last_progress = progress
            except Exception as e:
                logging.error(f"Chunk upload error: {str(e)}")
                time.sleep(5)
                continue

        video_id = response["id"]
        video_url = f"https://youtu.be/{video_id}"
        logging.info(f"Upload Complete! Video URL: {video_url}")

        # Upload thumbnail
        if os.path.exists(thumbnail_path):
            try:
                youtube.thumbnails().set(
                    videoId=video_id,
                    media_body=MediaFileUpload(thumbnail_path)
                ).execute()
                logging.info("Thumbnail uploaded successfully")
            except Exception as e:
                logging.error(f"Thumbnail upload error: {str(e)}")

        # Post a relaxing comment
        post_comment(youtube, video_id)

        return video_id

    except Exception as e:
        logging.error(f"Upload error: {str(e)}", exc_info=True)
        raise

def post_comment(youtube, video_id):
    """Post a calming comment on the uploaded video."""
    try:
        comment_text = random.choice(RELAXING_COMMENTS)

        request_body = {
            "snippet": {
                "videoId": video_id,
                "topLevelComment": {
                    "snippet": {
                        "textOriginal": comment_text
                    }
                }
            }
        }

        youtube.commentThreads().insert(
            part="snippet",
            body=request_body
        ).execute()

        logging.info(f"Comment posted: {comment_text}")

    except Exception as e:
        logging.error(f"Comment posting error: {str(e)}")

def main(title):
    try:
        youtube = authenticate_youtube()
        upload_video(youtube, title, VIDEO_FILENAME, THUMBNAIL_FILENAME)

        logging.info("Process completed successfully!")

    except Exception as e:
        logging.error(f"Fatal error: {str(e)}", exc_info=True)
        raise

import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        logging.error("This script is meant to be run from main.py with a title argument.")
        sys.exit(1)

    video_title = sys.argv[1]
    logging.info(f"Received title from main.py: {video_title}")
    main(video_title)
