import re

log_file = r"/var/log/system.log"
pattern = "[a-zA-Z0-9]+@[a-zA-Z]+\.(com|local)"
read_line = True

with open(log_file, "r") as file:
    match_list = []
    if read_line == True:
        for line in file:
            for match in re.finditer(pattern, line, re.S):
                match_text = match.group()
                match_list.append(match_text)
                print match_text
    else:
        data = f.read()
        for match in re.finditer(pattern, data, re.S):
            match_text = match.group()
            match_list.append(match_text)
file.close()