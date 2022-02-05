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
    if audio.title is None:return None
    if audio.album is not None:
        info["album"] = audio.album.lower()
    if audio.title is not None:
        info["title"] = audio.title.lower()
    info["size"] = audio.filesize
    info["hash"] = hashlib.md5(open(path, 'rb').read()).hexdigest()
    info["provider"] = provider
    info["ext"] = os.path.splitext(path)[1]
    return(info)


# {"album": "Howrah Bridge", "albumartist": null, "artist": "Asha Bhosle", "audio_offset": 25323, "bitrate": 320, "channels": 2, "comment": null, "composer": null, 
# "disc": "1", "disc_total": null, "duration": 251.9728, "extra": {}, "filesize": 10104363, "genre": null, "samplerate": 48000, "title": "Aaiye Meharban", 
# "track": "2", "track_total": null, "year": null}