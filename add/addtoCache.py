#!/usr/bin/python3

# Assume that LRU cache data has been read into memory
# Assume that all necessary files have been deleted to make space for this file
# As maintained by the main program.

import sys
import os
from pathlib import Path
import glob
from urllib.parse import urlparse, urlsplit
import re

regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

# Input takes the form of a list URL,cache

for x in sys.argv[1:]:
    x = x.split(",")
    if (not len(x) == 2):
        print("Input must take the form u_k,c_k (URL,cache).")
        exit(1)
    else:
        if (not os.path.exists(os.path.join(Path("./cache"),x[1]))):
            print("Invalid cache.")
            exit(1)
        if (re.match(regex, x[0]) is None):
            print("Invalid URL.")
            exit(1)

        split = urlsplit(x[0])
        
        p = os.path.join("./cache/%s" % x[1], os.path.basename(split.path))
        pid = os.fork()
        if (pid < 0):
            print("Fork failed.")
            exit(1)
        elif (pid == 0):  # child
            os.execlp("./add/wget", "./wget", split.netloc, "80", split.path)
        else:
            os.waitpid(pid, 0)
            os.rename(os.path.basename(split.path), p)
            p = Path("./cache/%s" % x[1])
            p_size = os.path.join(p, ".size")
            p_files = os.path.join(p, ".files")
            
            p = os.path.join("./cache/%s" % x[1], os.path.basename(split.path))
            f = open(p_size, "r")
            lines = f.readlines()

            sizetoAdd = round(os.stat(p).st_size / (1024 * 1024), 8)
            if (sizetoAdd > float(lines[0])):
                print("File is too large.")
                execlp("rm", "rm", "-r", os.path.basename(split.path))

            y = float(lines[1]) + sizetoAdd
            g = open(p_files, "r")
            files = g.readlines()
            while (y > float(lines[0])):
                remove = files.pop(0).strip("\n")
                size = round(os.stat(Path("./cache/%s/%s" % (x[1], remove))).st_size / (1024 * 1024), 8)
                rm = os.fork()
                if (rm < 0):
                    print("Fork failed.")
                    exit(1)
                elif (rm == 0):
                    os.execlp("rm", "rm", "-r", os.path.join("./cache/%s" % x[1], remove))
                else:
                    os.waitpid(rm, 0)
                    y -= size
            g = open(p_files, "w")
            for d in files:
                g.write(d)
            g.close()

            lines[1] = str(y)
            f = open(p_size, "w")
            f.writelines(lines)
            f.close()

            # maintain list of files in LRU order
            # most recent is at the bottom of the file
            g = open(p_files, "a")
            g.write(os.path.basename(split.path))
            g.write("\n")
            g.close()
