import os
import os.path

file_name = "manju.doc" #The file which need to be searched
cur_dir = os.getcwd() # The search will start from this directory

while True:
    file_list = os.listdir(cur_dir)
    parent_dir = os.path.dirname(cur_dir)
    if file_name in file_list:
        print "Wow ! the file found in: ", cur_dir
        break
    else:
        if cur_dir == parent_dir: #if dir is root dir
            print "Sorry the file not found"
            break
        else:
            cur_dir = parent_dir