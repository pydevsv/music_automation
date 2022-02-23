from Functionalities import audio_info, fileList
import os, shutil
import hashlib


def processFinal(conn, base_path):
    folder_path = os.path.join(base_path, "Final", "Songs")
    files = fileList(folder_path)
    for file_path in files:
        song_info = audio_info(file_path, None)
        if song_info is None:continue
        print(song_info)
        if song_info["provider"] == "Spotify":
            shutil.move(file_path,os.path.join(base_path, "Final", "Songs", "Spotify", os.path.basename(file_path)))




def processRaw(conn, base_path):
    cur = conn.cursor()
    folder_path = os.path.join(base_path, "Gaana", "RawFiles")
    files = fileList(folder_path)
    for file_path in files:
        info = dict()
        info["gaana_id"] = os.path.basename(file_path)
        info["size"] = os.path.getsize(file_path)
        info["hash"] = hashlib.md5(open(file_path, 'rb').read()).hexdigest()
        info["provider"] = "Gaana"
        query = f'''select * from gaana_raw where hash = '{info["hash"]}' '''

        cur.execute(query)
        row = cur.fetchone()
        if row is not None:                   
            print(f'[-] hash match, deleting file --> {os.path.basename(file_path)}')
            os.remove(file_path)
        else:
            query = f'''Insert Into gaana_raw({",".join(info.keys())}) Values {tuple(info.values())}'''
            cur.execute(query)
            print(f'[+] adding file --> {os.path.basename(file_path)}')
    conn.commit()        
