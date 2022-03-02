import os,shutil

counter = 1
loop = 1
folder_path = "C:\\Users\\main\\Documents\\Songs\\Gaana\\Pending"
for file in os.listdir(folder_path):
    if loop % 100 == 0:
        counter = counter+1
    print(f'{loop} --> {str(counter).zfill(2)}')
    loop +=1
    if not os.path.exists(os.path.join(folder_path,  str(counter).zfill(2))):
        os.mkdir(os.path.join(folder_path,  str(counter).zfill(2)))
    shutil.move(os.path.join(folder_path,file), os.path.join(folder_path,str(counter).zfill(2)))
