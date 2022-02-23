import os, shutil
from Functionalities import audio_info, fileList
from tinytag import TinyTag
from mp3_tagger import MP3File,VERSION_2
import logging

logging.basicConfig(filename='final.log', filemode='w', format='%(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


pattern = (('(Original Motion Picture Soundtrack)', ''), ('(Original Soundtrack)', ''), ('(Original Soundtrack)', ''), ('- EP', ''), ('[Dialogues Version]', '')
, (', Pt. 2', ''), (', Pt. 1', ''), ('(Original Motion Pictures Soundtrack)', ''), ('((Original Motion Picture Soundtrack ))', ''))
 

def processFinal(providers, conn, base_path):
    cur = conn.cursor()
    for provider in providers:
        folder_path = os.path.join(base_path, provider, "MP3Tag")
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
                
            query = f'''select * from final where hash = '{song_info["hash"]}' '''
            logger.debug(query)
            cur.execute(query)
            row = cur.fetchone()
            if row is not None:                   
                logger.debug(f'[-] hash match, deleting file --> {os.path.basename(file_path)}')
                print(f'[-] hash match, deleting file --> {os.path.basename(file_path)}')
                os.remove(file_path)
                continue
            else:
                try:
                    query = f'''select * from final where title = '{song_info["title"]}' and album = '{song_info["album"]}' and ext = '{song_info["ext"]}' '''
                
                    logger.debug(query)
                    cur.execute(query)
                except:
                    continue
                query_res = cur.fetchall()
                flag = 0
                if len(query_res) == 0:
                    print(f'[+] title/album not match --> {os.path.basename(file_path)}')
                else:
                    print(f'[-] title/album match , deleting file --> {os.path.basename(file_path)}')
                    os.remove(file_path)
                



def process_tags(providers, conn, base_path):
    cur = conn.cursor()
    for provider in providers:
        folder_path = os.path.join(base_path, provider, "MP3Tag")
        files = fileList(folder_path)
        for file_path in files:
            print(f'Processing --> {file_path}')
            # print("="*150)
            try:song_info = MP3File(file_path)
            except:continue
            song_info.set_version(VERSION_2)
            tags = song_info.get_tags()
            # print(tags)
            
            album = song_info.album
            if "- Single" in album:
                album = "Single"
            else:
                for r in pattern:
                    album = album.replace(*r)
            album = album.strip()
            # print(f'{song_info.album} --> {album}')
            song_info.comment = provider
            song_info.album = album
            song_info.save()
    # processFinal(providers, conn, base_path)


    

