import os, shutil
import eyed3, hashlib
import sqlite3

conn = sqlite3.connect("songs.db")
cur = conn.cursor()
base_path = "/media/user/data/Songs"

try:
    cur.execute('CREATE TABLE all_downloads (title text, album text, size integer, provider text, hash text PRIMARY KEY)')
except:
    pass
try:
    cur.execute('CREATE TABLE final (title text, album text, size integer, provider text, hash text PRIMARY KEY)')
except:
    pass

def audio_info(path, provider):
    info = dict()
    audio=eyed3.load(path)
    if audio is None: return None
    if audio.tag.album:
        info["album"] = audio.tag.album.lower()
    if audio.tag.title:
        info["title"] = audio.tag.title.lower()
    if os.path.exists(path):
        info["size"] = os.path.getsize(path)
        info["hash"] = hashlib.md5(open(path, 'rb').read()).hexdigest()
    info["provider"] = provider
    return(info)

spotify_path = os.path.join(base_path, "Spotify")
spotify_path_new = os.path.join(spotify_path, "New")

gaana_path = os.path.join(base_path, "Gaana")
gaana_path_new = os.path.join(gaana_path, "New")

for file in os.listdir(spotify_path_new):
    file_path = os.path.join(spotify_path_new, file)
    song_info = audio_info(file_path, "spotify")
    if song_info is None:continue
    # print(song_info)
    #check for hash
    try:
        query = f'''select * from all_downloads where hash = '{song_info["hash"]}' '''
        # print(query)
        cur.execute(query)
        row = cur.fetchone()
        if row is not None:
            os.remove(file_path)
            print(f'[-] hash match, removing file --> {os.path.basename(file_path)}')
            continue
        else:
            query = f'''Insert Into all_downloads({",".join(song_info.keys())}) Values {tuple(song_info.values())}'''
            # print(query)
            cur.execute(query)
            shutil.move(file_path,os.path.join(spotify_path, "Pending", os.path.basename(file_path)))
            print(f'[+] hash mismatch, adding file --> {os.path.basename(file_path)}')
    except sqlite3.OperationalError:
        print(f'[*] error, moving file --> {os.path.basename(file_path)}')
        shutil.move(file_path,os.path.join(spotify_path, "Error", os.path.basename(file_path)))
        conn.commit()
conn.commit()
    
    # #check for title and album
    # query = f'''select * from all_downloads where title = '{song_info["title"]}' and album = '{song_info["album"]}' '''
    # print(query)
    # cur.execute(query)
    # row = cur.fetchone()
    # if row is not None:
    #     # os.remove(file_path)
    #     print(f'[-] title/album match, removing file --> {os.path.basename(file_path)}')


#         query = f'''Insert Into songs({",".join(song_info.keys())}) Values {tuple(song_info.values())}'''
#         cur.execute(query)
#     else:
#         print(ret)
# conn.commit()

# for file in os.listdir(spotify_path_new):
#     file_path = os.path.join(spotify_path_new, file)
    # print(audio_info(file_path, "spotify"))



exit()



source_folder = r'/media/user/data/Songs/SpotifySongs/Songs'
backup_folder = r'/media/user/data/Songs/SpotifySongs/Songs_Old'
match_folder = r'/media/user/data/Songs/SpotifySongs/PendingScriptMatch'
move_folder = r'/media/user/data/Songs/SpotifySongs/SongsToBeProcessed'
source_list = os.listdir(source_folder)
backup_list = os.listdir(backup_folder)
match_list = os.listdir(match_folder)
bck_lst = []
for files in backup_list:
    backup_file_path = os.path.join(backup_folder, files)
    audio=eyed3.load(backup_file_path)
    try:
        bck_lst.append(audio.tag.title)
    except:
        pass


for files in match_list:
    match_file_path = os.path.join(match_folder, files)
    # print(match_file_path)
    audio=eyed3.load(match_file_path)
    try:
        match_title = audio.tag.title
    except:
        continue
    for songs in bck_lst:
        if songs.startswith(match_title):
            try:
                shutil.move(match_file_path, move_folder)
            except:
                os.remove(match_file_path)
            print(match_file_path)
            break




    # print("Album:",audio.tag.album)


#Match and delete from spotify and gaana songs
for songs in list(set(source_list) & set(backup_list)):
    del_path = os.path.join(backup_folder,songs)
    print(del_path)
    os.remove(del_path)