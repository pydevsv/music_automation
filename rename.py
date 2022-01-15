import os
for file in os.listdir("."):
    filename, ext = os.path.splitext(file)
    if ext !="" and filename.isdigit():
        os.rename(file,filename)