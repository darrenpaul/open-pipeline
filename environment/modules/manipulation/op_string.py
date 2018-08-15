import re
import os

def resolve_string(data, string, pattern=r"({\w+})"):
    regex = re.findall(pattern, string)
    for key in regex:
        resolvedkey = key.replace("{", "").replace("}", "")
        if resolvedkey in data.keys():
            resolvedkey = str(data[resolvedkey])
            string = string.replace(key, resolvedkey)
    return string.replace(os.sep, "/")