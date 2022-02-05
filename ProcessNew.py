from Functionalities import audio_info
import os,shutil, sqlite3


def process(providers, conn, base_path):
    cur = conn.cursor()
    for provider in providers:
        folder_path = os.path.join(base_path, provider, "New")
        print(folder_path)
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            # print("-"*100)
            # print(file_path)
            song_info = audio_info(file_path, provider)
            # print(song_info)
            if song_info is None:
                print(f'[-] ID3 not fetch, deleting file --> {os.path.basename(file_path)}')
                os.remove(file_path)
                continue
            
        #     #check for hash
            try:
                query = f'''select * from all_downloads where hash = '{song_info["hash"]}' '''
                # print(query)
                cur.execute(query)
                row = cur.fetchone()
                if row is not None:                   
                    # print(f'[-] hash match, deleting file --> {os.path.basename(file_path)}')
                     # os.remove(file_path)
                    continue
                else:
                    query = f'''select * from all_downloads where title = '{song_info["title"]}' and album = '{song_info["album"]}' and ext = '{song_info["ext"]}' '''
                    # print(query)
                    cur.execute(query)
                    query_res = cur.fetchall()


                    if len(query_res) > 1:
                        print("="*100)
                        print(query)
                        print(song_info)
                        flag = 0
                        for res in query_res:
                            print(res)
                            if provider == "Spotify" and res[3] == "spotify" and song_info["size"] > res[2]:
                                flag = 1
                            if provider == "Gaana" and res[3] == "gaana" and song_info["size"] > res[2]:
                                flag = 1
                        if flag == 0:
                                print(f'[-] title/album match size small, deleting file --> {os.path.basename(file_path)}')
                                query = f'''Insert Into all_downloads({",".join(song_info.keys())}) Values {tuple(song_info.values())}'''
                                print(query)
                                cur.execute(query)
                        else:
                            print(f'[+] title/album match big size, adding file --> {os.path.basename(file_path)}')
                            query = f'''Insert Into all_downloads({",".join(song_info.keys())}) Values {tuple(song_info.values())}'''
                            print(query)
                            cur.execute(query)
                            shutil.move(file_path,os.path.join(base_path, provider, "Pending", os.path.basename(file_path)))

                        # exit()
                    # if len(query_res) != 0: 
                        
                    #     print(f'[-] title/album match, deleting file --> {os.path.basename(file_path)}')
                    #     print("+"*10)
                    #     print(song_info)
                    #     print(query_res)
                    #     print(provider)
                         # os.remove(file_path)

            except sqlite3.OperationalError:
                pass
                print(f'[*] error, moving file --> {os.path.basename(file_path)}')
                # shutil.move(file_path,os.path.join(base_path, provider, "Error", os.path.basename(file_path)))
                # conn.commit()
        # conn.commit()




        #             shutil.move(file_path,os.path.join(base_path, provider, "Pending", os.path.basename(file_path)))
        #             print(f'[+] hash mismatch, adding file --> {os.path.basename(file_path)}')