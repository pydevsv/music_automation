import os
import glob
import shutil

mp3_folder = '//media//user//data//vm_share//music//6) mp3_final//'
m4a_folder = "//media//user//data//vm_share//music//2) m4a_checked//rename_complete//"
m4a_final = "//media//user//data//vm_share//music//3) m4a_final//"
mp3_final = "//media//user//data//vm_share//music//7) final//mp3//"

mp3_list = []
for file in glob.glob(mp3_folder + "*.mp3"):
    file_name = os.path.splitext(os.path.split(file)[1])[0]
    mp3_list.append([file, file_name, file_name[:file_name.find("(")].strip()])

m4a_list = []
for file in glob.glob(m4a_final + "*.m4a"):
    file_name = os.path.splitext(os.path.split(file)[1])[0]
    m4a_list.append([file, file_name, file_name[:file_name.find("(")].strip()])

for m4a_file in m4a_list:
    for mp3_file in mp3_list:
        if m4a_file[1] == mp3_file[1]:
            print m4a_file[0], mp3_file[0]
            # shutil.move(m4a_file[0], m4a_final)
            # shutil.move(mp3_file[0], mp3_final)
        elif m4a_file[2] == mp3_file[2]:
            print m4a_file[0], mp3_file[0]
        #     shutil.move(m4a_file[0], m4a_final)
        #     shutil.move(mp3_file[0], mp3_final)