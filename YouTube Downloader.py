import os
from tqdm import tqdm
import moviepy.editor as mp
from pytube import YouTube
from pytube import Playlist 


def validate_resolution(resolution):
    valid_resolutions = ['144p', '240p', '360p', '480p', '720p', '1080p']
    if resolution not in valid_resolutions:
        print(f'{resolution} is not a valid resolution. Valid resolutions are: {", ".join(valid_resolutions)}')
        return False
    return True


def download_video(url, resolution):
    try:
        yt = YouTube(url, on_progress_callback=on_download_progress)
        video = yt.streams.filter(res=resolution, file_extension='mp4').first()
        video_path = video.download()
        audio = yt.streams.filter(only_audio=True).order_by('bitrate').last()
        audio_path = audio.download()

        video_basename = os.path.basename(video_path)
        audio_basename = os.path.basename(audio_path)
        final_path = os.path.join(os.path.dirname(video_path), f'{os.path.splitext(video_basename)[0]}_combined.mp4')

        video_clip = mp.VideoFileClip(video_path)
        audio_clip = mp.AudioFileClip(audio_path)
        final_clip = video_clip.set_audio(audio_clip) 
        final_clip.write_videofile(final_path)

        for f in [video_path, audio_path]:
            os.remove(f)
        
        print(f'Download complete: {final_path}')
    except Exception as e:
        print(f'Download failed: {e}')


def download_audio(url):
    try:
        yt = YouTube(url, on_progress_callback=on_download_progress)
        audio = yt.streams.filter(only_audio=True).order_by('bitrate').last()
        audio_path = audio.download()

        audio_basename = os.path.basename(audio_path)
        final_path = os.path.join(os.path.dirname(audio_path), f'{os.path.splitext(audio_basename)[0]}.mp3')

        os.rename(audio_path, final_path)
        
        print(f'Download complete: {final_path}')
    except Exception as e:
        print(f'Download failed: {e}')


def download_playlist(url, resolution):
    try:
        playlist = Playlist(url)
        video_count = 1

        for video_url in playlist.video_urls:
            yt = YouTube(video_url, on_progress_callback=on_download_progress)
            video = yt.streams.filter(res=resolution, file_extension='mp4').first()
            video_path = video.download()
            audio = yt.streams.filter(only_audio=True).order_by('bitrate').last()
            audio_path = audio.download()

            video_basename = os.path.basename(video_path)
            audio_basename = os.path.basename(audio_path)
            final_path = os.path.join(os.path.dirname(video_path), f'{os.path.splitext(video_basename)[0]}_combined_{video_count}.mp4')

            video_clip = mp.VideoFileClip(video_path)
            audio_clip = mp.AudioFileClip(audio_path)
            final_clip = video_clip.set_audio(audio_clip)
            final_clip.write_videofile(final_path)

            for f in [video_path, audio_path]:
                os.remove(f)

            print(f'Download complete: {final_path}')
            video_count += 1

    except Exception as e:
        print(f'Download failed: {e}')


def on_download_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    progress = bytes_downloaded / total_size * 100
    bar_length = 40
    filled_length = int(progress / 100 * bar_length)
    bar = '=' * filled_length + '-' * (bar_length - filled_length)
    tqdm.write(f'Download progress: |{bar}| {progress:.2f}%')


def main():
    url = input("Enter the YouTube URL: ")
    download_type = input("Enter the download type (video, audio, playlist): ")

    if download_type == "video":
        resolution = input("Enter the resolution (144p, 240p, 360p, 480p, 720p, 1080p): ")
        if not validate_resolution(resolution):
            return 
        download_video(url, resolution)
    elif download_type == "audio":
        download_audio(url)
    elif download_type == "playlist":
        resolution = input("Enter the resolution (144p, 240p, 360p, 480p, 720p, 1080p): ")
        if not validate_resolution(resolution):
            return 
        download_playlist(url, resolution)
    else:
        print("Invalid download type. Please enter video, audio, or playlist.")


if __name__ == "__main__":
    main()
