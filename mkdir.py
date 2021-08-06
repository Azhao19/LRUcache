#!/usr/bin/python3
import os                    # create directory
from pathlib import Path     # find parent directory
import sys                   # access argv
import glob

# input can be:
# empty
# number of caches to create
# list of cache names

DEFAULT_CACHE_SIZE = 500     # size in MB
def write_size(path, size: int):
    f = open(os.path.join(path, ".size"), "w")
    f.write("%d" % size)
    f.close()
if (not glob.glob(os.path.join(Path("."), "cache"))):
    os.mkdir("cache")
cache = Path("./cache")
# Case 1: empty
if (len(sys.argv) == 1 and not glob.glob(os.path.join(cache, "*"))):
    print("No cache folder detected. Creating one now.") 
    path = os.path.join(cache, "cache")  
    os.mkdir(os.path.join(cache, "cache"))
    write_size(os.path.join(cache, "cache"), DEFAULT_CACHE_SIZE)
# Case 2: just a number
elif (len(sys.argv) == 2 and sys.argv[1].isdigit()):
    i = int(sys.argv[1])
    j = 0
    if (os.path.exists(os.path.join(cache, "cache"))):
        os.rename("cache/cache", "cache/cache_0")
        while (i > 0):
            if (not os.path.exists(os.path.join(cache, "cache_%d" % i))):
                os.mkdir(os.path.join(cache, "cache_%d" % i))
                write_size(os.path.join(cache, "cache_%d" % i), DEFAULT_CACHE_SIZE)
            i = i - 1
    elif (os.path.exists(os.path.join(cache, "cache_0"))):
        while (i > 0):
            if (not os.path.exists(os.path.join(cache, "cache_%d" % j))):
                os.mkdir(os.path.join(cache, "cache_%d" % j))
                write_size(os.path.join(cache, "cache_%d" % j), DEFAULT_CACHE_SIZE)
                i = i - 1
            j += 1
    else:
        i = i - 1
        while (i > -1):
            if (not os.path.exists(os.path.join(cache, "cache_%d" % i))):
                os.mkdir(os.path.join(cache, "cache_%d" % i))
                write_size(os.path.join(cache, "cache_%d" % i), DEFAULT_CACHE_SIZE)
            i = i - 1
else:
    for x in sys.argv[1:]:
        x = x.split(",")
        if (len(x) == 1 or len(x) > 2 or not x[1].isdigit()):
            print("To make directory, format data as a spaced list of the form x_k,y_k.")
            exit(1)
        if (not os.path.exists(os.path.join(cache, x[0]))):
            os.mkdir(os.path.join(cache,x[0]))
            write_size(os.path.join(cache,x[0]),int(x[1]))
