#!/usr/bin/python3
import os                    # create directory
from pathlib import Path     # find parent directory
import sys                   # access argv
import glob

# input can be:
# empty
# number of caches to create
# list of cache names

if (not glob.glob(os.path.join(Path("."), "cache"))):
    os.mkdir("cache")
cache = Path("./cache")
# Case 1: empty
if (len(sys.argv) == 1 and not glob.glob(os.path.join(cache, "*"))):
    print("No cache folder detected. Creating one now.") 
    path = os.path.join(cache, "cache")  
    os.mkdir(os.path.join(cache, "cache"))

# Case 2: just a number
elif (len(sys.argv) == 2):
    if (not sys.argv[1].isdigit()):
        print("Must provide number of caches to create.")
        sys.exit(1);
    i = int(sys.argv[1])
    j = 0
    if (os.path.exists(os.path.join(cache, "cache"))):
        os.rename("cache/cache", "cache/cache_0")
        while (i > 0):
            if (not os.path.exists(os.path.join(cache, "cache_%d" % i))):
                os.mkdir(os.path.join(cache, "cache_%d" % i))
            i = i - 1
    elif (os.path.exists(os.path.join(cache, "cache_0"))):
        while (os.path.exists(os.path.join(cache, "cache_%d" % j))):
            j += 1
        while (i > 0):
            if (not os.path.exists(os.path.join(cache, "cache_%d" % j))):
                os.mkdir(os.path.join(cache, "cache_%d" % j))
            i = i - 1
    else:
        i = i - 1
        while (i > -1):
            if (not os.path.exists(os.path.join(cache, "cache_%d" % i))):
                os.mkdir(os.path.join(cache, "cache_%d" % i))
            i = i - 1
else:
    for x in sys.argv:
        if (x == "./mkdir.py"):
            continue
        if (not os.path.exists(os.path.join(cache, x))):
            os.mkdir(os.path.join(cache,x))
