YouTube Downloader

This script allows you to download YouTube videos, audio, and playlists.

To use:

Run the script: python youtube_downloader.py

Enter the YouTube URL you want to download

Select the download type:

video - Downloads a video file. You will be prompted to enter the resolution (144p to 1080p)
audio - Downloads an audio MP3 file
playlist - Downloads all videos in a playlist. You will be prompted to enter the resolution (144p to 1080p)
The file(s) will be downloaded to the same directory as the script, and progress bars will be shown during the download.

The final combined MP4 videos will be named with the format: <video_name>_combined.mp4. Audio files will be named <video_name>.mp3.

Requirements:

Python 3
moviepy
pytube
tqdm
