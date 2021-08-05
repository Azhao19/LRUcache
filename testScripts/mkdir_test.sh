#!/bin/bash

cd ..
./mkdir.py 7 && rm -r cache && mkdir cache && mkdir cache/test && ./mkdir.py 5

cd cache
for entry in "."/*
do
    echo "$entry"
done

cd ..
rm -r cache
./mkdir.py && ./mkdir.py 4 && ./mkdir.py test1 test2 && ./mkdir.py 4 5
./mkdir.py 4 5 test3 test2
cd cache
for entry in "."/*
do
    echo "$entry"
done
cd ..
