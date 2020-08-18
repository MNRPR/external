import re

log_file_path = r"/var/log/system.log"
#regex = '(<property name="(.*?)">(.*?)<\/property>)'
regex = "[a-zA-Z0-9]+@[a-zA-Z]+\.(com|net)"
match_list = []
with open(log_file_path, "r") as file:
    for line in file:
        for match in re.search(regex, str):
            match_text = match.group()
            match_list.append(match_text)
            print
            match_text