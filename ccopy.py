import shutil
for line in open("GaanaExtractor.log",'r').readlines():
    if "File Data Not Found" in line:
        files = line.replace("File Data Not Found ::","").strip().split(";")
for file in files:
    try:shutil.copy2("//media//user//data//vm_share/music//10) gaana extractor//raw_songs//"+str(file), "//media//user//data//vm_share//music//10) gaana extractor//not_converted//")    
    except:print "File Not Found: " + file
