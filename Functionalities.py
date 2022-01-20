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
    audio = TinyTag.get(path)
    # print(audio)
    if audio.title is None:return None
    if audio.album is not None:
        info["album"] = audio.album.lower()
    if audio.title is not None:
        info["title"] = audio.title.lower()
    info["size"] = audio.filesize
    info["hash"] = hashlib.md5(open(path, 'rb').read()).hexdigest()
    info["provider"] = provider
    return(info)


# {"album": null, "albumartist": null, "artist": null, "audio_offset": null, "bitrate": null, "channels": null, "comment": null, "composer": null, "disc": null, "disc_total": null, "duration": null, "extra": {}, "filesize": 0, "genre": null, "samplerate": null, "title": null, "track": null, "track_total": null, "year": null}