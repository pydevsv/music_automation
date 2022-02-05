import os, shutil
import hashlib
import sqlite3
import ProcessNew, ProcessPending
import Functionalities


conn = sqlite3.connect("songs.db")
cur = conn.cursor()

base_path = "/media/user/data/Songs"

spotify_path = os.path.join(base_path, "Spotify")
spotify_path_new = os.path.join(spotify_path, "New")
spotify_path_final = os.path.join(spotify_path, "Final")

gaana_path = os.path.join(base_path, "Gaana")
gaana_path_new = os.path.join(gaana_path, "New")
gaana_path_final = os.path.join(gaana_path, "Final")

final_path = os.path.join(base_path, "Final", "Songs")

try:
    cur.execute('CREATE TABLE all_downloads (title text, album text, size integer, provider text, hash text PRIMARY KEY)')
except:
    pass
try:
    cur.execute('CREATE TABLE final (title text, album text, size integer, provider text, ext text, hash text PRIMARY KEY)')
except:
    pass

providers = ["Spotify", "Gaana"]
ProcessNew.process(providers, conn, base_path)
ProcessPending.process(providers, conn, base_path)



exit()



# Process gaana final
for file in os.listdir(gaana_path_final):
    file_path = os.path.join(gaana_path_final, file)
    song_info = audio_info(file_path, "gaana")
    if song_info is None:continue
    song_info["ext"] = os.path.splitext(file_path)[1]
    # print(song_info)
    query = f'''select * from final where title = "{song_info["title"]}" and album = "{song_info["album"]}" '''
    cur.execute(query)
    row = cur.fetchone()
    if row is not None:
        print(row)
        print(song_info)

        if row[3] == "spotify":
            # os.remove(file_path)
            print(f'[-] title/album match spotify, deleting file --> {os.path.basename(file_path)}')
        elif row[3] == "gaana" and row[2] > song_info["size"]:
            # os.remove(file_path)
            print(f'[-] title/album/gaana match and small size, deleting file --> {os.path.basename(file_path)}')
        else:
            print(f'[+] title/album/gaana match and big size, moving file --> {os.path.basename(file_path)}')
            # shutil.move(file_path, os.path.join(final_path, file))
            # query = f'''UPDATE final SET size = {song_info["size"]} WHERE hash = "{song_info["hash"]}" ''' 
            # cur.execute(query)
            # conn.commit()
    else:
        print(f'[+] title/album/gaana mismatch , moving file --> {os.path.basename(file_path)}')
        # shutil.move(file_path, os.path.join(final_path, file))
        # query = f'''Insert Into final({",".join(song_info.keys())}) Values {tuple(song_info.values())}'''
        # cur.execute(query)
        # conn.commit()


    
    # #check for title and album
    # query = f'''select * from all_downloads where title = '{song_info["title"]}' and album = '{song_info["album"]}' '''
    # print(query)
    # cur.execute(query)
    # row = cur.fetchone()
    # if row is not None:
    #     # os.remove(file_path)
    #     print(f'[-] title/album match, deleting file --> {os.path.basename(file_path)}')


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


#Match and deleting from spotify and gaana songs
for songs in list(set(source_list) & set(backup_list)):
    del_path = os.path.join(backup_folder,songs)
    print(del_path)
    os.remove(del_path)






# add new songs in final
# for file in os.listdir(spotify_path_final):
#     file_path = os.path.join(spotify_path_final, file)
#     song_info = Functionalities.audio_info(file_path, "gaana")
    
#     if song_info is None:continue
#     song_info["ext"] = os.path.splitext(file_path)[1]
#     # print(song_info)
#     query = f'''Insert Into final({",".join(song_info.keys())}) Values {tuple(song_info.values())}'''
#     print(query)
#     cur.execute(query)
#     os.remove(file_path)
#     conn.commit()