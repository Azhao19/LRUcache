#!/usr/bin/python3

# flags:
# -c create
# -r remove; -f force remove
# -u list of URL,cache
# -o open

import os
import sys
import argparse
from LRUCache import *

def help():
    print("create: create caches. You may supply the number of caches to create or a list of specific names. To initialize your first cache, simply run with no additional arguments.")
    print("remove: remove caches.")
    print("force_remove: continue to remove in the case of error.")
    print("add: Add files to cache. Supply files to be added as a spaced list of the form file,cache or URL,cache. In the latter case, the data of the website will be retrieved on your behalf.")
    print("open: Open files in a cache. Supply files to be opened as a spaced list of the form file,cache.")
    print("bash: Access a bash shell command.")
    print("help: Show this information again.")
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
        if (line[0] == "help"):
            help()
        if (not line[0] == "create" and len(line) == 1):
            print("Insufficient arguments provided. The following commands you may use are listed here:")
            help()
        if (line[0] == "create"):
            line[0] = "./mkdir.py"
            os.execvp("./modify_cache/mkdir.py", line)
        elif (line[0] == "remove"):
            line[0] = "false"
            line.insert(0, "./rmdir.py")
            os.execvp("./modify_cache/rmdir.py", line)
        elif (line[0] == "force_remove"):
            line[0] = "true"
            line.insert(0, "./rmdir.py")
            os.execvp("./modify_cache/mkdir.py", line)
        elif (line[0] == "add"):
            line[0] = "./addtoCache.py"
            os.execvp("./add/addtoCache.py", line)
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

    print(">>", end=' ', flush=True)
# include a while(1) loop and continually accept from stdin
# fork out child, call bash in execl
# do the below in the child bash execl program
#if (__name__ == __main__):
 #   parser = argparse.ArgumentParser()
  #  parser = argparse.ArgumentParser(description='Maintain persistent LRU cache.')
   # parser.add_argument("-c", "--create", help="Specify caches to create.", type=str)
    #parser.add_argument("-r", "--remove", help="Remove caches.", type=str)
    #parser.add_argument("-f", "--force", help="Remove by force. Must be used with the -r flag.", type=str, action="store_true")
    #parser.add_argument("-u", "--url", help="List of ordered pairs file,cache, where the file can be a URL.", type=str)
    #parser.add_argument("-o", "--open_file", help="Open a file in vim.", type=str)

#args = parser.parse_args()

#list_of_LRU_caches = {}
#create = args.create
#remove = args.remove
#force = args.force
#url = args.url
#open_file = args.open_file

#for x in sys.argv[1:]:
        
    # open routine
    # python script

    
