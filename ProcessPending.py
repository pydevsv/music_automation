from Functionalities import audio_info
import os,shutil, sqlite3

def process(providers, conn, base_path):
    cur = conn.cursor()
    for provider in providers:
        folder_path = os.path.join(base_path, provider, "Pending")
        print(folder_path)
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            song_info = audio_info(file_path, provider)
            query = f'''select * from all_downloads where title = '{song_info["title"]}' and album = '{song_info["album"]}' '''
            print("*"*100)
            print(query)
            cur.execute(query)
            row = cur.fetchone()
            print(row)
            print(song_info)

            if row is None:
                # print("[+] not match")
                pass
            else:

                print("[-] file match")