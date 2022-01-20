from Functionalities import audio_info
import os,shutil, sqlite3


def process(providers, conn, base_path):
    cur = conn.cursor()
    for provider in providers:
        folder_path = os.path.join(base_path, provider, "New")
        print(folder_path)
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            song_info = audio_info(file_path, provider)
            # print(song_info)
            if song_info is None:
                print(f'[-] ID3 not fetch, deleting file --> {os.path.basename(file_path)}')
                os.remove(file_path)
                continue
            
            #check for hash
            try:
                query = f'''select * from all_downloads where hash = '{song_info["hash"]}' '''
                # print(query)
                cur.execute(query)
                row = cur.fetchone()
                if row is not None:
                    os.remove(file_path)
                    print(f'[-] hash match, deleting file --> {os.path.basename(file_path)}')
                    continue
                else:
                    query = f'''Insert Into all_downloads({",".join(song_info.keys())}) Values {tuple(song_info.values())}'''
                    # print(query)
                    cur.execute(query)
                    shutil.move(file_path,os.path.join(base_path, provider, "Pending", os.path.basename(file_path)))
                    print(f'[+] hash mismatch, adding file --> {os.path.basename(file_path)}')
            except sqlite3.OperationalError:
                print(f'[*] error, moving file --> {os.path.basename(file_path)}')
                shutil.move(file_path,os.path.join(base_path, provider, "Error", os.path.basename(file_path)))
                conn.commit()
        conn.commit()