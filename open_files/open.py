#!/usr/bin/python3

# Pre scraping
# Only when a file is opened does the maintenance of LRU cache structure become more complex.
# This program will process one open at a time
# It is assumed there will be no edits to the file

import os
import sys
from pathlib import Path

if (not os.path.exists(os.path.join(Path("."), "cache"))):
    print("File does not exist.")
    exit(1)

p = Path("./cache")

# input validation
for test in sys.argv[1:]:
    test = test.split(",")
    if (not len(test) == 2):
        print("Invalid input to open.")
        exit(1)
    if (not os.path.exists(os.path.join(p, "%s/%s"% (test[1], test[0])))):
        print("Not all files exist.")
        exit(1)
 
for x in sys.argv[1:]:
    x = x.split(",")
    
    p_file = os.path.join(p, "%s/%s" % (x[1], x[0]))
    y = round(os.stat(p_file).st_size / (1024 * 1024), 8)
    pid = os.fork()
    if (pid < 0):
        print("Fork failed.")
        exit(1)
    elif (pid == 0):
        os.execlp("vim", "vim", p_file)
    else:
        os.waitpid(pid, 0)

        y = round(os.stat(p_file).st_size / (1024 * 1024), 8) - y
        f = open(os.path.join(p, "%s/.size" % x[1]), "r")
        lines = f.readlines()
        z = float(lines[1]) + y
        lines[1] = str(z)
        f = open(os.path.join(p, "%s/.size" % x[1]), "w")
        f.writelines(lines)
        f.close()

        g = open(os.path.join(p, "%s/.files" % x[1]), "a")
        g.write(x[0])
        g.close()

        # Deletion of the old entry corresponding to x[0] will be done by the main program
        # which has access to the LRUCache data structures



        
