#!/usr/bin/python3

import os                    # create directory
from pathlib import Path     # find parent directory
import sys                   # access argv
import glob
import shutil                # to delete directories with stuff in them
# command line arguments specified by -r flag
# must be names of actual directories
# -f flag can be a forced removal
path = Path(".")
if (not os.path.exists(os.path.join(path, "cache"))):
    print("No caches to remove.")
    exit(1)
path = os.path.join(path, "cache")
if (not sys.argv[1] == "true" and not sys.argv[1] == "false"):
    print("First argument must either be true or false.")
    exit(1)
for x in sys.argv[2:]:
    if (not os.path.exists(os.path.join(path, x))):
        if sys.argv[1] == "true":
            continue
        else:
            print("No cache named %s." % x)
            exit(1)
    else:
        shutil.rmtree(os.path.join(path, x))
        
