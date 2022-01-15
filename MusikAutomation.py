import os, shutil
import eyed3
# import tinytag

# pending_folder = r'/media/user28/disk/Songs/SpotifySongs/Pending'

# for file in os.listdir(pending_folder):
#     dct = {}
#     file_path = os.path.join(pending_folder, file)
#     print(file_path)

#     dct["gaana_id"] = os.path.splitext(file)[0]
#     dct["size"] = os.stat(file_path).st_size
#     dct["md5"] = hashlib.md5(open(file_path).read()).hexdigest()
#     md5_and_id(file_path, dct)
#     if os.path.exists(file_path):
#         try:
#             tag = TinyTag.get(file_path)
#             if tag.title is not None:
#                 dct["title"] = tag.title.lower()
#             else:
#                 dct["title"] = tag.title
#             if tag.album is not None:
#                 dct["album"] = tag.album.lower()
#             else:
#                 dct["album"] = tag.album

#             for k in dct.keys():
#                 dct[k] = str(dct[k])
#             print "[+] TinyTag File Read"
#             title_album(file_path, dct)
#         except:
#             print "[-] File Read Error"
#     if os.path.exists(file_path):
#         print "[+] File Move To Final"
#         shutil.move(file_path, os.path.join(folder, "final"))
# conn.commit()










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