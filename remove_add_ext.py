import os

folder = "//media//user//data//vm_share//music//1) m4a_downloaded//"

# for files in os.listdir(folder):
#     file, ext = os.path.splitext(files)
#     if ext != "":
#         print file, ext
#         os.rename(folder+files,folder+file)

for files in os.listdir(folder):
    print files
    os.rename(folder+files, folder+files+".m4a")
