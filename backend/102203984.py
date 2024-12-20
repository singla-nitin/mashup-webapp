import sys
from googleapiclient.discovery import build
from moviepy.editor import AudioFileClip, concatenate_audioclips
import os
import yt_dlp
from dotenv import load_dotenv
import os

load_dotenv()


api_key = os.getenv('API_KEY')

def check_arguments():
    if len(sys.argv) != 5:
        sys.exit(1)

    try:
        num_videos = int(sys.argv[2])
        duration = int(sys.argv[3])

        if num_videos < 10:
            print("Number of videos should be greater than or equal to 10.")
            sys.exit(1)

        if duration < 20:
            print("Audio duration should be greater than or equal to 20 seconds.")
            sys.exit(1)

    except ValueError:
        print("Number of videos and audio duration should be integers.")
        sys.exit(1)


def urls(artist_name, num_videos):

    youtube = build('youtube', 'v3', developerKey=api_key)

    request = youtube.search().list(
        q=artist_name,
        part='snippet',
        type='video',
        maxResults=num_videos
    )
    
    response = request.execute()

    video_urls = []
    for item in response['items']:
        video_id = item['id']['videoId']
        video_urls.append(f"https://www.youtube.com/watch?v={video_id}")

    return video_urls


def download_videos(video_urls):
    audio_files = []
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': './downloaded_videos/%(id)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    os.makedirs('./downloaded_videos', exist_ok=True) 

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for url in video_urls:
            ydl.download([url])
            video_id = url.split('=')[-1]
            audio_file = f'./downloaded_videos/{video_id}.mp3'
            audio_files.append(audio_file)

    return audio_files


def trim_audio_files(audio_files, duration):
    trimmed_files = []

    for audio_file in audio_files:
        output_file = audio_file.replace('.mp3', f'_trimmed_{duration}.mp3')

        if os.path.exists(audio_file):
            with AudioFileClip(audio_file) as audio:
                trimmed_audio = audio.subclip(0, duration)
                trimmed_audio.write_audiofile(output_file)
                trimmed_files.append(output_file)
                print(f"Trimmed {audio_file} to {duration} seconds.")
        else:
            print(f"File {audio_file} does not exist!")

    return trimmed_files


def merge_audios(trimmed_files, output_filename):
    audio_clips = [AudioFileClip(audio) for audio in trimmed_files]
    final_clip = concatenate_audioclips(audio_clips)
    final_clip.write_audiofile(output_filename)
    print(f"Final mashup created: {output_filename}")

# Main program execution
if __name__ == "__main__":
    
    check_arguments()

    
    artist_name = sys.argv[1]
    num_videos = int(sys.argv[2])
    duration = int(sys.argv[3])
    output_filename = sys.argv[4]


    video_urls = urls(artist_name, num_videos)
    audio_files = download_videos(video_urls)
    trimmed_files = trim_audio_files(audio_files, duration)
    merge_audios(trimmed_files, output_filename)
