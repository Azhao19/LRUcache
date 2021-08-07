#!/usr/bin/python3

# flags:
# -c create
# -r remove; -f force remove
# -u list of URL,cache
# -o open

import os
import sys
import argparse
from LRUCache import LRU
from pathlib import Path
from urllib.parse import urlparse, urlsplit

CACHE_FILENO_CAPACITY = 10000
not_allowed = 0

list_of_LRU_caches = {}
def help():
    print("create: create caches. You may supply the number of caches to create or a list of specific names. To initialize your first cache, simply run with no additional arguments.")
    print("remove: remove caches.")
    print("force_remove: continue to remove in the case of error.")
    print("add: Add files to cache. Supply files to be added as a spaced list of the form file,cache or URL,cache. In the latter case, the data of the website will be retrieved on your behalf.")
    print("open: Open files in a cache. Supply files to be opened as a spaced list of the form file,cache.")
    print("bash: Access a bash shell command. Do not try to call scripts called by commands above will lead to undefined behavior.")
    print("help: Show this information again.")

def is_program_script(path) -> bool:
    return os.path.abspath(path) == os.path.abspath("./modify_cache/mkdir.py") or os.path.abspath(path) == os.path.abspath("./modify_cache/rmdir.py") or os.path.abspath(path) == os.path.abspath("./add/addtoCache.py") or os.path.abspath(path) == os.path.abspath("./open_files/open.py")
print(">>", end=' ', flush=True) 
for line in sys.stdin:
    line = line[:-1]
    pid = os.fork()

    if (pid < 0):
        print("Fork failed.")
        exit(1)
    elif (pid == 0):
        line = line.split(" ")
        if (line[0] == "exit"):
            print("Exiting cache manager.")
            break
        if (line[0] == "help" or line[0] == ""):
            help()
            print(">>", end=' ', flush=True)
            continue
        for li in line:
            not_allowed = 0
            if (os.path.exists(li) and is_program_script(li)):
                print(">>", end=' ', flush=True)
                not_allowed = 1
                continue
        if (not_allowed == 1):
            not_allowed = 0
            continue
        if (not line[0] == "create" and len(line) == 1):
            print("Insufficient arguments provided. The following commands you may use are listed here:")
            help()
        if (line[0] == "create"):
            line[0] = "./mkdir.py"
            os.execvp("./modify_cache/mkdir.py", line)
        elif (line[0] == "remove"):
            line[0] = "false"
            line.insert(0, "./rmdir.py")
            os.execvp("./modify_cache/rmdir.py", line) #it should be the job of rmdir.py to process the file correctly?
        elif (line[0] == "force_remove"):
            line[0] = "true"
            line.insert(0, "./rmdir.py")
            os.execvp("./modify_cache/mkdir.py", line)
        elif (line[0] == "add"):
            for x in line[1:]:
                pid_add = os.fork()
                if (pid_add < 0):
                    print("Fork failed.")
                    exit(1)
                elif (pid_add == 0):
                    os.execlp("./add/addtoCache.py", "./addtoCache.py", x)
                else:
                    os.waitpid(pid_add, 0)
            print("exiting", flush=True)
            exit(0)
        elif (line[0] == "open"):
            line[0] = "./open.py"
            os.execvp("./open_files/open.py", line)
        elif (line[0] == "bash"):
            line[0] = line[1]
            os.execvp(line[0], line[1:])
        else:
            print("Invalid option. The following commands you may use are listed here:")
            help()
    else:
        os.waitpid(pid, 0)
        line = line.split(" ")
        if (line[0] == "open" and len(line) >= 2):
            # If len is 1 or 0 we know that child didn't do anything to caches
            # Furthermore, if the input wasn't valid, open.py took care of that
            for li in line[1:]:
                li = li.split(",")
                
                if li[1] not in list_of_LRU_caches:
                    g = open("./cache/%s/.size" % li[1], "r")
                    gl = g.readlines()
                    g.close()
                    list_of_LRU_caches[li[1]] = LRU.LRUCache(int(gl[0]))
                    
                    new = list_of_LRU_caches[li[1]]
                    f = open("./cache/%s/.files" % li[1], "r")
                    for line in f:
                        new.append_new_node(LRU.LinkedNode(li[1], li[1]))
                    f.close()
                    # At this point, constructed the LRU cache list
                cache = list_of_LRU_caches[li[1]]
                temp = cache.get(li[0])
                f = open("./cache/%s/.files" % li[1], "r")
                lines = f.readlines()
                f = open("./cache/%s/.files" % li[1], "w")
                for line in lines:
                    if (not line.strip("\n") == li[0]):
                        f.write(line)
                f.write(li[0])
                f.close()
            print(">>", end=' ', flush=True)
        elif (line[0] == "remove" or line[0] == "force_remove" and len(line) >= 2):
            for li in line[1:]:
                if li[1] in list_of_LRU_caches:
                    del list_of_LRU_caches[li[1]]
                else:
                    if (line[0] == "force_remove"):
                        break
                    continue
            print(">>", end=' ', flush=True)
        elif (line[0] == "add" and len(line) >= 2):
            # remove files from the cache
            for li in line[1:]:
                li = li.split(",")

                if li[1] not in list_of_LRU_caches:
                    g = open("./cache/%s/.size" % li[1], "r")
                    gl = g.readlines()
                    g.close()
                    list_of_LRU_caches[li[1]] = LRU.LRUCache(int(gl[0]))

                    new = list_of_LRU_caches[li[1]]
                    f = open("./cache/%s/.files" % li[1], "r")
                    for line in f:
                        new.append_new_node(LRU.LinkedNode(line, line))
                    f.close()
                else:
                    f = open("./cache/%s/.files" % li[1], "r")
                    target = f.readline()
                    f.close()
                    access = list_of_LRU_caches[li[1]]
                    split = urlsplit(li[0])
                    basename = os.path.basename(split.path)
                    access.append_new_node(LRU.LinkedNode(basename, basename))
                    while (access.head is not None and access.head.val != target):
                        access.remove_head_node()
                        access.head = access.head.next
            print(">>", end=' ', flush=True)
        else:
            print(">>", end=' ', flush=True)
        # Note: modifying the .files file after adding is done by addtoCache.py
