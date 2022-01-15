import sqlite3
import os
from tinytag import TinyTag
import sys
import hashlib
import shutil

reload(sys)
sys.setdefaultencoding("utf-8")

conn = sqlite3.connect("ganna_db.db")
c = conn.cursor()

try:
    c.execute('''CREATE TABLE gaana_table (gaana_id PRIMARY KEY, title, album, size, md5)''')
except:
    pass

folder = "//media//user//data//vm_share//music//1) m4a_downloaded//"
table = "gaana_table"


def md5_and_id(file_path, dct):
    print "dict ->", dct
    c.execute("select * from gaana_table where md5 = '%s'" % (dct["md5"]))
    ret = c.fetchone()
    print "md5 ->", ret
    if ret is not None:
        c.execute("select * from gaana_table where gaana_id = '%s'" % (dct["gaana_id"]))
        ret = c.fetchone()
        print "id ->", ret
        if ret is not None:
            print "[-] Deleting: ", file_path, "(md5 and id same)"
            os.remove(file_path)
        else:
            print "[+] DB Inserting"
            c.execute("Insert Into %s(%s) Values %s" % (table, ",".join(dct.keys()), tuple(dct.values())))
            conn.commit()
            print "[-] Deleting: ", file_path, "(md5 same id different)"
            os.remove(file_path)
    else:
        c.execute("select * from gaana_table where gaana_id = '%s'" % (dct["gaana_id"]))
        ret = c.fetchone()
        print "id ->", ret
        if ret is None:
            print "[+] DB Inserting", "(neither md5 nor id found)"
            c.execute("Insert Into %s(%s) Values %s" % (table, ",".join(dct.keys()), tuple(dct.values())))
            conn.commit()
        else:
            db_row = [str(item) for item in ret]
            if int(dct["size"]) > int(db_row[3]):
                print "[+] DB Updating", "(update size in DB)"
                c.execute("update gaana_table set size = %s where gaana_id = '%s'" % (dct["size"], dct["gaana_id"]))
                conn.commit()
            else:
                print "[-] Deleting: ", file_path, "(less size, deleting file)"
                os.remove(file_path)


def title_album(file_path, dct):
    print "dict-> ", dct
    if dct["album"] is None: return
    try:
        c.execute("select * from gaana_table where title = '%s'" % (dct["title"]))
    except:
        return
    ret = c.fetchone()
    print "title ->", ret
    if ret is not None:
        common = list(set(dct["album"].split()).intersection(set(ret[2].split())))
        print common, len(common)
        if len(common) > 0 and dct["size"] <= ret[3]:
            print "Removing --> ", file_path
            os.remove(file_path)


for file in os.listdir(folder):
    if file == "final":
        continue
    print "*" * 150
    dct = {}
    file_path = os.path.join(folder, file)

    dct["gaana_id"] = os.path.splitext(file)[0]
    dct["size"] = os.stat(file_path).st_size
    dct["md5"] = hashlib.md5(open(file_path).read()).hexdigest()
    md5_and_id(file_path, dct)
    if os.path.exists(file_path):
        try:
            tag = TinyTag.get(file_path)
            if tag.title is not None:
                dct["title"] = tag.title.lower()
            else:
                dct["title"] = tag.title
            if tag.album is not None:
                dct["album"] = tag.album.lower()
            else:
                dct["album"] = tag.album

            for k in dct.keys():
                dct[k] = str(dct[k])
            print "[+] TinyTag File Read"
            title_album(file_path, dct)
        except:
            print "[-] File Read Error"
    if os.path.exists(file_path):
        print "[+] File Move To Final"
        shutil.move(file_path, os.path.join(folder, "final"))
conn.commit()
