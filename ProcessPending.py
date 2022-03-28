from Functionalities import audio_info, fileList
import os,shutil, sqlite3

def process(providers, conn, base_path):
    cur = conn.cursor()
    for provider in providers:
        folder_path = os.path.join(base_path, provider, "Pending")
        print(folder_path)
        files = fileList(folder_path)
        for file in files:
            file_path = os.path.join(folder_path, file)
            song_info = audio_info(file_path, provider)
            song_info["title"] = song_info["title"].replace("'", "''")
            song_info["album"] = song_info["album"].replace("'", "''")
            query = f'''select * from final where title = '{song_info["title"]}' and album = '{song_info["album"]}' and ext = '{song_info["ext"]}' '''
            cur.execute(query)
            query_res = cur.fetchone()
            # print("-"*100)
            # print(query_res)
            # print(song_info)
            if query_res is None:
                 print(f'[+] title/album not match --> {os.path.basename(file_path)}')
            elif song_info["size"] < query_res[2]:
                print(f'[-] title/album match size small, deleting file --> {os.path.basename(file_path)}')
                os.remove(file_path)