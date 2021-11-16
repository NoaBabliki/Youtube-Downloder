from __future__ import unicode_literals
import youtube_dl, subprocess
from moviepy.editor import *
import os
import sys
import re


def download_first_30_seconds(urls_file, destination_dir):
    """
    downloads first minute of a youtube video
    :param urls_file: path to the txt file with youtube urls
    :param destination_dir: path to directory for downloaded video
    :return: none
    """
    file = open(urls_file, 'r')
    for line in file:

        youtube_url = line
        time_from = "00:00:00"
        time_to = "00:01:00"
        print(youtube_url)
        with youtube_dl.YoutubeDL({'format': 'best'}) as ydl:
            result = ydl.extract_info(youtube_url, download=False)
            title = re.sub('[^a-zA-Z0-9 \n\.]', '', result["title"])
            target = destination_dir + "/" + title + ".mp4"
            print(target)
            video = result['entries'][0] if 'entries' in result else result

        url = video['url']
        subprocess.call('ffmpeg -i "%s" -ss %s -t %s -c:v copy -c:a copy "%s"' % (url, time_from, time_to, target), shell=True)

    file.close()


def mp4_to_mp3(mp4, mp3):
    """
    convert mp4 to mp3
    :param mp4: path to mp4 file
    :param mp3: path to mp3 file
    :return: none
    """
    mp4_without_frames = AudioFileClip(mp4)
    mp4_without_frames.write_audiofile(mp3)
    mp4_without_frames.close()


def convert_mp4_to_mp3(source_dir, destination_dir):
    """
    convert all mp4 files in the source directory to mp3 files in the destination directory
    :param source_dir: path to source directory
    :param destination_dir: path to destination directory
    :return: none
    """
    for filename in os.listdir(source_dir):
        if filename.endswith('.mp4'):
            mp4_to_mp3(source_dir + '/' + filename, destination_dir + '/' + filename.replace("mp4", "mp3"))


if __name__ == "__main__":
    if len(sys.argv) == 4:
        if sys.argv[1] == "d":
            urls_file = sys.argv[2]
            destination_dir = sys.argv[3]
            download_first_30_seconds(urls_file, destination_dir)
        if sys.argv[1] == "c":
            source_dir = sys.argv[2]
            destination_dir = sys.argv[3]
            convert_mp4_to_mp3(source_dir, destination_dir)
    if len(sys.argv) == 5:
        if sys.argv[1] == "dc":
            urls_file = sys.argv[2]
            source_dir = sys.argv[3]
            destination_dir = sys.argv[4]
            download_first_30_seconds(urls_file, source_dir)
            convert_mp4_to_mp3(source_dir, destination_dir)
    else:
        print('Instructions: \n'
              'Please specify the action you want to do, and the arguments, as follows:\n\n'
              'action: download first 30 seconds of youtube videos\n'
              'first argument: d\n'
              'second argument: full path to a text file that contains the youtube videos urls.\n'
              'third argument: full path to the directory you want to download to.\n'
              '\n'
              'action: convert mp4 videos to mp3 audios\n'
              'first argument: c\n'
              'second argument: full path to the directory of the mp4 files.\n'
              'third argument: full path to the directory you want to put the mp3 files in.\n'
              '\n'
              'action: download and convert'
              'first argument: dc\n'
              'second argument: full path to a text file that contains the youtube videos urls\n'
              'third argument: full path to the directory of the mp4 files.\n'
              'fourth argument: full path to the directory you want to put the mp3 files in.\n'
              )
