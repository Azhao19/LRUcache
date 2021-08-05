#!/usr/bin/python3
import os                    # create directory
from pathlib import Path     # find parent directory

path = Path(".")             # path of current directory
if (os.path.exists(os.path.join(path, "cache"))):
    os.rename("cache", "cache_0")
    path = os.path.join(path, "cache_1")
    os.mkdir(path)
elif (os.path.exists(os.path.join(path, "cache_0"))):
    i = 0;
    while (os.path.exists(os.path.join(path, "cache_%d" % i))):
        i += 1
    path = os.path.join(path, "cache_%d" % i)
    os.mkdir(path)
else:
    path = os.path.join(path, "cache")  
    os.mkdir(path)
