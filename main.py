import getopt
import pytube as yt
import os
from sys import argv


def help():
    print(f"Usage: {argv[0]}.py -l link [-p, --playlist] [-o file/folder, --output file/folder] [-a, --audio]")
    print(f"-a, --audio\tDownload only audio instead of video.")
    print(f"-h, --help\tShows this information.")
    print(f"-l, --link\tSpecifies the link of the video or playlist")
    print(f"-o, --output\tSpecifies the output folder")
    print(f"-p, --playlist\tSpecifies that the given link is a playlist (Will be detected automatically in the future)")
    exit(0)

def get_video(url, oauth):
    if oauth:
        return yt.YouTube(url, use_oauth=True, allow_oauth_cache=True)
    return yt.YouTube(url)

def playlist(link, onlyAudio, restrictions, outputFolder):
    playlist = yt.Playlist(link)
    folder = playlist.title
    urls = playlist.video_urls
    size = len(urls)
    outputFolder = os.path.realpath(outputFolder + '/' + folder)
    if not os.path.isdir(outputFolder):
        os.mkdir(outputFolder)
    for i, url in enumerate(urls,start=1):
        video = get_video(url, restrictions)
        print(f"[{i}/{size}] Downloading {video.title}.")
        downlaod(video, onlyAudio, outputFolder)

def downlaod(video, onlyAudio, outputFolder):
    try:
        if onlyAudio:
            title = video.title.replace("/","").replace("\\","").replace("\"","")
            video.streams.get_audio_only().download(outputFolder, filename=f"{title}.mp3")
            #  + ".mp3")
        else:
            video.streams.get_highest_resolution().download(outputFolder)
    except:
        print(f"Error while downloading {video.title}")
        print("Try option -r/--restrictions in order to authenticate with an account avoiding video restrictions from youtube")
        print("If -r is already in use, we may not be able to download this video.")


def optionsHandler():
    try:
        opts, args = getopt.getopt(argv[1:], "ahl:o:pr", ["audio", "help", "link=", "output=", "playlist","restrictions"])
    except getopt.getopt.GetoptError:
        help()

    link = None
    onlyAudio = playList = restrictions = False
    output = os.getcwd()

    for opt, str in opts:
        if (opt == "-a") or (opt == "--audio"):
            onlyAudio = True
        elif (opt == "-h") or (opt == "--help"):
            help()
        elif (opt == "-l") or (opt == "--link"):
            link = str
        elif (opt == "-o") or (opt == "--output"):
            output = os.path.realpath(str)
        elif (opt == "-p") or (opt == "--playlist"):
            playList = True
        elif (opt == "-r") or (opt == "--restrictions"):
            restrictions = True
        else:
            continue
    
    if link == None:
        help()

    if playList:
        if not os.path.isdir(output):
            print(f"{output} is not a directory")
            exit(-1)
        playlist(link, onlyAudio, restrictions, output)
    else:
        if not os.path.isdir(output):
            print(f"Directory not found")
            exit(-1)
        video = get_video(link, restrictions)
        print(f"Downloading {video.title}.")
        downlaod(video, onlyAudio, output)


def exec():
    optionsHandler()


exec()