print('\n\n\nnew run')
import subprocess
from pytube import YouTube
import urllib.request
import re
import os
import shutil
import yt_dlp
import random
import datetime
from english_words import get_english_words_set

scriptpath = "/Users/a/coding/"

def setup(): ### delete old files 
    try:
        shutil.rmtree(f"{scriptpath}files/")
        os.rmdir(f"{scriptpath}files/")
        os.makedirs(f"{scriptpath}files/")
        os.chdir(f"{scriptpath}files/")
    except:
        os.makedirs(f"{scriptpath}files/")
        os.chdir(f"{scriptpath}files/")    


def get_video_title(url):
    print('get video title')
    ydl_opts = {}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        title = info.get('title', None)
        print(f"\n\n\nVideo Title: {title}\n\n\n")
    print('video title end')
    return title

def get_video_tags(url):
    print('get video tags')
    ydl_opts = {}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        tags = info.get('tags', None)
        if len(tags) < 1:
            tags.append("reverse")
            print('added tag because tags were empty')
        tags = ','.join(map(str,tags))
        print(f"\n\n\nVideo Tags: {tags}\n\n\n")
    print('video tags end')
    return tags

def get_video_channel(url):
    print('get channel url')
    ydl_opts = {}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        channel_url = info.get('channel_url', None)
        print(f"\n\n\nChannel URL: {channel_url}\n\n\n")
    print('channel url end')
    return channel_url


# lädt video von youtube runter
def download_youtube_video(link):
    print('download video')
    # old command for maximum video quality always (Requires minimum Disk space of 512 GB and fiber optics internet because some File sizes can be huge)
    #command = f"yt-dlp -f bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best '{link}' --sponsorblock-remove intro,outro,sponsor -o 'video'" # video bv(best video resolution) ba(best audio resolution) -o "output file name"
    command = f"yt-dlp -f bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best -S \"filesize:20G\" '{link}' --sponsorblock-remove intro,outro,sponsor -o 'video'" # video bv(best video resolution) ba(best audio resolution) -o "output file name"

    subprocess.run(command, shell=True)
    print('video download process end')

def download_youtube_thumbnail(link, thumbnailname):
    print('download thumbnail')
    # Create a YouTube object
    yt = YouTube(link)
    # Get the thumbnail URL
    thumbnail_url = yt.thumbnail_url
    # Download the thumbnail
    urllib.request.urlretrieve(thumbnail_url, thumbnailname)
    print('thumbnail download process end')


def reverse_video(input_file, full_reversed_file):
    # Set the input video file and chunk size
    chunk_size = 10  # in seconds

    # Create a directory to store the chunked files
    chunk_dir = 'chunks'
    reversed_chunk_dir = 'reversed_chunks'
    if not os.path.exists(chunk_dir):
        os.makedirs(chunk_dir)

    # Split the video into chunks using FFmpeg
    cmd = f"ffmpeg -i {input_file} -f segment -segment_time {chunk_size} -segment_format mp4 {chunk_dir}/chunk_%06d.mp4"
    subprocess.run(cmd.split(' '))


    if not os.path.exists(reversed_chunk_dir):
        os.makedirs(reversed_chunk_dir)

    # Reverse each chunk
    for filename in os.listdir(chunk_dir):
        if filename.endswith('.mp4'):
            chunk_file = os.path.join(chunk_dir, filename)
            output_file = os.path.join(reversed_chunk_dir, f"reversed_{filename}")
            cmd = f"ffmpeg -i {chunk_file} -vf reverse -af areverse {output_file}"
            subprocess.run(cmd.split(' '))

    # Create a text file with the list of reversed chunks

    with open('reversed_chunks.txt', 'w') as f:
        filelist = os.listdir(reversed_chunk_dir)
        filelist.sort(reverse=True)
        for filename in filelist:
            if filename.endswith('.mp4'):
                f.write(f"file '{os.path.join(reversed_chunk_dir, filename)}'\n")

    # Concatenate the reversed chunks
    cmd = f"ffmpeg -f concat -i reversed_chunks.txt -c copy {full_reversed_file}"
    subprocess.run(cmd.split(' '))



def generate_random_filename(min_words=6, max_words=12):
    wordslist = get_english_words_set(['web2'])
    num_words = random.randint(min_words, max_words)
    for i in range(num_words):
        filename = "_".join(random.choice(list(wordslist)) for _ in range(num_words))
        i + 1
    return filename

def cut_string_to_82_chars(string):
    if len(string) > 82:
        return string[:82] + "..., but backwards"  # Add ellipsis to indicate truncation.
    else:
        return string + ", but backwards"

def upload_video(videolinkbro):
    print('uploading video to youtube')
    os.chdir("..")
    VIDEO_FILE = "files/" + videoname
    THUMBNAIL_FILE = "files/" + thumbnailname
    command = f'/usr/bin/python3 {scriptpath}upload_video.py --file=\'{VIDEO_FILE}\' ' +\
                    f'--thumbnail=\'{THUMBNAIL_FILE}\' ' +\
                    f'--title=\'{cut_string_to_82_chars(videotitle)}\' ' +\
                    f'--description=\'===Credits===\nChannel: {videochannel} \nVideo: {videolinkbro}\n\nThis video falls under Section 107 of the Copyright Act called fair use: https://www.youtube.com/watch?v=1PvjRIkwIl8\n\n\n\n\nWhy do I upload these videos?\nBecause I find it interesting and satisfying to watch such videos. Maybe I am not the only one\' ' +\
                    f'--keywords=\'{videotags}\' ' +\
                    f'--category=\'24\' ' +\
                    f'--privacyStatus=\'private\'' # public or private
    subprocess.run(command, shell=True)

    print('upload process end')



yes = ["JA", "J", ""]
no = ["NEIN", "N", "NEI", "NE"]

def linkListeErstellen():

    # Gibt erste Anweisungen an den Nutzer
    print("Link eingeben")


    # holt asset namen; werden in der Liste "assets" gespeichert
    a = []
    a.append(input())
    # jetzt mit loop, weil jetzt zusätzlich immer gefragt wird, ob man noch ein asset laden will
    while True:
        nocheins = input("Willst du noch ein link eingeben? Wenn nicht, dann schreib irgendwas in die Zeile \n")
        if is_youtube_watch_link(nocheins) == False:
            print('Keine Weitere Links eingegeben, Anfang mit video Runterladen')
            break
        else:
            a.append(nocheins)
    return a

def is_youtube_watch_link(url):
    """
    Returns True if the input URL is a YouTube watch link, False otherwise.
    """
    pattern = r"^https?://(?:www\.)?youtube\.com/watch\?.*v=([a-zA-Z0-9_-]+)$"
    if re.match(pattern, url):
        return True
    return False



## Anfang

#checkt, ob das api token erneuert werden muss
def save_current_date(file_path):
    """
    Save the current date to a file
    """
    current_date = datetime.date.today()
    with open(file_path, 'w') as f:
        f.write(str(current_date))

def check_date(file_path):
    """
    Check if the saved date is older than 6 days
    """

    with open(file_path, 'r') as f:
        saved_date = datetime.date.fromisoformat(f.read())
    current_date = datetime.date.today()
    if (current_date - saved_date).days > 5:
        print("Hello future!")
        print("Authentication required. Auth key is older than 5 days.")
        # holt google api authentifizierungs token
        os.remove("upload_video.py-oauth2.json")
        try:
            command = f'/usr/bin/python3 {scriptpath}get_authed.py'
            subprocess.run(command, shell=True)
            
            save_current_date(file_path)
        except:
            print("NEW AUTH FILE CREATION FAILED!")
            exit()
        


# checkt, ob die Authentifizierung deurchgefuehrt werden muss:
file_path = scriptpath + "date.txt"  # replace with your file path
if not os.path.exists(file_path):
    save_current_date(file_path)
else:
    check_date(file_path)

url = linkListeErstellen()

for items in url:
    setup() # delete old files
    videoname = generate_random_filename() + '.mp4'
    thumbnailname = generate_random_filename() + '.jpg'
    videotitle = get_video_title(items)
    videotags = get_video_tags(items)
    videochannel = get_video_channel(items)
    try:
        download_youtube_video(items) # download video    
        download_youtube_thumbnail(items, thumbnailname) # download thumbnail
    except:
        continue
    try:
        reverse_video('video.mp4', videoname)
    except:
        continue
    try:
        upload_video(items)
    except:
        continue

print('done')