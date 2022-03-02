import eyed3, hashlib, os
from tinytag import TinyTag

# def audio_info(path, provider):
#     info = dict()
#     audio=eyed3.load(path)
#     if audio is None: return None
#     if audio.tag.album:
#         info["album"] = audio.tag.album.lower()
#     if audio.tag.title:
#         info["title"] = audio.tag.title.lower()
#     if os.path.exists(path):
#         info["size"] = os.path.getsize(path)
#         info["hash"] = hashlib.md5(open(path, 'rb').read()).hexdigest()
#     info["provider"] = provider
#     return(info)

def audio_info(path, provider):
    info = dict()
    try:audio = TinyTag.get(path)
    except:return None
    # print(audio)
    if audio.title is None:return None
    if audio.album is not None:
        info["album"] = audio.album
    if audio.title is not None:
        info["title"] = audio.title
    info["size"] = audio.filesize
    info["hash"] = hashlib.md5(open(path, 'rb').read()).hexdigest()
    
    info["ext"] = os.path.splitext(path)[1]
    if info["ext"] == ".flac":
        info["provider"] = "None"
    elif provider is None:
        info["provider"] = audio.comment
    else:
        info["provider"] = provider
    if provider == "Gaana" or info["provider"] == "Gaana":
        info["priority"] = 2
    elif provider == "Spotify" or info["provider"] == "Spotify":
        info["priority"] = 2 
    return(info)

def fileList(source):
    files = []
    for root, dirnames, filenames in os.walk(source):
        for filename in filenames:
            files.append(os.path.join(root, filename))
    return files


# {"album": "Howrah Bridge", "albumartist": null, "artist": "Asha Bhosle", "audio_offset": 25323, "bitrate": 320, "channels": 2, "comment": null, "composer": null, 
# "disc": "1", "disc_total": null, "duration": 251.9728, "extra": {}, "filesize": 10104363, "genre": null, "samplerate": 48000, "title": "Aaiye Meharban", 
# "track": "2", "track_total": null, "year": null}