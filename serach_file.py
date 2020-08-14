import os
import os.path

file_name = "test.txt" #file to be searched
cur_dir = os.getcwd() # Dir from where search starts can be replaced with any path

while True:
    file_list = os.listdir(cur_dir)
    parent_dir = os.path.dirname(cur_dir)
    if file_name in file_list:
        print "File Exists in: ", cur_dir
        break
    else:
        if cur_dir == parent_dir: #if dir is root dir
            print "File not found"
            break
        else:
            cur_dir = parent_dir