import os
import shutil

temp_folder = ['Z:\\share\\music\\to check\\gaana.com\\comp']
final_folder = "Z:\\share\\music\\final\\my songs"

final_list = list()
final_fname_list = list()
dct = dict()
for root, dir, files in os.walk(final_folder):
    for file in files:
        if not file == "Thumbs.db":
            final_list.append([root, file, os.path.splitext(file)[0], file[:file.find('(')].strip()])
test = "on"

for dir in temp_folder:
    for root, dir, files in os.walk(dir):
        for file in files:
            for i in range(0, len(final_list)):
                temp_path = os.path.join(root, file)
                final_path = os.path.join(final_list[i][0], final_list[i][1])
                if file == final_list[i][1]:  # ----------------------exact match----------------------
                    temp_size = os.path.getsize(temp_path)
                    final_size = os.path.getsize(final_path)
                    if file[:file.find('(')].strip() == final_list[i][3]:
                        print file
                    if temp_size > final_size:
                        print " ".join(
                            ["[move]", temp_path, "(", str(temp_size), ")", "-->", final_path, "(", str(final_size),
                             ")"])
                        if test == "shut-off":
                            shutil.move(temp_path, final_path)
                    else:
                        if test == "off":
                            os.remove(temp_path)
                        print "[deleting] :", temp_path

                # if os.path.splitext(file)[0] == final_list[i][2]:
                #     os.remove(temp_path)
                #     print "[-] deleting:", temp_path
exit()

# for files in common_list:
#     temp_size = os.path.getsize(temp_folder+os.sep+files)
#     final_size = os.path.getsize(final_folder+os.sep+files)
#     print temp_size,final_size
#     if temp_size > final_size:
#         shutil.copy2(temp_folder+os.sep+files,final_folder+os.sep+files)
#         print "move temp to final"
#         print temp_folder+os.sep+files
#         os.remove(temp_folder + os.sep + files)
#     else:
#         os.remove(temp_folder+os.sep+files)
#         print "delete temp file"


temp_list = os.listdir(temp_folder)
final_list = os.listdir(final_folder)
# --------------size base deletion---------------
# common_list = list(set(temp_list).intersection(final_list))
# for files in common_list:
#     temp_size = os.path.getsize(temp_folder+os.sep+files)
#     final_size = os.path.getsize(final_folder+os.sep+files)
#     print temp_size,final_size
#     if temp_size > final_size:
#         shutil.copy2(temp_folder+os.sep+files,final_folder+os.sep+files)
#         print "move temp to final"
#         print temp_folder+os.sep+files
#         os.remove(temp_folder + os.sep + files)
#     else:
#         os.remove(temp_folder+os.sep+files)
#         print "delete temp file"

# --------------file name only base deletion---------------
flname_temp_list = list()
flname_final_list = list()
for file in temp_list:
    print os.path.splitext(file)[0]
    flname_temp_list.append(os.path.splitext(file)[0])
for file in final_list:
    flname_final_list.append(os.path.splitext(file)[0])
print flname_temp_list
print flname_final_list

common_list = list(set(flname_temp_list).intersection(flname_final_list))
print common_list

for file in common_list:
    try:
        shutil.move(temp_folder + os.sep + file + ".m4a", final_folder)
    except:
        pass
#     try:os.remove(temp_folder + os.sep + file+".m4a")
#     except:pass
#     try:os.remove(temp_folder + os.sep + file+".mp3")
#     except:pass
#     print temp_folder + os.sep + file + ".m4a"
