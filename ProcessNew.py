from Functionalities import audio_info, fileList
import os,shutil, sqlite3
import logging

logging.basicConfig(filename='new.log', filemode='w', format='%(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def process(providers, conn, base_path):
    cur = conn.cursor()
    for provider in providers:
        folder_path = os.path.join(base_path, provider, "New")
        print(folder_path)
        files = fileList(folder_path)
        for file_path in files:
            logger.debug("="*150)
            song_info = audio_info(file_path, provider)
            logger.debug(song_info)
            if song_info is None:
                logger.debug(f'[-] ID3 not fetch, deleting file --> {os.path.basename(file_path)}')
                print(f'[-] ID3 not fetch, deleting file --> {os.path.basename(file_path)}')
                os.remove(file_path)
                continue

            query = f'''select * from all_downloads where hash = '{song_info["hash"]}' '''
            logger.debug(query)
            cur.execute(query)
            row = cur.fetchone()
            if row is not None:                   
                logger.debug(f'[-] hash match, deleting file --> {os.path.basename(file_path)}')
                print(f'[-] hash match, deleting file --> {os.path.basename(file_path)}')
                os.remove(file_path)
                continue
            else:
                query = f'''Insert Into all_downloads({",".join(song_info.keys())}) Values {tuple(song_info.values())}'''
                cur.execute(query)
                logger.debug(f'--> {query}')
                print(f'[+] adding file --> {os.path.basename(file_path)}')
        conn.commit()

        #             query = f'''select * from all_downloads where title = '{song_info["title"]}' and album = '{song_info["album"]}' and ext = '{song_info["ext"]}' '''
        #             logger.debug(query)
        #             cur.execute(query)
        #             query_res = cur.fetchall()
        #             flag = 0
        #             if len(query_res) == 0:
        #                 flag = 2
        #             for res in query_res:
        #                 logger.debug(res)
        #                 if provider == "Spotify" and res[3] == "spotify" and song_info["size"] > res[2]:
        #                     flag = 1
        #                 if provider == "Gaana" and res[3] == "gaana" and song_info["size"] > res[2]:
        #                     flag = 1
        #             if flag == 0:
        #                     logger.debug(f'[-] title/album match size small, deleting file --> {os.path.basename(file_path)}')
        #                     print(f'[-] title/album match size small, deleting file --> {os.path.basename(file_path)}')
        #                     os.remove(file_path)
        #             elif flag == 1:
        #                 logger.debug(f'[+] title/album match big size, moving file --> {os.path.basename(file_path)}')
        #                 print(f'[+] title/album match big size, moving file --> {os.path.basename(file_path)}')
        #                 shutil.move(file_path,os.path.join(base_path, provider, "Pending", os.path.basename(file_path)))
        #             elif flag == 2:
        #                 logger.debug(f'[+] title/album not match, moving file --> {os.path.basename(file_path)}')
        #                 print(f'[+] title/album not match, moving file --> {os.path.basename(file_path)}')
        #                 shutil.move(file_path,os.path.join(base_path, provider, "Pending", os.path.basename(file_path)))
                    
        #             if flag in [0,1,2]:
        #                 query = f'''Insert Into all_downloads({",".join(song_info.keys())}) Values {tuple(song_info.values())}'''
        #                 cur.execute(query)
        #                 logger.debug(f'--> {query}')
                    
        #     except sqlite3.OperationalError:
        #         logger.debug(f'[*] error, moving file --> {os.path.basename(file_path)}')
        #         print(f'[*] error, moving file --> {os.path.basename(file_path)}')
        #         shutil.move(file_path,os.path.join(base_path, provider, "Error", os.path.basename(file_path)))
        #         conn.commit()
        # conn.commit()
